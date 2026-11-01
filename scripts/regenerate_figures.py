#!/usr/bin/env python3
"""Rebuild the reconciled v9 figures from explicit tracked numerical sources.

Usage: python scripts/regenerate_figures.py
The program works from any working directory; original simulations are NOT rerun.
Inputs: explicit data/figure_sources CSVs exported from the unchanged cohort
and restored saved final 14-feature out-of-fold predictions.
Outputs: 6 main + 4 SI + original-data-driven TOC plots (PDF/PNG/TIFF),
summary JSON, provenance QA and figure CSVs.

IMPORTANT: Original voxel-resolved insertion maps were absent from supplied
analytical release. This script never fabricates fields or refits models.
"""
import sys,json,hashlib,logging,datetime,argparse
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib.colors import Normalize
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch
from scipy.stats import spearmanr

BASE=Path(__file__).resolve().parents[1]
OUT=BASE/'figures'
QA=BASE/'quality_control'
QA.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.titlesize':11.5,'axes.titleweight':'bold','axes.labelsize':10,
 'xtick.labelsize':9,'ytick.labelsize':9,'pdf.fonttype':42,'ps.fonttype':42,'savefig.facecolor':'white',
 'axes.spines.top':False,'axes.spines.right':False,'axes.linewidth':0.8,'grid.linewidth':.55,'figure.dpi':130})
INK='#18324C'; TEAL='#007F83'; CORAL='#D56D52'; BLUE='#4576AC'; GOLD='#D6A13F'; PURPLE='#745E9E'; GREY='#788596'; PALE='#E8EEF1'; BG='#F7F9FA'
logging.basicConfig(filename=QA/'figure_build.log',filemode='w',level=logging.INFO,
 format='%(asctime)s | %(levelname)s | %(message)s')

def label(ax,letter,title):
 ax.text(-.12,1.075,letter,transform=ax.transAxes,color=TEAL,fontsize=14,fontweight='bold',va='bottom')
 ax.set_title(title,loc='left',pad=14,color=INK)

def savefig(fig,key,sub='main'):
 d=OUT/sub; d.mkdir(exist_ok=True,parents=True)
 fig.subplots_adjust(top=.9,bottom=.11,left=.095,right=.97)
 for typ in ['pdf','png','tiff']:
  fn=d/(key+'.'+typ)
  fig.savefig(fn,bbox_inches='tight',pad_inches=.18,dpi=(600 if typ=='tiff' else 290 if typ=='png' else 160))
  if typ=='tiff':
   # TIFF is kept at 600 dpi but losslessly DEFLATE-compressed to avoid >600 MB output.
   with Image.open(fn) as im:
    compressed=fn.with_suffix('.compressed.tiff')
    im.save(compressed,compression='tiff_deflate',dpi=(600,600))
   # Pillow can retain the TIFF source handle on Windows after __exit__.
   im.close()
   compressed.replace(fn)
  logging.info('%s %s bytes',fn.relative_to(BASE),fn.stat().st_size)
 plt.close(fig)

def medtext(ax,x,y,title,value):
 ax.text(x,y,title,transform=ax.transAxes,color=GREY,fontsize=9,ha='left')
 ax.text(x,y-.11,value,transform=ax.transAxes,color=INK,fontsize=17,fontweight='bold',ha='left')

def errproof(df,src1,src2):
 assert len(df)==238 and df.mof_id.is_unique
 assert df[['lnS_wca','delta_lnS_attr','delta_lnS_elec']].notna().all().all()
 assert set(df.mof_id)==set(src1.mof_id)==set(src2.mof_id)
 for col in ['lnS_wca','delta_lnS_attr','delta_lnS_elec','lnS_full']:
  other=src2.set_index('mof_id').loc[df.mof_id,col].to_numpy()
  err=np.max(np.abs(df[col].to_numpy()-other))
  assert err <1e-8,(col,err)
 assert np.max(abs(df.lnS_full-(df.lnS_wca+df.delta_lnS_attr+df.delta_lnS_elec)))<1e-10
 assert (df.lnS_wca<0).all() and (df.delta_lnS_attr>0).all() and (df.delta_lnS_elec>0).all()
 assert (df.lnS_lj_only>0).all()

