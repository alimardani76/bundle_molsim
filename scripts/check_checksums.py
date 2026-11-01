"""Check all released file digests without modifying any artifact."""
from pathlib import Path
import argparse,hashlib
ROOT=Path(__file__).resolve().parents[1]
def main():
    checked=0;errors=[]
    for name in ['SHA256SUMS.txt','input_hashes.sha256']:
        for line in (ROOT/'quality_control'/name).read_text().splitlines():
            if not line.strip():continue
            digest,path=line.split('  ',1);p=ROOT/path;checked+=1
            if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=digest:errors.append(path)
    if errors:raise SystemExit('Checksum failures: '+', '.join(errors))
    print('PASS:',checked,'checksums')
if __name__=='__main__':argparse.ArgumentParser(description=__doc__).parse_args();main()
