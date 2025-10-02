# backend/crypto.py
from cryptography.fernet import Fernet
import os


def load_master_key():
key = os.getenv('MASTER_KEY')
if not key:
raise RuntimeError('MASTER_KEY environment variable not set. Use a secure KMS in production.')
# Allow using either 32-byte base64 or raw bytes; Fernet expects urlsafe_base64
return key.encode() if isinstance(key, str) else key


class Crypto:
def __init__(self, master_key=None):
if master_key is None:
master_key = load_master_key()
self.f = Fernet(master_key)


def encrypt(self, plaintext: str) -> bytes:
return self.f.encrypt(plaintext.encode())


def decrypt(self, token: bytes) -> str:
return self.f.decrypt(token).decode()