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

RUN useradd -m -s /bin/bash student && \
    echo "student:student" | chpasswd

RUN groupadd webops && \
    usermod -aG webops student

RUN echo "FLAG{cron_wildcard_checkpoint_escape}" > /root/flag.txt && \
    chmod 600 /root/flag.txt

RUN mkdir -p /srv/portal/uploads /opt/backups /opt/ops /var/log/ops && \
    chown root:webops /srv/portal/uploads && \
    chmod 2775 /srv/portal/uploads && \
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

RUN printf '%s\n' \
    'SHELL=/bin/bash' \
    'PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin' \
    '*/5 * * * * root /opt/ops/cleanup.sh >/dev/null 2>&1' \
    '* * * * * root /opt/ops/archive-uploads.sh >> /var/log/ops/archive.log 2>&1' \
    >> /etc/crontab

# The challenge needs root at runtime to start cron and run the root-owned jobs.
USER student
# trivy:ignore:DS-0002
USER root

CMD ["bash", "-lc", "mkdir -p /var/log/ops && touch /var/log/ops/archive.log /var/log/ops/cleanup.log && cron && tail -f /var/log/ops/archive.log"]
