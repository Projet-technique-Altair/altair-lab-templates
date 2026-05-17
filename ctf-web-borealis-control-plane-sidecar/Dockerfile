FROM python:3.12-alpine

WORKDIR /app

COPY contents/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY contents/ ./

RUN addgroup -S app && \
    adduser -S -G app app && \
    chown -R app:app /app

EXPOSE 3000
ENV PORT=3000

USER app

CMD ["python", "server.py"]
