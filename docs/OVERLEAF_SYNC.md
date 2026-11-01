# Overleaf/GitHub synchronized submission

The original V13 Overleaf ZIP is **not** the same as the scientific release. The publication source of truth is frozen at [commit 4227244e](https://github.com/alimardani76/bundle_molsim/commit/4227244e23912611facf6b60d2b84eb4bc97971e).

This repository exports a flat Overleaf package using exactly the TeX and figure PDF blobs from that commit. It rewrites only the two \`\\graphicspath\` directives and the SI bibliography's relative path. Scientific wording, numbers and original figures are not changed.

## Download

Open [GitHub Actions: Export frozen JCTC manuscript for Overleaf](https://github.com/alimardani76/bundle_molsim/actions/workflows/export-overleaf.yml), then choose the most recent successful run. Under **Artifacts** download \`JCTC-Overleaf-Ready-4227244e\`. The downloaded artifact ZIP is an Overleaf-ready project whose root contains \`main.tex\`, \`supporting_information.tex\`, \`references.bib\`, \`figures/\` and a manifest.

A separate \`JCTC-Overleaf-ZIP-4227244e\` artifact contains a ZIP inside the downloaded artifact; extract that inner ZIP if you prefer a named submission ZIP.

## Compile

Upload the ZIP as a **new Overleaf project** and select \`main.tex\` as the main document. To compile the SI, select \`supporting_information.tex\` as the main document. Keep old V13 as a separate historical project.

To generate locally from this repository, with Git installed and the pinned commit available:

\`\`\`bash
python scripts/export_overleaf.py
\`\`\`

No venv, simulations, model training, plotting or Python packages are required for this export. Every source blob is verified against a pinned Git SHA-1. The output manifest includes file SHA-256 hashes.

The publication repo’s original \`manuscript/main.tex\`, \`supporting_information/supporting_information.tex\`, and figure PDFs remain unmodified. This export only adapts paths for Overleaf.
