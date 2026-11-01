"""Audit saved final evidence by arithmetic only. No fitting or simulation imports."""
from pathlib import Path
import argparse,hashlib,json,itertools
import numpy as np
import pandas as pd
from scipy.stats import rankdata,spearmanr
ROOT=Path(__file__).resolve().parents[1]
COHORT_SHA='f317eef220e6f8757be6aa8d6e4ec29b9bf90e0eeaad8d86009a265b65b1b149'

def run(shuffles=True):
    rows=[]
    def check(source,field,got,expected,tol=1e-10,explanation=''):
        try:ok=bool(np.allclose(got,expected,rtol=0,atol=tol,equal_nan=False))
        except (ValueError,TypeError):ok=got==expected
        rows.append(dict(source=source,field=field,computed=str(got),manuscript_SI_stated=str(expected),tolerance=tol,status='PASS' if ok else 'FAIL',explanation=explanation))
    def err(a,b):return float(np.max(abs(np.asarray(a)-np.asarray(b))))
    def r2(y,p):return float(1-np.sum((y-p)**2)/np.sum((y-y.mean())**2))
    data=ROOT/'data';prov=data/'provenance';final=data/'final';q=ROOT/'quality_control'
    d=pd.read_csv(data/'authoritative/mechanism_238_authoritative.csv');ids=d.mof_id.tolist();ix=d.set_index('mof_id')
    check('v9 frozen bytes','cohort sha256',hashlib.sha256((data/'authoritative/mechanism_238_authoritative.csv').read_bytes()).hexdigest(),COHORT_SHA,0)
    check('cohort','n',len(d),238,0);check('cohort','unique IDs',d.mof_id.nunique(),238,0);check('cohort','missing cells',int(d.isna().sum().sum()),0,0)
    for label,c,n in [('WCA negative','lnS_wca',238),('attraction positive','delta_lnS_attr',238),('electrostatics positive','delta_lnS_elec',238)]:check('cohort',label,int((d[c]<0).sum()) if c=='lnS_wca' else int((d[c]>0).sum()),n,0)
    for lhs,rhs in [(d.lnS_lj_only,d.lnS_wca+d.delta_lnS_attr),(d.lnS_full,d.lnS_lj_only+d.delta_lnS_elec),(d.lnS_full,d.lnS_wca+d.delta_lnS_attr+d.delta_lnS_elec)]:check('cohort','nested identity max residual',err(lhs,rhs),0,1e-12)
    for c,expected in [('lnS_wca',-.2037494852370207),('delta_lnS_attr',2.537375623648152),('delta_lnS_elec',.3094920366015232)]:check('main/SI',c+' median',np.median(d[c]),expected)
    check('main/SI','uncertain WCA signs',int((d.lnS_wca+1.96*d.lnS_wca_se>=0).sum()),19,0)
    check('main/SI','WCA SE>.1',int((d.lnS_wca_se>.1).sum()),4,0)
    summary=pd.read_csv(data/'authoritative/mechanism_summary.csv').set_index('metric')
    for c in summary.index:
        if c not in d:continue
        for field,func in [('mean',np.mean),('sd',lambda x:np.std(x,ddof=1)),('median',np.median),('q05',lambda x:np.quantile(x,.05)),('q25',lambda x:np.quantile(x,.25)),('q75',lambda x:np.quantile(x,.75)),('q95',lambda x:np.quantile(x,.95)),('min',np.min),('max',np.max)]:check('authoritative summary',c+' '+field,func(d[c]),summary.loc[c,field])
    sets={s:set(d.nlargest(24,col).mof_id) for s,col in [('wca','lnS_wca'),('lj','lnS_lj_only'),('full','lnS_full')]}
    check('shortlists','WCA-LJ overlap',len(sets['wca']&sets['lj']),0,0);check('shortlists','LJ-full overlap',len(sets['lj']&sets['full']),17,0)
    for filename in ['figure_1_source.csv','figure_2_source.csv']:
        t=pd.read_csv(data/'source_v2'/filename).set_index('mof_id')
        for c in t:check(filename,c,err(t[c],ix.loc[t.index,c]),0)
    # Every restored original input has a captured SHA; normalized data are separately checked below.
    manifest=json.loads((ROOT/'docs/RESTORED_SOURCE_MANIFEST.json').read_text())
    for m in manifest['files']:check('restored provenance',m['restored_path'],hashlib.sha256((ROOT/m['restored_path']).read_bytes()).hexdigest(),m['sha256'],0)
    raw=pd.read_csv(prov/'descriptor_hierarchy_predictions.csv');raw=raw[raw.feature_set=='geometry'].copy()
    normal=pd.read_csv(final/'geometry_oof_predictions.csv');check('OOF','rows',len(raw),952,0)
    metrics=pd.read_csv(prov/'descriptor_hierarchy_metrics.csv');metrics=metrics[metrics.feature_set=='geometry'].set_index('target')
    published=pd.read_csv(data/'authoritative/geometry_cv_FINAL_v5_transcribed.csv').set_index('target')
    fm=pd.read_csv(prov/'descriptor_feature_manifest.csv');features=fm.loc[fm.feature_set=='geometry','column'].tolist()
    check('CV features','count',len(features),14,0);check('CV features','only geometry source columns',bool(all(c.startswith('geom_') and c in d for c in features)),True,0)
    shuffle=np.arange(238);np.random.RandomState(20260918).shuffle(shuffle);fold=np.empty(238,dtype=int)
    for k,v in enumerate(np.array_split(shuffle,5)):fold[v]=k
    fold_by_id=dict(zip(ids,fold));foldtable=pd.read_csv(final/'geometry_fold_membership.csv').set_index('mof_id')
    check('CV reconstructed metadata','membership',err(foldtable.loc[ids,'fold'],fold),0,0,explanation='Reconstructed from archived code and row order; no fit replay claimed')
    computed_metrics=[];wide={}
    target_map={'delta_attr':'delta_lnS_attr','delta_elec':'delta_lnS_elec','lnS_wca':'lnS_wca','lnS_full':'lnS_full'}
    for target,c in target_map.items():
        g=raw[raw.target==target].set_index('mof_id').loc[ids];n=normal[normal.target==c].set_index('mof_id').loc[ids]
        check('OOF raw',target+' unique IDs',g.index.nunique(),238,0)
        check('OOF raw',target+' observed vs authoritative',err(g.observed,ix.loc[ids,c]),0)
        check('normalized OOF',target+' predictions unchanged',err(g.predicted,n.predicted),0,1e-14)
        check('normalized OOF',target+' folds',err(n.fold,[fold_by_id[mid] for mid in ids]),0,0)
        check('normalized OOF',target+' reference median',err(n.baseline_prediction,np.repeat(np.median(g.observed),238)),0)
        y=g.observed.to_numpy();yp=g.predicted.to_numpy();wide[target]=(y,yp)
        vals=dict(r2=r2(y,yp),mae=float(np.mean(abs(y-yp))),baseline_mae=float(np.mean(abs(y-np.median(y)))))
        for field,value in vals.items():
            check('archived OOF -> exact metric',target+' '+field,value,metrics.loc[target,field])
            check('archived OOF -> manuscript rounding',target+' '+field,value,published.loc[c,field],.0005)
        computed_metrics.append(dict(target=c,**vals))
    check('CV protocol','KFold5 archived',bool((metrics.cv=='KFold5').all()),True,0)
    # Independent bootstrap uses the original row-aligned saved predictions, not computed summary tables.
    rng=np.random.default_rng(20260920);boot={k:[] for k in ['median_attr','median_elec','rho_attr_elec','fraction_attr_positive','fraction_elec_positive','r2_attr','r2_elec','predictability_gap']}
    for _ in range(5000):
        idx=rng.integers(0,238,238);a=d.delta_lnS_attr.to_numpy()[idx];e=d.delta_lnS_elec.to_numpy()[idx];ra=r2(wide['delta_attr'][0][idx],wide['delta_attr'][1][idx]);re=r2(wide['delta_elec'][0][idx],wide['delta_elec'][1][idx])
        vals=[np.median(a),np.median(e),spearmanr(a,e).statistic,np.mean(a>0),np.mean(e>0),ra,re,ra-re]
        for key,value in zip(boot,vals):boot[key].append(value)
    reference=json.loads((prov/'pi_bootstrap_summary.json').read_text());cis={k:np.quantile(v,[.025,.975]).tolist() for k,v in boot.items()}
    for key,ci in cis.items():check('archived bootstrap',key+' 95% endpoints',err(ci,reference['ci95'][key]),0,1e-10)
    check('main/SI','predictability gap',r2(*wide['delta_attr'])-r2(*wide['delta_elec']),reference['point']['predictability_gap'])
    # Independently pool both primary numerical sources.
    w=pd.concat([pd.read_csv(prov/f) for f in ['wca_base_jobs.csv','wca_extension_jobs.csv','wca_rescue_jobs.csv']],ignore_index=True)
    check('WCA jobs','archive total',len(w),2052,0);check('WCA jobs','duplicate IDs',int(w.job_id.duplicated().sum()),0,0);check('WCA jobs','retained',int(w.mof_id.isin(ids).sum()),2034,0)
    w['B']=np.exp(-w.mu_ex_kcal_mol/(.00198720425864083*298))
    for (mid,gas),g in w[w.mof_id.isin(ids)].groupby(['mof_id','gas']):
        b=g.B.to_numpy();avg=b.mean();se=b.std(ddof=1)/np.sqrt(len(b));suf='_'+gas.lower()
        for key,value in [('wca_seed_count',len(b)),('B_wca_mean',avg),('B_wca_se',se),('lnB_wca',np.log(avg)),('lnB_wca_se',se/avg)]:check('WCA independent pooling',mid+' '+key+suf,value,ix.loc[mid,key+suf])
    r=pd.read_csv(prov/'raspa_final_gas_rows.csv');check('RASPA summary','gas-specific rows',len(r),2960,0);check('RASPA summary','positive finite Henry',bool(((r.kh_mol_kg_Pa>0)&np.isfinite(r.kh_mol_kg_Pa)).all()),True,0)
    for (mid,mode,gas),g in r[r.mof_id.isin(ids)].groupby(['mof_id','mode','gas']):
        v=np.log(g.kh_mol_kg_Pa.to_numpy());suf='_'+mode+'_'+gas.lower()
        for key,value in [('raspa_seed_count',len(v)),('lnkh_mean',v.mean()),('lnkh_sd',v.std(ddof=1)),('lnkh_se',v.std(ddof=1)/np.sqrt(len(v)))]:check('RASPA independent aggregation',mid+' '+key+suf,value,ix.loc[mid,key+suf])
    # Bridge: 90 matched per-seed records -> 30 MOF/gas means -> reported statistics.
    bridge=pd.read_csv(prov/'wca_paired_seed_comparison_90.csv');check('bridge','paired seed rows',len(bridge),90,0)
    agg=bridge.groupby(['mof_id','gas'])[['mu_ex_kcal_mol_uff','mu_ex_kcal_mol_dreiding_uff']].mean().reset_index();bref=pd.read_csv(prov/'wca_robustness_statistics.csv').set_index('scope')
    for gas,g in agg.groupby('gas'):
        delta=g.mu_ex_kcal_mol_dreiding_uff-g.mu_ex_kcal_mol_uff
        for field,value in [('n',len(g)),('mae_delta_mu',abs(delta).mean()),('max_abs_delta_mu',abs(delta).max()),('spearman_rho',spearmanr(g.mu_ex_kcal_mol_uff,g.mu_ex_kcal_mol_dreiding_uff).statistic)]:check('bridge -> SI',gas+' '+field,value,bref.loc[gas,field])
    # Finite saved pilot descriptors; no energy/pose calculation or production probe model is run.
    lo=pd.read_csv(prov/'pi_gate_c_pilot_descriptors_6000.csv').set_index('template_alias');hi=pd.read_csv(prov/'pi_gate_c_pilot_descriptors_10000.csv').set_index('template_alias').loc[lo.index]
    gate=json.loads((prov/'PI_GATE_C_PILOT_10000.json').read_text())
    for c in hi:
        val=float(np.max(abs(hi[c]-lo[c]))/np.std(hi[c],ddof=0));check('probe saved-descriptor convergence',c,val,gate['descriptor_convergence'][c]['max_abs_standardized_change'])
    for c,key in [('probe_co2_minus_n2_median_z','median_gap_spearman'),('probe_co2_minus_n2_q90_z','q90_gap_spearman')]:check('probe saved-descriptor ordering',c,spearmanr(lo[c],hi[c]).statistic,gate['cross_gas_ordering'][key])
    check('probe','converged feature count',sum(v['passed'] for v in gate['descriptor_convergence'].values()),1,0)
    # Shuffle frozen targets within saved strata. Prediction training and PCA are not rerun.
    if shuffles:
        strata=pd.read_csv(prov/'pi_geometry_strata_assignments.csv').set_index('mof_id').loc[ids];table=pd.read_csv(prov/'pi_geometry_controlled_permutation_summary.csv');master=np.random.default_rng(20260920)
        for k in [8,10,12]:
            labels=strata['balanced_geometry_stratum_k'+str(k)].to_numpy();groups=[np.flatnonzero(labels==s) for s in np.unique(labels)]
            for target in ['delta_attr','delta_elec']:
                expected=table[(table.nominal_k==k)&(table.target==target)].iloc[0];y,yp=wide[target];yr=rankdata(y);pr=rankdata(yp);pc=pr-pr.mean();den=np.linalg.norm(yr-yr.mean())*np.linalg.norm(pc);rng=np.random.default_rng(int(master.integers(0,2**32-1)))
                nr=[];ns=[];nm=[]
                for _ in range(10000):
                    permutation=np.arange(238)
                    for group in groups:permutation[group]=rng.permutation(permutation[group])
                    shuffled=y[permutation];nr.append(float(np.dot(yr[permutation]-yr.mean(),pc)/den));ns.append(r2(shuffled,yp));nm.append(float(np.mean(abs(shuffled-yp))))
                for field,value in [('observed_spearman_pred_vs_target',spearmanr(y,yp).statistic),('null_spearman_q025',np.quantile(nr,.025)),('null_spearman_q975',np.quantile(nr,.975)),('null_r2_q025',np.quantile(ns,.025)),('null_r2_q975',np.quantile(ns,.975)),('null_mae_q025',np.quantile(nm,.025)),('null_mae_q975',np.quantile(nm,.975))]:check('saved-strata shuffle replay',f'k{k} {target} {field}',value,expected[field],1e-10)
        # Explain PCA percentages by direct singular values, not a learned predictive fit.
        x=d[features].to_numpy();x=(x-x.mean(axis=0))/x.std(axis=0);singular=np.linalg.svd(x,compute_uv=False);fraction=float(np.sum(singular[:2]**2)/np.sum(singular**2))
        check('geometry PC variance','first two components percent',100*fraction,92.87,.005)
    report=dict(status='PASS' if all(r['status']=='PASS' for r in rows) else 'FAIL',checks=len(rows),failed=sum(r['status']=='FAIL' for r in rows),cohort=238,OOF_rows=952,model_refit=False,simulation=False,fold_membership='reconstructed metadata; source-inspected protocol',bootstrap_ci95=cis,shuffle_replayed=shuffles)
    pd.DataFrame(rows).to_csv(q/'NUMERICAL_RECONCILIATION.csv',index=False)
    (q/'final_evidence_audit.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2));
    for row in rows:
        if row['status']=='FAIL':print(row)
    return report

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--skip-shuffles',action='store_true',help='Only for quick checks; full release audit always includes shuffles');args=parser.parse_args();raise SystemExit(0 if run(not args.skip_shuffles)['status']=='PASS' else 2)
