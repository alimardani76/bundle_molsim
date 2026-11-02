#!/usr/bin/env python3
"""Shayan's design-only redraw for JCTC V13 panels 1(d) and 4(c).
Sources: the frozen 238-row figure_1.csv and exact pair snapshot.
The graphics remain visual supplements to the verified scientific results.
"""
import csv, hashlib, json, math
from pathlib import Path
from statistics import median
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import fitz

HERE=Path(__file__).resolve().parent
NAVY='#17344F'; MUTED='#52687B'; BLUE='#4077AD'; CORAL='#D46C53'; TEAL='#007F83'
BORDER='#CDD9E2'; LIGHT='#EAF1F4'; BG='#FFFFFF'
plt.rcParams.update({'font.family':'DejaVu Sans','pdf.fonttype':42,'ps.fonttype':42,
                     'svg.fonttype':'none','savefig.facecolor':'white','savefig.edgecolor':'white',
                     'text.color':NAVY})
STATS={
  'n':238, 'median_lnS_wca':-0.203749485237,
  'median_delta_lnS_attr':2.537375623648,
  'median_delta_lnS_elec':0.309492036602,
  'wca_positive':0,'lj_positive':238
}
def get_csv(path):
 with Path(path).open(newline='',encoding='utf-8-sig') as f:return list(csv.DictReader(f))
def verify_numeric_sources(repo=None):
 pair_rows=get_csv(HERE/'figure_4_pair_verified.csv')
 pair=[x for x in pair_rows if 'electrostatic' in x['case_label']]
 assert len(pair)==1
 if repo:
  root=Path(repo)/'data'/'figure_sources'
  rows=get_csv(root/'figure_1.csv')
  assert len(rows)==238 and len({r['mof_id'] for r in rows})==238
  for sourcecol,checkname in [('lnS_wca','median_lnS_wca'),('delta_lnS_attr','median_delta_lnS_attr'),('delta_lnS_elec','median_delta_lnS_elec')]:
   result=median(float(row[sourcecol]) for row in rows)
   assert math.isclose(result,STATS[checkname],abs_tol=2e-8,rel_tol=0), (sourcecol,result,STATS[checkname])
  assert sum(float(r['lnS_wca'])>0 for r in rows)==STATS['wca_positive']
  assert sum(float(r['lnS_lj_only'])>0 for r in rows)==STATS['lj_positive']
  for r in rows:
   assert math.isclose(float(r['lnS_full']),float(r['lnS_wca'])+float(r['delta_lnS_attr'])+float(r['delta_lnS_elec']),abs_tol=1e-9,rel_tol=0)
  pr=[x for x in get_csv(root/'figure_4_pair.csv') if 'electrostatic' in x['case_label']]
  assert len(pr)==1
  for k in pair[0]:
   try:assert math.isclose(float(pr[0][k]),float(pair[0][k]),abs_tol=1e-9,rel_tol=0),k
   except ValueError:assert pr[0][k]==pair[0][k]
  mode='full_source_csv_verified'
 else:mode='verified_V13_summary_and_full_precision_pair_snapshot'
 p=pair[0]
 eleca=float(p['delta_lnS_elec_a']);elecb=float(p['delta_lnS_elec_b'])
 delta=abs(elecb-eleca);factor=math.exp(delta)
 geometry=float(p['geometry_distance']);wca=abs(float(p['lnS_wca_a'])-float(p['lnS_wca_b']))
 assert math.isclose(delta,float(p['abs_elec_contrast']),abs_tol=1e-11)
 assert math.isclose(factor,float(p['elec_contrast_factor']),abs_tol=1e-11)
 assert math.isclose(geometry,0.2575292552493384,abs_tol=1e-12)
 assert math.isclose(wca,0.0031379311761581,abs_tol=1e-9)
 assert math.isclose(math.exp(STATS['median_delta_lnS_attr']),12.646435,abs_tol=.0002)
 return dict(mode=mode,elec_a=eleca,elec_b=elecb,delta=delta,factor=factor,geometry=geometry,wca=wca)
def canvas(w,h):
 fig=plt.figure(figsize=(w/72,h/72),facecolor='white')
 ax=fig.add_axes([0,0,1,1]);ax.set_xlim(0,w);ax.set_ylim(h,0);ax.axis('off')
 return fig,ax
def txt(ax,x,y,s,size=9,color=NAVY,weight='normal',ha='left',va='center',**k):
 return ax.text(x,y,s,fontsize=size,fontweight=weight,color=color,ha=ha,va=va,**k)
def ln(ax,x1,y1,x2,y2,col=BORDER,lw=.8,**kwargs):
 ax.plot([x1,x2],[y1,y2],color=col,lw=lw,solid_capstyle='round',**kwargs)
