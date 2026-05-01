# Altair Lab Templates

Docker-based lab environments for Altair cybersecurity training.

This repository contains deliberately vulnerable lab templates. Each directory is a self-contained challenge with a `Dockerfile`, a `metadata.json` file consumed by the Altair lab services, and usually a local `README.md` with challenge-specific notes.

These images are meant to run in isolated, ephemeral environments through the Lab API Service and the proxy/webshell stack. They can also be built locally for development, but should not be exposed on an untrusted network.

## Current Templates

| Directory | Lab | Type | Difficulty | Category | Duration | Steps |
| --- | --- | --- | --- | --- | --- | --- |
| `ctf-terminal/` | PATH Hijacking Challenge | `ctf_terminal_guided` | easy | `privilege_escalation` | 30-45min | 3 |
| `ctf-terminal-sudo-find-easy/` | Sudo Find PrivEsc | `ctf_terminal_guided` | easy | `privilege_escalation` | 20-30min | 3 |
| `ctf-terminal-capabilities-reader/` | Linux Capabilities Abuse | `ctf_terminal_guided` | medium | `linux_security` | 25-35min | 3 |
| `ctf-terminal-suid-maint-runner/` | SUID Runner Misconfiguration | `ctf_terminal_guided` | medium | `linux_security` | 30-45min | 3 |
| `ctf-terminal-cron-wildcard-hard/` | Cron Wildcard PrivEsc | `ctf_terminal_guided` | advanced | `privilege_escalation` | 45-60min | 3 |
| `ctf-terminal-cron-symlink-race-insane/` | Cron Chain + Symlink Race | `ctf_terminal_guided` | advanced | `privilege_escalation` | 60-90min | 4 |
| `ctf-web/` | Orbital Console Injection | `ctf_web_guided` | medium | `web_security` | 30-45min | 3 |
| `ctf-web-sqli-login-easy/` | SQLi Login Bypass | `ctf_web_guided` | easy | `web_security` | 20-30min | 3 |
| `ctf-web-sqli-union-intermediate/` | SQLi UNION Exfiltration | `ctf_web_guided` | medium | `web_security` | 30-45min | 3 |
| `ctf-web-sqli-filter-bypass-advanced/` | SQLi Filter Bypass | `ctf_web_guided` | advanced | `web_security` | 40-60min | 3 |
| `nmap-course/` | Nmap Basics - First Recon | `ctf_terminal_guided` | easy | `network_recon` | 15-25min | 7 |

## Repository Layout

```text
altair-lab-templates/
├── README.md
├── .gitignore
├── ctf-terminal*/
├── ctf-web*/
└── nmap-course/
```

Every template directory follows the same baseline shape:

```text
template-name/
├── Dockerfile
├── metadata.json
└── README.md
```

Some templates include extra helper files such as vulnerable scripts, cron helpers, C sources, or a `SOLVE.md` walkthrough for internal validation.

## Metadata Contract

`metadata.json` is the source of truth for the platform import/build flow.

Common fields:

```json
{
  "name": "Lab name",
  "lab_type": "ctf_terminal_guided",
  "difficulty": "easy",
  "category": "privilege_escalation",
  "estimated_duration": "20-30min",
  "objectives": "What the learner should achieve",
  "template_path": "lab-image-name:v1",
  "steps": [
    {
      "step_number": 1,
      "title": "Step title",
      "description": "Learner instructions",
      "question": "Validation question",
      "expected_answer": "Expected answer or flag",
      "validation_type": "exact_match",
      "points": 10,
      "hints": []
    }
  ]
}
```

Platform mapping:

- `metadata.json` describes the lab record.
- `steps[]` describes learner progression and validation.
- `hints[]` describes optional learner assistance and scoring cost.
- `template_path` identifies the container image used by the lab runtime.

## Template Families

**Terminal privilege escalation**

These labs teach local Linux enumeration and exploitation patterns:

- unsafe `PATH` usage in privileged jobs
- dangerous sudo allowances
- writable privileged scripts
- Linux file capabilities
- cron wildcard injection
- symlink race conditions

**Web exploitation**

These labs expose intentionally vulnerable web applications:

- eval/command injection in a diagnostics console
- login bypass via SQL injection
- UNION-based data extraction
- naive blacklist/filter bypass

**Network reconnaissance**

`nmap-course/` provides a guided first recon lab around core Nmap usage, scan modes, open-port discovery, and service recognition.

## Local Development

Build a template image:

```bash
cd ctf-terminal-sudo-find-easy
docker build -t lab-terminal-sudo-find-easy:v1 .
```

Run a terminal template locally:

```bash
docker run --rm -it lab-terminal-sudo-find-easy:v1
```

Run a web template locally, mapping the exposed port from the template Dockerfile:

```bash
docker run --rm -p 8080:8080 lab-sqli-login-easy:v1
```

The exact port and command can vary by template, so check the template `Dockerfile` and local `README.md` before testing.

## Security Notes

These templates intentionally contain vulnerabilities, weak permissions, exploitable scripts, flags, and insecure application logic. That is the product surface of this repository, not a production hardening target.

Operational guardrails:

- Run labs only in isolated containers or Kubernetes namespaces.
- Treat each container as disposable and learner-controlled.
- Do not mount host-sensitive paths into a lab container.
- Do not reuse these Dockerfiles as production service templates.
- Do not publish flags, generated solutions, credentials, or cloud project IDs in README files.

Security fixes applied to the platform services, such as non-root production containers and Trivy-clean service images, do not automatically apply to these deliberately vulnerable lab images. The lab templates are excluded from that hardening pass by design.

## Adding a Template

1. Create a new directory with a clear, stable name.
2. Add a `Dockerfile` that builds the isolated lab environment.
3. Add `metadata.json` with the same top-level fields and step structure used by existing labs.
4. Add a local `README.md` describing the scenario, intended learning path, exposed ports, users, and validation flow.
5. Build and smoke-test the image locally.
6. Keep secrets out of the repository; flags are challenge artifacts, not service credentials.

Before merging a new template, verify that `metadata.json` parses cleanly and that the `template_path` matches the image tag expected by the lab runtime.
