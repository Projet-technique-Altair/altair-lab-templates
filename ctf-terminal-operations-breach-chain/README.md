# Operations Breach Chain

## Goal

Chain several weaknesses in one mono-Pod terminal lab:

1. cron wildcard injection from `student` to `backup`;
2. discovery of a backup-only secret;
3. access to a local-only service on `127.0.0.1:8081`;
4. abuse of an `operator` maintenance sudo rule;
5. PATH hijacking to root.

## Intended Path

```bash
cat /etc/crontab
cat /opt/ops/archive-uploads.sh
```

Use tar checkpoint files in `/srv/portal/uploads` to create a SUID shell owned by `backup`, then read:

```bash
cat /var/lib/ops/service.env
curl -H 'X-Ops-Token: ORBIT-31415' http://127.0.0.1:8081/runbook
su operator
```

The runbook returns the `operator` password. After reaching that account, inspect sudo and hijack `tar` through `PATH` when running:

```bash
sudo env PATH=/tmp:$PATH /usr/local/bin/maint-check
```

## Local Notes

The image starts cron plus the localhost runbook service from the initial `student` shell. No extra public service is exposed.
