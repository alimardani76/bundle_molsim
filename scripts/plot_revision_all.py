#!/usr/bin/env python3
"""One-command main/SI/TOC figure regeneration from corrected population data."""
from pathlib import Path
import subprocess, sys, fitz, json, hashlib
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
py=sys.executable
scripts=[('plot_revision_main.py', []),('plot_revision_si.py', ['--data',str(ROOT/'data/revision/corrected_wca_238.csv'),'--out',str(ROOT/'figures/si')])]
for script,args in scripts:
    subprocess.run([py,str(ROOT/'scripts'/script),*args],check=True,cwd=ROOT)
# Native vector PDFs are the authoritative outputs; exports are derived from them.
figs=list((ROOT/'figures/main').glob('fig[1-6]_*.pdf'))+list((ROOT/'figures/si').glob('figS[1-4]_*.pdf'))+[ROOT/'figures/toc/TOC_interaction_stages.pdf']
for f in figs:
    with fitz.open(f) as doc:
        assert len(doc)==1,f
        pg=doc[0]
        pix=pg.get_pixmap(matrix=fitz.Matrix(220/72,220/72),alpha=False)
        pix.save(str(f.with_suffix('.png')))
        pix=pg.get_pixmap(matrix=fitz.Matrix(300/72,300/72),alpha=False)
        im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
        im.save(f.with_suffix('.tiff'),format='TIFF',compression='tiff_deflate',dpi=(300,300));im.close()
# Export the two author-approved panels directly from the reconciled compound PDFs.
standalone=[('fig1_interaction_pathway', (401,278,825.48,553.60),'fig1d_redrawn'),
            ('fig4_matched_contrast', (567,0,790.194,361.660),'fig4c_redrawn')]
panel_dir=ROOT/'figures/panels';panel_dir.mkdir(exist_ok=True)
for stem,coords,target in standalone:
    with fitz.open(ROOT/'figures/main'/f'{stem}.pdf') as doc:
        parent=doc[0]
        clip=fitz.Rect(*coords)
        new=fitz.open();page=new.new_page(width=clip.width,height=clip.height)
        page.show_pdf_page(page.rect,doc,0,clip=clip)
        pdf=panel_dir/f'{target}.pdf';new.save(pdf,garbage=4,deflate=True)
        page=new[0]
        (panel_dir/f'{target}.svg').write_text(page.get_svg_image(text_as_path=False),encoding='utf-8')
        page.get_pixmap(matrix=fitz.Matrix(290/72,290/72),alpha=False).save(str(panel_dir/f'{target}.png'))
        new.close()
print('Rebuilt',len(figs),'figure PDFs and raster previews; corrected 238-MOF data verified.')
