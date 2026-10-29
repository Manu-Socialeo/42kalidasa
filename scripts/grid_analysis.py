import cv2
import numpy as np

photo = cv2.imread(r"c:\Users\manpr\Documents\42 Kalidasa\assets\WhatsApp Image 2026-10-27 at 11.30.09 AM.jpeg")
h, w, c = photo.shape

# Let's divide photo into a 3x3 grid:
# Rows: [0:266], [266:533], [533:800]
# Cols: [0:400], [400:800], [800:1200]

grid_summary = []
for r in range(3):
    r_start, r_end = r * (h // 3), (r + 1) * (h // 3)
    row_info = []
    for col in range(3):
        c_start, c_end = col * (w // 3), (col + 1) * (w // 3)
        cell = photo[r_start:r_end, c_start:c_end]
        mean_bgr = np.mean(cell, axis=(0,1))
        std_bgr = np.std(cell, axis=(0,1))
        row_info.append(f"Cell({r},{col}) BGR=({mean_bgr[0]:.0f},{mean_bgr[1]:.0f},{mean_bgr[2]:.0f}) std={np.mean(std_bgr):.0f}")
        # Save each cell
        cv2.imwrite(rf"c:\Users\manpr\Documents\42 Kalidasa\renders\preview\grid_cell_{r}_{col}.png", cell)
    grid_summary.append(" | ".join(row_info))

for line in grid_summary:
    print(line)

