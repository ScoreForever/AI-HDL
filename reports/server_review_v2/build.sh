#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
# Local cloud fallback only; normal TeX installations use their own package paths.
if [ -d /workspace/tools/tex-cjk/usr/share/texlive/texmf-dist/tex ]; then
  export TEXINPUTS="/workspace/tools/tex-cjk/usr/share/texlive/texmf-dist/tex//:${TEXINPUTS:-}"
fi
# --from-md regenerates TeX. Omit it to preserve manual edits to report.tex.
if [ "${1:-}" = --from-md ]; then
  pandoc report.md -s -t latex --include-in-header=header.tex \
    -V documentclass=article -V papersize=a4 -V geometry:margin=22mm \
    -V fontsize=10pt -V mainfont='DejaVu Serif' -V monofont='DejaVu Sans Mono' \
    -V CJKmainfont='Noto Serif CJK SC' -V colorlinks=true -o report.tex
fi
xelatex -interaction=nonstopmode -halt-on-error -jobname=Lab1_Report_team01 report.tex > build-pass1.log
xelatex -interaction=nonstopmode -halt-on-error -jobname=Lab1_Report_team01 report.tex > build-pass2.log
printf 'Created Lab1_Report_team01.pdf\n'
