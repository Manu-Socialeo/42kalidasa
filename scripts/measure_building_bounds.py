import cv2
import numpy as np

photo = cv2.imread(r"c:\Users\manpr\Documents\42 Kalidasa\assets\WhatsApp Image 2026-10-27 at 11.30.09 AM.jpeg")
render = cv2.imread(r"c:\Users\manpr\Documents\42 Kalidasa\renders\preview\exterior_photo_match_render.png")

# Let's find building columns across middle row (y=300 to y=500)
# In photo:
row_p = np.mean(photo[300:500, :, :], axis=0) # shape (1200, 3)
# In render:
row_r = np.mean(render[300:500, :, :], axis=0)

# Sky in photo is roughly blue/cyan: B > 180, G > 160, R > 140
# Building is distinctly darker or different color
non_sky_p = np.where(~((row_p[:,0] > 180) & (row_p[:,1] > 160) & (row_p[:,2] > 140)))[0]
print(f"Photo building horizontal range at y=300-500: x={non_sky_p.min()} to x={non_sky_p.max()} (width={non_sky_p.max() - non_sky_p.min()}px)")

# In render:
non_sky_r = np.where(~((row_r[:,0] > 180) & (row_r[:,1] > 180) & (row_r[:,2] > 180)))[0]
if len(non_sky_r) > 0:
    print(f"Render building horizontal range at y=300-500: x={non_sky_r.min()} to x={non_sky_r.max()} (width={non_sky_r.max() - non_sky_r.min()}px)")
else:
    print("Render building not detected in range!")

