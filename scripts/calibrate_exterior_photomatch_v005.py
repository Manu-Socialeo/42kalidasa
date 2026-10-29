"""
Calibration Iteration v005:
- Uncropped full tower architectural framing (ground canopy to rooftop pergola)
- Remove low-poly icosphere tree placeholders
- Calibrated exposure with AgX High Contrast
- Warm golden hour sunset palette and rich blue balcony glass
"""

import bpy
import math
import os

def calibrate_exterior_v005():
    blend_path = r"C:\Users\manpr\Documents\42 Kalidasa\blender\kalidasa42_animated_v001.blend"
    out_render = r"C:\Users\manpr\Documents\42 Kalidasa\renders\preview\exterior_photo_match_render_v005.png"
    
    print(f"Loading {blend_path} for v005 calibration...")
    bpy.ops.wm.open_mainfile(filepath=blend_path)
    scene = bpy.context.scene

    # 1. Hide low-poly placeholder trees/icospheres
    hidden_count = 0
    for obj in bpy.data.objects:
        lower_name = obj.name.lower()
        if "tree" in lower_name or "icosphere" in lower_name or "placeholder" in lower_name:
            obj.hide_render = True
            obj.hide_viewport = True
            hidden_count += 1
    print(f"  Hidden {hidden_count} low-poly tree/placeholder objects from render.")

    # 2. Color Management & Realistic Film Exposure
    if hasattr(scene, 'view_settings'):
        scene.view_settings.view_transform = 'AgX'
        scene.view_settings.look = 'AgX - Medium High Contrast'
        scene.view_settings.exposure = -0.35 # Natural exposure
        print("  Color management set to AgX with Medium High Contrast.")

    # 3. World Sky & Lighting Calibration
    world = scene.world
    if world and world.node_tree:
        for node in world.node_tree.nodes:
            if node.type == 'BACKGROUND':
                node.inputs["Strength"].default_value = 0.65
            elif node.type == 'TEX_SKY':
                node.sun_elevation = math.radians(16.0) # Golden hour sun
                node.sun_rotation = math.radians(135.0)
                node.sun_intensity = 0.85
                if hasattr(node, 'turbidity'):
                    node.turbidity = 2.8
    print("  World sky calibrated to soft golden hour dusk.")

    # 4. Sun Key Lamp
    sun = bpy.data.objects.get("Sun_Daylight_Hero") or bpy.data.objects.get("Sun_GoldenHour")
    if sun:
        sun.data.energy = 2.2 # Soft golden sun
        sun.data.color = (1.0, 0.82, 0.62)
        sun.data.angle = math.radians(2.0)
        sun.rotation_euler = (math.radians(56.0), math.radians(10.0), math.radians(138.0))
        print("  Key sun lamp energy calibrated to 2.2.")

    # 5. Facade Warmth & Balcony Materials
    mat_facade = bpy.data.materials.get("Mat_Facade_Walls") or bpy.data.materials.get("Mat_Tower_Facade")
    if mat_facade and mat_facade.node_tree:
        bsdf = mat_facade.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            # Rich warm sandstone beige
            bsdf.inputs["Base Color"].default_value = (0.68, 0.55, 0.42, 1.0)
            bsdf.inputs["Roughness"].default_value = 0.75

    mat_glass = bpy.data.materials.get("Mat_Balcony_Glass")
    if mat_glass and mat_glass.node_tree:
        bsdf_g = mat_glass.node_tree.nodes.get("Principled BSDF")
        if bsdf_g:
            # Vibrant cyan-blue architectural glass
            bsdf_g.inputs["Base Color"].default_value = (0.02, 0.45, 0.80, 1.0)
            if "Transmission Weight" in bsdf_g.inputs:
                bsdf_g.inputs["Transmission Weight"].default_value = 0.65
            elif "Transmission" in bsdf_g.inputs:
                bsdf_g.inputs["Transmission"].default_value = 0.65
            bsdf_g.inputs["Roughness"].default_value = 0.04

    # 6. Camera: Full Architectural View (Canopy to Pergola)
    cam_name = "Cam_Photo_Match_Hero_v5"
    if cam_name in bpy.data.objects:
        cam_obj = bpy.data.objects[cam_name]
    else:
        cam_data = bpy.data.cameras.new(cam_name)
        cam_obj = bpy.data.objects.new(cam_name, cam_data)
        scene.collection.objects.link(cam_obj)

    # Positioned at corner street viewpoint with two-point perspective shift
    cam_obj.location = (32.0, -56.0, 4.2)
    cam_obj.rotation_euler = (math.radians(82.0), 0.0, math.radians(28.0))
    cam_obj.data.lens = 28.0
    cam_obj.data.shift_y = 0.38 # Captures ground canopy and full rooftop pergola
    cam_obj.data.shift_x = -0.02
    cam_obj.data.clip_start = 0.1
    cam_obj.data.clip_end = 500.0

    scene.camera = cam_obj
    print("  Camera Cam_Photo_Match_Hero_v5 positioned for full tower framing.")

    # Save blend file
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print(f"Master Blender file updated: {blend_path}")

    # 7. Render high-res exterior still v005 (1200 x 800)
    scene.render.engine = 'CYCLES'
    if hasattr(scene, 'cycles'):
        scene.cycles.device = 'CPU'
        scene.cycles.samples = 18
        scene.cycles.use_denoising = True

    scene.render.resolution_x = 1200
    scene.render.resolution_y = 800
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = out_render

    print(f"Rendering v005 exterior still to {out_render}...")
    bpy.ops.render.render(write_still=True)
    print("Render v005 complete!")

if __name__ == '__main__':
    calibrate_exterior_v005()
