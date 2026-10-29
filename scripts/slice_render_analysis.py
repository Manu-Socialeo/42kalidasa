import cv2
import numpy as np

render = cv2.imread(r"c:\Users\manpr\Documents\42 Kalidasa\renders\preview\exterior_photo_match_render.png")

slices = {
    "crown_top": render[50:180, 350:850],
    "upper_floors": render[180:350, 350:850],
    "mid_floors": render[350:520, 350:850],
    "lower_floors": render[520:680, 350:850],
    "ground_entrance": render[650:780, 350:850],
    "balcony_detail": render[300:450, 500:700]
}

print("=== SLICE ANALYSIS OF PREVIOUS RENDER ===")
for s_name, img in slices.items():
    h, w, c = img.shape
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    v = hsv[:,:,2]
    p10, p50, p90 = np.percentile(v, [10, 50, 90])
    white_pct = np.mean((v > 210) & (hsv[:,:,1] < 40)) * 100
    blue_pct = np.mean((hsv[:,:,0] >= 85) & (hsv[:,:,0] <= 130) & (hsv[:,:,1] > 30) & (v > 50)) * 100
    dark_pct = np.mean(v < 50) * 100
    warm_pct = np.mean((hsv[:,:,0] >= 10) & (hsv[:,:,0] <= 35) & (hsv[:,:,1] >= 20) & (v >= 80)) * 100
    print(f"[{s_name:<16}] Brightness (10/50/90): {p10:.0f}/{p50:.0f}/{p90:.0f} | White: {white_pct:.1f}% | Blue/Cyan: {blue_pct:.1f}% | Dark: {dark_pct:.1f}% | Warm Beige: {warm_pct:.1f}%")


