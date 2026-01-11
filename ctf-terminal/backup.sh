#!/bin/bash
set -u

echo "[+] Running backup as $(id)"

tar -czf /tmp/backup.tar.gz /home/student

echo "[+] Backup finished"
