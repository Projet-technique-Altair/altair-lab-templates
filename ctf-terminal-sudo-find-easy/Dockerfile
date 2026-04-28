FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    sudo \
    findutils \
    bash \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash student && \
    echo "student:student" | chpasswd

RUN echo "FLAG{sudo_find_priv_esc}" > /root/flag.txt && \
    chmod 600 /root/flag.txt

RUN printf '%s\n' \
    'student ALL=(root) NOPASSWD: /usr/bin/find' \
    > /etc/sudoers.d/student-find && \
    chmod 440 /etc/sudoers.d/student-find

CMD ["bash", "-lc", "tail -f /dev/null"]