def make_fig1(df):
 fig,axes=plt.subplots(2,2,figsize=(11.7,8.5),gridspec_kw={'height_ratios':[1,1.02]});fig.subplots_adjust(hspace=.53,wspace=.31)
 ax=axes[0,0]; st=['lnS_wca','lnS_lj_only','lnS_full']; colors=[BLUE,CORAL,TEAL]
 rng=np.random.default_rng(20261031)
 for i,(name,c) in enumerate(zip(st,colors)):
  vals=df[name].to_numpy()
  jitter=rng.normal(0,.055,len(vals))
  ax.scatter(np.full(len(vals),i)+jitter,vals,s=5,alpha=.16,color=c,rasterized=True)
  q1,m,q3=np.percentile(vals,[25,50,75]);ax.plot([i,i],[q1,q3],lw=6,solid_capstyle='round',color=c)
  ax.plot([i-.15,i+.15],[m,m],lw=2.5,color=INK)
 ax.axhline(0,color=INK,lw=.9,ls='--',alpha=.7)
 ax.set_xticks(range(3),['WCA\nrepulsive','LJ-only\n+ attraction','Full\n+ electrostatics'])
 ax.set_ylabel(r'$\ln (K_{H,CO_2}/K_{H,N_2})$')
 label(ax,'a','Interaction-state distribution (238 MOFs)')
 ax=axes[0,1]
 for row in df.itertuples():
  vals=[row.lnS_wca,row.lnS_lj_only,row.lnS_full]
  ax.plot([0,1,2],vals,color=BLUE,alpha=.075,lw=.9,rasterized=True)
 meds=[df[x].median() for x in st]
 ax.plot([0,1,2],meds,color=INK,lw=2.9,marker='o',markersize=7,zorder=8)
 for i,v in enumerate(meds): ax.annotate(f'{v:.2f}',(i,v),xytext=(8,7),textcoords='offset points',color=INK,fontweight='bold')
 ax.axhline(0,color=GREY,lw=.9,ls='--')
 ax.set_xticks(range(3),['Repulsion','Attraction restored','Charges restored'])
 ax.set_ylabel('Log Henry selectivity')
 label(ax,'b','Trajectory through the nested potentials')
 ax=axes[1,0]
 vals=[df.delta_lnS_attr.to_numpy(),df.delta_lnS_elec.to_numpy()]
 vp=ax.violinplot(vals,positions=[0,1],showextrema=False,showmedians=False,widths=.72)
 for v,c in zip(vp['bodies'],[CORAL,TEAL]):v.set_facecolor(c);v.set_edgecolor(INK);v.set_alpha(.32)
 for i,(a,c) in enumerate(zip(vals,[CORAL,TEAL])):
  q1,med,q3=np.percentile(a,[25,50,75]);ax.plot([i,i],[q1,q3],lw=8,color=c,solid_capstyle='round');ax.plot([i-.14,i+.14],[med,med],color=INK,lw=2)
 ax.set_xticks([0,1],['Attractive increment','Electrostatic increment'])
 ax.set_ylabel(r'$\Delta \ln S$')
 label(ax,'c','Both increments positive, different scales')
 ax=axes[1,1];ax.set_axis_off()
 ax.text(0,1,'WHAT THE NUMBERS SAY',color=TEAL,weight='bold',size=10,va='top',transform=ax.transAxes)
 medtext(ax,.01,.84,'Median WCA preference',f'{np.exp(df.lnS_wca.median()):.3f} ×')
 medtext(ax,.51,.84,'Median attractive factor',f'{np.exp(df.delta_lnS_attr.median()):.2f} ×')
 medtext(ax,.01,.47,'Median electrostatic factor',f'{np.exp(df.delta_lnS_elec.median()):.2f} ×')
 medtext(ax,.51,.47,'Frameworks with LJ CO₂ preference',f'{(df.lnS_lj_only>0).sum()} / 238')
 ax.text(.01,.06,'Finite differences along a selected force-field path;\nnot separately measurable energy contributions.',transform=ax.transAxes,fontsize=9,color=GREY)
 label(ax,'d','Population-level summary')
 savefig(fig,'fig1_interaction_pathway')

