#!/usr/bin/env bash
set -euo pipefail
# Official Debian trixie amd64 package, checksum from its HTTPS Packages index.
base=/workspace/tools/iverilog
if [ ! -x "$base/usr/bin/iverilog" ]; then
  deb=$(mktemp /tmp/aihdl-iverilog.XXXXXX.deb)
  trap 'rm -f "$deb"' EXIT
  curl -fSL --retry 2 --max-time 90 'https://deb.debian.org/debian/pool/main/i/iverilog/iverilog_12.0-2+b1_amd64.deb' -o "$deb"
  echo "febe027d2d3f5a7e570844d55758339ab5490acc09f404f214a8719d89d07056  $deb" | sha256sum -c -
  mkdir -p "$base"
  dpkg-deb -x "$deb" "$base"
fi
"$base/usr/bin/iverilog" -B "$base/usr/lib/x86_64-linux-gnu/ivl" -V
