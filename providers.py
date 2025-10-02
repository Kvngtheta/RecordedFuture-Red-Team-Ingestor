# backend/providers.py
# Minimal Recorded Future adapter and generic provider interface.
import requests
from typing import List, Dict


class ProviderInterface:
def __init__(self, api_key: str):
self.api_key = api_key


def search(self, query: str) -> List[Dict]:
raise NotImplementedError


class RecordedFutureProvider(ProviderInterface):
# NOTE: this is a minimal example. Replace endpoint and params with RF's real API.
BASE_URL = 'https://api.recordedfuture.com/v2' # placeholder - verify before use


def search(self, query: str) -> List[Dict]:
# Example: recorded future has multiple endpoints; this is pseudocode.
headers = {'X-RFToken': self.api_key, 'Accept': 'application/json'}
params = {'query': query}
resp = requests.get(f'{self.BASE_URL}/enrichment/query', headers=headers, params=params, timeout=30)
resp.raise_for_status()
data = resp.json()
# Map to list of items (raw text or structured)
items = []
# The real Recorded Future response will differ; adapt mapping accordingly.
for hit in data.get('data', []):
items.append({
'id': hit.get('id'),
'title': hit.get('title') or hit.get('name') or query,
'body': hit.get('attributes', {}).get('description', str(hit))
})
return items