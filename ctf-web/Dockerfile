FROM node:20-alpine

WORKDIR /app

COPY contents/package.json /app/package.json
RUN npm install --omit=dev

COPY contents /app

RUN mkdir -p /opt/flag \
  && cp /app/flag.txt /opt/flag/flag.txt \
  && chmod 444 /opt/flag/flag.txt

EXPOSE 3000

CMD ["npm", "start"]
