import urllib.request, json, ssl, os

with open(r"C:\Users\manpr\Documents\42 Kalidasa\scripts\janction_key.json", "r", encoding="utf-8") as f:
    key_data = json.load(f)
api_key = key_data["api_key"]

url = "https://render.janction.jp/mcp"
ctx = ssl.create_default_context()

print("=== EXECUTING PHASE 4 TEST RENDER (FREE PREVIEW) ===")

payload = {
    "jsonrpc": "2.0",
    "id": 101,
    "method": "tools/call",
    "params": {
        "name": "render_preview",
        "arguments": {
            "scene_url": "https://render.janction.jp/samples/cube_scene.py",
            "environment": "studio"
        }
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

with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
    res = json.loads(resp.read().decode("utf-8"))
    print("Preview Call Result:")
    print(json.dumps(res, indent=2))

# Extract image link from result
img_url = None
if "result" in res:
    # check structuredContent or content text
    content_list = res["result"].get("content", [])
    for item in content_list:
        if item.get("type") == "text":
            try:
                parsed = json.loads(item["text"])
                img_url = parsed.get("preview_url") or parsed.get("view_url") or parsed.get("image_url")
                if not img_url and "artifacts" in parsed and len(parsed["artifacts"]) > 0:
                    img_url = parsed["artifacts"][0].get("view_url") or parsed["artifacts"][0].get("url")
            except:
                pass
    if not img_url and "structuredContent" in res["result"]:
        sc = res["result"]["structuredContent"]
        img_url = sc.get("preview_url") or sc.get("view_url")

print("\nExtracted image URL:", img_url)

if img_url:
    # Download test image
    out_img = r"C:\Users\manpr\Documents\42 Kalidasa\renders\preview\cloud_gpu_test_render.png"
    img_req = urllib.request.Request(img_url, headers={"User-Agent": "Antigravity/1.0"})
    with urllib.request.urlopen(img_req, context=ctx) as img_resp:
        with open(out_img, "wb") as f:
            f.write(img_resp.read())
    print(f"Downloaded cloud GPU test render to {out_img} (Size: {os.path.getsize(out_img)} bytes)")
