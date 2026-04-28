# Nmap Basics - First Recon

## Goal

Learn basic Nmap usage and report the services exposed on localhost.

Final answer format:

```text
22/tcp ssh, 80/tcp http
```

## Run Locally

```bash
docker build -t lab-nmap-basics:v1 .
docker run --rm -it --name nmap-basics lab-nmap-basics:v1
docker exec -it nmap-basics bash -lc 'exec su - student'
```

## Step 1. Verify Nmap

Run:

```bash
nmap --version
```

Submit:

```text
nmap --version
```

## Step 2. Read Help

Run:

```bash
nmap -h
```

Submit:

```text
nmap -h
```

## Step 3. Basic Local Scan

Run:

```bash
nmap 127.0.0.1
```

Submit:

```text
nmap 127.0.0.1
```

## Step 4. Scan Specific Ports

Run:

```bash
nmap -p 22,80 127.0.0.1
```

Submit:

```text
nmap -p 22,80 127.0.0.1
```

## Step 5. Detect Service Versions

Run:

```bash
nmap -sV 127.0.0.1
```

Submit:

```text
nmap -sV 127.0.0.1
```

## Step 6. Aggressive Detection

Run:

```bash
nmap -A 127.0.0.1
```

Submit:

```text
nmap -A 127.0.0.1
```

## Step 7. Report Services

Read the scan output and report:

```text
22/tcp ssh, 80/tcp http
```

## Full Solve

```bash
nmap --version
nmap -h
nmap 127.0.0.1
nmap -p 22,80 127.0.0.1
nmap -sV 127.0.0.1
nmap -A 127.0.0.1
```