def make_fig2(df):
 fig=plt.figure(figsize=(11.7,4.9));gs=fig.add_gridspec(1,2,width_ratios=[1.65,.85],wspace=.32)
 ax=fig.add_subplot(gs[0,0]);x=df.delta_lnS_attr;y=df.delta_lnS_elec
 sc=ax.scatter(x,y,c=df.lnS_full,cmap='viridis',s=34,alpha=.85,edgecolors='white',linewidths=.27)
 cb=fig.colorbar(sc,ax=ax,shrink=.85,pad=.015);cb.set_label('Final log selectivity')
 rho,p=spearmanr(x,y)
 ax.text(.035,.95,f'Spearman ρ = {rho:.3f}',transform=ax.transAxes,va='top',color=INK,fontsize=11,fontweight='bold',bbox={'facecolor':'white','edgecolor':'none','alpha':.9,'pad':4})
 ax.set_xlabel('Attractive increment, Δln S');ax.set_ylabel('Electrostatic increment, Δln S')
 label(ax,'a','Attraction and charge response are weakly coupled')
 ax=fig.add_subplot(gs[0,1]);d= df.copy();d['mix']=d.delta_lnS_elec/(d.delta_lnS_attr+d.delta_lnS_elec)
 ax.hist(d.mix,bins=np.linspace(0,.56,24),color=TEAL,alpha=.8,edgecolor='white',lw=.6)
 ax.axvline(d.mix.median(),color=CORAL,linewidth=2,label=f'Median = {d.mix.median():.2f}')
 ax.legend(frameon=False,fontsize=9,loc='upper right');ax.set_xlabel('Electrostatic share of added log selectivity');ax.set_ylabel('Number of MOFs')
 label(ax,'b','A small median share with a long tail')
 # Main title omitted to maintain clear panel hierarchy in journal-size graphics
 savefig(fig,'fig2_mechanism_diversity')

def make_fig3(geo):
 fig,axes=plt.subplots(1,2,figsize=(11.7,4.8),gridspec_kw={'width_ratios':[1,1]})
 names=['WCA','Attraction','Electrostatics','Final']
 colors=[BLUE,CORAL,TEAL,PURPLE];y=np.arange(4)
 ax=axes[0];ax.barh(y,geo.r2,color=colors,height=.59,alpha=.95)
 ax.set_yticks(y,names);ax.invert_yaxis();ax.set_xlim(-.02,1.04);ax.set_xlabel('Cross-validated $R^2$')
 for i,v in enumerate(geo.r2):ax.text(v+.02,i,f'{v:.3f}',va='center',fontsize=10,color=INK)
 label(ax,'a','What the selected pore descriptors predict')
 ax=axes[1];ratio=geo.mae/geo.baseline_mae
 ax.barh(y,ratio,color=colors,height=.59,alpha=.95)
 ax.axvline(1,color=GREY,lw=1.2,ls='--',label='Full-cohort median reference')
 ax.set_yticks(y,names);ax.invert_yaxis();ax.set_xlim(0,1.23);ax.set_xlabel('MAE / full-cohort median-reference MAE')
 for i,v in enumerate(ratio):ax.text(min(v+.022,1.14),i,f'{v:.2f}',va='center',fontsize=10,color=INK)
 ax.legend(loc='lower right',frameon=False,fontsize=8)
 label(ax,'b','Electrostatics gains almost nothing over baseline')
 # Panel titles carry the comparison
 savefig(fig,'fig3_geometry_information')

