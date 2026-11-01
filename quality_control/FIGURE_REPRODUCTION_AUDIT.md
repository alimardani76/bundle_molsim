# Final figure and document validation

PASS. All six main figures, four SI figures and one TOC graphic regenerated in the existing clean environment from tracked explicit CSV inputs. PDF, PNG and compressed 600-dpi TIFF outputs exist for every figure. The Windows batch command completed successfully. No simulation or predictive model fitting ran.

All 11 final figure PDFs were rendered and visually reviewed. Figure 3 uses the restored saved-final-OOF metrics and explicitly labels the full-cohort median reference. The original illustrative M029/M085 data are retained. TOC annotation overlap is resolved. Figure content and numerical annotations are verified; cross-environment byte/pixel identity is not claimed.

The 23-page main manuscript and 15-page SI compiled with pdfLaTeX/BibTeX. All main figures 1?6 and SI figures S1?S4 are included; table/equation S numbering is correct. Final logs have no undefined references/citations or overfull boxes. All pages were rendered and reviewed. A final specific SI command-sequence correction added the validated checksum-refresh steps after plotting; only the SI was rebuilt for that correction, its affected pages were reviewed, and its build hashes were updated. Numerical audits were not repeated for this documentation-only change.

The final clean test exposed and removed one manifest pointer to a local audit-only artifact. Historical SHA match records remain in the public provenance manifest. Release commands now require no files outside this repository. The successful clean pipeline commands are recorded in VALIDATION_COMMANDS.json.
