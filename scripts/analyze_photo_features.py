import cv2
import numpy as np

photo = cv2.imread(r"c:\Users\manpr\Documents\42 Kalidasa\assets\WhatsApp Image 2026-10-27 at 11.30.09 AM.jpeg")
h, w, c = photo.shape

# Let's crop 6 distinct areas of the building in the photo to understand its exact facade:
# 1. Tower upper facade (floors 14-19)
# 2. Tower mid facade (floors 7-13)
# 3. Tower lower facade (floors 1-6)
# 4. Balcony railings / glass
# 5. Vertical piers / columns
# 6. Entrance / ground podium

# Let's find building horizontal boundaries
# In the photo (1200 wide), where is the tower?
# Let's compute column gradients
gray = cv2.cvtColor(photo, cv2.COLOR_BGR2GRAY)

# Let's slice vertical regions
slices = {
    "crown_top": photo[50:180, 350:850],
    "upper_floors": photo[180:350, 350:850],
    "mid_floors": photo[350:520, 350:850],
    "lower_floors": photo[520:680, 350:850],
    "ground_entrance": photo[650:780, 350:850],
    "balcony_detail": photo[300:450, 500:700]
}

for name, s in slices.items():
    cv2.imwrite(rf"c:\Users\manpr\Documents\42 Kalidasa\renders\preview\photo_slice_{name}.png", s)
    avg_bgr = np.mean(s, axis=(0,1))
    std_bgr = np.std(s, axis=(0,1))
    print(f"Slice {name:<16}: BGR=({avg_bgr[0]:.1f}, {avg_bgr[1]:.1f}, {avg_bgr[2]:.1f}) | RGB=({avg_bgr[2]:.1f}, {avg_bgr[1]:.1f}, {avg_bgr[0]:.1f}) | std=({std_bgr[0]:.1f})")