def make_fig4(df,pairs):
 row=pairs[pairs.case_label.str.contains('electrostatic')].iloc[0]
 ids=[row.mof_a,row.mof_b];m=df.set_index('mof_id').loc[ids]
 fig=plt.figure(figsize=(11.7,5));gs=fig.add_gridspec(1,3,width_ratios=[1.2,1,.95],wspace=.36)
 ax=fig.add_subplot(gs[0,0]);colors=[BLUE,CORAL]
 for i,(_,r) in enumerate(m.iterrows()):
  vals=[r.lnS_wca,r.lnS_lj_only,r.lnS_full]
  ax.plot(range(3),vals,'-o',color=colors[i],lw=2.8,ms=6,label=['M029','M085'][i])
 ax.axhline(0,color=GREY,ls='--',lw=.8)
 ax.set_xticks([0,1,2],['WCA','LJ-only','Full']);ax.set_ylabel('Log Henry selectivity');ax.legend(frameon=False,loc='upper left')
 label(ax,'a','Two geometry-nearest neighbours')
 ax=fig.add_subplot(gs[0,1]);gas=np.array(['CO₂','N₂']); xx=np.arange(2); w=.31
 for i,(_,r) in enumerate(m.iterrows()):
  v=[r.lnkh_mean_full_co2-r.lnkh_mean_lj_only_co2,r.lnkh_mean_full_n2-r.lnkh_mean_lj_only_n2]
  ax.bar(xx+(i-.5)*w,v,width=w,color=colors[i],label=['M029','M085'][i])
 ax.set_xticks(xx,gas);ax.set_ylabel(r'Full $-$ LJ-only $\Delta \ln K_H$')
 ax.legend(frameon=False,fontsize=9);label(ax,'b','The difference is CO₂-driven')
 ax=fig.add_subplot(gs[0,2]);ax.set_axis_off()
 metrics=[('Matched-space distance',f'{row.geometry_distance:.3f}'),
          ('WCA log-S difference',f'{abs(row.lnS_wca_a-row.lnS_wca_b):.3f}'),
          ('Electrostatic contrast',f'{row.abs_elec_contrast:.3f}'),
          ('Multiplier contrast',f'{row.elec_contrast_factor:.2f} ×')]
 for i,(title,val) in enumerate(metrics):
  y0=.89-i*.235
  ax.text(0,y0,title,transform=ax.transAxes,color=GREY,fontsize=9)
  ax.text(0,y0-.09,val,transform=ax.transAxes,color=INK,fontsize=17,fontweight='bold')
 label(ax,'c','Matched-pair audit')
 # Panel titles carry the comparison
 savefig(fig,'fig4_matched_contrast')

