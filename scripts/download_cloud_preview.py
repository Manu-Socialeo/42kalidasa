import json
import urllib.request
import cv2
import os

dl_url = "https://render.janction.jp/dl/eyJqIjoial9mODgxZGNiODQ3ZGM0NTRjIiwibiI6ImZyYW1lXzAwMDEucG5nIiwiZSI6MTc5MzM4MTAyM30.LBJqMoHR-0N2ExUrWIg9uSoDaetcgxAz"
output_path = "renders/preview/cloud_gpu_exterior_preview_v003.png"

print(f"Downloading {dl_url}...")
urllib.request.urlretrieve(dl_url, output_path)

file_size = os.path.getsize(output_path)
print(f"Saved to {output_path} ({file_size} bytes)")

img = cv2.imread(output_path)
if img is not None:
    h, w, c = img.shape
    print(f"SUCCESS: Decoded image {w}x{h} with {c} channels.")
else:
    print("FAILED to decode image with cv2.")
