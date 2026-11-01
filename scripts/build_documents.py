"""Build main and SI with pdfLaTeX/BibTeX, rejecting unresolved document errors."""
from pathlib import Path
import argparse,hashlib,json,re,subprocess
ROOT=Path(__file__).resolve().parents[1]
def main():
    records=[]
    for folder,stem in [('manuscript','main'),('supporting_information','supporting_information')]:
        cwd=ROOT/folder
        # Clear only auxiliary outputs inside each explicit document directory.
        for ext in ['aux','bbl','blg','log','out','toc']:
            p=cwd/(stem+'.'+ext)
            if p.is_file():p.unlink()
        for cmd in [['pdflatex','-interaction=nonstopmode','-halt-on-error',stem+'.tex'],['bibtex',stem],['pdflatex','-interaction=nonstopmode','-halt-on-error',stem+'.tex'],['pdflatex','-interaction=nonstopmode','-halt-on-error',stem+'.tex']]:
            p=subprocess.run(cmd,cwd=cwd,capture_output=True,timeout=120)
            records.append(dict(document=stem,command=cmd,exit_code=p.returncode))
            if p.returncode:raise RuntimeError(p.stdout.decode(errors='replace')[-5000:])
        log=(cwd/(stem+'.log')).read_text(errors='replace')
        assert not re.search(r'(undefined|There were undefined|Rerun to get cross-references right|Overfull \\hbox)',log,re.I),(stem,'unresolved LaTeX diagnostics')
        print(stem,'compiled; references/citations/layout diagnostics pass',flush=True)
    hashes={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'manuscript/main.tex',ROOT/'manuscript/main.pdf',ROOT/'manuscript/references.bib',ROOT/'supporting_information/supporting_information.tex',ROOT/'supporting_information/supporting_information.pdf']}
    (ROOT/'quality_control/document_build.json').write_text(json.dumps(dict(status='PASS',commands=records,artifacts=hashes),indent=2)+'\n')
if __name__=='__main__':argparse.ArgumentParser(description=__doc__).parse_args();main()
