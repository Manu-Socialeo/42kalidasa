import cv2
import numpy as np

slices = ["crown_top", "upper_floors", "mid_floors", "lower_floors", "ground_entrance", "balcony_detail"]

print("=== SLICE ANALYSIS OF APPROVED BUILDING PHOTOGRAPH ===")
for s_name in slices:
    img = cv2.imread(rf"c:\Users\manpr\Documents\42 Kalidasa\renders\preview\photo_slice_{s_name}.png")
    if img is None:
        continue
    h, w, c = img.shape
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Analyze brightness percentiles:
    v = hsv[:,:,2]
    p10, p50, p90 = np.percentile(v, [10, 50, 90])
    
    # Count pure white / near white (V > 210, S < 40)
    white_pct = np.mean((v > 210) & (hsv[:,:,1] < 40)) * 100
    
    # Count blue / cyan (H: 85-130, S > 30, V > 50)
    blue_pct = np.mean((hsv[:,:,0] >= 85) & (hsv[:,:,0] <= 130) & (hsv[:,:,1] > 30) & (v > 50)) * 100
    
    # Count dark / shadow (V < 50)
    dark_pct = np.mean(v < 50) * 100
    
    # Count warm beige / sandstone (H: 10-35, S: 20-80, V: 80-200)
    warm_pct = np.mean((hsv[:,:,0] >= 10) & (hsv[:,:,0] <= 35) & (hsv[:,:,1] >= 20) & (v >= 80)) * 100
    
    print(f"[{s_name:<16}] Brightness (10/50/90): {p10:.0f}/{p50:.0f}/{p90:.0f} | White: {white_pct:.1f}% | Blue/Cyan: {blue_pct:.1f}% | Dark: {dark_pct:.1f}% | Warm Beige: {warm_pct:.1f}%")


