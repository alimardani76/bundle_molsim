#!/usr/bin/env python3
"""Deterministic source-derived descriptive evidence for the expanded v7 paper.

Run from anywhere: python scripts/export_derived_tables.py
No fitted model or simulation is rerun. This script creates only independently
verifiable calculations from the 238-row authoritative V2/V5 table.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/derived_v7'
OUT.mkdir(parents=True,exist_ok=True)
a=pd.read_csv(ROOT/'data/authoritative/mechanism_238_authoritative.csv')
assert len(a)==238 and a.mof_id.is_unique
assert np.max(abs(a.lnS_full-a.lnS_wca-a.delta_lnS_attr-a.delta_lnS_elec))<1e-10
a['identifier_family']=a.mof_id.str.extract(r'^(DB0-m\d+)')
a['topology_suffix']=a.mof_id.str.split('_').str[-1]
assert a.identifier_family.value_counts().to_dict()=={'DB0-m15':210,'DB0-m12':28}
assert (a.topology_suffix=='fsc').sum()==171
summ=[]
for fam,g in a.groupby('identifier_family',sort=True):
 summ.append(dict(identifier_family=fam,n=len(g),wca_median=g.lnS_wca.median(),
        attr_median=g.delta_lnS_attr.median(),elec_median=g.delta_lnS_elec.median(),
        attr_elec_spearman=spearmanr(g.delta_lnS_attr,g.delta_lnS_elec).statistic))
pd.DataFrame(summ).to_csv(OUT/'family_summary.csv',index=False,float_format='%.10g')
for source,stem in [('lnS_wca','wca'),('lnS_lj_only','lj'),('lnS_full','full')]:
 # Stable tie-breaking for potential exact ties, independent of source row order.
 ordered=a.sort_values([source,'mof_id'],ascending=[False,True]).mof_id.tolist()
 rank={name:i+1 for i,name in enumerate(ordered)}
 a[f'rank_{stem}']=a.mof_id.map(rank)
 a[f'top24_{stem}']=a[f'rank_{stem}']<=24
sets={stem:set(a.loc[a[f'top24_{stem}'],'mof_id']) for stem in ['wca','lj','full']}
overlap={f'{u}_to_{v}':len(sets[u]&sets[v]) for u,v in [('wca','lj'),('lj','full')]}
assert overlap=={'wca_to_lj':0,'lj_to_full':17},overlap
cols=['mof_id','identifier_family','topology_suffix','lnS_wca','lnS_lj_only','lnS_full','delta_lnS_attr','delta_lnS_elec',
      'rank_wca','rank_lj','rank_full','top24_wca','top24_lj','top24_full']
a[cols].to_csv(OUT/'population_with_rank_and_family.csv',index=False,float_format='%.12g')
subset=a[a[['top24_wca','top24_lj','top24_full']].any(axis=1)][['mof_id','rank_wca','rank_lj','rank_full','top24_wca','top24_lj','top24_full']].copy()
subset.sort_values(['rank_full','rank_lj','mof_id'],inplace=True)
subset.to_csv(OUT/'union_top24_membership.csv',index=False)
summary={'count':len(a),'families':summ,'topology_fsc':int((a.topology_suffix=='fsc').sum()),
        'shortlist_k':24,'shortlist_overlap':overlap,
        'shortlist_fraction':{'wca_to_lj':0,'lj_to_full':17/24},
        'recorded_source':'data/authoritative/mechanism_238_authoritative.csv',
        'status':'Source-derived descriptive analyses only; no new simulation or ML refitting'}
(OUT/'v7_new_results.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
