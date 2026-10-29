import json
import urllib.request
import os
import concurrent.futures

def download_cloud_sequence():
    with open('scripts/janction_key.json', 'r', encoding='utf-8') as f:
        key_info = json.load(f)
    key = key_info['api_key']

    job_id = "j_acd007b4afda4fd1"
    print(f"Fetching artifacts for job {job_id}...")

    req = urllib.request.Request(
        f'https://render.janction.jp/v1/jobs/{job_id}',
        headers={'Authorization': f'Bearer {key}', 'Accept': 'application/json'}
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        artifacts = data.get('artifacts', [])

    art_by_name = {a['name']: a for a in artifacts}
    print(f"Found {len(artifacts)} total artifacts.")

    out_dir = "website/sequence"
    os.makedirs(out_dir, exist_ok=True)

    # 90 sequence frames spanning 180 timeline frames (step = 2)
    # timeline frame 1 -> sequence frame 1
    # timeline frame 3 -> sequence frame 2
    # ...
    # timeline frame 179 -> sequence frame 90
    tasks = []
    for seq_idx in range(1, 91):
        timeline_idx = (seq_idx - 1) * 2 + 1
        src_name = f"frame_{timeline_idx:04d}.png"
        dst_name = f"frame_{seq_idx:04d}.png"
        dst_path = os.path.join(out_dir, dst_name)

        if src_name in art_by_name:
            art = art_by_name[src_name]
            url = art.get('view_url') or art.get('url')
            tasks.append((url, dst_path, seq_idx, timeline_idx))
        else:
            print(f"Warning: {src_name} not found in artifacts!")

    print(f"Ready to download {len(tasks)} frames concurrently...")

    def download_one(item):
        url, path, seq, time_f = item
        for retry in range(3):
            try:
                urllib.request.urlretrieve(url, path)
                return True
            except Exception as e:
                pass
        return False

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(download_one, tasks))

    success_count = sum(1 for r in results if r)
    print(f"Downloaded {success_count}/{len(tasks)} sequence frames successfully!")

if __name__ == '__main__':
    download_cloud_sequence()

