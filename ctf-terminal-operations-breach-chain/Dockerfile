FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    ca-certificates \
    coreutils \
    cron \
    curl \
    python3 \
    sudo \
    tar \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash student && \
    useradd -m -g operator -s /bin/bash operator && \
    echo "student:student" | chpasswd && \
    echo "operator:night-shift" | chpasswd

RUN getent passwd backup >/dev/null

RUN groupadd portal && \
    usermod -aG portal student && \
    usermod -aG portal backup

RUN mkdir -p /srv/portal/uploads /opt/ops /opt/internal /var/log/ops /var/lib/ops && \
    chown root:portal /srv/portal/uploads && \
    chmod 2775 /srv/portal/uploads && \
    chown backup:backup /var/lib/ops && \
    chmod 750 /var/lib/ops

RUN printf '%s\n' \
    'ops_service_token=ORBIT-31415' \
    > /var/lib/ops/service.env && \
    chown backup:backup /var/lib/ops/service.env && \
    chmod 640 /var/lib/ops/service.env

RUN printf '%s\n' \
    '#!/bin/bash' \
    'set -e' \
    'cd /srv/portal/uploads' \
    'tar -czf /tmp/uploads.tar.gz *' \
    > /opt/ops/archive-uploads.sh && \
    chown root:root /opt/ops/archive-uploads.sh && \
    chmod 755 /opt/ops/archive-uploads.sh

RUN printf '%s\n' \
    '#!/usr/bin/env python3' \
    'from http.server import BaseHTTPRequestHandler, HTTPServer' \
    'TOKEN = "ORBIT-31415"' \
    'class Handler(BaseHTTPRequestHandler):' \
    '    def do_GET(self):' \
    '        if self.path != "/runbook":' \
    '            self.send_response(404); self.end_headers(); return' \
    '        if self.headers.get("X-Ops-Token") != TOKEN:' \
    '            self.send_response(403); self.end_headers(); self.wfile.write(b"forbidden"); return' \
    '        self.send_response(200); self.end_headers()' \
    '        self.wfile.write(b"operator_password=night-shift\noperator can run /usr/local/bin/maint-check with sudo\n")' \
    '    def log_message(self, *_):' \
    '        return' \
    'HTTPServer(("127.0.0.1", 8081), Handler).serve_forever()' \
    > /opt/internal/runbook.py && \
    chmod 755 /opt/internal/runbook.py

RUN printf '%s\n' \
    '#!/bin/bash' \
    'echo "[maint-check] collecting archive report"' \
    'tar --version >/dev/null' \
    > /usr/local/bin/maint-check && \
    chown root:root /usr/local/bin/maint-check && \
    chmod 755 /usr/local/bin/maint-check && \
    printf '%s\n' 'operator ALL=(root) NOPASSWD: SETENV: /usr/local/bin/maint-check' > /etc/sudoers.d/operator-maint && \
    chmod 440 /etc/sudoers.d/operator-maint

RUN echo 'FLAG{operations_breach_chain_root}' > /root/flag.txt && \
    chmod 600 /root/flag.txt

RUN printf '%s\n' \
    'SHELL=/bin/bash' \
    'PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin' \
    '* * * * * backup /opt/ops/archive-uploads.sh >> /var/log/ops/archive.log 2>&1' \
    >> /etc/crontab && \
    touch /var/log/ops/archive.log && \
    chown backup:portal /var/log/ops/archive.log && \
    chmod 664 /var/log/ops/archive.log

RUN printf '%s\n' \
    '#!/bin/bash' \
    'set -euo pipefail' \
    '/usr/bin/sudo -n /usr/sbin/cron || true' \
    '/usr/bin/python3 /opt/internal/runbook.py >/tmp/runbook.log 2>&1 &' \
    > /opt/ops/startup.sh && \
    chown root:root /opt/ops/startup.sh && \
    chmod 755 /opt/ops/startup.sh && \
    printf '%s\n' 'student ALL=(root) NOPASSWD: /usr/sbin/cron ""' > /etc/sudoers.d/start-cron && \
    chmod 440 /etc/sudoers.d/start-cron

USER student

CMD ["bash", "-lc", "/opt/ops/startup.sh; exec bash"]
