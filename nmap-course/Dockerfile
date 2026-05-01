FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    nmap \
    openssh-server \
    python3 \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# Create student user expected by the webshell/runtime flow.
RUN useradd -m -s /bin/bash student && \
    echo "student:student" | chpasswd && \
    usermod -aG sudo student && \
    echo 'student ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# Prepare SSH runtime.
RUN mkdir -p /var/run/sshd /opt/lab/www && \
    echo "Altair Nmap Basics Lab" > /opt/lab/www/index.html

# The course image starts sshd and a privileged port, so the launcher remains root.
USER student
# trivy:ignore:DS-0002
USER root

CMD ["bash", "-lc", "python3 -m http.server 80 --directory /opt/lab/www >/tmp/http.log 2>&1 & /usr/sbin/sshd && tail -f /dev/null"]
