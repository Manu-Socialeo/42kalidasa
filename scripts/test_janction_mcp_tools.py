import urllib.request, urllib.error, json, ssl

with open(r"C:\Users\manpr\Documents\42 Kalidasa\scripts\janction_key.json", "r", encoding="utf-8") as f:
    key_data = json.load(f)
api_key = key_data["api_key"]

url = "https://render.janction.jp/mcp"
ctx = ssl.create_default_context()

# 1. Initialize
init_payload = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {"name": "Antigravity", "version": "1.0.0"}
    }
}

req = urllib.request.Request(
    url,
    data=json.dumps(init_payload).encode("utf-8"),
    headers={
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "Authorization": f"Bearer {api_key}"
    }
)

with urllib.request.urlopen(req, context=ctx) as resp:
    init_res = json.loads(resp.read().decode("utf-8"))
    print("Initialize result:", json.dumps(init_res, indent=2))

# 2. List tools
tools_payload = {
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/list",
    "params": {}
}

req_tools = urllib.request.Request(
    url,
    data=json.dumps(tools_payload).encode("utf-8"),
    headers={
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "Authorization": f"Bearer {api_key}"
    }
)

with urllib.request.urlopen(req_tools, context=ctx) as resp:
    tools_res = json.loads(resp.read().decode("utf-8"))
    print("\n=== AVAILABLE MCP TOOLS ===")
    tools = tools_res.get("result", {}).get("tools", [])
    print(f"Total tools: {len(tools)}")
    for t in tools:
        print(f" - {t['name']}: {t.get('description', '')[:80]}...")
