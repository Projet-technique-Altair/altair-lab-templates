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

# Utilisateur joueur
RUN useradd -m -s /bin/bash student && \
    echo "student:student" | chpasswd

# Ne pas utiliser "backup" : il existe déjà dans Debian.
RUN useradd -m -s /bin/bash backupuser && \
    echo "backupuser:backupuser" | chpasswd

# Groupe commun pour certaines zones du lab
RUN groupadd webops && \
    usermod -aG webops student && \
    usermod -aG webops backupuser

# Flag root
RUN echo "FLAG{cron_chain_symlink_race_root}" > /root/flag.txt && \
    chmod 600 /root/flag.txt

# Dossiers du portail et des backups
RUN mkdir -p /srv/portal/uploads /opt/backups /opt/ops /var/log/ops && \
    chown root:webops /srv/portal/uploads && \
    chmod 2775 /srv/portal/uploads && \
    chown root:webops /opt/backups && \
    chmod 775 /opt/backups

# Dossiers du système de rapports
RUN mkdir -p /var/ops/reports/pending /var/ops/reports/public && \
    chown -R backupuser:backupuser /var/ops/reports && \
    chmod 770 /var/ops/reports/pending && \
    chmod 775 /var/ops/reports/public && \
    printf '%s\n' "daily_status=ok" > /var/ops/reports/pending/report.txt && \
    chown backupuser:backupuser /var/ops/reports/pending/report.txt && \
    touch /var/ops/reports/public/latest-report.txt && \
    chown root:root /var/ops/reports/public/latest-report.txt && \
    chmod 440 /var/ops/reports/public/latest-report.txt

# Scripts du lab
COPY archive-uploads.sh /opt/ops/archive-uploads.sh
COPY publish-report.sh /opt/ops/publish-report.sh

RUN chown root:root /opt/ops/archive-uploads.sh /opt/ops/publish-report.sh && \
    chmod 755 /opt/ops/archive-uploads.sh && \
    chmod 750 /opt/ops/publish-report.sh

# Script annexe de rotation
RUN printf '%s\n' \
    '#!/bin/bash' \
    'echo "[*] rotate $(date)" >> /var/log/ops/rotate.log' \
    > /opt/ops/rotate.sh && \
    chown root:root /opt/ops/rotate.sh && \
    chmod 700 /opt/ops/rotate.sh

# Fichiers de logs avec permissions adaptées
RUN touch /var/log/ops/archive.log /var/log/ops/publish.log /var/log/ops/rotate.log && \
    chown backupuser:webops /var/log/ops/archive.log && \
    chmod 664 /var/log/ops/archive.log && \
    chown root:root /var/log/ops/publish.log /var/log/ops/rotate.log && \
    chmod 644 /var/log/ops/publish.log /var/log/ops/rotate.log

# Cron jobs
RUN printf '%s\n' \
    'SHELL=/bin/bash' \
    'PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin' \
    '*/6 * * * * root /opt/ops/rotate.sh >/dev/null 2>&1' \
    '* * * * * backupuser /opt/ops/archive-uploads.sh >> /var/log/ops/archive.log 2>&1' \
    '* * * * * root /opt/ops/publish-report.sh >> /var/log/ops/publish.log 2>&1' \
    >> /etc/crontab

# Le conteneur doit démarrer en root pour lancer cron.
# Ensuite, on donne une session student au joueur.
USER root

CMD ["bash", "-lc", "cron && exec su - student"]