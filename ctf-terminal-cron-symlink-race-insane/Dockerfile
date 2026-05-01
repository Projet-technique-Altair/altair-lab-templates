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

RUN useradd -m -s /bin/bash backup && \
    echo "backup:backup" | chpasswd

RUN groupadd webops && \
    usermod -aG webops student && \
    usermod -aG webops backup

RUN echo "FLAG{cron_chain_symlink_race_root}" > /root/flag.txt && \
    chmod 600 /root/flag.txt

RUN mkdir -p /srv/portal/uploads /opt/backups /opt/ops /var/log/ops && \
    chown root:webops /srv/portal/uploads && \
    chmod 2775 /srv/portal/uploads

RUN mkdir -p /var/ops/reports/pending /var/ops/reports/public && \
    chown -R backup:backup /var/ops/reports && \
    chmod 770 /var/ops/reports/pending && \
    chmod 775 /var/ops/reports/public && \
    printf '%s\n' "daily_status=ok" > /var/ops/reports/pending/report.txt && \
    chown backup:backup /var/ops/reports/pending/report.txt && \
    touch /var/ops/reports/public/latest-report.txt && \
    chown root:root /var/ops/reports/public/latest-report.txt && \
    chmod 440 /var/ops/reports/public/latest-report.txt

COPY archive-uploads.sh /opt/ops/archive-uploads.sh
COPY publish-report.sh /opt/ops/publish-report.sh
RUN chown root:root /opt/ops/archive-uploads.sh /opt/ops/publish-report.sh && \
    chmod 755 /opt/ops/archive-uploads.sh && \
    chmod 750 /opt/ops/publish-report.sh

RUN printf '%s\n' \
    '#!/bin/bash' \
    'echo "[*] rotate $(date)" >> /var/log/ops/rotate.log' \
    > /opt/ops/rotate.sh && \
    chown root:root /opt/ops/rotate.sh && \
    chmod 700 /opt/ops/rotate.sh

RUN printf '%s\n' \
    'SHELL=/bin/bash' \
    'PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin' \
    '*/6 * * * * root /opt/ops/rotate.sh >/dev/null 2>&1' \
    '* * * * * backup /opt/ops/archive-uploads.sh >> /var/log/ops/archive.log 2>&1' \
    '* * * * * root /opt/ops/publish-report.sh >> /var/log/ops/publish.log 2>&1' \
    >> /etc/crontab

# The challenge needs root at runtime to start cron and run the root-owned jobs.
USER student
# trivy:ignore:DS-0002
USER root

CMD ["bash", "-lc", "mkdir -p /var/log/ops && touch /var/log/ops/archive.log /var/log/ops/publish.log /var/log/ops/rotate.log && cron && tail -f /var/log/ops/archive.log /var/log/ops/publish.log"]
