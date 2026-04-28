FROM python:3.12-alpine

WORKDIR /app

COPY contents/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY contents/ ./

RUN mkdir -p /opt/flag && \
    cp flag.txt /opt/flag/flag.txt && \
    chmod 444 /opt/flag/flag.txt

EXPOSE 3000
ENV PORT=3000

CMD ["python", "server.py"]
