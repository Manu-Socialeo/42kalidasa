import cv2
import numpy as np

photo = cv2.imread(r"c:\Users\manpr\Documents\42 Kalidasa\assets\WhatsApp Image 2026-10-27 at 11.30.09 AM.jpeg")
h, w, _ = photo.shape

print(f"Image resolution: {w}x{h}")

# Let's inspect:
# 1. What is the sky color?
# 2. What is the lighting / sun direction? (Where are the shadows falling?)
# 3. What are the colors of the building elements?
# 4. Where are the balconies? Are they on the left, center, or right?
# 5. What are the horizontal slab bands?
# 6. What is at the ground level?

# Let's check sun shadows:
# In the photo, which facade is in direct sunlight, and which is in shade?
# Left facade vs Right facade:
left_facade = photo[200:500, 200:500]
right_facade = photo[200:500, 600:900]

print("Left facade mean BGR:", np.mean(left_facade, axis=(0,1)))
print("Right facade mean BGR:", np.mean(right_facade, axis=(0,1)))

# If right facade is brighter than left facade or vice versa:
left_v = np.mean(cv2.cvtColor(left_facade, cv2.COLOR_BGR2HSV)[:,:,2])
right_v = np.mean(cv2.cvtColor(right_facade, cv2.COLOR_BGR2HSV)[:,:,2])
print(f"Value/Brightness: Left={left_v:.1f}, Right={right_v:.1f}")

# Look at color clusters in photo using K-Means (5 dominant colors)
data = photo.reshape((-1, 3)).astype(np.float32)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
k = 6
_, labels, centers = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
print("\nDominant 6 Colors in Approved Photo (BGR & RGB):")
for i, center in enumerate(centers):
    b, g, r = center
    count = np.sum(labels == i)
    pct = (count / len(data)) * 100
    print(f"Color {i+1}: BGR=({b:.0f}, {g:.0f}, {r:.0f}) | RGB=({r:.0f}, {g:.0f}, {b:.0f}) | {pct:.1f}%")


