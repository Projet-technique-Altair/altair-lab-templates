#!/bin/bash
set -euo pipefail

SRC="/var/ops/reports/pending/report.txt"
DEST="/var/ops/reports/public/latest-report.txt"

if [ ! -f "$SRC" ]; then
  echo "[!] Missing source report"
  exit 0
fi

if [ -L "$DEST" ]; then
  echo "[!] Destination is a symlink, refusing"
  exit 1
fi

# Intentionally vulnerable TOCTOU window for CTF.
/bin/sleep 6

/bin/cat "$SRC" > "$DEST"
/bin/chown root:root "$DEST"
/bin/chmod 440 "$DEST"

echo "[+] Published report to $DEST"
