import json
import urllib.request
import urllib.error
import os

def upload_file():
    with open('scripts/janction_key.json', 'r', encoding='utf-8') as f:
        key_info = json.load(f)
    key = key_info['api_key']

    blend_path = 'blender/kalidasa42_animated_v001.blend'
    filename = os.path.basename(blend_path)
    file_size = os.path.getsize(blend_path)
    print(f'Uploading {filename} ({file_size} bytes)...')

    boundary = '----JanctionUploadBoundary123456789'
    header = (
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
        f'Content-Type: application/octet-stream\r\n\r\n'
    ).encode('utf-8')
    footer = f'\r\n--{boundary}--\r\n'.encode('utf-8')

    with open(blend_path, 'rb') as f:
        content = f.read()

    body = header + content + footer

    req = urllib.request.Request(
        'https://render.janction.jp/v1/files',
        headers={
            'Authorization': f'Bearer {key}',
            'Content-Type': f'multipart/form-data; boundary={boundary}',
            'Accept': 'application/json'
        },
        data=body
    )

    try:
        with urllib.request.urlopen(req) as resp:
            data = resp.read().decode('utf-8')
            print('Upload success:')
            print(data)
            return json.loads(data)
    except urllib.error.HTTPError as e:
        print('HTTP Error:', e.code, e.read().decode('utf-8'))
        return None

if __name__ == '__main__':
    upload_file()

