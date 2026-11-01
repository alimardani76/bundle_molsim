"""Write checksums for selected release artifacts, excluding historical bulk."""
from pathlib import Path
import argparse,hashlib
ROOT=Path(__file__).resolve().parents[1]
TOP={'README.md','README_START_HERE.md','CHANGELOG_SCIENTIFIC.md','requirements.txt','run_figures_windows.bat','.gitignore','.gitattributes'}
DIRS=['scripts','data','figures/main','figures/si','figures/toc','manuscript','supporting_information','docs','environment','.github','quality_control']
SKIP={'SHA256SUMS.txt','input_hashes.sha256','release_check.json','INITIAL_AUDIT.md','editorial_checks.json','NUMERICAL_RECONCILIATION.csv','final_evidence_audit.json','acs-main.bib'}
def selected():
    found={ROOT/p for p in TOP if (ROOT/p).is_file()}
    for folder in DIRS:
        for p in (ROOT/folder).rglob('*'):
            if not p.is_file() or '__pycache__' in p.parts or p.suffix in ['.pyc','.aux','.blg','.log','.out','.toc','.synctex'] or p.name in SKIP:continue
            found.add(p)
    return sorted(found,key=lambda p:p.relative_to(ROOT).as_posix())
def run():
    q=ROOT/'quality_control';q.mkdir(exist_ok=True)
    line=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(ROOT).as_posix()
    files=selected();(q/'SHA256SUMS.txt').write_text('\n'.join(line(p) for p in files)+'\n')
    inputs=sorted(p for p in (ROOT/'data').rglob('*') if p.is_file())
    (q/'input_hashes.sha256').write_text('\n'.join(line(p) for p in inputs)+'\n')
    print('Checksummed',len(files),'release artifacts and',len(inputs),'data inputs.')
if __name__=='__main__':argparse.ArgumentParser(description=__doc__).parse_args();run()
