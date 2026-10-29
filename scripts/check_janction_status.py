import urllib.request, urllib.error, json, ssl, os

KEY_FILE = r"C:\Users\manpr\Documents\42 Kalidasa\scripts\janction_key.json"

# First, issue or load key
if not os.path.exists(KEY_FILE):
    url = 'https://render.janction.jp/v1/keys'
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, data=b'{}', headers={'Content-Type': 'application/json', 'User-Agent': 'Antigravity/1.0'})
    with urllib.request.urlopen(req, context=ctx) as resp:
        key_data = json.loads(resp.read().decode('utf-8'))
        with open(KEY_FILE, 'w', encoding='utf-8') as f:
            json.dump(key_data, f, indent=2)
else:
    with open(KEY_FILE, 'r', encoding='utf-8') as f:
        key_data = json.load(f)

api_key = key_data.get('api_key')
print("Using key with prefix:", key_data.get('prefix'))

# Check /v1/me
ctx = ssl.create_default_context()
req = urllib.request.Request(
    'https://render.janction.jp/v1/me',
    headers={
        'X-API-Key': api_key,
        'User-Agent': 'Antigravity/1.0'
    }
)

with urllib.request.urlopen(req, context=ctx) as resp:
    me_data = json.loads(resp.read().decode('utf-8'))
    print("\n=== JANCTION /v1/me STATUS ===")
    print(json.dumps(me_data, indent=2))

# Check /v1/health
req_health = urllib.request.Request('https://render.janction.jp/v1/health', headers={'User-Agent': 'Antigravity/1.0'})
with urllib.request.urlopen(req_health, context=ctx) as resp:
    health_data = json.loads(resp.read().decode('utf-8'))
    print("\n=== JANCTION /v1/health STATUS ===")
    print(json.dumps(health_data, indent=2))


