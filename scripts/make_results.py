"""Regenerate final paper statistics and explicit figure inputs without fitting."""
from pathlib import Path
import argparse,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
def main():
    for name in ['export_derived_tables.py','reconcile_results.py','export_figure_sources.py']:
        subprocess.run([sys.executable,str(ROOT/'scripts'/name)],cwd=ROOT,check=True)
if __name__=='__main__':argparse.ArgumentParser(description=__doc__).parse_args();main()
