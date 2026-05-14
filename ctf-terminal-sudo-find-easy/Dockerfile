FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    ca-certificates \
    findutils \
    sudo \
    && rm -rf /var/lib/apt/lists/*

RUN id -u student >/dev/null 2>&1 || useradd -m -s /bin/bash student && \
    echo "student:student" | chpasswd

RUN echo "FLAG{sudo_find_priv_esc}" > /root/flag.txt && \
    chown root:root /root/flag.txt && \
    chmod 600 /root/flag.txt

RUN printf '%s\n' 'student ALL=(root) NOPASSWD: /usr/bin/find' > /etc/sudoers.d/student-find && \
    chown root:root /etc/sudoers.d/student-find && \
    chmod 440 /etc/sudoers.d/student-find

USER student

CMD ["/bin/bash"]
