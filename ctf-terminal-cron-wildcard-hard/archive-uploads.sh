#!/bin/bash
set -euo pipefail

UPLOAD_DIR="/srv/portal/uploads"
ARCHIVE_DIR="/opt/backups"
STAMP="$(date +%Y%m%d-%H%M%S)"

/bin/mkdir -p "$ARCHIVE_DIR"
/bin/cd "$UPLOAD_DIR"

if [ -z "$(/bin/ls -A "$UPLOAD_DIR")" ]; then
  echo "[!] No uploads to archive"
  exit 0
fi

# Intentionally vulnerable for CTF:
# wildcard expansion allows attacker-controlled file names to be parsed as tar options.
/bin/tar -czf "${ARCHIVE_DIR}/uploads-${STAMP}.tgz" *

/usr/bin/find "$ARCHIVE_DIR" -type f -name 'uploads-*.tgz' -mmin +30 -delete
echo "[+] Archive created: ${ARCHIVE_DIR}/uploads-${STAMP}.tgz"
