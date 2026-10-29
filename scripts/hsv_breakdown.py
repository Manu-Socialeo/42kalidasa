import cv2
import numpy as np

photo = cv2.imread(r"c:\Users\manpr\Documents\42 Kalidasa\assets\WhatsApp Image 2026-10-27 at 11.30.09 AM.jpeg")
render = cv2.imread(r"c:\Users\manpr\Documents\42 Kalidasa\renders\preview\exterior_photo_match_render.png")

# Let's inspect the tower in the photo in detail:
# Where are the curved balconies located?
# In Cell(1,0) and Cell(1,1):
# Let's extract the balcony railing colors in the photo:
# Let's find pixels in the balcony region that have cyan/blue hue:
hsv_photo = cv2.cvtColor(photo, cv2.COLOR_BGR2HSV)
hsv_render = cv2.cvtColor(render, cv2.COLOR_BGR2HSV)

# In photo:
# Blue/cyan hue is typically 80 - 130 in OpenCV HSV (range 0-180)
blue_mask_photo = (hsv_photo[:,:,0] >= 80) & (hsv_photo[:,:,0] <= 135) & (hsv_photo[:,:,1] > 20)
print("Photo blue/cyan pixel count:", np.sum(blue_mask_photo))

blue_mask_render = (hsv_render[:,:,0] >= 80) & (hsv_render[:,:,0] <= 135) & (hsv_render[:,:,1] > 20)
print("Render blue/cyan pixel count:", np.sum(blue_mask_render))

# White slab edges in photo:
# High Value (V > 180), Low Saturation (S < 40)
white_mask_photo = (hsv_photo[:,:,2] > 180) & (hsv_photo[:,:,1] < 45)
print("Photo white/bright pixel count:", np.sum(white_mask_photo))

white_mask_render = (hsv_render[:,:,2] > 180) & (hsv_render[:,:,1] < 45)
print("Render white/bright pixel count:", np.sum(white_mask_render))

# Dark charcoal / shadows / frames in photo:
# Low Value (V < 60)
dark_mask_photo = (hsv_photo[:,:,2] < 70)
print("Photo dark/shadow/frame pixel count:", np.sum(dark_mask_photo))

dark_mask_render = (hsv_render[:,:,2] < 70)
print("Render dark/shadow/frame pixel count:", np.sum(dark_mask_render))

