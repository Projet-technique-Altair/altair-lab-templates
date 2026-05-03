FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    libcap2-bin \
    sudo \
    bash \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN id -u student >/dev/null 2>&1 || useradd -m -s /bin/bash student && \
    echo "student:student" | chpasswd

RUN echo "FLAG{linux_capability_data_access}" > /flag.txt && \
    chown root:root /flag.txt && \
    chmod 600 /flag.txt

RUN cp /bin/cat /usr/local/bin/syscat && \
    chown root:root /usr/local/bin/syscat && \
    chmod 755 /usr/local/bin/syscat && \
    setcap cap_dac_read_search+ep /usr/local/bin/syscat

USER student

CMD ["/bin/bash"]