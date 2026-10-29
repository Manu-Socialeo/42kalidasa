import cv2
import numpy as np

photo_path = r"c:\Users\manpr\Documents\42 Kalidasa\assets\WhatsApp Image 2026-10-27 at 11.30.09 AM.jpeg"
render_path = r"c:\Users\manpr\Documents\42 Kalidasa\renders\preview\exterior_photo_match_render.png"

photo = cv2.imread(photo_path)
render = cv2.imread(render_path)

print(f"Photo shape: {photo.shape}, Render shape: {render.shape}")

# Sample key regions in the photograph
# Let's crop:
# 1. Crown / upper floors: y: [50:250], x: [400:800]
# 2. Mid curved balconies: y: [250:500], x: [450:750]
# 3. Ground / Entrance / Canopy: y: [500:750], x: [400:850]

cv2.imwrite(r"c:\Users\manpr\Documents\42 Kalidasa\renders\preview\photo_crop_crown.png", photo[50:250, 400:800])
cv2.imwrite(r"c:\Users\manpr\Documents\42 Kalidasa\renders\preview\photo_crop_balconies.png", photo[250:500, 450:750])
cv2.imwrite(r"c:\Users\manpr\Documents\42 Kalidasa\renders\preview\photo_crop_ground.png", photo[500:750, 400:850])

print("Saved photo crops for crown, balconies, ground.")

# Calculate average colors in balconies region
balc_roi = photo[250:500, 450:750]
b_avg = np.mean(balc_roi[:, :, 0])
g_avg = np.mean(balc_roi[:, :, 1])
r_avg = np.mean(balc_roi[:, :, 2])
print(f"Balconies ROI BGR: ({b_avg:.1f}, {g_avg:.1f}, {r_avg:.1f})")

# Sky ROI: y: [20:120], x: [100:300]
sky_roi = photo[20:120, 100:300]
print(f"Sky ROI BGR: ({np.mean(sky_roi[:,:,0]):.1f}, {np.mean(sky_roi[:,:,1]):.1f}, {np.mean(sky_roi[:,:,2]):.1f})")

# Render comparison
render_balc_roi = render[250:500, 450:750]
print(f"Render Balconies ROI BGR: ({np.mean(render_balc_roi[:,:,0]):.1f}, {np.mean(render_balc_roi[:,:,1]):.1f}, {np.mean(render_balc_roi[:,:,2]):.1f})")

