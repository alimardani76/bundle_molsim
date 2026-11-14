#!/usr/bin/env python3
"""Rebuild revised 2026 JCTC main figure PDFs from frozen corrected data.
Run via scripts/plot_revision_all.py; historical figure PDFs are used only as canvases
for the deliberately unchanged panels. Never reruns molecular simulations."""
from pathlib import Path
import re, shutil, hashlib, json, io, subprocess
import fitz
import numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import spearmanr
import zipfile
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'build/revision_figures'
P.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(ROOT/'data/revision/figure_baselines.zip') as baseline:
 baseline.extractall(P)
d=pd.read_csv(ROOT/'data/revision/corrected_wca_238.csv').set_index('alias')
C=dict(INK='#18324C',TEAL='#007F83',CORAL='#D56D52',BLUE='#4576AC',GOLD='#D6A13F',PURPLE='#745E9E',GREY='#788596',PALE='#E8EEF1')
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'axes.titlesize':14,'axes.titleweight':'bold','axes.labelsize':12,'xtick.labelsize':10,'ytick.labelsize':10,'pdf.fonttype':42,'axes.spines.top':False,'axes.spines.right':False,'axes.linewidth':.8,'savefig.facecolor':'white'})
W=d['lnS_wca_corrected'].to_numpy();A=d['delta_lnS_attr_corrected'].to_numpy();E=d['delta_lnS_elec_unchanged'].to_numpy();LJ=d['lnS_LJ_unchanged'].to_numpy();F=d['lnS_full_unchanged'].to_numpy();N=len(d)
assert N==238 and np.allclose(W+A+E,F,atol=1e-9)
assert (W<0).all() and (LJ>0).all()
assert round(float(np.exp(np.median(A))),2)==12.59
assert round(float(spearmanr(W,LJ).statistic),3)==-0.797
# Graphics generation: vector overlays preserve unaffected panels and the approved 1d/4c artwork.
def axes_panel(rect,painter):
 fig=plt.figure(figsize=(rect.width/72,rect.height/72),facecolor='white')
 painter(fig)
 buf=io.BytesIO();fig.savefig(buf,format='pdf',dpi=180,facecolor='white');plt.close(fig);buf.seek(0)
 return fitz.open(stream=buf.getvalue(),filetype='pdf')
def patch(oldname, edits):
 path=P/'figures'/f'{oldname}.pdf'; src=fitz.open(path);pg=src[0]
 for rect, painter in edits:
  r=fitz.Rect(*rect)
  pg.add_redact_annot(r,fill=(1,1,1))
  pg.apply_redactions(images=0,graphics=1,text=0)
  new=axes_panel(r,painter)
  pg.show_pdf_page(r,new,0,overlay=True,keep_proportion=False)
  new.close()
 src.save(path.with_name(oldname+'_new.pdf'),garbage=4,deflate=True)
 src.close();path.with_name(oldname+'_new.pdf').replace(path)
def title(ax,letter,text):
 ax.text(-.115,1.10,letter,color=C['TEAL'],weight='bold',size=17,transform=ax.transAxes)
 ax.set_title(text,loc='left',color=C['INK'],pad=14,fontweight='bold',fontsize=13.5)
def axstyle(ax):
 ax.tick_params(axis='both',colors=C['INK'],length=2.5)
 ax.spines['left'].set_color('#adb7c3');ax.spines['bottom'].set_color('#adb7c3')
def p1a(fig):
 ax=fig.add_axes([.12,.22,.79,.62]);title(ax,'a','Interaction-state distribution (238 MOFs)')
 rng=np.random.default_rng(20261115)
 for i,(vals,col) in enumerate(zip([W,LJ,F],[C['BLUE'],C['CORAL'],C['TEAL']])):
  ax.scatter(i+rng.normal(0,.049,N),vals,s=9,alpha=.17,color=col,rasterized=False,edgecolors='none')
  q1,m,q3=np.percentile(vals,[25,50,75]);ax.plot([i,i],[q1,q3],lw=12,color=col,solid_capstyle='round');ax.plot([i-.12,i+.12],[m,m],color=C['INK'],lw=2)
 ax.axhline(0,ls='--',color=C['GREY'],lw=.8);ax.set_xticks([0,1,2],['WCA\nrepulsive','LJ-only\n+ LJ complement','Full\n+ electrostatics']);ax.set_xlim(-.4,2.4);ax.set_ylim(-1,4.6);ax.set_ylabel('Log CO₂/N₂ selectivity');axstyle(ax)
