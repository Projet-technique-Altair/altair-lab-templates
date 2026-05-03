FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    ca-certificates \
    coreutils \
    cron \
    findutils \
    sudo \
    tar \
    && rm -rf /var/lib/apt/lists/*

RUN id -u student >/dev/null 2>&1 || useradd -m -s /bin/bash student && \
    echo "student:student" | chpasswd

RUN groupadd webops && \
    usermod -aG webops student

RUN echo "FLAG{cron_wildcard_checkpoint_escape}" > /flag.txt && \
    chown root:root /flag.txt && \
    chmod 600 /flag.txt

RUN mkdir -p /srv/portal/uploads /opt/backups /opt/ops /var/log/ops && \
    chown root:webops /srv/portal/uploads && \
    chmod 2775 /srv/portal/uploads && \
    chown root:root /opt/backups && \
    chmod 755 /opt/backups && \
    printf '%s\n' "Drop files here for nightly archive." > /srv/portal/uploads/readme.txt

COPY archive-uploads.sh /opt/ops/archive-uploads.sh

RUN chown root:root /opt/ops/archive-uploads.sh && \
    chmod 750 /opt/ops/archive-uploads.sh

RUN printf '%s\n' \
    '#!/bin/bash' \
    'echo "[*] cleanup $(date)" >> /var/log/ops/cleanup.log' \
    > /opt/ops/cleanup.sh && \
    chown root:root /opt/ops/cleanup.sh && \
    chmod 700 /opt/ops/cleanup.sh

RUN touch /var/log/ops/archive.log /var/log/ops/cleanup.log && \
    chown root:root /var/log/ops/archive.log /var/log/ops/cleanup.log && \
    chmod 644 /var/log/ops/archive.log /var/log/ops/cleanup.log

RUN printf '%s\n' \
    'SHELL=/bin/bash' \
    'PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin' \
    '*/5 * * * * root /opt/ops/cleanup.sh >/dev/null 2>&1' \
    '* * * * * root /opt/ops/archive-uploads.sh >> /var/log/ops/archive.log 2>&1' \
    >> /etc/crontab

USER root

CMD ["bash", "-lc", "cron && exec su - student"]