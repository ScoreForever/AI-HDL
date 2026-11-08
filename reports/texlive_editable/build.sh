#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
for pass in 1 2; do
 xelatex -interaction=nonstopmode -halt-on-error -jobname=Lab1_Report_team01 report.tex
done
