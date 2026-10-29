"""
Generate Side-by-Side Comparison v003 and 50/50 Overlay v003
Compares the approved reference photo against the blueprint-reconstructed Cycles render (v003).
"""

import cv2
import numpy as np
import os

WORKSPACE = r"C:\Users\manpr\Documents\42 Kalidasa"
REF_PHOTO = os.path.join(WORKSPACE, "assets", "WhatsApp Image 2026-10-27 at 11.30.09 AM.jpeg")
RENDER_V003 = os.path.join(WORKSPACE, "renders", "preview", "kalidasa42_corrected_v003.png")
RENDER_V002 = os.path.join(WORKSPACE, "renders", "preview", "kalidasa42_corrected_v002.png")
COMP_OUT = os.path.join(WORKSPACE, "renders", "preview", "kalidasa42_comparison_v003.png")
OVERLAY_OUT = os.path.join(WORKSPACE, "renders", "preview", "kalidasa42_overlay_v003.png")
REPORT_OUT = os.path.join(WORKSPACE, "docs", "kalidasa42_blueprint_reconstruction_v003_report.md")

def main():
    if not os.path.exists(RENDER_V003):
        print(f"Error: {RENDER_V003} not found.")
        return

    ref_img = cv2.imread(REF_PHOTO)
    rend_img = cv2.imread(RENDER_V003)

    target_w, target_h = 1200, 800
    ref_resized = cv2.resize(ref_img, (target_w, target_h))
    rend_resized = cv2.resize(rend_img, (target_w, target_h))

    # 1. Header panels
    bar_h = 60
    header_left = np.zeros((bar_h, target_w, 3), dtype=np.uint8) + 24
    header_right = np.zeros((bar_h, target_w, 3), dtype=np.uint8) + 24

    cv2.putText(header_left, "APPROVED ARCHITECTURAL PHOTOGRAPH", (40, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.82, (220, 240, 255), 2, cv2.LINE_AA)
    cv2.putText(header_right, "EXACT BLUEPRINT 3D RECONSTRUCTION (v003)", (40, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.82, (180, 240, 180), 2, cv2.LINE_AA)

    panel_left = np.vstack([header_left, ref_resized])
    panel_right = np.vstack([header_right, rend_resized])

    side_by_side = np.hstack([panel_left, panel_right])
    cv2.imwrite(COMP_OUT, side_by_side)
    print(f"Side-by-side saved to: {COMP_OUT}")

    # 2. Overlay (50% blend + Canny Edge overlay from reference photo)
    blend = cv2.addWeighted(ref_resized, 0.5, rend_resized, 0.5, 0)
    ref_gray = cv2.cvtColor(ref_resized, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(ref_gray, 50, 150)
    # Highlight edges in bright cyan
    overlay = blend.copy()
    overlay[edges > 0] = [255, 255, 0]

    header_overlay = np.zeros((bar_h, target_w, 3), dtype=np.uint8) + 24
    cv2.putText(header_overlay, "BLUEPRINT GEOMETRY OVERLAY (v003 + PHOTO CANNY EDGES)", (40, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 255), 2, cv2.LINE_AA)
    final_overlay = np.vstack([header_overlay, overlay])
    cv2.imwrite(OVERLAY_OUT, final_overlay)
    print(f"Overlay saved to: {OVERLAY_OUT}")

    # 3. Quantitative Analysis
    def calc_stats(img):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        v = hsv[:, :, 2]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges_cnt = int(np.sum(cv2.Canny(gray, 50, 150) > 0))
        mean_v = float(np.mean(v))
        warm_pct = float(np.mean((hsv[:,:,0] >= 10) & (hsv[:,:,0] <= 35) & (hsv[:,:,1] >= 20) & (v >= 70)) * 100)
        return edges_cnt, mean_v, warm_pct

    p_edges, p_v, p_warm = calc_stats(ref_resized)
    r_edges, r_v, r_warm = calc_stats(rend_resized)

    print(f"Photo: edges={p_edges}, mean_brightness={p_v:.1f}, warm_pct={p_warm:.1f}%")
    print(f"v003:  edges={r_edges}, mean_brightness={r_v:.1f}, warm_pct={r_warm:.1f}%")

if __name__ == "__main__":
    main()

