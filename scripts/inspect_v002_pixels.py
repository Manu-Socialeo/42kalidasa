import cv2
import numpy as np

img = cv2.imread(r"c:\Users\manpr\Documents\42 Kalidasa\renders\preview\exterior_photo_match_render_v002.png")
h, w, c = img.shape

# Let's inspect what colors exist in the render:
# What percentage of the image is sky?
# Sky in render is around: BGR:
sky_sample = img[50, 50]
print("Render Sky sample BGR:", sky_sample)

# Find non-sky pixels:
diff_from_sky = np.linalg.norm(img.astype(float) - sky_sample.astype(float), axis=2)
building_pixels = diff_from_sky > 25
print(f"Total non-sky (building + ground) pixels: {np.sum(building_pixels)} / {h*w} ({np.mean(building_pixels)*100:.1f}%)")

# Let's inspect only the building pixels:
b_bgr = img[building_pixels]
mean_b = np.mean(b_bgr, axis=0)
print("Mean BGR of building pixels:", mean_b)
print("Mean RGB of building pixels:", mean_b[2], mean_b[1], mean_b[0])

# Let's check HSV of building pixels:
b_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)[building_pixels]
print("Building HSV Hue distribution (0-180):")
print("  Red/Orange/Beige (H 10-35):", np.mean((b_hsv[:,0] >= 10) & (b_hsv[:,0] <= 35)) * 100, "%")
print("  Blue/Cyan (H 80-135):", np.mean((b_hsv[:,0] >= 80) & (b_hsv[:,0] <= 135)) * 100, "%")
print("  Value (Brightness) mean:", np.mean(b_hsv[:,2]))

# Where is the building positioned in the image?
pts = cv2.findNonZero(building_pixels.astype(np.uint8))
if pts is not None:
    x, y, bw, bh = cv2.boundingRect(pts)
    print(f"Building bounding box in render v002: x={x}, y={y}, width={bw}, height={bh}")

