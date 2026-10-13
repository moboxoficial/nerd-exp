FROM node:22-slim

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --omit=dev
COPY src ./src

# Agendamentos e tokens renovados ficam aqui: monte um volume persistente.
ENV DATA_DIR=/data
VOLUME /data

ENV PORT=3000
EXPOSE 3000
CMD ["node", "src/server.js"]
