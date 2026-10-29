import cv2
import numpy as np

img = cv2.imread(r"c:\Users\manpr\Documents\42 Kalidasa\assets\WhatsApp Image 2026-10-27 at 11.30.09 AM.jpeg")
# Let's inspect the entire image composition
# Let's print out what colors dominate, what text or features are visible
# Let's resize and save a high-contrast version to inspect edges
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
cv2.imwrite(r"c:\Users\manpr\Documents\42 Kalidasa\renders\preview\photo_adaptive_thresh.png", thresh)

# Let's check the perspective:
# Where is the building positioned?
# Top-left of building, top-right, bottom-left, bottom-right
print("Image dimensions:", img.shape)
# Let's find vertical lines with HoughLinesP
edges = cv2.Canny(gray, 50, 150)
lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)
print("Detected prominent straight lines:", len(lines) if lines is not None else 0)

# Check line angles:
vertical_lines = []
horizontal_lines = []
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
        if abs(abs(angle) - 90) < 15:
            vertical_lines.append(line[0])
        elif abs(angle) < 15 or abs(angle - 180) < 15:
            horizontal_lines.append(line[0])

print(f"Vertical lines: {len(vertical_lines)}, Horizontal lines: {len(horizontal_lines)}")
if vertical_lines:
    v_xs = [(l[0] + l[2])//2 for l in vertical_lines]
    print(f"Building horizontal span: min_x={min(v_xs)}, max_x={max(v_xs)}")