def make_fig5(df,represent):
 d=df.copy();d['rank_wca']=d.lnS_wca.rank(ascending=False,method='min');d['rank_lj']=d.lnS_lj_only.rank(ascending=False,method='min');d['rank_full']=d.lnS_full.rank(ascending=False,method='min')
 fig=plt.figure(figsize=(11.7,7.1));gs=fig.add_gridspec(2,2,height_ratios=[1,.92],wspace=.31,hspace=.48)
 for j,(a,b,title,c) in enumerate([('rank_wca','rank_lj','Attraction reorganizes the order',CORAL),('rank_lj','rank_full','Electrostatics mostly preserves order',TEAL)]):
  ax=fig.add_subplot(gs[0,j]);ax.scatter(d[a],d[b],s=22,alpha=.45,color=c,edgecolors='none');ax.plot([1,238],[1,238],ls='--',color=GREY,lw=1.2)
  ax.set_xlim(-2,241);ax.set_ylim(241,-2);ax.set_xlabel(a.replace('rank_','').upper()+' rank (1 = best)');ax.set_ylabel(b.replace('rank_','').upper()+' rank (1 = best)')
  rho=spearmanr(d[a],d[b]).statistic
  ax.text(.04,.93,f'ρ = {rho:.3f}',transform=ax.transAxes,color=INK,fontweight='bold',fontsize=11)
  label(ax,['a','b'][j],title)
 ax=fig.add_subplot(gs[1,:]);labels={'jointly_reinforced':'Jointly reinforced','weak_on_both_energetic_axes':'Weak on both axes','largest_attraction_rank_promotion':'Largest attraction promotion','largest_electrostatic_rank_promotion':'Largest electrostatic promotion'}
 yy=np.arange(len(represent))[::-1]
 for k,r in enumerate(represent.itertuples()):
  y0=yy[k];vals=[r.rank_wca,r.rank_lj,r.rank_full]
  ax.plot([0,1,2],vals,color=[BLUE,CORAL,TEAL,PURPLE][k],lw=2.5,marker='o',ms=6,label=labels.get(r.case_label,r.case_label))
  # Trajectories remain individually identified in the detached legend.
 ax.legend(frameon=False,fontsize=8.5,loc='upper left',bbox_to_anchor=(1.02,1.0))
 ax.invert_yaxis();ax.set_xlim(-.25,2.25);ax.set_ylim(245,-8);ax.set_xticks([0,1,2],['WCA','LJ-only','Full']);ax.set_ylabel('Rank (1 = highest selectivity)')
 label(ax,'c','Illustrative candidate trajectories (selected cases)')
 # Panel titles carry the comparison
 savefig(fig,'fig5_ranking_consequences')

def make_si(df):
 fig,axes=plt.subplots(1,2,figsize=(10.7,4.2))
 ax=axes[0];se=df.lnS_wca_se.to_numpy();lo=df.lnS_wca+1.96*se
 ax.hist(se,bins=22,color=BLUE,edgecolor='white',linewidth=.65);ax.axvline(.10,color=CORAL,ls='--',lw=1.5,label='0.10 precision threshold');ax.legend(frameon=False,fontsize=8)
 ax.set_xlabel('Standard error of WCA log selectivity');ax.set_ylabel('MOF count')
 label(ax,'a','Repulsive-reference precision')
 ax=axes[1];ax.scatter(df.lnS_wca,se,alpha=.5,c=np.where(lo>=0,CORAL,TEAL),s=20,edgecolors='none');ax.plot([-1,0],[1/1.96,0],color=GREY,ls='--',lw=1)
 ax.set_xlim(-.8,.03);ax.set_ylim(0,max(.2,se.max()*1.08));ax.set_xlabel('WCA log selectivity estimate');ax.set_ylabel('Estimated standard error')
 label(ax,'b',f'{int((lo>=0).sum())} estimates have upper normal-approx. 95% bound ≥ 0')
 savefig(fig,'figS1_precision_diagnostics','si')
 fig,axes=plt.subplots(1,2,figsize=(10.7,4.1))
 ax=axes[0];dc=df.lnkh_mean_full_co2-df.lnkh_mean_lj_only_co2;dn=df.lnkh_mean_full_n2-df.lnkh_mean_lj_only_n2
 ax.scatter(dc,dn,color=TEAL,alpha=.5,s=22,edgecolors='none');ax.axhline(0,color=GREY,ls='--');ax.axvline(0,color=GREY,ls='--');ax.set_xlabel('CO₂ full – LJ-only log Henry coefficient');ax.set_ylabel('N₂ full – LJ-only log Henry coefficient')
 label(ax,'a','Guest-specific electrostatic response (n = 238)')
 ax=axes[1];ax.hist(dc,bins=26,color=CORAL,alpha=.7,label='CO₂');ax.hist(dn,bins=26,color=BLUE,alpha=.62,label='N₂');ax.legend(frameon=False);ax.set_xlabel('Full – LJ-only log Henry coefficient');ax.set_ylabel('Count')
 label(ax,'b','Electrostatic response distribution by gas')
 savefig(fig,'figS2_gas_specific_increment','si')

