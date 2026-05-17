# Operations Breach Chain - Sidecar

Advanced terminal example for the mono-Pod sidecar runtime.

## Topology

- `lab-container`: learner shell, cron, Unix users, vulnerable maintenance flow
- `runbook`: local-only HTTP sidecar on `127.0.0.1:8081`

The two containers share the Pod network namespace, so the learner can reach the sidecar through localhost without any extra Kubernetes Service.

## Local build

```bash
docker build -t lab-terminal-operations-breach-chain-sidecar:v1 .
docker build -t lab-terminal-operations-runbook:v1 sidecars/runbook
```

## Why this exists

This is the same family of challenge as `Operations Breach Chain`, but the internal runbook has been moved out of the main image to exercise `runtime.services` in a realistic way.
