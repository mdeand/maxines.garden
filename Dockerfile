FROM nixos/nix:latest AS builder

WORKDIR /app

COPY shell.nix .
COPY requirements.txt .
COPY Makefile .

COPY shared/ ./shared/
COPY tools/ ./tools/
COPY content/ ./content/
COPY styles/ ./styles/
COPY templates ./templates/
COPY tailwind.config.js .

# RUN echo "experimental-features = nix-command flakes" >> /etc/nix/nix.conf

RUN nix-shell --run "mkdir -p dist && make compile && make css"

FROM python:3.12-slim-bookworm

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY shared/ ./shared/
COPY server/ ./server/
COPY templates ./templates/

COPY --from=builder /app/dist/ ./dist/
COPY --from=builder /app/.db.sqlite3 ./.db.sqlite3

ENV DATABASE_URL=/app/.db.sqlite3
ENV DEPLOYMENT_MODE=Production
ENV PYTHONPATH=.

EXPOSE 5000

CMD ["python3.12", "-m", "server.main"]
