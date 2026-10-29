"""
Calibration Iteration v006:
- True architectural camera framing: full 67.7m tower from entrance drop-off to rooftop pergola
- Authentic warm sandstone buff walls, rich bronze vertical fins, brilliant white slab fascias
- Vibrant cyan-blue balcony glass and deep reflective architectural window glazing
- Golden hour sunset atmosphere with warm sun highlights and rich shadow depth
"""

import bpy
import math
import os

def calibrate_exterior_v006():
    blend_path = r"C:\Users\manpr\Documents\42 Kalidasa\blender\kalidasa42_animated_v001.blend"
    out_render = r"C:\Users\manpr\Documents\42 Kalidasa\renders\preview\exterior_photo_match_render_v006.png"
    
    print(f"Loading {blend_path} for v006 calibration...")
    bpy.ops.wm.open_mainfile(filepath=blend_path)
    scene = bpy.context.scene

    # 1. Hide placeholder trees/icospheres
    for obj in bpy.data.objects:
        lower_name = obj.name.lower()
        if "tree" in lower_name or "icosphere" in lower_name or "placeholder" in lower_name:
            obj.hide_render = True
            obj.hide_viewport = True

    # 2. Color Management & Controlled Exposure
    if hasattr(scene, 'view_settings'):
        scene.view_settings.view_transform = 'AgX'
        scene.view_settings.look = 'AgX - Medium High Contrast'
        scene.view_settings.exposure = -0.75 # Prevents washed out highlights, enriches warm tones

    # 3. World Sky & Atmosphere
    world = scene.world
    if world and world.node_tree:
        for node in world.node_tree.nodes:
            if node.type == 'BACKGROUND':
                node.inputs["Strength"].default_value = 0.45
            elif node.type == 'TEX_SKY':
                node.sun_elevation = math.radians(18.0)
                node.sun_rotation = math.radians(135.0)
                node.sun_intensity = 0.70
                if hasattr(node, 'turbidity'):
                    node.turbidity = 3.2

    # 4. Sun Key Lamp (Golden Hour Directional Light)
    sun = bpy.data.objects.get("Sun_Daylight_Hero") or bpy.data.objects.get("Sun_GoldenHour")
    if sun:
        sun.data.energy = 1.3
        sun.data.color = (1.0, 0.76, 0.52) # Deep golden sunset amber
        sun.data.angle = math.radians(2.5) # Soft realistic shadows
        sun.rotation_euler = (math.radians(54.0), math.radians(12.0), math.radians(135.0))

    # 5. Precise Architectural Material Calibration
    # A. Façade Walls: Authentic warm sandstone buff
    for mat_name in ["Mat_Facade_Walls", "Mat_Tower_Facade", "Facade_Walls"]:
        mat = bpy.data.materials.get(mat_name)
        if mat and mat.node_tree:
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                bsdf.inputs["Base Color"].default_value = (0.55, 0.42, 0.30, 1.0)
                bsdf.inputs["Roughness"].default_value = 0.80

    # B. Vertical Accent Piers / Mullions: Warm terracotta/bronze
    for mat_name in ["Mat_Vertical_Fins", "Mat_Accent_Piers", "Mat_Bronze_Accents"]:
        mat = bpy.data.materials.get(mat_name)
        if mat and mat.node_tree:
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                bsdf.inputs["Base Color"].default_value = (0.42, 0.28, 0.16, 1.0)
                bsdf.inputs["Roughness"].default_value = 0.60

    # C. Balcony Slab Fascias (Edges): Brilliant White Highlights
    for mat_name in ["Mat_Slab_Fascia", "Mat_Balcony_Edges", "Mat_Slab_Edges"]:
        mat = bpy.data.materials.get(mat_name)
        if mat and mat.node_tree:
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                bsdf.inputs["Base Color"].default_value = (0.95, 0.95, 0.95, 1.0)
                bsdf.inputs["Roughness"].default_value = 0.25

    # D. Balcony Glass: Vibrant Cyan-Blue Architectural Glazing
    mat_glass = bpy.data.materials.get("Mat_Balcony_Glass")
    if mat_glass and mat_glass.node_tree:
        bsdf_g = mat_glass.node_tree.nodes.get("Principled BSDF")
        if bsdf_g:
            bsdf_g.inputs["Base Color"].default_value = (0.01, 0.42, 0.78, 1.0)
            if "Transmission Weight" in bsdf_g.inputs:
                bsdf_g.inputs["Transmission Weight"].default_value = 0.60
            elif "Transmission" in bsdf_g.inputs:
                bsdf_g.inputs["Transmission"].default_value = 0.60
            bsdf_g.inputs["Roughness"].default_value = 0.02
            if "IOR" in bsdf_g.inputs:
                bsdf_g.inputs["IOR"].default_value = 1.48

    # E. Window Glass: Dark Specular Glazing with Crisp Reflections
    for mat_name in ["Mat_Window_Glazing_Reflective", "Mat_Window_Glass"]:
        mat_win = bpy.data.materials.get(mat_name)
        if mat_win and mat_win.node_tree:
            bsdf_w = mat_win.node_tree.nodes.get("Principled BSDF")
            if bsdf_w:
                bsdf_w.inputs["Base Color"].default_value = (0.01, 0.02, 0.04, 1.0)
                bsdf_w.inputs["Roughness"].default_value = 0.03
                bsdf_w.inputs["Metallic"].default_value = 0.35

    # 6. Camera: Perfectly Framed Architectural View
    cam_name = "Cam_Photo_Match_Hero_v6"
    if cam_name in bpy.data.objects:
        cam_obj = bpy.data.objects[cam_name]
    else:
        cam_data = bpy.data.cameras.new(cam_name)
        cam_obj = bpy.data.objects.new(cam_name, cam_data)
        scene.collection.objects.link(cam_obj)

    # Positioned ~78m back at 30-degree street corner with shift lens
    cam_obj.location = (38.0, -66.0, 5.0)
    cam_obj.rotation_euler = (math.radians(80.5), 0.0, math.radians(29.0))
    cam_obj.data.lens = 28.0
    cam_obj.data.shift_y = 0.44 # Perfectly frames entire tower from ground plinth to top pergola
    cam_obj.data.shift_x = -0.03
    cam_obj.data.clip_start = 0.1
    cam_obj.data.clip_end = 500.0

    scene.camera = cam_obj
    print("  Camera Cam_Photo_Match_Hero_v6 positioned with full architectural vertical framing.")

    # Save blend file
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print(f"Master Blender file updated: {blend_path}")

    # 7. Render high-res exterior still v006 (1200 x 800)
    scene.render.engine = 'CYCLES'
    if hasattr(scene, 'cycles'):
        scene.cycles.device = 'CPU'
        scene.cycles.samples = 20
        scene.cycles.use_denoising = True

    scene.render.resolution_x = 1200
    scene.render.resolution_y = 800
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = out_render

    print(f"Rendering v006 exterior still to {out_render}...")
    bpy.ops.render.render(write_still=True)
    print("Render v006 complete!")

if __name__ == '__main__':
    calibrate_exterior_v006()

