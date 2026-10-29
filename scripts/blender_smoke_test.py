"""
Blender Automation Smoke Test for Kalidasa 42
Validates headless Blender execution, scene creation, metric unit setup,
saving .blend project file, and rendering a preview image.
"""

import bpy
import os
import sys

def run_smoke_test():
    print("=== STARTING BLENDER SMOKE TEST ===")
    print(f"Blender Version: {bpy.app.version_string}")

    # Project directories
    workspace_root = r"C:\Users\manpr\Documents\42 Kalidasa"
    blender_dir = os.path.join(workspace_root, "blender")
    renders_dir = os.path.join(workspace_root, "renders", "preview")
    
    os.makedirs(blender_dir, exist_ok=True)
    os.makedirs(renders_dir, exist_ok=True)
    
    blend_path = os.path.join(blender_dir, "smoke_test.blend")
    render_output_path = os.path.join(renders_dir, "smoke_test.png")

    # 1. Clean existing objects
    bpy.ops.wm.read_factory_settings(use_empty=True)

    # 2. Configure Scene & Metric Units (architectural standard)
    scene = bpy.context.scene
    scene.unit_settings.system = 'METRIC'
    scene.unit_settings.scale_length = 1.0
    scene.unit_settings.length_unit = 'METERS'

    # 3. Create a test geometry (Representative Kalidasa 42 plinth + massing block)
    # Ground slab: 36m x 16m x 0.5m
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.25))
    ground = bpy.context.active_object
    ground.name = "Test_Ground_Plinth"
    ground.scale = (36.0, 16.0, 0.5)

    # Tower mass: 30m x 14m x 67.2m
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 34.1))
    tower = bpy.context.active_object
    tower.name = "Test_Tower_Mass"
    tower.scale = (30.0, 14.0, 67.2)

    # Apply a test material
    mat = bpy.data.materials.new(name="Mat_Test_Concrete")
    if hasattr(mat, "node_tree") and mat.node_tree:
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf and "Base Color" in bsdf.inputs:
            bsdf.inputs['Base Color'].default_value = (0.75, 0.72, 0.68, 1.0)
            if "Roughness" in bsdf.inputs:
                bsdf.inputs['Roughness'].default_value = 0.4
    tower.data.materials.append(mat)
    ground.data.materials.append(mat)

    # 4. Create Sun Light
    bpy.ops.object.light_add(type='SUN', location=(40, -50, 80))
    sun = bpy.context.active_object
    sun.name = "Sun_Light"
    sun.data.energy = 3.5
    sun.rotation_euler = (0.8, 0.2, 0.6)

    # 5. Create Camera with architectural focal length (35mm)
    bpy.ops.object.camera_add(location=(70, -80, 45))
    camera = bpy.context.active_object
    camera.name = "Test_Camera"
    camera.data.lens = 35
    camera.data.clip_end = 500

    # Aim camera at tower midpoint
    track = camera.constraints.new(type='TRACK_TO')
    track.target = tower
    track.track_axis = 'TRACK_NEGATIVE_Z'
    track.up_axis = 'UP_Y'
    scene.camera = camera

    # 6. Set Render Settings
    scene.render.engine = 'BLENDER_EEVEE'
    scene.render.resolution_x = 960
    scene.render.resolution_y = 540
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = render_output_path

    # 7. Save .blend Project File
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print(f"Successfully saved project file: {blend_path}")

    # 8. Render Still Frame
    print(f"Rendering frame to: {render_output_path}")
    bpy.ops.render.render(write_still=True)
    
    # 9. Verification
    if os.path.exists(render_output_path) and os.path.getsize(render_output_path) > 0:
        size_kb = os.path.getsize(render_output_path) / 1024
        print(f"VERIFICATION SUCCESS: Rendered image exists ({size_kb:.1f} KB)")
    else:
        print("VERIFICATION FAILURE: Rendered image was not created")
        sys.exit(1)

    if os.path.exists(blend_path) and os.path.getsize(blend_path) > 0:
        size_kb = os.path.getsize(blend_path) / 1024
        print(f"VERIFICATION SUCCESS: Blend file exists ({size_kb:.1f} KB)")
    else:
        print("VERIFICATION FAILURE: Blend file was not saved")
        sys.exit(1)

    print("=== BLENDER SMOKE TEST COMPLETED SUCCESSFULLY ===")

if __name__ == "__main__":
    run_smoke_test()
