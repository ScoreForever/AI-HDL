#!/usr/bin/env bash
set -euo pipefail
base=/workspace/tools/tex-cjk
if [ ! -f "$base/usr/share/texlive/texmf-dist/tex/xelatex/xecjk/xeCJK.sty" ] && ! kpsewhich xeCJK.sty >/dev/null 2>&1; then
 deb=$(mktemp /tmp/aihdl-cjk.XXXXXX.deb)
 trap 'rm -f "$deb"' EXIT
 curl -fSL --retry 2 --max-time 90 'https://deb.debian.org/debian/pool/main/t/texlive-lang/texlive-lang-cjk_2024.20250309-1_all.deb' -o "$deb"
 echo "56c795c17b392766c66132f469aab024c374eb92848685ab1d66072a14115b66  $deb" | sha256sum -c -
 mkdir -p "$base"
 dpkg-deb -x "$deb" "$base"
fi
# Existing image prerequisites: pandoc, xelatex, matplotlib, Noto CJK fonts.
command -v pandoc
command -v xelatex
