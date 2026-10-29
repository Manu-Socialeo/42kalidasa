import bpy
import sys

blend_path = r"C:\Users\manpr\Documents\42 Kalidasa\blender\kalidasa42_interior_v001.blend"
bpy.ops.wm.open_mainfile(filepath=blend_path)
scene = bpy.context.scene

print("Loaded scene:", scene.name)
print("Camera:", scene.camera.name if scene.camera else "None")
print("Engine:", scene.render.engine)
print("Available engines:", [item.identifier for item in scene.render.bl_rna.properties['engine'].enum_items])

# Let's test Cycles with 1 sample
scene.render.engine = 'CYCLES'
scene.cycles.samples = 1
scene.cycles.device = 'CPU'
scene.render.resolution_x = 640
scene.render.resolution_y = 360
scene.render.filepath = r"C:\Users\manpr\Documents\42 Kalidasa\renders\preview\test_cycles.png"
print("Rendering 1 test frame with Cycles...")
bpy.ops.render.render(write_still=True)
print("Cycles test completed successfully!")