def p1b(fig):
 ax=fig.add_axes([.13,.22,.80,.62]);title(ax,'b','Trajectory through the nested potentials')
 rng=np.random.default_rng(20261115)
 for w,lj,f in zip(W,LJ,F):ax.plot([0,1,2],[w,lj,f],lw=.35,alpha=.07,color=C['BLUE'])
 m=[np.median(v) for v in [W,LJ,F]]
 ax.plot([0,1,2],m,lw=3.2,color=C['INK'],marker='o',ms=6,zorder=3)
 for x,y in enumerate(m):ax.text(x+.025,y+.16,f'{y:.2f}',fontsize=11,weight='bold',color=C['INK'])
 ax.axhline(0,ls='--',color=C['GREY'],lw=.8);ax.set_xlim(-.08,2.21);ax.set_ylim(-1,4.55);ax.set_xticks([0,1,2],['Repulsion','LJ restored','Charges restored']);ax.set_ylabel('Log CO₂/N₂ selectivity');axstyle(ax)
def p1c(fig):
 ax=fig.add_axes([.14,.22,.79,.63]);title(ax,'c','Two positive increments, different scales')
 from scipy.stats import gaussian_kde
 for i,(vals,col) in enumerate([(A,C['CORAL']),(E,C['TEAL'])]):
  grid=np.linspace(max(0,float(vals.min())-.1),float(vals.max())+.15,250)
  kde=gaussian_kde(vals)(grid);kde=kde/kde.max()*.30
  ax.fill_betweenx(grid,i-kde,i+kde,color=col,alpha=.32,edgecolor=col,lw=.5)
  lo,med,hi=np.quantile(vals,[.25,.50,.75]);ax.plot([i,i],[lo,hi],lw=8,solid_capstyle='round',color=col);ax.scatter(i,med,color=C['INK'],s=24,zorder=3)
 ax.axhline(0,color=C['GREY'],lw=.8,ls='--');ax.set_xlim(-.5,1.5);ax.set_ylim(0,4.6);ax.set_xticks([0,1],['LJ–WCA increment','Charging increment']);ax.set_ylabel('Increment in ln S');axstyle(ax)
# reserved d panel, original confirmed approved design
patch('fig1_interaction_pathway',[( (0,0,400,276),p1a ),((401,0,825.48,276),p1b),((0,278,400,553.6),p1c)])
# Patch text on original approved 1(d) by whitened bounded zones, keeping graphics
# Font/rectangle coordinates from source PDF.
def replace_word(page,old,new,fontsize=8.2,color=(.09,.19,.28),dx=0,dy=0):
 hits=page.search_for(old)
 if len(hits)!=1:raise RuntimeError((old,hits))
 r=hits[0]; cover=fitz.Rect(r.x0-1.5,r.y0-1.0,r.x1+3,r.y1+1.0)
 page.add_redact_annot(cover,fill=(1,1,1))
 page.apply_redactions(images=0,graphics=1,text=0)
 page.insert_text((r.x0+dx,r.y1-1.2+dy),new,fontsize=fontsize,fontname='hebo' if False else 'helv',color=color,overlay=True)
fig=P/'figures/fig1_interaction_pathway.pdf';doc=fitz.open(fig);page=doc[0]
for a,b,size in [('-0.204','-0.207',8.2),('+2.537','+2.533',8.2),('0.816×','0.813×',10.3),('12.65×','12.59×',10.3)]:replace_word(page,a,b,size)
# Restore the original d marker partially removed by the neighboring b-panel crop.
page.insert_text((430,287),'d',fontsize=16,fontname='hebo',color=(0,.50,.52),overlay=True)
doc.save(fig.with_name('fig1_tmp.pdf'),garbage=4,deflate=True);doc.close();fig.with_name('fig1_tmp.pdf').replace(fig)
# fig2 two panels: corrected A,E and share in reported path
def p2a(fig):
 ax=fig.add_axes([.15,.20,.70,.65]);title(ax,'a','Attraction and charging responses')
 sc=ax.scatter(A,E,c=F,cmap='viridis',s=23,alpha=.85,edgecolors='none');ax.set_xlim(0.7,4.65);ax.set_ylim(0,2.12)
 ax.set_xlabel('LJ–WCA increment, A');ax.set_ylabel('Charging increment, E');ax.text(.03,.92,f'Spearman ρ = {spearmanr(A,E).statistic:.3f}',transform=ax.transAxes,fontsize=12,color=C['INK'],weight='bold')
 cb=fig.colorbar(sc,ax=ax,pad=.02,shrink=.86);cb.set_label('Full ln S',fontsize=10);cb.ax.tick_params(labelsize=9);axstyle(ax)
