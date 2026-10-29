import json
import urllib.request
import urllib.error
import time

def call_preview():
    with open('scripts/janction_key.json', 'r', encoding='utf-8') as f:
        key_info = json.load(f)
    key = key_info['api_key']

    scene_id = "f_2215911eab8f41ac"
    
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "render_preview",
            "arguments": {
                "scene_id": scene_id,
                "camera": "Cam_Photo_Match_Hero_v2",
                "width": 1280,
                "height": 720,
                "samples": 32,
                "blender": "5.2"
            }
        }
    }

    print("Submitting preview job to JANCTION Render...")
    req = urllib.request.Request(
        'https://render.janction.jp/mcp',
        headers={
            'Authorization': f'Bearer {key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        data=json.dumps(payload).encode('utf-8')
    )

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print("Response:")
            print(json.dumps(data, indent=2))
            return data
    except urllib.error.HTTPError as e:
        print("HTTP Error:", e.code, e.read().decode('utf-8'))
        return None

if __name__ == '__main__':
    call_preview()
