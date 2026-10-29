import cv2
import numpy as np

sbs = cv2.imread(r"c:\Users\manpr\Documents\42 Kalidasa\renders\preview\exterior_comparison_side_by_side.png")
h, w, c = sbs.shape
print(f"Side-by-side shape: {h}x{w}")

# The side-by-side is 2400 wide, with padding.
# Let's inspect where the photo and render are positioned:
# Typically left side: x: [0:1200], right side: x: [1200:2400]
# Let's save both halves
left_half = sbs[60:, 0:1200]
right_half = sbs[60:, 1200:2400]

# Let's analyze color distributions, edge density, and vertical structure in both halves:
gray_left = cv2.cvtColor(left_half, cv2.COLOR_BGR2GRAY)
gray_right = cv2.cvtColor(right_half, cv2.COLOR_BGR2GRAY)

edges_left = cv2.Canny(gray_left, 50, 150)
edges_right = cv2.Canny(gray_right, 50, 150)

print("Edge count left (photo):", np.sum(edges_left > 0))
print("Edge count right (render):", np.sum(edges_right > 0))

# Let's inspect specific areas of the reference photograph:
# 1. What does the tower in the photograph actually look like?
# Let's find the bounding box of the building in the photograph:
# In the photo, the building is in the center-right or center?
# Let's sample columns to see where the building stands
col_mean_left = np.mean(gray_left, axis=0)
col_mean_right = np.mean(gray_right, axis=0)

# Let's save vertical slices or samples
cv2.imwrite(r"c:\Users\manpr\Documents\42 Kalidasa\renders\preview\debug_left_photo.png", left_half)
cv2.imwrite(r"c:\Users\manpr\Documents\42 Kalidasa\renders\preview\debug_right_render.png", right_half)
print("Saved debug_left_photo.png and debug_right_render.png")