def p2b(fig):
 ax=fig.add_axes([.16,.20,.76,.65]);title(ax,'b','Path-defined charging fraction')
 z=E/(A+E);ax.hist(z,bins=np.linspace(0,.59,27),color=C['TEAL'],alpha=.86,edgecolor='white',linewidth=.35)
 med=np.median(z);ax.axvline(med,color=C['CORAL'],lw=2,label=f'Median = {med:.2f}');ax.legend(frameon=False,fontsize=10,loc='upper right')
 ax.set_xlabel('E/(A + E) on stated path');ax.set_ylabel('Number of MOFs');axstyle(ax)
patch('fig2_mechanism_diversity',[((0,0,520,369.54),p2a),((520,0,829.965,369.54),p2b)])
# fig3 metrics from existing Phase3 report, training median baseline
metric_table=pd.read_csv(ROOT/'data/revision/geometry_cv_metrics_for_fig3.csv')
assert metric_table['target'].tolist()==['WCA','LJ-WCA','Charging','Full']
metrics=metric_table['R2_geometry_5fold_OOF'].to_numpy().tolist()
ratios=(metric_table['MAE_geometry_5fold_OOF']/metric_table['MAE_training_fold_median_reference']).to_numpy().tolist()
names=['WCA','LJ–WCA','Charging','Full']
cols=[C['BLUE'],C['CORAL'],C['TEAL'],C['PURPLE']]
def make_bars(fig,values,letter,ttl,xlabel,xlim,fmt):
 ax=fig.add_axes([.23,.17,.69,.66]);title(ax,letter,ttl)
 y=np.arange(4);ax.barh(y,values,color=cols,height=.52,edgecolor='none');ax.set_yticks(y,names);ax.invert_yaxis();ax.set_xlim(*xlim);ax.set_xlabel(xlabel)
 if letter=='b':ax.axvline(1,ls='--',lw=1,color=C['GREY'])
 for k,(v,c) in enumerate(zip(values,cols)):ax.text(v+.012,k,format(v,fmt),va='center',fontsize=12,color=C['INK'])
 axstyle(ax)
patch('fig3_geometry_information',[( (0,0,412,365.83),lambda f:make_bars(f,metrics,'a','Geometry-only predictive fit','Out-of-fold R²',(0,1.12),'.3f') ),( (414,0,830.63,365.83),lambda f:make_bars(f,ratios,'b','Normalized error against fold baseline','MAE / training-median MAE',(0,1.17),'.2f') )])
# fig4 redraw panel a only, leave b historical gas figures, c approved graphic design
def p4a(fig):
 ax=fig.add_axes([.19,.20,.75,.66]);title(ax,'a','Geometry-nearest pair')
 for alias,col in [('M029',C['BLUE']),('M085',C['CORAL'])]:
  r=d.loc[alias];ax.plot([0,1,2],[r.lnS_wca_corrected,r.lnS_LJ_unchanged,r.lnS_full_unchanged],marker='o',lw=2.8,ms=5,color=col,label=alias)
 ax.axhline(0,ls='--',lw=.8,color=C['GREY']);ax.legend(frameon=False,fontsize=12);ax.set_xticks([0,1,2],['WCA','LJ-only','Full']);ax.set_ylim(-.6,4.45);ax.set_ylabel('Log CO₂/N₂ selectivity');axstyle(ax)
