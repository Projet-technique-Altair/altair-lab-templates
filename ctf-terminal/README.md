# PATH Hijacking Challenge — Guided Terminal CTF (Intermediate)

## Context
You are a pentester for TechCorp. An internal server runs a backup script as `root` via cron.
Your mission is to exploit a `PATH` misconfiguration to execute your own binary and read a root-only flag.

## Objective
Capture the flag located at:
- `/root/flag.txt`

After exploitation, the flag must be retrievable here (readable by `student`):
- `/opt/output/flag.txt`

## What you will learn
- How to read and understand cron jobs (`/etc/crontab`)
- How command resolution works via `PATH`
- How to spot a dangerous privileged script calling a command without an absolute path
- How to exploit PATH hijacking to escalate privileges (via root cron)

## Run the lab

### Build
```bash
docker build -t altair-path-hijacking:v1 .
```
### Run
```bash
docker run --rm -it --name path-hijack altair-path-hijacking:v1
```
### Execute 
```bash
docker exec -it path-hijack bash -lc 'exec su - student'
```