def toc(df):
 fig,ax=plt.subplots(figsize=(7.5,3.4))
 med=[df.lnS_wca.median(),df.lnS_lj_only.median(),df.lnS_full.median()]
 xs=[.65,2.95,5.25];names=['REPULSION','+ ATTRACTION','+ ELECTROSTATICS']; cs=[BLUE,CORAL,TEAL]
 for x,m,c,t in zip(xs,med,cs,names):
  ax.scatter(x,m,s=370,color=c,zorder=4,edgecolor='white',linewidth=1.5)
  ax.text(x,m+.6,t,color=c,ha='center',weight='bold',fontsize=9)
  ax.text(x,m-.48,rf'$\ln S={m:.2f}$',color=INK,ha='center',fontsize=9)
 ax.plot(xs,med,color=INK,lw=2.2,zorder=2);ax.axhline(0,color=GREY,ls='--',lw=1)
 ax.set_xlim(-.15,6.05);ax.set_ylim(-1.15,4.45);ax.set_axis_off()
 ax.text(.5,-.12,'One framework panel. Three nested potentials. Distinct physical roles.',transform=ax.transAxes,ha='center',fontsize=9.5,color=INK)
 savefig(fig,'TOC_interaction_stages','toc')



def make_fig6(df):
 """New descriptive Figure 6: population balance, subgroups, and shortlist overlap."""
 d=df.copy()
 d['family']=d.mof_id.str.extract(r'^(DB0-m\d+)')
 assert d.family.value_counts().to_dict()=={'DB0-m15':210,'DB0-m12':28}
 fig,axes=plt.subplots(1,3,figsize=(12.8,4.5),gridspec_kw={'width_ratios':[.83,1.28,1.05]})
 fig.subplots_adjust(wspace=.41)
 ax=axes[0];fams=['DB0-m15','DB0-m12'];ns=[int((d.family==f).sum()) for f in fams]
 ax.barh([0,1],ns,color=[BLUE,TEAL],height=.55)
 for i,n in enumerate(ns):ax.text(n+3,i,f'{n} / 238',va='center',fontsize=10,color=INK)
 ax.set_yticks([0,1],fams);ax.set_xlim(0,270);ax.invert_yaxis()
 ax.set_xlabel('MOF count');label(ax,'a','Unequal identifier-family sizes')
 ax=axes[1];x=np.arange(2);wa=.27
 for j,f in enumerate(fams):
  g=d[d.family==f]
  at=g.delta_lnS_attr.median();el=g.delta_lnS_elec.median()
  ax.bar(j-wa/2,at,width=wa*1.65,color=CORAL,edgecolor='white',label='Attraction' if j==0 else None)
  ax.bar(j+wa*1.55,el,width=wa*1.65,color=TEAL,edgecolor='white',label='Electrostatics' if j==0 else None)
  ax.text(j-wa/2,at+.07,f'{at:.2f}',ha='center',fontsize=9,color=INK)
  ax.text(j+wa*1.55,el+.07,f'{el:.2f}',ha='center',fontsize=9,color=INK)
 ax.set_xticks(x+.17,fams);ax.set_ylim(0,3.2);ax.set_ylabel('Median log-selectivity increment')
 ax.legend(frameon=False,loc='upper right',fontsize=8)
 label(ax,'b','Within-family responses differ')
 ax=axes[2]
 trans=['WCA to LJ','LJ to full']
 top=[set(d.sort_values([c,'mof_id'],ascending=[False,True]).head(24).mof_id) for c in ['lnS_wca','lnS_lj_only','lnS_full']]
 together=[len(top[0]&top[1]),len(top[1]&top[2])];different=[24-n for n in together]
 ax.barh([0,1],together,color=TEAL,height=.53,label='Retained candidates')
 ax.barh([0,1],different,left=together,color=CORAL,height=.53,label='Replaced candidates')
 for i,(n,m) in enumerate(zip(together,different)):
  if n:ax.text(n/2,i,str(n),color='white',ha='center',va='center',weight='bold')
  ax.text(n+m/2,i,str(m),color='white',ha='center',va='center',weight='bold')
 ax.set_yticks([0,1],trans);ax.invert_yaxis();ax.set_xlim(0,24)
 ax.set_xlabel('Number of entries in top-24 shortlist')
 ax.legend(frameon=False,fontsize=8,loc='upper right',bbox_to_anchor=(1.05,1.25))
 label(ax,'c','Top-list sensitivity to each stage')
 savefig(fig,'fig6_family_and_shortlist')