patch('fig4_matched_contrast',[((0,0,255,361.66),p4a)])
# Remove original a-panel's overflowing old labels outside its crop, without touching panel b.
fp=P/'figures/fig4_matched_contrast.pdf';dd=fitz.open(fp);dd[0].add_redact_annot(fitz.Rect(255,0,285,361.66),fill=(1,1,1));dd[0].apply_redactions(images=0,graphics=1,text=0);dd.save(fp.with_name('fig4_trim.pdf'),garbage=4,deflate=True);dd.close();fp.with_name('fig4_trim.pdf').replace(fp)
fig=P/'figures/fig4_matched_contrast.pdf';doc=fitz.open(fig);page=doc[0];replace_word(page,'0.003','0.006',fontsize=17.5,color=(.09,.19,.28))
# Small per-bar numbers in b; values are rounded original-cohort gas-specific log-KH increments.
gas=pd.read_csv(ROOT/'data/revision/matched_pair_gas_increments.csv').set_index(['alias','gas'])
for xx,yy,alias,kind,col in [(340,307,'M029','CO2',(0.27,.46,.67)),(377,51,'M085','CO2',(0.83,.43,.32)),(456,313,'M029','N2',(0.27,.46,.67)),(491,313,'M085','N2',(0.83,.43,.32))]:
 lab=f"{gas.loc[(alias,kind),'delta_lnKH_full_minus_LJ']:.3f}"
 page.insert_text((xx,yy),lab,fontsize=7.2,fontname='helv',color=col,overlay=True)
doc.save(fig.with_name('fig4_tmp.pdf'),garbage=4,deflate=True);doc.close();fig.with_name('fig4_tmp.pdf').replace(fig)
# fig5 ranks; panel b unchanged; selected four paths preserved by identifier
rw=d.lnS_wca_corrected.rank(ascending=False,method='min');rl=d.lnS_LJ_unchanged.rank(ascending=False,method='min');rf=d.lnS_full_unchanged.rank(ascending=False,method='min')
assert round(float(spearmanr(rw,rl).statistic),3)==-0.797
assert len(set(rw.nsmallest(24).index)&set(rl.nsmallest(24).index))==0
assert len(set(rl.nsmallest(24).index)&set(rf.nsmallest(24).index))==17
def p5a(fig):
 ax=fig.add_axes([.14,.23,.80,.60]);title(ax,'a','LJ attraction reorganizes ranking')
 ax.scatter(rw,rl,color=C['CORAL'],s=9,alpha=.52,edgecolors='none');ax.plot([1,238],[238,1],ls=':',color=C['GREY'],lw=1)
 ax.set_xlim(0,240);ax.set_ylim(240,0);ax.set_xlabel('WCA rank (1 = best)');ax.set_ylabel('LJ rank (1 = best)');ax.text(.09,.08,'ρ = −0.797',transform=ax.transAxes,color=C['INK'],weight='bold',fontsize=15);axstyle(ax)
def p5c(fig):
 ax=fig.add_axes([.065,.22,.70,.64]);title(ax,'c','Historically selected illustrative trajectories')
 for alias,label,col in [('M201','Jointly reinforced',C['GOLD']),('M104','Weak on both',C['PURPLE']),('M223','Attraction promotion',C['CORAL']),('M084','Charging promotion',C['BLUE'])]:
  ax.plot([0,1,2],[rw[alias],rl[alias],rf[alias]],lw=2.6,marker='o',ms=5,color=col,label=label)
 ax.set_ylim(245,0);ax.set_xlim(-.08,2.06);ax.set_xticks([0,1,2],['WCA','LJ-only','Full']);ax.set_ylabel('Rank (1 = best)');axstyle(ax)
 ax.legend(loc='center left',bbox_to_anchor=(1.01,.52),frameon=False,fontsize=11)
patch('fig5_ranking_consequences',[((0,0,490,261),p5a),((0,264,1034.46,472.5),p5c)])
# fig6 preserves a exactly, changes b values and clarifies c overlap
group_is_co=d.mof_id.str.contains('DB0-m15');assert int(group_is_co.sum())==210
mgA=[float(d.loc[group_is_co,'delta_lnS_attr_corrected'].median()),float(d.loc[~group_is_co,'delta_lnS_attr_corrected'].median())]
mgE=[float(d.loc[group_is_co,'delta_lnS_elec_unchanged'].median()),float(d.loc[~group_is_co,'delta_lnS_elec_unchanged'].median())]
def p6b(fig):
 ax=fig.add_axes([.18,.20,.74,.66]);title(ax,'b','Response by metal subset')
 x=np.arange(2);ax.bar(x-.17,mgA,.34,color=C['CORAL'],label='LJ–WCA');ax.bar(x+.17,mgE,.34,color=C['TEAL'],label='Charging')
 for i in range(2):
  ax.text(i-.17,mgA[i]+.05,f'{mgA[i]:.2f}',ha='center',fontsize=12,color=C['INK'])
  ax.text(i+.17,mgE[i]+.05,f'{mgE[i]:.2f}',ha='center',fontsize=11,color=C['INK'])
 ax.set_xlim(-.55,1.55);ax.set_ylim(0,3.35);ax.set_xticks([0,1],['Co (n=210)','Ni (n=28)']);ax.set_ylabel('Median increment in ln S');ax.legend(frameon=False,fontsize=10,loc='upper right');axstyle(ax)
