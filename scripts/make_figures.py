"""Regenerate the 6 main, 4 SI and 1 TOC scientific figures from released sources."""
from pathlib import Path
import argparse,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
def main():
    for name in ['make_results.py','regenerate_figures.py','redraw_final_panels.py']:
        subprocess.run([sys.executable,str(ROOT/'scripts'/name)],cwd=ROOT,check=True)
if __name__=='__main__':argparse.ArgumentParser(description=__doc__).parse_args();main()
