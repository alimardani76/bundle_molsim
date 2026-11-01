"""Verify the reconciled scientific release, documents and checksums."""
from pathlib import Path
import argparse,hashlib,json,re
import numpy as np
import pandas as pd
from audit_final_evidence import run as audit
ROOT=Path(__file__).resolve().parents[1]

def run(check_hashes=True):
    errors=[];checks=[]
    def check(ok,name):
        checks.append(dict(check=name,status='PASS' if ok else 'FAIL'))
        if not ok:errors.append(name)
    numeric=audit()
    check(numeric['status']=='PASS','independent final numerical evidence')
    d=pd.read_csv(ROOT/'data/authoritative/mechanism_238_authoritative.csv');ix=d.set_index('mof_id')
    cols=['geom_df','geom_di','geom_dif','geom_density','geom_asa','geom_avaf','geom_navaf','geom_poavaf','geom_npoavaf']
    z=d[cols].to_numpy();s=z.std(axis=0);z=(z-z.mean(axis=0))/np.where(s==0,1,s)
    matrix=np.sqrt(np.sum((z[:,None,:]-z[None,:,:])**2,axis=2));np.fill_diagonal(matrix,np.inf)
    ai,bi=np.triu_indices(238,1);pair_order=np.argsort(matrix[ai,bi],kind='stable');subset=pair_order[:564]
    recon=pd.read_csv(ROOT/'data/final/pair_selection_reconciliation.csv')
    for target,field in [('attraction','delta_lnS_attr'),('electrostatic','delta_lnS_elec')]:
        winner=subset[np.argmax(abs(d[field].to_numpy()[ai[subset]]-d[field].to_numpy()[bi[subset]]))]
        row=recon[(recon.target==target)&(recon.rule=='all_pairs_closest_2_percent')].iloc[0]
        check({row.mof_a,row.mof_b}=={d.loc[ai[winner],'mof_id'],d.loc[bi[winner],'mof_id']},target+' exhaustive optimum')
        example=recon[(recon.target==target)&(recon.role=='retained_illustrative_case')].iloc[0]
        check({example.mof_a,example.mof_b}!={row.mof_a,row.mof_b},target+' illustrative example distinguished from all-pair optimum')
    for p in sorted((ROOT/'data/figure_sources').glob('*.csv')):
        t=pd.read_csv(p)
        if 'mof_id' in t:
            check(t.mof_id.is_unique and set(t.mof_id)<=set(ix.index),p.name+' cohort IDs')
            for col in set(t.columns)&set(ix.columns):
                if pd.api.types.is_numeric_dtype(t[col]):check(np.allclose(t[col],ix.loc[t.mof_id,col],atol=1e-12,rtol=0),p.name+' '+col)
        if p.name=='figure_3.csv':
            reference=pd.read_csv(ROOT/'data/final/geometry_cv_metrics.csv')
            check(t.target.equals(reference.target) and np.allclose(t.select_dtypes('number'),reference.select_dtypes('number'),atol=1e-14,rtol=0),'Figure 3 uses saved-final-OOF metrics')
    for folder,stem,n in [('manuscript','main',6),('supporting_information','supporting_information',4)]:
        tex=(ROOT/folder/(stem+'.tex')).read_text(encoding='utf8')
        refs=re.findall(r'\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}',tex)
        check(len(refs)==n,stem+' exact figure inclusion count')
        for name in refs:check(sum((ROOT/'figures'/s/name).is_file() for s in ['main','si'])==1,stem+' resolves '+name)
        check(not re.search(r'\\{2,}(rho|cite)',tex),stem+' TeX command escapes')
        check('final out-of-fold prediction vectors, voxel arrays' not in tex,stem+' restored prediction availability')
        p=ROOT/folder/(stem+'.pdf');check(p.is_file() and p.read_bytes().startswith(b'%PDF') and p.stat().st_size>20000,stem+' built PDF')
        if stem=='main':check('fig4_matched_contrast.pdf' in refs,'matched-pair figure included')
        else:check(r'\renewcommand{\thefigure}{S\arabic{figure}}' in tex and r'\renewcommand{\thetable}{S\arabic{table}}' in tex,'SI figure/table S numbering')
        log=ROOT/folder/(stem+'.log')
        if log.is_file():check(not re.search(r'(undefined|There were undefined|Rerun to get cross-references right|Overfull \\hbox)',log.read_text(errors='replace'),re.I),stem+' final LaTeX diagnostics')
    for sub,n in [('main',6),('si',4),('toc',1)]:
        for ext in ['pdf','png','tiff']:check(len(list((ROOT/'figures'/sub).glob('*.'+ext)))==n,sub+' '+ext+' count')
    build=ROOT/'quality_control/document_build.json';check(build.is_file(),'scratch document build record')
    if build.is_file():
        for path,digest in json.loads(build.read_text())['artifacts'].items():check(hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,'built document matches '+path)
    if check_hashes:
        for filename in ['SHA256SUMS.txt','input_hashes.sha256']:
            mf=ROOT/'quality_control'/filename;check(mf.is_file(),filename+' exists')
            if mf.is_file():
                for line in mf.read_text().splitlines():
                    if not line.strip():continue
                    digest,path=line.split('  ',1);p=ROOT/path
                    check(p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==digest,filename+' '+path)
    report=dict(status='PASS' if not errors else 'FAIL',errors=errors,numerical_checks=numeric['checks'],release_checks=len(checks),frameworks=238,geometry_OOF_rows=952,main_figures=6,SI_figures=4,TOC=1,model_refit=False,fresh_simulation=False,hashes_checked=check_hashes)
    (ROOT/'quality_control/release_check.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2));return report
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--prepare-checksums',action='store_true',help='Audit before writing a new manifest; not sufficient as the final publication gate');args=parser.parse_args()
    raise SystemExit(0 if run(not args.prepare_checksums)['status']=='PASS' else 2)
