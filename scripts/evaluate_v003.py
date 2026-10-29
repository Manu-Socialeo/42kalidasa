import cv2
import numpy as np
import os

workspace = r"C:\Users\manpr\Documents\42 Kalidasa"
photo_path = os.path.join(workspace, "assets", "WhatsApp Image 2026-10-27 at 11.30.09 AM.jpeg")
v001_path = os.path.join(workspace, "renders", "preview", "exterior_photo_match_render.png")
v002_path = os.path.join(workspace, "renders", "preview", "exterior_photo_match_render_v002.png")
v003_path = os.path.join(workspace, "renders", "preview", "exterior_photo_match_render_v003.png")
sbs_v003_path = os.path.join(workspace, "renders", "preview", "exterior_comparison_side_by_side_v003.png")

ref_img = cv2.resize(cv2.imread(photo_path), (1200, 800))
rend_v003 = cv2.resize(cv2.imread(v003_path), (1200, 800))

# Create v003 side by side
bar_h = 60
header_left = np.zeros((bar_h, 1200, 3), dtype=np.uint8) + 24
header_right = np.zeros((bar_h, 1200, 3), dtype=np.uint8) + 24

cv2.putText(header_left, "APPROVED BUILDING REFERENCE PHOTOGRAPH", (40, 40),
            cv2.FONT_HERSHEY_SIMPLEX, 0.82, (220, 240, 255), 2, cv2.LINE_AA)
cv2.putText(header_right, "CORRECTED 3D ARCHITECTURAL MODEL (CYCLES v003)", (40, 40),
            cv2.FONT_HERSHEY_SIMPLEX, 0.82, (180, 240, 180), 2, cv2.LINE_AA)
            
panel_left = np.vstack([header_left, ref_img])
panel_right = np.vstack([header_right, rend_v003])
sbs_v003 = np.hstack([panel_left, panel_right])
cv2.imwrite(sbs_v003_path, sbs_v003)
print(f"Saved side-by-side v003: {sbs_v003_path}")

def analyze(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    edge_count = int(np.sum(edges > 0))
    v = hsv[:,:,2]
    white_pct = float(np.mean((v > 200) & (hsv[:,:,1] < 45)) * 100)
    blue_pct = float(np.mean((hsv[:,:,0] >= 80) & (hsv[:,:,0] <= 135) & (hsv[:,:,1] > 25)) * 100)
    dark_pct = float(np.mean(v < 60) * 100)
    warm_pct = float(np.mean((hsv[:,:,0] >= 10) & (hsv[:,:,0] <= 35) & (hsv[:,:,1] >= 20) & (v >= 70)) * 100)
    return {
        "edge_count": edge_count,
        "white_percent": round(white_pct, 1),
        "blue_cyan_percent": round(blue_pct, 1),
        "dark_shadow_percent": round(dark_pct, 1),
        "warm_beige_percent": round(warm_pct, 1),
        "mean_brightness": round(float(np.mean(v)), 1)
    }

m_photo = analyze(ref_img)
m_v001 = analyze(cv2.imread(v001_path))
m_v002 = analyze(cv2.imread(v002_path))
m_v003 = analyze(rend_v003)

print("\n=== METRIC COMPARISON ACROSS ALL ITERATIONS ===")
print("Metric                 | Photo     | v001 (Baseline) | v002 (Framing/Mat) | v003 (Glazing/Shadows)")
print("-----------------------+-----------+-----------------+--------------------+-----------------------")
for k in ["edge_count", "warm_beige_percent", "blue_cyan_percent", "white_percent", "dark_shadow_percent", "mean_brightness"]:
    print(f"{k:<22} | {str(m_photo[k]):<9} | {str(m_v001[k]):<15} | {str(m_v002[k]):<18} | {str(m_v003[k]):<20}")


