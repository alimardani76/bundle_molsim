"""Regenerate SI figures S1, S3, S4 from the corrected 238-framework table.
S2 is deliberately retained: its full-minus-LJ gas responses are unchanged by WCA correction.
Usage: python rebuild_si_figures.py --data data/corrected_wca_238.csv --out figures
"""
from pathlib import Path
import argparse
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from scipy.stats import t

ap=argparse.ArgumentParser();ap.add_argument('--data',type=Path,default=Path('data/corrected_wca_238.csv'));ap.add_argument('--out',type=Path,default=Path('figures'));args=ap.parse_args()
df=pd.read_csv(args.data).sort_values('alias').reset_index(drop=True)
assert len(df)==238 and df.alias.is_unique and df.precision_pass.all()
W=df.lnS_wca_corrected.to_numpy();A=df.delta_lnS_attr_corrected.to_numpy();E=df.delta_lnS_elec_unchanged.to_numpy();L=df.lnS_LJ_unchanged.to_numpy();F=df.lnS_full_unchanged.to_numpy()
assert (W<0).all() and (L>0).all() and (df.CI95_upper.to_numpy()<0).all()
assert np.allclose(W+A+E,F,atol=1e-8)
assert round(np.median(W),6)==round(-0.207469591893,6)
assert round(np.median(A),6)==round(2.53268730205,6)
args.out.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10.2,'axes.labelsize':10.5,'axes.titlesize':11.3,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42,'savefig.facecolor':'white'})
INK='#18324C';TEAL='#007F83';BLUE='#4576AC';CORAL='#D56D52';GREY='#667582'
def save(fig,name):
 fig.savefig(args.out/(name+'.pdf'),bbox_inches='tight',pad_inches=.18)
 fig.savefig(args.out/(name+'.png'),dpi=200,bbox_inches='tight',pad_inches=.18)
 plt.close(fig)
def panel(ax,name,title):
 ax.set_title(f'{name}   {title}',loc='left',weight='bold',color=INK,pad=9)

# S1: registered paired SE and the t(df=2) sign resolution, never old 1.96-SE diagnostics.
se=df.SE_lnS_registered.to_numpy();upper=df.CI95_upper.to_numpy();critical=t.ppf(.975,2)
fig,axes=plt.subplots(1,2,figsize=(11.4,4.3));fig.subplots_adjust(wspace=.29)
ax=axes[0];panel(ax,'a','Corrected WCA precision (238 frameworks)')
ax.hist(se,bins=23,color=BLUE,edgecolor='white',linewidth=.4);ax.set_xlabel('Registered SE of log selectivity');ax.set_ylabel('Framework count');ax.axvline(se.max(),color=CORAL,lw=1,ls='--');ax.text(.96,.94,f'Max SE = {se.max():.4f}',transform=ax.transAxes,ha='right',va='top',color=INK)
ax=axes[1];panel(ax,'b','Each individual 95% interval remains below zero')
ax.scatter(se,W,s=18,color=TEAL,alpha=.67,edgecolors='none',label='Corrected estimates');x=np.linspace(0,se.max()*1.05,100);ax.plot(x,-critical*x,ls='--',lw=1.4,color=CORAL,label=r'Upper $t_2$ limit = 0');ax.axhline(0,color=GREY,lw=.75);ax.set_xlabel('Registered SE of log selectivity');ax.set_ylabel(r'Corrected $\ln S_{\rm WCA}$');ax.legend(loc='lower left',frameon=False,fontsize=8.5);ax.set_ylim(min(W)*1.06,.025)
fig.suptitle('Recomputed repulsive-reference sampling diagnostics',color=INK,weight='bold',fontsize=13,y=1.02);save(fig,'figS1_precision_diagnostics')

# S3: actual Co/Ni composition, not inferred SBU/topology.
mask=[df.mof_id.str.startswith('DB0-m15').to_numpy(),df.mof_id.str.startswith('DB0-m12').to_numpy()]
fig,axes=plt.subplots(1,3,figsize=(11.9,4.25));fig.subplots_adjust(wspace=.30)
for ax,(letter,title,values) in zip(axes,[('a','Repulsive reference',W),('b','LJ complement',A),('c','Charging increment',E)]):
 panel(ax,letter,title)
 rng=np.random.default_rng({'a':1,'b':2,'c':3}[letter]); groups=[values[m] for m in mask]
 bx=ax.boxplot(groups,positions=[0,1],widths=.35,patch_artist=True,showfliers=False,medianprops={'color':'white','linewidth':1.8})
 for patch,c in zip(bx['boxes'],[BLUE,TEAL]):patch.set_facecolor(c);patch.set_alpha(.9)
 for el in bx['whiskers']+bx['caps']:el.set_color(GREY)
 for i,vals in enumerate(groups):ax.scatter(np.full(len(vals),i)+rng.normal(0,.08,len(vals)),vals,s=7,color=[BLUE,TEAL][i],alpha=.22,edgecolors='none')
 ax.set_xticks([0,1],['Co (n=210)','Ni (n=28)']);ax.set_ylabel('Log selectivity / increment' if letter=='a' else 'Dimensionless log increment');ax.grid(axis='y',alpha=.14)
 ax.text(.5,.97,f'Medians: {np.median(groups[0]):.3f} / {np.median(groups[1]):.3f}',ha='center',va='top',transform=ax.transAxes,fontsize=8.2,color=INK)
fig.suptitle('Composition-stratified 238-MOF data (not topology-family validation)',color=INK,weight='bold',fontsize=13,y=1.02)
save(fig,'figS3_family_details')

# S4: corrected WCA shortlist and unchanged LJ/full shortlists; alias map is in CSV.
cols=['lnS_wca_corrected','lnS_LJ_unchanged','lnS_full_unchanged']
tops=[]
for col in cols:tops.append(set(df.sort_values([col,'alias'],ascending=[False,True],kind='mergesort').alias.head(24)))
assert len(tops[0]&tops[1])==0 and len(tops[1]&tops[2])==17
union=sorted(set.union(*tops))
mat=np.array([[1 if k in ids else 0 for ids in tops] for k in union])
fig,ax=plt.subplots(figsize=(6.6,13.5));fig.subplots_adjust(left=.22,right=.88,bottom=.045,top=.955)
ax.imshow(mat,aspect='auto',cmap=ListedColormap(['#f3f6f8',TEAL]),vmin=0,vmax=1,interpolation='nearest')
ax.set_xticks(np.arange(3),['WCA','LJ-only','Full']);ax.xaxis.tick_top();ax.tick_params(axis='x',labelsize=10,pad=7)
ax.set_yticks(np.arange(len(union)),union);ax.tick_params(axis='y',length=0,labelsize=7.7,pad=5)
ax.set_xticks(np.arange(-.5,3,.999),minor=True);ax.set_yticks(np.arange(-.5,len(union),1),minor=True)
ax.grid(which='minor',color='white',linewidth=.8);ax.tick_params(which='minor',bottom=False,left=False)
ax.set_title(f'Corrected point-estimate top-24 union (n={len(union)})\n0/24 WCA–LJ; 17/24 LJ–full common entries',loc='left',fontsize=11.3,color=INK,weight='bold',pad=27)
ax.text(0,-.085,'Teal = selected in state; pale = outside that state\nRows identify frameworks by stable M-alias; see source CSV for full IDs.',transform=ax.transAxes,fontsize=9,color=GREY,va='top')
save(fig,'figS4_shortlist_membership')
print('SI figures created and validated; union',len(union),'max WCA SE',se.max())
