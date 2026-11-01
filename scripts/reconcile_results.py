"""Reconcile the frozen v9 cohort; no simulation, training or model fitting."""
from pathlib import Path
import argparse,hashlib,json,math
import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist,squareform
from scipy.stats import spearmanr

ROOT=Path(__file__).resolve().parents[1]
GEOMETRY=['geom_df','geom_di','geom_dif','geom_density','geom_asa','geom_avaf','geom_navaf','geom_poavaf','geom_npoavaf']
COHORT_SHA='f317eef220e6f8757be6aa8d6e4ec29b9bf90e0eeaad8d86009a265b65b1b149'

def run():
    out=ROOT/'data/final';out.mkdir(exist_ok=True)
    q=ROOT/'quality_control';q.mkdir(exist_ok=True)
    source=ROOT/'data/authoritative/mechanism_238_authoritative.csv'
    d=pd.read_csv(source);assert len(d)==238 and d.mof_id.is_unique and not d.isna().any().any()
    assert hashlib.sha256(source.read_bytes()).hexdigest()==COHORT_SHA,'Frozen cohort changed'
    assert np.max(abs(d.lnS_full-(d.lnS_wca+d.delta_lnS_attr+d.delta_lnS_elec)))<1e-12
    z=d[GEOMETRY].to_numpy();sd=z.std(axis=0);z=(z-z.mean(axis=0))/np.where(sd==0,1,sd)
    distances=squareform(pdist(z));np.fill_diagonal(distances,np.inf)
    ia,ib=np.triu_indices(len(d),1)
    pairs=pd.DataFrame({'mof_a':d.mof_id.to_numpy()[ia],'mof_b':d.mof_id.to_numpy()[ib],
        'geometry_distance':distances[ia,ib],
        'abs_attr_contrast':abs(d.delta_lnS_attr.to_numpy()[ia]-d.delta_lnS_attr.to_numpy()[ib]),
        'abs_elec_contrast':abs(d.delta_lnS_elec.to_numpy()[ia]-d.delta_lnS_elec.to_numpy()[ib])})
    nearest=pairs.sort_values(['geometry_distance','mof_a','mof_b'],kind='stable').head(math.floor(.02*len(pairs))).copy()
    # Faithful reconstruction of the archived asymmetric i<j / nearest-three algorithm.
    legacy_indices=[(i,j) for i in range(len(d)) for j in np.argsort(distances[i])[:3] if i<j]
    legacy=pd.DataFrame([dict(mof_a=d.loc[i,'mof_id'],mof_b=d.loc[j,'mof_id'],geometry_distance=distances[i,j],
        abs_attr_contrast=abs(d.loc[i,'delta_lnS_attr']-d.loc[j,'delta_lnS_attr']),
        abs_elec_contrast=abs(d.loc[i,'delta_lnS_elec']-d.loc[j,'delta_lnS_elec'])) for i,j in legacy_indices])
    threshold=legacy.geometry_distance.quantile(.25);restricted=legacy[legacy.geometry_distance<=threshold].copy()
    selected=pd.read_csv(ROOT/'data/authoritative/matched_pairs.csv')
    findings=[]
    for target,field in [('attraction','abs_attr_contrast'),('electrostatic','abs_elec_contrast')]:
        for rule,table in [('all_pairs_closest_2_percent',nearest),('archived_nearest_three_lower_quartile',restricted)]:
            best=table.sort_values([field,'geometry_distance','mof_a','mof_b'],ascending=[False,True,True,True]).iloc[0]
            findings.append(dict(role='optimal_within_stated_candidate_set',target=target,rule=rule,candidate_n=len(table),**best.to_dict()))
        r=selected[selected.case_label.str.contains(target)].iloc[0]
        a,b=sorted([r.mof_a,r.mof_b]);record=pairs[(pairs.mof_a==a)&(pairs.mof_b==b)].iloc[0]
        findings.append(dict(role='retained_illustrative_case',target=target,rule='original_archived_example',candidate_n=0,**record.to_dict()))
        assert {r.mof_a,r.mof_b}==set(findings[-2][c] for c in ['mof_a','mof_b'])
    pd.DataFrame(findings).to_csv(out/'pair_selection_reconciliation.csv',index=False,float_format='%.16g')
    nearest.to_csv(out/'geometry_closest_2percent_candidates.csv',index=False,float_format='%.16g')
    restricted.to_csv(out/'archived_geometry_candidate_set.csv',index=False,float_format='%.16g')
    rank=pd.DataFrame({'mof_id':d.mof_id})
    for key,col in [('wca','lnS_wca'),('lj','lnS_lj_only'),('full','lnS_full')]:
        ordered=d.sort_values([col,'mof_id'],ascending=[False,True]).mof_id.tolist()
        rank['rank_'+key]=rank.mof_id.map({m:i+1 for i,m in enumerate(ordered)});rank['top24_'+key]=rank['rank_'+key]<=24
    rank.to_csv(out/'ranks_and_shortlists.csv',index=False)
    families=[]
    for family,g in d.groupby(d.mof_id.str.extract(r'^(DB0-m\d+)')[0]):
        families.append(dict(family=family,n=len(g),median_wca=g.lnS_wca.median(),median_attr=g.delta_lnS_attr.median(),median_elec=g.delta_lnS_elec.median(),rho=spearmanr(g.delta_lnS_attr,g.delta_lnS_elec).statistic))
    pd.DataFrame(families).to_csv(out/'family_summary.csv',index=False,float_format='%.16g')
    statecols=['lnS_wca','delta_lnS_attr','delta_lnS_elec','lnS_lj_only','lnS_full']
    summary=[dict(field=c,median=d[c].median(),q05=d[c].quantile(.05),q95=d[c].quantile(.95),positive=int((d[c]>0).sum())) for c in statecols]
    pd.DataFrame(summary).to_csv(out/'coordinate_summary.csv',index=False,float_format='%.16g')
    gap=abs(d.lnS_full.to_numpy()[ia]-d.lnS_full.to_numpy()[ib]);which=np.argsort(gap,kind='stable')[:math.ceil(.05*len(gap))]
    endpoint=pd.DataFrame({'mof_a':d.mof_id.to_numpy()[ia[which]],'mof_b':d.mof_id.to_numpy()[ib[which]],'full_lnS_difference':gap[which],
        'mechanism_distance':np.hypot(d.delta_lnS_attr.to_numpy()[ia[which]]-d.delta_lnS_attr.to_numpy()[ib[which]],d.delta_lnS_elec.to_numpy()[ia[which]]-d.delta_lnS_elec.to_numpy()[ib[which]])})
    endpoint.sort_values('mechanism_distance',ascending=False).to_csv(out/'endpoint_matched_pairs.csv',index=False,float_format='%.16g')
    report=dict(population=238,cohort_sha256=COHORT_SHA,pair_count=len(pairs),all_pair_candidates=len(nearest),legacy_initial_candidates=len(legacy),legacy_candidate_n=len(restricted),legacy_cutoff=threshold,OOF_status='BLOCKED_MISSING_FINAL_PREDICTIONS',no_model_refit=True,no_simulation=True)
    pred=ROOT/'data/final/geometry_oof_predictions.csv'
    if pred.is_file():
        p=pd.read_csv(pred);expected=pd.read_csv(ROOT/'data/authoritative/geometry_cv_FINAL_v5_transcribed.csv').set_index('target');metrics=[]
        for target,g in p.groupby('target'):
            assert len(g)==238 and g.mof_id.is_unique and set(g.mof_id)==set(d.mof_id)
            assert set(g.fold)==set(range(5)),(target,'invalid folds')
            true=d.set_index('mof_id').loc[g.mof_id,target].to_numpy();assert np.max(abs(true-g.observed))<1e-10
            assert np.isfinite(g[['observed','predicted','baseline_prediction']]).all().all()
            r2=1-np.sum((g.observed-g.predicted)**2)/np.sum((g.observed-g.observed.mean())**2)
            mae=np.mean(abs(g.observed-g.predicted));baseline=np.mean(abs(g.observed-g.baseline_prediction))
            metric=dict(target=target,r2=r2,mae=mae,baseline_mae=baseline);metrics.append(metric)
            for field in ['r2','mae','baseline_mae']:assert abs(metric[field]-expected.loc[target,field])<=.0005,(target,field,metric[field])
        assert set(p.target)==set(expected.index)
        pd.DataFrame(metrics).set_index('target').loc[expected.index].reset_index().to_csv(out/'geometry_cv_metrics.csv',index=False,float_format='%.16g')
        report['OOF_status']='PASS_SAVED_PREDICTIONS';report['OOF_rows']=len(p)
    (q/'reconciliation_results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
    print(json.dumps(report,indent=2))
    return report

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.parse_args();run()
