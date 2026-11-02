#!/usr/bin/env python3
"""Publication postprocessor for Shayan's Figure 1(d)/4(c) redesign.

Runs after regenerate_figures.py. Preserves other panels. Validates all 238
tracked figure records and full-precision M029/M085 matched-pair source before
writing PDFs or raster exports. Does not alter scientific data or ML models.
"""
from __future__ import annotations
import argparse,json,hashlib,shutil,tempfile
from pathlib import Path
import numpy as np
import fitz
from PIL import Image
from final_panel_assets import redraw_v2 as art

FIGURE_NAMES=('fig1_interaction_pathway','fig4_matched_contrast')
def sha256(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def untouched_pixels(original,revised,rect,dpi=144):
 with fitz.open(original) as src,fitz.open(revised) as dst:
  assert len(src)==len(dst)==1
  assert abs(src[0].rect.width-dst[0].rect.width)<.01 and abs(src[0].rect.height-dst[0].rect.height)<.01
  matrix=fitz.Matrix(dpi/72,dpi/72)
  a=src[0].get_pixmap(matrix=matrix,alpha=False);b=dst[0].get_pixmap(matrix=matrix,alpha=False)
  assert (a.width,a.height,a.n)==(b.width,b.height,b.n)
  aa=np.frombuffer(a.samples,np.uint8).reshape(a.height,a.width,a.n)
  bb=np.frombuffer(b.samples,np.uint8).reshape(b.height,b.width,b.n)
  ys,xs=np.indices((a.height,a.width));x0,y0,x1,y1=rect;sc=dpi/72;margin=sc
  outside=(xs<(x0*sc-margin))|(xs>=(x1*sc+margin))|(ys<(y0*sc-margin))|(ys>=(y1*sc+margin))
  return {'unchanged_area_pixels_compared':int(outside.sum()),'changed_pixels_outside_panel':int(np.count_nonzero(np.any(aa!=bb,axis=2)&outside))}
def rasterize(pdf,png,tiff):
 with fitz.open(pdf) as doc:
  page=doc[0]
  pix=page.get_pixmap(matrix=fitz.Matrix(290/72,290/72),alpha=False);pix.save(str(png))
  pix=page.get_pixmap(matrix=fitz.Matrix(600/72,600/72),alpha=False)
  im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
  im.save(tiff,format='TIFF',compression='tiff_deflate',dpi=(600,600));im.close()
def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[1])
 p.add_argument('--qa-output',type=Path,default=None)
 a=p.parse_args();repo=a.repo.resolve();fig_dir=repo/'figures/main'
 for name in FIGURE_NAMES:
  assert (fig_dir/(name+'.pdf')).is_file()
 numbers=art.verify_numeric_sources(repo=repo)
 assert numbers['mode']=='full_source_csv_verified'
 with tempfile.TemporaryDirectory(prefix='molsim_panel_redraw_') as td:
  temp=Path(td);base=temp/'base';base.mkdir();panels=temp/'panels';panels.mkdir()
  result=temp/'redrawn';result.mkdir()
  for name in FIGURE_NAMES:shutil.copy2(fig_dir/(name+'.pdf'),base/(name+'.pdf'))
  with fitz.open(base/(FIGURE_NAMES[0]+'.pdf')) as d1,fitz.open(base/(FIGURE_NAMES[1]+'.pdf')) as d4:
   size1=d1[0].rect;size4=d4[0].rect
  r1=fitz.Rect(401,278,size1.width,size1.height)
  r4=fitz.Rect(567,0,size4.width,size4.height)
  assert abs(r1.width-424.48)<1 and abs(r1.height-275.60)<1 and abs(r4.width-223.194)<1 and abs(r4.height-361.660)<1
  art.export(art.fig1_panel(r1.width,r1.height),panels/'fig1d_final')
  art.export(art.fig4_panel(numbers,r4.width,r4.height),panels/'fig4c_final')
  art.merge(base/(FIGURE_NAMES[0]+'.pdf'),panels/'fig1d_final.pdf',result/(FIGURE_NAMES[0]+'.pdf'),r1)
  art.merge(base/(FIGURE_NAMES[1]+'.pdf'),panels/'fig4c_final.pdf',result/(FIGURE_NAMES[1]+'.pdf'),r4)
  checks={}
  for name,rect,values in [
   (FIGURE_NAMES[0],r1,('0 / 238','238 / 238','12.65','0.816','1.36')),
   (FIGURE_NAMES[1],r4,('0.258','0.003','0.141','2.001','1.860','6.42'))]:
   qa=untouched_pixels(base/(name+'.pdf'),result/(name+'.pdf'),rect)
   assert qa['changed_pixels_outside_panel']==0,(name,qa)
   with fitz.open(result/(name+'.pdf')) as pdf:
    t=pdf[0].get_text()
    for v in values:assert v in t,(name,'missing',v)
   checks[name]=qa
   rasterize(result/(name+'.pdf'),result/(name+'.png'),result/(name+'.tiff'))
  for name in FIGURE_NAMES:
   for ext in ('.pdf','.png','.tiff'):shutil.copy2(result/(name+ext),fig_dir/(name+ext))
 qa={'mode':numbers['mode'],'verified':numbers,'panels':checks,
  'pdf_sha256':{name:sha256(fig_dir/(name+'.pdf')) for name in FIGURE_NAMES},
  'scope':'Only Figure 1(d) and 4(c) changed. All other scientific inputs and panels preserved.'}
 out=a.qa_output or repo/'quality_control/final_panel_redraw.json'
 out.parent.mkdir(exist_ok=True,parents=True);out.write_text(json.dumps(qa,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(qa,indent=2))
if __name__=='__main__':main()
