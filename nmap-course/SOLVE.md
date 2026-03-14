# How to Solve the Nmap Lab

This file explains the intended resolution path for the lab `Nmap Basics - First Recon`.

## Goal

Identify the services exposed on the local machine and answer the guided questions.

## Step 1. Verify that Nmap is installed

Run:

```bash
nmap --version
```

Expected idea:
- confirm that `nmap` is available
- this is the exact answer expected for step 1

## Step 2. Read the built-in help

Run:

```bash
nmap -h
```

Expected idea:
- inspect the built-in help page
- this is the exact answer expected for step 2

## Step 3. Run a basic scan on localhost

Run:

```bash
nmap 127.0.0.1
```

Expected idea:
- perform a default scan against localhost
- this is the exact answer expected for step 3

What the learner should notice:
- at least port `22/tcp` is open for SSH
- port `80/tcp` is open for HTTP

## Step 4. Scan specific ports

Run:

```bash
nmap -p 22,80 127.0.0.1
```

Expected idea:
- use `-p` to target selected ports
- this is the exact answer expected for step 4

## Step 5. Detect service versions

Run:

```bash
nmap -sV 127.0.0.1
```

Expected idea:
- use Nmap service version detection
- this is the exact answer expected for step 5

What the learner should notice:
- SSH is running on port `22`
- HTTP is running on port `80`

## Step 6. Use aggressive detection

Run:

```bash
nmap -A 127.0.0.1
```

Expected idea:
- use aggressive mode
- this is the exact answer expected for step 6

## Step 7. Report open services

From the scan output, report the result in the expected format:

```text
22/tcp ssh, 80/tcp http
```

This is the exact answer expected for step 4.

## Full intended resolution flow

```bash
nmap --version
nmap -h
nmap 127.0.0.1
nmap -p 22,80 127.0.0.1
nmap -sV 127.0.0.1
nmap -A 127.0.0.1
```

Then submit:

```text
22/tcp ssh, 80/tcp http
```

## Why this works

The container starts:
- an SSH service on port `22`
- a Python HTTP server on port `80`

So localhost intentionally exposes two simple services for reconnaissance training.
