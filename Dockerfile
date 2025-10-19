FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY server.js ./server.js

# Notes volume (mount your repo here)
VOLUME ["/app/notes"]

ENV REPO_PATH=/app/notes
ENV MARKDOWN_PATH=/app/notes/TODO.md
ENV PORT=8080

EXPOSE 8080
CMD ["node", "server.js"]