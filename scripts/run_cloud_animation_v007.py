import json
import urllib.request
import urllib.error
import time
import os

WORKSPACE = r"C:\Users\manpr\Documents\42 Kalidasa"
SCENE_ID = "f_e9bb7c8e0bef4475"

def run_animation_job():
    with open('scripts/janction_key.json', 'r', encoding='utf-8') as f:
        key_info = json.load(f)
    key = key_info['api_key']

    payload = {
        "jsonrpc": "2.0",
        "id": 10,
        "method": "tools/call",
        "params": {
            "name": "render_final",
            "arguments": {
                "scene_id": SCENE_ID,
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

    print(f"Submitting final render job for scene {SCENE_ID} (180 frames, max_yen: 0)...")
    req = urllib.request.Request(
        'https://render.janction.jp/mcp',
        headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json', 'Accept': 'application/json'},
        data=json.dumps(payload).encode('utf-8')
    )

    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        txt = res.get('result', {}).get('content', [{}])[0].get('text', '')
        job_info = json.loads(txt)
        job_id = job_info.get("job_id")
        status = job_info.get("status")
        print(f"Job launched successfully:")
        print(f"  Job ID: {job_id}")
        print(f"  Initial Status: {status}")

    # Polling loop
    print("Awaiting cloud GPU render completion...")
    for attempt in range(80):
        time.sleep(5)
        stat_req = urllib.request.Request(
            'https://render.janction.jp/mcp',
            headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json', 'Accept': 'application/json'},
            data=json.dumps({
                "jsonrpc": "2.0",
                "id": 20 + attempt,
                "method": "tools/call",
                "params": {
                    "name": "render_status",
                    "arguments": {"job_id": job_id}
                }
            }).encode('utf-8')
        )

        with urllib.request.urlopen(stat_req) as s_resp:
            s_res = json.loads(s_resp.read().decode('utf-8'))
            s_txt = s_res.get('result', {}).get('content', [{}])[0].get('text', '')
            status_obj = json.loads(s_txt)
            stat = status_obj.get("status")
            progress = status_obj.get("progress", {})
            done_frames = progress.get("frames_rendered", 0) if isinstance(progress, dict) else 0
            total_frames = progress.get("frames_total", 180) if isinstance(progress, dict) else 180
            print(f"  [{attempt*5}s] Status: {stat} | Progress: {done_frames}/{total_frames} frames")

            if stat == "done":
                print("Job finished! Downloading artifacts...")
                download_url = status_obj.get("download_url") or status_obj.get("files", {}).get("mp4")
                print("Download URL:", download_url)

                if download_url:
                    out_video = os.path.join(WORKSPACE, "website", "camera_path_preview.mp4")
                    backup_video = os.path.join(WORKSPACE, "renders", "preview", "camera_path_preview_v007.mp4")
                    
                    # Download video file
                    urllib.request.urlretrieve(download_url, out_video)
                    urllib.request.urlretrieve(download_url, backup_video)
                    print(f"Saved animation video to {out_video} and {backup_video} ({os.path.getsize(out_video)} bytes)")

                # Also save the full status
                with open("scripts/job_final_v007.json", "w", encoding="utf-8") as jf:
                    json.dump(status_obj, jf, indent=2)
                return True
            elif stat in ["failed", "canceled"]:
                print(f"Job failed with status: {stat}")
                print(status_obj)
                return False

    print("Polling timed out.")
    return False

if __name__ == "__main__":
    run_animation_job()

