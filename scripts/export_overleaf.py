#!/usr/bin/env python3
"""Export the frozen scientific release to a standalone Overleaf project.

Only layout paths differ from the frozen GitHub TeX source. No model fitting,
simulation, data conversion, replotting, or scientific editing takes place.
"""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import zipfile

RELEASE = "b7390df6efa58d5fd4ff2c6d665d3616b6183d25"
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "dist" / "overleaf_project"
ZIP = ROOT / "dist" / f"JCTC_OVERLEAF_SYNCED_{RELEASE[:8]}.zip"
EXPECTED = {
 "manuscript/main.tex": "cf1934945a184a47ce669e98801bc4880a9bce48",
 "supporting_information/supporting_information.tex": "96c4aac0096d1bdfa9e335a3341f9bda2206a9e0",
 "manuscript/references.bib": "184f491cd09ff8d01f6c5e3d3ad68bc29414dd5c",
 "CHANGELOG_SCIENTIFIC.md": "618ff0e437a20caab36fcc3688857e51376a25ee",
 "figures/main/fig1_interaction_pathway.pdf": "98d016ff811d205cf40817d6161148c0d6cc502f",
 "figures/main/fig2_mechanism_diversity.pdf": "c8a138b1917e8124b19b4d1c2e927d0209732586",
 "figures/main/fig3_geometry_information.pdf": "465fb53771efb4269052aa3aa8479502314d0edf",
 "figures/main/fig4_matched_contrast.pdf": "e9cebc12499191136d50601b1752b29db7dd8b88",
 "figures/main/fig5_ranking_consequences.pdf": "956f694bb72ef0231be46092d0da1a6a0c8df0f6",
 "figures/main/fig6_family_and_shortlist.pdf": "e8fbfc4b8bcf2bd4af4684209be227f50e4bac27",
 "figures/si/figS1_precision_diagnostics.pdf": "b665cc8acd7b09b92858fa49eae78775607a55e7",
 "figures/si/figS2_gas_specific_increment.pdf": "91390ba7cef2bb02be68f1487bbe3a9b4b3fa5d2",
 "figures/si/figS3_family_details.pdf": "3bb2b458ebab3075ffca306d938464430f6fdfbe",
 "figures/si/figS4_shortlist_membership.pdf": "4318c91badf3aaab74a6f413070f66896a1ccb0d",
 "figures/toc/TOC_interaction_stages.pdf": "a083099e90a99e1ed36a6b4272fbf0a783e9cbe3",
}
def blob(b):
 return hashlib.sha1(f"blob {len(b)}\0".encode()+b).hexdigest()

def read_git(path):
 b=subprocess.check_output(["git","show",f"{RELEASE}:{path}"],cwd=ROOT)
 actual=blob(b)
 assert actual==EXPECTED[path], (path,actual,EXPECTED[path])
 return b

def put(path,data):
 dest=OUT/path;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)

def main():
 if OUT.exists():
  import shutil
  shutil.rmtree(OUT)
 payload={path:read_git(path) for path in EXPECTED}
 main=payload["manuscript/main.tex"].decode("utf8")
 si=payload["supporting_information/supporting_information.tex"].decode("utf8")
 old=r"\graphicspath{{../figures/main/}{../figures/si/}}"
 assert main.count(old)==1,"Unexpected main graphics path"
 main=main.replace(old,r"\graphicspath{{figures/}}")
 old=r"\graphicspath{{../figures/si/}{../figures/main/}}"
 assert si.count(old)==1,"Unexpected SI graphics path"
 si=si.replace(old,r"\graphicspath{{figures/}}")
 old=r"\bibliography{../manuscript/references}"
 assert si.count(old)==1,"Unexpected SI bibliography path"
 si=si.replace(old,r"\bibliography{references}")
 put("main.tex",main.encode("utf8"))
 put("supporting_information.tex",si.encode("utf8"))
 put("references.bib",payload["manuscript/references.bib"])
 put("CHANGELOG_SCIENTIFIC.md",payload["CHANGELOG_SCIENTIFIC.md"])
 for path,b in payload.items():
  if path.startswith("figures/"):
   put("figures/"+Path(path).name,b)
 for name in ["main.tex","supporting_information.tex"]:
  t=(OUT/name).read_text()
  for f in re.findall(r"\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}",t):
   assert (OUT/"figures"/Path(f).name).is_file(),(name,f)
  assert "../" not in t,("Nonportable parent path",name)
 readme=(
  "# JCTC Overleaf submission — synchronized publication files\n\n"
  "Frozen publication source: https://github.com/alimardani76/bundle_molsim/commit/"+RELEASE+"\n\n"
  "Includes the verified main manuscript, Supporting Information, references, all ten scientific PDFs and the TOC PDF.\n"
  "Select main.tex as the Overleaf main document for the article. To compile SI, select supporting_information.tex.\n\n"
  "Only TeX image-directory and SI bibliography paths were changed to flatten the layout for Overleaf.\n"
  "The underlying GitHub TeX and PDF sources were checked by Git blob SHA-1 before packaging.\n"
  "This is the version that supersedes V13_JCTC_submit(1).zip.\n"
 )
 put("README_OVERLEAF.md",readme.encode())
 manifest={"source_repo":"alimardani76/bundle_molsim","frozen_commit":RELEASE,
  "source_git_blob_sha1":EXPECTED,
  "changes_to_tex":["graphicspath to figures/","SI bibliography path to references"],
  "output_sha256":{p.relative_to(OUT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
   for p in OUT.rglob("*") if p.is_file()}}
 put("OVERLEAF_SYNC_MANIFEST.json",(json.dumps(manifest,indent=2)+"\n").encode())
 ZIP.parent.mkdir(exist_ok=True)
 with zipfile.ZipFile(ZIP,"w",zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p in sorted(OUT.rglob("*")):
   if p.is_file():z.write(p,p.relative_to(OUT).as_posix())
 with zipfile.ZipFile(ZIP) as z:
  assert len(z.namelist())==len(list(OUT.rglob("*.*")))
  assert all(z.testzip() is None for _ in [0])
 print(f"PASS: verified {len(EXPECTED)} original Git blobs; exported {ZIP.name}, {ZIP.stat().st_size} bytes.")
 print("Files in direct-upload artifact:", sorted(p.relative_to(OUT).as_posix() for p in OUT.rglob("*") if p.is_file()))
if __name__=="__main__":main()
