FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    make \
    bash \
    sudo \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd maint && \
    useradd -m -s /bin/bash -G maint student && \
    echo "student:student" | chpasswd

RUN echo "FLAG{suid_runner_misconfig}" > /root/flag.txt && \
    chmod 600 /root/flag.txt

RUN mkdir -p /opt/maint

COPY runner.c /tmp/runner.c
RUN gcc /tmp/runner.c -o /usr/local/bin/maint-runner && \
    chown root:root /usr/local/bin/maint-runner && \
    chmod 4755 /usr/local/bin/maint-runner

COPY run-check.sh /opt/maint/run-check.sh
RUN chown root:maint /opt/maint/run-check.sh && \
    chmod 775 /opt/maint/run-check.sh

USER student

CMD ["bash", "-lc", "tail -f /dev/null"]
