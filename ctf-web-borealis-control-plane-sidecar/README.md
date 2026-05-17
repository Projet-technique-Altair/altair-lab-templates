# Borealis Control Plane - Sidecar

Advanced web example for the mono-Pod sidecar runtime.

## Topology

- `lab-container`: public Flask app on `3000`
- `admin-api`: local-only sidecar on `127.0.0.1:3001`

Only `3000` is public. The sidecar is reachable because all containers in a Pod share the same network namespace.

## Local build

```bash
docker build -t lab-web-borealis-control-plane-sidecar:v1 .
docker build -t lab-web-borealis-admin-api:v1 sidecars/admin-api
```

## Why this exists

This is the level-2 form of `Borealis Control Plane`: one public reverse surface, one internal admin API, same Pod, and a real reason to use SSRF against localhost.