def make_si_extended(df):
 d=df.copy();d['family']=d.mof_id.str.extract(r'^(DB0-m\d+)')
 fams=['DB0-m15','DB0-m12']
 fig,axes=plt.subplots(1,3,figsize=(12.3,4.3));fig.subplots_adjust(wspace=.34)
 for ax,(labeltext,col),letter in zip(axes,[('WCA reference','lnS_wca'),('Attraction','delta_lnS_attr'),('Electrostatics','delta_lnS_elec')],['a','b','c']):
  dat=[d.loc[d.family==f,col].to_numpy() for f in fams]
  vp=ax.violinplot(dat,positions=[0,1],showextrema=False,showmedians=True,widths=.72)
  for v,c in zip(vp['bodies'],[BLUE,TEAL]):v.set_facecolor(c);v.set_edgecolor(INK);v.set_alpha(.35)
  vp['cmedians'].set_color(INK)
  rng=np.random.default_rng(26)
  for i,arr in enumerate(dat):ax.scatter(i+rng.normal(0,.057,len(arr)),arr,s=6,alpha=.13,color=[BLUE,TEAL][i],rasterized=True)
  ax.set_xticks([0,1],fams);ax.set_ylabel('Log selectivity or increment')
  label(ax,letter,labeltext+' by identifier family')
 savefig(fig,'figS3_family_details','si')
 # Compact heatmap: deterministic stable sorts with source IDs as tie breaker.
 arrays=[]
 for stem,col in [('wca','lnS_wca'),('lj','lnS_lj_only'),('full','lnS_full')]:
  l=d.sort_values([col,'mof_id'],ascending=[False,True]).mof_id.head(24).tolist()
  arrays.append(set(l))
 ids=sorted(set.union(*arrays))
 ids=sorted(ids,key=lambda v:(v not in arrays[2],v not in arrays[1],v not in arrays[0],v))
 mat=np.array([[int(v in a) for a in arrays] for v in ids])
 fig,ax=plt.subplots(figsize=(7.7,10.8))
 from matplotlib.colors import ListedColormap
 ax.imshow(mat,aspect='auto',cmap=ListedColormap([PALE,TEAL]),vmin=0,vmax=1,interpolation='nearest')
 ax.set_xticks(range(3),['WCA','LJ-only','Full']);ax.set_yticks(np.arange(len(ids)),ids,fontsize=6.1)
 ax.xaxis.tick_top();ax.tick_params(axis='both',length=0)
 for i in np.arange(len(ids)+1)-.5:ax.axhline(i,color='white',lw=.7)
 for j in [-.5,.5,1.5,2.5]:ax.axvline(j,color='white',lw=1.2)
 ax.set_xlabel('White: outside top 24; teal: inside top 24',labelpad=13)
 ax.xaxis.set_label_position('bottom');ax.set_title('Membership of the union of three top-24 lists',pad=26,color=INK)
 savefig(fig,'figS4_shortlist_membership','si')

