FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

RUN apt-get update && apt-get install -y --no-install-recommends \
    libcap2-bin \
    sudo \
    bash \
    ca-certificates \
    && ln -s /usr/sbin/getcap /usr/local/bin/getcap \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash student && \
    echo "student:student" | chpasswd

RUN echo "FLAG{linux_capability_data_access}" > /root/flag.txt && \
    chmod 600 /root/flag.txt

RUN cp /bin/cat /usr/local/bin/syscat && \
    chown root:root /usr/local/bin/syscat && \
    chmod 755 /usr/local/bin/syscat && \
    setcap cap_dac_override+ep /usr/local/bin/syscat

USER student

CMD ["bash", "-lc", "tail -f /dev/null"]
