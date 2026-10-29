import cv2
import numpy as np

photo = cv2.imread(r"c:\Users\manpr\Documents\42 Kalidasa\assets\WhatsApp Image 2026-10-27 at 11.30.09 AM.jpeg")
render = cv2.imread(r"c:\Users\manpr\Documents\42 Kalidasa\renders\preview\exterior_photo_match_render.png")

# Let's save a visual representation of where non-sky pixels are in both photo and render
# Photo sky: B > 185, G > 165, R > 145 (and G > R)
# Let's create masks
sky_p = (photo[:,:,0] > 180) & (photo[:,:,1] > 160) & (photo[:,:,0] > photo[:,:,2] + 15)
building_p = ~sky_p

sky_r = (render[:,:,0] > 180) & (render[:,:,1] > 180) & (render[:,:,2] > 180)
building_r = ~sky_r

# Save masks as images
cv2.imwrite(r"c:\Users\manpr\Documents\42 Kalidasa\renders\preview\mask_photo_building.png", (building_p * 255).astype(np.uint8))
cv2.imwrite(r"c:\Users\manpr\Documents\42 Kalidasa\renders\preview\mask_render_building.png", (building_r * 255).astype(np.uint8))

# Find bounding rect of building in photo (excluding bottom 100px for foreground street if needed)
pts_p = cv2.findNonZero((building_p * 255).astype(np.uint8))
x_p, y_p, w_p, h_p = cv2.boundingRect(pts_p)
print(f"Photo building bounding box: x={x_p}, y={y_p}, w={w_p}, h={h_p}")

pts_r = cv2.findNonZero((building_r * 255).astype(np.uint8))
x_r, y_r, w_r, h_r = cv2.boundingRect(pts_r)
print(f"Render building bounding box: x={x_r}, y={y_r}, w={w_r}, h={h_r}")