def main():
 df=pd.read_csv(BASE/'data/authoritative/mechanism_238_authoritative.csv')
 s1=pd.read_csv(BASE/'data/source_v2/figure_1_source.csv');s2=pd.read_csv(BASE/'data/source_v2/figure_2_source.csv')
 source=BASE/'data/figure_sources'
 geo=pd.read_csv(source/'figure_3.csv')
 pairs=pd.read_csv(source/'figure_4_pair.csv')
 represent=pd.read_csv(source/'figure_5_cases.csv')
 errproof(df,s1,s2)
 assert set(pairs.mof_a).union(set(pairs.mof_b)).issubset(set(df.mof_id))
 assert set(represent.mof_id).issubset(set(df.mof_id))
 assert len(geo)==4
 read=lambda file:pd.read_csv(source/file)
 make_fig1(read('figure_1.csv'));make_fig2(read('figure_2.csv'));make_fig3(geo)
 make_fig4(read('figure_4_values.csv'),pairs);make_fig5(read('figure_5_population.csv'),represent)
 make_fig6(read('figure_6.csv'));make_si(read('figure_S1_S2.csv'))
 # The shared extended function reads family coordinates and shortlist states.
 family=read('figure_S3.csv');membership=read('figure_S4.csv')
 make_si_extended(family.merge(membership,on=['mof_id','lnS_wca'],validate='one_to_one'));toc(read('TOC.csv'))
 r1=spearmanr(df.delta_lnS_attr,df.delta_lnS_elec).statistic
 rank=lambda x:df[x].rank(ascending=False,method='min')
 sumry={ 'population_n':len(df),'wca_negative_n':int((df.lnS_wca<0).sum()),'lj_positive_n':int((df.lnS_lj_only>0).sum()),
  'electrostatic_positive_n':int((df.delta_lnS_elec>0).sum()),'lnS_wca_median':float(df.lnS_wca.median()),
  'delta_lnS_attr_median':float(df.delta_lnS_attr.median()),'delta_lnS_elec_median':float(df.delta_lnS_elec.median()),
  'median_attr_multiplier':float(np.exp(df.delta_lnS_attr.median())),'median_elec_multiplier':float(np.exp(df.delta_lnS_elec.median())),
  'spearman_attr_elec':float(r1), 'rank_rho_wca_lj':float(spearmanr(rank('lnS_wca'),rank('lnS_lj_only')).statistic),
  'rank_rho_lj_full':float(spearmanr(rank('lnS_lj_only'),rank('lnS_full')).statistic),
  'max_telescoping_residual':float(np.abs(df.lnS_full-(df.lnS_wca+df.delta_lnS_attr+df.delta_lnS_elec)).max()),
  'wca_nominal_95_interval_crosses_zero_n':int(((df.lnS_wca+1.96*df.lnS_wca_se)>=0).sum()),
  'wca_SE_above_0p1_n':int((df.lnS_wca_se>.1).sum()),
  'top24_overlap_wca_to_lj':len(set(df.nlargest(24,'lnS_wca').mof_id)&set(df.nlargest(24,'lnS_lj_only').mof_id)),
  'top24_overlap_lj_to_full':len(set(df.nlargest(24,'lnS_lj_only').mof_id)&set(df.nlargest(24,'lnS_full').mof_id)),
  'family_m15_n':int(df.mof_id.str.startswith('DB0-m15_').sum()),'family_m12_n':int(df.mof_id.str.startswith('DB0-m12_').sum()),'fsc_suffix_n':int(df.mof_id.str.endswith('_fsc').sum()),
  'input_source':'unchanged 238-framework cohort; explicit figure_sources; restored final 14-feature saved OOF predictions',
  'limits':'Saved-prediction statistics and plots reproduced; no model refitting, molecular simulation, or voxel-field replay.'}
 (QA/'regenerated_metrics.json').write_text(json.dumps(sumry,indent=2,ensure_ascii=False)+'\n')
 h=[]
 for path in sorted((BASE/'data').rglob('*')):
  if path.is_file():h.append(f'{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.relative_to(BASE).as_posix()}')
 (QA/'input_hashes.sha256').write_text('\n'.join(h)+'\n')
 print(json.dumps(sumry,indent=2,ensure_ascii=False))
 print('PASS: raw-to-authoritative checks, nested identity, 6 main + 4 SI figures and TOC; TIFF/PNG/PDF')
if __name__=='__main__':
 argparse.ArgumentParser(description=__doc__).parse_args();main()
