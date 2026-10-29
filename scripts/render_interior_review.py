"""
Render Stage 7 Interior Review
Using Cycles (CPU, 16 samples) for robust photorealistic architectural global illumination.
Outputs: renders/preview/interior_review.png (1920 x 1080)
"""

import bpy
import os
import sys

blend_path = r"C:\Users\manpr\Documents\42 Kalidasa\blender\kalidasa42_interior_v001.blend"
output_path = r"C:\Users\manpr\Documents\42 Kalidasa\renders\preview\interior_review.png"

print(f"Loading interior model: {blend_path}")
bpy.ops.wm.open_mainfile(filepath=blend_path)
scene = bpy.context.scene

print("Configuring Cycles render settings...")
scene.render.engine = 'CYCLES'
if hasattr(scene, 'cycles'):
    scene.cycles.device = 'CPU'
    scene.cycles.samples = 16
    scene.cycles.preview_samples = 16
    scene.cycles.use_denoising = True

scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.filepath = output_path

print(f"Rendering 1080p interior review to: {output_path}...")
bpy.ops.render.render(write_still=True)

if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
    print(f"SUCCESS: Interior review render saved ({os.path.getsize(output_path)/1024:.1f} KB)")
else:
    print("ERROR: Render output failed!")
    sys.exit(1)

