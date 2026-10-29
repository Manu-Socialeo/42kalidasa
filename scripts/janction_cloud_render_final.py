import json
import urllib.request
import urllib.error
import time
import os

def run_cloud_final():
    with open('scripts/janction_key.json', 'r', encoding='utf-8') as f:
        key_info = json.load(f)
    key = key_info['api_key']

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "render_final",
            "arguments": {
                "scene_id": "f_2215911eab8f41ac",
                "frame_start": 1,
                "frame_end": 180,
                "width": 1280,
                "height": 720,
                "samples": 16,
                "output": "mp4",
                "camera": "Kalidasa42_Cinematic_Camera",
                "blender": "5.2",
                "max_yen": 0
            }
        }
    }

    print("Launching final cloud GPU render on JANCTION...")
    req = urllib.request.Request(
        'https://render.janction.jp/mcp',
        headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json', 'Accept': 'application/json'},
        data=json.dumps(payload).encode('utf-8')
    )

    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        txt = res.get('result', {}).get('content', [{}])[0].get('text', '')
        job_info = json.loads(txt)
        print("Job launched:")
        print("  Job ID:", job_info.get("job_id"))
        print("  Status:", job_info.get("status"))
        job_id = job_info.get("job_id")

    # Poll until done
    for attempt in range(60):
        time.sleep(5)
        stat_req = urllib.request.Request(
            'https://render.janction.jp/mcp',
            headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json', 'Accept': 'application/json'},
            data=json.dumps({
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": "render_status",
                    "arguments": {"job_id": job_id}
                }
            }).encode('utf-8')
        )
        with urllib.request.urlopen(stat_req) as resp:
            s_res = json.loads(resp.read().decode('utf-8'))
            s_txt = s_res.get('result', {}).get('content', [{}])[0].get('text', '')
            status_data = json.loads(s_txt)
            status = status_data.get("status")
            progress = status_data.get("progress")
            print(f"[{attempt*5}s] Status: {status}, Progress: {progress}")
            
            if status == "done":
                print("Job finished! Artifacts:", status_data.get("artifacts"))
                links = status_data.get("links", {})
                print("Download links:", links)
                
                # Download MP4
                for fname, link in links.items():
                    if fname.endswith(".mp4"):
                        target_path = "website/camera_path_preview.mp4"
                        print(f"Downloading {fname} to {target_path}...")
                        urllib.request.urlretrieve(link, target_path)
                        print(f"Saved {target_path} ({os.path.getsize(target_path)} bytes)")
                return status_data
            elif status in ["failed", "canceled"]:
                print("Job did not finish:", status)
                return status_data

if __name__ == '__main__':
    run_cloud_final()

