# backend/app.py
import os
import json
from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uvicorn
from db import SessionLocal, init_db, ProviderCred, IngestedItem, LogEntry
from crypto import Crypto
from providers import RecordedFutureProvider
import typer
from typing import Optional
import requests


app = FastAPI()
cli = typer.Typer()
crypto = Crypto()


# simple admin token (for prototype only) - in prod use proper auth
ADMIN_TOKEN = os.getenv('ADMIN_TOKEN', 'change-me')
OPENAI_API_KEY_ENV = os.getenv('OPENAI_API_KEY_VAR', 'OPENAI_API_KEY')


class CredIn(BaseModel):
provider: str
name: Optional[str]
api_key: str
meta: Optional[str] = None


class IngestRequest(BaseModel):
provider: str
query: str
forward_to_openai: bool = False


@app.on_event('startup')
def startup():
init_db()


@app.get('/', response_class=HTMLResponse)
def index():
html = open('frontend/index.html').read()
return HTMLResponse(content=html)


@app.post('/api/creds')
async def save_creds(cred: CredIn, token: Optional[str] = None):
if token != ADMIN_TOKEN:
raise HTTPException(401, 'Unauthorized')
db = SessionLocal()
encrypted = crypto.encrypt(cred.api_key)
pc = ProviderCred(provider=cred.provider, name=cred.name, encrypted_api_key=encrypted, meta=cred.meta)
db.add(pc)
db.commit()
db.refresh(pc)
return {'id': pc.id, 'provider': pc.provider}


@app.get('/api/creds')
def list_creds(token: Optional[str] = None):
if token != ADMIN_TOKEN:
raise HTTPException(401, 'Unauthorized')
db = SessionLocal()
rows = db.query(ProviderCred).all()
result = []
for r in rows:
result.append({'id': r.id, 'provider': r.provider, 'name': r.name})
return result


@app.post('/api/ingest')
def ingest(req: IngestRequest, token: Optional[str] = None):
if token != ADMIN_TOKEN:
raise HTTPException(401, 'Unauthorized')
db = SessionLocal()
# fetch credentials
cred = db.query(ProviderCred).filter(ProviderCred.provider == req.provider).first()
if not cred:
raise HTTPException(404, 'No credentials for provider')
api_key = crypto.decrypt(cred.encrypted_api_key)


# select provider adapter
if req.provider.lower() == 'recordedfuture' or 'recorded' in req.provider.lower():
cli()