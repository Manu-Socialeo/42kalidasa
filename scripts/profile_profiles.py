import cv2
import numpy as np

mask_p = cv2.imread(r"c:\Users\manpr\Documents\42 Kalidasa\renders\preview\mask_photo_building.png", cv2.IMREAD_GRAYSCALE)
mask_r = cv2.imread(r"c:\Users\manpr\Documents\42 Kalidasa\renders\preview\mask_render_building.png", cv2.IMREAD_GRAYSCALE)

# Sum across columns (vertical profile)
v_profile_p = np.mean(mask_p, axis=1) # shape 800
v_profile_r = np.mean(mask_r, axis=1)

# Sum across rows (horizontal profile)
h_profile_p = np.mean(mask_p, axis=0) # shape 1200
h_profile_r = np.mean(mask_r, axis=0)

print("=== Vertical Building Presence (y=0 to 800) ===")
for y in range(0, 800, 50):
    print(f"y={y:<3}: photo={v_profile_p[y]:.1f}/255 | render={v_profile_r[y]:.1f}/255")

print("\n=== Horizontal Building Presence (x=0 to 1200) ===")
for x in range(0, 1200, 100):
    print(f"x={x:<4}: photo={h_profile_p[x]:.1f}/255 | render={h_profile_r[x]:.1f}/255")

