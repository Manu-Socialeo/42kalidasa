import cv2
import numpy as np

photo = cv2.imread(r"c:\Users\manpr\Documents\42 Kalidasa\assets\WhatsApp Image 2026-10-27 at 11.30.09 AM.jpeg")
render = cv2.imread(r"c:\Users\manpr\Documents\42 Kalidasa\renders\preview\exterior_photo_match_render.png")

# Let's inspect the differences between photo and render:
# 1. Sky:
photo_sky = photo[50:150, 100:300]
render_sky = render[50:150, 100:300]
print("Photo Sky mean BGR:", np.mean(photo_sky, axis=(0,1)))
print("Render Sky mean BGR:", np.mean(render_sky, axis=(0,1)))

# 2. Main tower body in photo vs render:
# In render:
# Let's check where the building is located in both images:
# Find building mask (pixels that are not sky/background)
photo_bg_thresh = (photo[:,:,0] > 180) & (photo[:,:,1] > 160) & (photo[:,:,2] > 140)
print("Photo background sky percentage:", np.mean(photo_bg_thresh[:400, :]) * 100)

render_bg_thresh = (render[:,:,0] > 180) & (render[:,:,1] > 180) & (render[:,:,2] > 180)
print("Render background sky percentage:", np.mean(render_bg_thresh[:400, :]) * 100)

# Let's save a visual comparison with difference map
# Resize or align if needed: both are 800x1200!
diff = cv2.absdiff(photo, render)
cv2.imwrite(r"c:\Users\manpr\Documents\42 Kalidasa\renders\preview\diff_map.png", diff)
print("Saved diff_map.png")

