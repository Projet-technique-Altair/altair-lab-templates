#!/bin/bash
set -euo pipefail

UPLOAD_DIR="/srv/portal/uploads"
ARCHIVE_DIR="/opt/backups"
STAMP="$(date +%Y%m%d-%H%M%S)"

/bin/mkdir -p "$ARCHIVE_DIR"
/bin/cd "$UPLOAD_DIR"

if [ -z "$(/bin/ls -A "$UPLOAD_DIR")" ]; then
  echo "[!] Nothing to archive"
  exit 0
fi

# Intentionally vulnerable for CTF:
# '*' expands attacker-controlled names that tar parses as options.
/bin/tar -czf "${ARCHIVE_DIR}/uploads-${STAMP}.tgz" *

echo "[+] archive done ${ARCHIVE_DIR}/uploads-${STAMP}.tgz"