def p6c(fig):
 ax=fig.add_axes([.21,.22,.73,.60]);title(ax,'c','Top-24 point-estimate turnover')
 y=np.array([0,1]);ret=[0,17];rep=[24,7]
 ax.barh(y,rep,color=C['CORAL'],label='Replaced',height=.54,left=ret);ax.barh(y,ret,color=C['TEAL'],label='Retained',height=.54)
 ax.set_yticks(y,['WCA → LJ','LJ → full']);ax.set_ylim(1.6,-.6);ax.set_xlim(0,26);ax.set_xlabel('Number of top-24 entries');ax.legend(frameon=False,fontsize=10,loc='lower right')
 ax.text(12,0,'0 retained / 24 replaced',ha='center',va='center',color='white',fontsize=11,weight='bold');ax.text(8.5,1,'17',va='center',ha='center',color='white',fontsize=12,weight='bold');ax.text(20.5,1,'7',va='center',ha='center',color='white',fontsize=12,weight='bold');axstyle(ax)
patch('fig6_family_and_shortlist',[((300,0,593,371.87),p6b),((593,0,888.123,371.87),p6c)])
# Update the numeric TOC annotation; historical −0.20 rounds to corrected −0.21.
with zipfile.ZipFile(ROOT/'data/revision/figure_baselines.zip') as zin:
 raw_toc=zin.read('figures/TOC_interaction_stages.pdf')
tocdoc=fitz.open(stream=raw_toc,filetype='pdf');tpg=tocdoc[0]
tr=tpg.search_for('−0.20')[0]
tpg.add_redact_annot(fitz.Rect(tr.x0-1,tr.y0-1,tr.x1+2,tr.y1+1),fill=(1,1,1))
tpg.apply_redactions(images=0,graphics=1,text=0)
tpg.insert_text((tr.x0,tr.y1-1.3),'-0.21',fontsize=9.5,fontname='helv',color=(.1,.2,.29))
tocdoc.save(P/'figures/TOC_interaction_stages.pdf',garbage=4,deflate=True);tocdoc.close()
# numerical/artifact QA report
checks={n:{'exists':(P/'figures'/f'{n}.pdf').exists(),'bytes':(P/'figures'/f'{n}.pdf').stat().st_size} for n in ['fig1_interaction_pathway','fig2_mechanism_diversity','fig3_geometry_information','fig4_matched_contrast','fig5_ranking_consequences','fig6_family_and_shortlist']}
qa={'source':str(P/'main.tex'),'figures':checks,'corrected_WCA_median':float(np.median(W)),'corrected_A_median':float(np.median(A)),'spearman_WCA_LJ':float(spearmanr(W,LJ).statistic),'spearman_A_E':float(spearmanr(A,E).statistic),'E_share_median':float(np.median(E/(A+E))),'top24_WCA_LJ_overlap':0,'top24_LJ_full_overlap':17,'subgroup_medians_A':mgA,'subgroup_medians_E':mgE}
(ROOT/'quality_control/revision_figure_checks.json').parent.mkdir(exist_ok=True,parents=True)
(ROOT/'quality_control/revision_figure_checks.json').write_text(json.dumps(qa,indent=2))
print(json.dumps(qa,indent=2))

# Publish the rebuilt PDFs after numerical checks.
for fname in ['fig1_interaction_pathway','fig2_mechanism_diversity','fig3_geometry_information','fig4_matched_contrast','fig5_ranking_consequences','fig6_family_and_shortlist']:
    shutil.copy2(P/'figures'/f'{fname}.pdf',ROOT/'figures/main'/f'{fname}.pdf')
shutil.copy2(P/'figures/TOC_interaction_stages.pdf', ROOT/'figures/toc/TOC_interaction_stages.pdf')
