import urllib.request, json, ssl

with open(r"C:\Users\manpr\Documents\42 Kalidasa\scripts\janction_key.json", "r", encoding="utf-8") as f:
    key_data = json.load(f)
api_key = key_data["api_key"]

url = "https://render.janction.jp/mcp"
ctx = ssl.create_default_context()

def call_mcp_tool(tool_name, arguments={}):
    payload = {
        "jsonrpc": "2.0",
        "id": 100,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments
        }
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "Authorization": f"Bearer {api_key}"
        }
    )
    with urllib.request.urlopen(req, context=ctx) as resp:
        return json.loads(resp.read().decode("utf-8"))

print("=== CALLING render_info ===")
info_res = call_mcp_tool("render_info")
print(json.dumps(info_res, indent=2))

print("\n=== CALLING billing ===")
billing_res = call_mcp_tool("billing")
print(json.dumps(billing_res, indent=2))