def fig1_panel(w,h):
 fig,ax=canvas(w,h)
 ax.set_xlim(0,424);ax.set_ylim(275,0)
 txt(ax,15,20,'d',14,TEAL,'bold')
 txt(ax,38,20,'Population-level summary',12.6,NAVY,'bold')
 txt(ax,16,47,'CO₂-FAVORING POINT ESTIMATES',8.1,TEAL,'bold')
 txt(ax,16,66,'WCA / repulsion',8.4,MUTED,'medium')
 txt(ax,16,88,'0 / 238',20.5,BLUE,'bold')
 txt(ax,407,66,'LJ-only / attraction restored',8.4,MUTED,ha='right')
 txt(ax,407,88,'238 / 238',20.5,CORAL,'bold',ha='right')
 ln(ax,179,86,235,86,BORDER,1.7)
 ax.add_patch(FancyArrowPatch((223,86),(237,86),arrowstyle='-|>',mutation_scale=11,lw=0,color=CORAL))
 txt(ax,207,72,'restore',7.0,MUTED,ha='center')
 txt(ax,207,100,'attraction',7.0,MUTED,ha='center')
 ln(ax,15,115,408,115,BORDER,0.9)
 txt(ax,16,134,'MEDIAN PATHWAY TERMS',8.2,TEAL,'bold')
 txt(ax,405,134,'factor',8.2,MUTED,ha='right')
 xlo,xhi=146,341
 def xx(v):return xlo+(v+.5)/3.5*(xhi-xlo)
 xzero=xx(0)
 labels=[('WCA baseline',STATS['median_lnS_wca'],BLUE,'0.816×',163),
         ('Attraction added',STATS['median_delta_lnS_attr'],CORAL,'12.65×',195),
         ('Charges added',STATS['median_delta_lnS_elec'],TEAL,'1.36×',227)]
 for lab,val,color,factor,y in labels:
  txt(ax,16,y-4,lab,8.2,NAVY,'bold')
  txt(ax,16,y+10,f'{val:+.3f} ln S',7.2,MUTED)
  ln(ax,xlo,y,xhi,y,LIGHT,6.2)
  ln(ax,xzero,y,xx(val),y,color,5)
  ax.add_patch(Circle((xx(val),y),2.8,facecolor=color,edgecolor='white',linewidth=.65))
  txt(ax,410,y,factor,10,NAVY,'bold',ha='right')
 for t in [-.5,0,1,2,3]:
  xp=xx(t);ln(ax,xp,243,xp,247,BORDER,.65)
  txt(ax,xp,254,('0' if t==0 else f'{t:g}'),6.9,MUTED,ha='center')
 ln(ax,xzero,149,xzero,236,BORDER,1,linestyle=':')
 txt(ax,16,265,'Separate medians; factors = exp(median log term).',6.8,MUTED)
 return fig
def fig4_panel(v,w,h):
 fig,ax=canvas(w,h)
 ax.set_xlim(0,223);ax.set_ylim(362,0)
 txt(ax,11,22,'c',14,TEAL,'bold')
 txt(ax,34,22,'Matched-pair contrast',12.4,NAVY,'bold')
 txt(ax,12,58,'BASELINE SIMILARITY',8.3,TEAL,'bold')
 txt(ax,12,81,'Geometry distance',8.0,MUTED)
 txt(ax,12,106,f"{v['geometry']:.3f}",19,NAVY,'bold')
 ln(ax,111,77,111,118,BORDER,.7)
 txt(ax,122,81,'WCA |Δln S|',8.0,MUTED)
 txt(ax,122,106,f"{v['wca']:.3f}",19,NAVY,'bold')
 ln(ax,12,128,211,128,BORDER,.9)
 txt(ax,12,149,'ELECTROSTATIC INCREMENT',8.2,TEAL,'bold')
 txt(ax,12,168,'Δln S = full − LJ-only',8.0,MUTED)
 xa,xb=19,202
 def xp(val):return xa+val/2.2*(xb-xa)
 y=219;ln(ax,xa,y,xb,y,BORDER,1.4)
 ln(ax,xp(v['elec_a']),y,xp(v['elec_b']),y,TEAL,2.4)
 for t in (0,1,2):
  x=xp(t);ln(ax,x,y+6,x,y+11,BORDER,.8);txt(ax,x,y+21,str(t),7.1,MUTED,ha='center')
 ax.scatter([xp(v['elec_a'])],[y],s=66,marker='o',facecolor=BLUE,edgecolor='white',linewidth=1,zorder=5)
 ax.scatter([xp(v['elec_b'])],[y],s=69,marker='D',facecolor=CORAL,edgecolor='white',linewidth=1,zorder=5)
 txt(ax,11,194,f"M029  {v['elec_a']:.3f}",9.1,BLUE,'bold')
 txt(ax,210,194,f"M085  {v['elec_b']:.3f}",9.1,CORAL,'bold',ha='right')
 txt(ax,111,261,f"|Δ(Δln S)| = {v['delta']:.3f}",10.1,NAVY,'bold',ha='center')
 ln(ax,12,282,211,282,BORDER,.9)
 txt(ax,12,309,f"{v['factor']:.2f}×",29,NAVY,'bold')
 txt(ax,12,336,'electrostatic enhancement ratio',8.5,MUTED)
 txt(ax,210,309,'exp(1.860)',8.0,TEAL,ha='right')
 return fig
def export(fig,prefix):
 for ext in ['pdf','svg','png']:
  kw={} if ext!='png' else {'dpi':450}
  fig.savefig(str(prefix)+'.'+ext,facecolor='white',pad_inches=0,**kw)
 plt.close(fig)
def merge(baseline,panel,out,rect):
 d=fitz.open(baseline);assert len(d)==1
 page=d[0];page.add_redact_annot(rect,fill=(1,1,1),cross_out=False)
 page.apply_redactions(images=0,graphics=1,text=0)
 p=fitz.open(panel);page.show_pdf_page(rect,p,0,keep_proportion=False,overlay=True)
 d.save(out,garbage=4,deflate=True);d.close();p.close()
