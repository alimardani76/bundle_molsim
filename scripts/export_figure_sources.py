"""Export explicit panel sources from the unchanged cohort and restored OOF metrics."""
from pathlib import Path
import argparse,json
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
def run():
    d=pd.read_csv(ROOT/'data/authoritative/mechanism_238_authoritative.csv');out=ROOT/'data/figure_sources';out.mkdir(exist_ok=True)
    specs={
        'figure_1.csv':['lnS_wca','lnS_lj_only','lnS_full','delta_lnS_attr','delta_lnS_elec'],
        'figure_2.csv':['delta_lnS_attr','delta_lnS_elec','lnS_full'],
        'figure_4_values.csv':['lnS_wca','lnS_lj_only','lnS_full','lnkh_mean_full_co2','lnkh_mean_full_n2','lnkh_mean_lj_only_co2','lnkh_mean_lj_only_n2'],
        'figure_5_population.csv':['lnS_wca','lnS_lj_only','lnS_full'],
        'figure_6.csv':['lnS_wca','lnS_lj_only','lnS_full','delta_lnS_attr','delta_lnS_elec'],
        'figure_S1_S2.csv':['lnS_wca','lnS_wca_se','lnkh_mean_full_co2','lnkh_mean_full_n2','lnkh_mean_lj_only_co2','lnkh_mean_lj_only_n2'],
        'figure_S3.csv':['lnS_wca','delta_lnS_attr','delta_lnS_elec'],
        'figure_S4.csv':['lnS_wca','lnS_lj_only','lnS_full'],
        'TOC.csv':['lnS_wca','lnS_lj_only','lnS_full']}
    for file,cols in specs.items():d[['mof_id']+cols].to_csv(out/file,index=False,float_format='%.17g')
    pd.read_csv(ROOT/'data/final/geometry_cv_metrics.csv').to_csv(out/'figure_3.csv',index=False,float_format='%.17g')
    p=pd.read_csv(ROOT/'data/authoritative/matched_pairs.csv');p[p.case_label.str.contains('electrostatic')].to_csv(out/'figure_4_pair.csv',index=False,float_format='%.17g')
    pd.read_csv(ROOT/'data/source_v2/figure_5_source.csv').to_csv(out/'figure_5_cases.csv',index=False,float_format='%.17g')
    (out/'SOURCE_MAP.json').write_text(json.dumps(dict(
        figure_1='unchanged authoritative cohort: states, increments, medians and exp(medians)',
        figure_2='unchanged authoritative cohort: mechanism coordinates and electrostatic share',
        figure_3='restored saved 14-feature OOF predictions -> data/final/geometry_cv_metrics.csv; no refit',
        figure_4='retained illustrative M029/M085 from authoritative matched_pairs.csv; cohort gas responses; not exhaustive optimum',
        figure_5='cohort descending ranks and original four retained cases in source_v2/figure_5_source.csv',
        figure_6='cohort identifier families, medians and recomputed top24 overlap',
        figure_S1='cohort WCA SE and 1.96-SE normal boundary',figure_S2='cohort full-minus-LJ per-gas log Henry increments',
        figure_S3='cohort identifier-family distributions',figure_S4='cohort stable top24 membership matrix',TOC='cohort state medians'),indent=2)+'\n')
    print('Exported 11 figure source mappings; no simulation or fitting.')
if __name__=='__main__':argparse.ArgumentParser(description=__doc__).parse_args();run()
