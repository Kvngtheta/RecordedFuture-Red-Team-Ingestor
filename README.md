# RecordedFuture-Red-Team-Ingestor


A lightweight application for ingesting threat intelligence (e.g., from Recorded Future) with both a CLI and optional web interface.  
All sensitive data (API keys) are stored encrypted in a lightweight database. Supports forwarding data to ChatGPT for inference.

---

## Features
- FastAPI backend with optional web interface
- CLI with [Typer](https://typer.tiangolo.com/)
- Secure credential storage using Fernet encryption (`MASTER_KEY` env variable)
- Ingest from Recorded Future (stub adapter, extendable to others)
- Store ingested intel + logs in SQLite (encrypted at rest)
- Forward ingested items to OpenAI API for enrichment/inference
- Dockerfile + docker-compose for containerized deployment

---

## Quickstart

### 1. Clone & Install
```bash
unzip lightweight-intel-ingest.zip
cd lightweight-intel-ingest
pip install -r requirements.txt  # (generate if needed, see packages below)
```

**Dependencies (install manually if not using requirements.txt):**
```bash
pip install fastapi uvicorn sqlalchemy cryptography requests typer
```

### 2. Environment Variables
Set environment variables before running:
```bash
export MASTER_KEY=$(python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")
export ADMIN_TOKEN=super-secret-admin
export OPENAI_API_KEY=sk-xxxxxxx
```

### 3. Run Server
```bash
python backend/app.py run-server --port 8000
```
Visit `http://localhost:8000` to access the web UI.

### 4. CLI Usage
```bash
python backend/app.py ingest-cli --provider recordedfuture --query "ransomware" --forward true
```

---

## Docker

### Build & Run
```bash
docker build -t intel-ingest .
docker run -it -p 8000:8000   -e MASTER_KEY=$MASTER_KEY   -e ADMIN_TOKEN=$ADMIN_TOKEN   -e OPENAI_API_KEY=$OPENAI_API_KEY   intel-ingest
```

### Docker Compose
```bash
docker-compose up --build
```

---

## Security Notes
- Do **not** hardcode secrets. Use env vars or a KMS (Vault, AWS KMS, Azure KeyVault).
- The prototype uses simple token auth via `ADMIN_TOKEN` query param — replace with OAuth2/JWT before production.
- Protect SQLite file with file-level encryption if needed; migrate to Postgres/MySQL for multi-user scenarios.
- Always run behind TLS (reverse proxy with Nginx/Traefik + certs).

---

## Next Steps
- Add more provider adapters (VirusTotal, AlienVault OTX, MISP, etc.)
- Harden authentication & authorization (OAuth2/JWT, RBAC)
- Add dashboards & filtering in the web UI
- CI/CD pipeline with SAST/DAST and image scanning (Trivy, Semgrep, etc.)
- Integrate with HashiCorp Vault or AWS KMS for key management

---

**Author:** De'Alonzius White
**Status:** Prototype (not production-ready)  
