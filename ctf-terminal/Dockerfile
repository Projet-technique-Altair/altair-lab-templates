FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    cron \
    sudo \
    vim \
    nano \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create user student
RUN useradd -m -s /bin/bash student && \
    echo "student:student" | chpasswd

# Flag setup
RUN echo "FLAG{path_hijacking_pwned_2026}" > /root/flag.txt && \
    chmod 600 /root/flag.txt

# Root-owned output directory (student can read files, cannot create/overwrite)
RUN mkdir -p /opt/output && \
    chown root:root /opt/output && \
    chmod 755 /opt/output

# Vulnerable backup script
COPY backup.sh /opt/backup.sh
RUN chmod +x /opt/backup.sh

# Ensure /tmp is writable and sticky (normal behavior)
RUN chmod 1777 /tmp

# Cron: vulnerable PATH includes /tmp first
RUN printf '%s\n' \
  'SHELL=/bin/bash' \
  'PATH=/tmp:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin' \
  '* * * * * root /opt/backup.sh > /var/log/backup.log 2>&1' \
  >> /etc/crontab

# Start cron safely and keep container alive
CMD ["bash", "-lc", "touch /var/log/backup.log && cron && tail -f /var/log/backup.log"]
