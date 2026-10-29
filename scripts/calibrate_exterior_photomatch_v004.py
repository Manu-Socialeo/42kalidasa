"""
Calibration Iteration v004:
- Multiple Scattering Physical Sky Model (Golden Hour Sunset Dusk)
- Architectural Two-Point Perspective Camera with vertical lens shift
- Warm interior apartment and balcony ceiling illumination
- Warm architectural wood Pergola materials
"""

import bpy
import math
import os

def calibrate_exterior_v004():
    blend_path = r"C:\Users\manpr\Documents\42 Kalidasa\blender\kalidasa42_animated_v001.blend"
    out_render = r"C:\Users\manpr\Documents\42 Kalidasa\renders\preview\exterior_photo_match_render_v004.png"
    
    print(f"Loading {blend_path} for v004 calibration...")
    bpy.ops.wm.open_mainfile(filepath=blend_path)
    scene = bpy.context.scene

    # 1. World: Multiple Scattering Physical Golden-Hour Sky
    world = scene.world
    if not world:
        world = bpy.data.worlds.new("World_GoldenHour")
        scene.world = world
    world.use_nodes = True
    tree = world.node_tree
    tree.nodes.clear()

    node_out = tree.nodes.new(type="ShaderNodeOutputWorld")
    node_bg = tree.nodes.new(type="ShaderNodeBackground")
    node_sky = tree.nodes.new(type="ShaderNodeTexSky")
    
    node_sky.sky_type = 'MULTIPLE_SCATTERING'
    node_sky.sun_elevation = math.radians(14.0) # Golden hour low sun
    node_sky.sun_rotation = math.radians(138.0)  # Front-left illumination
    node_sky.sun_disc = True
    node_sky.sun_intensity = 0.90
    if hasattr(node_sky, 'turbidity'):
        node_sky.turbidity = 2.8 # Warm dusk scatter
    if hasattr(node_sky, 'ground_albedo'):
        node_sky.ground_albedo = 0.2
    
    node_bg.inputs["Strength"].default_value = 0.95
    tree.links.new(node_sky.outputs["Color"], node_bg.inputs["Color"])
    tree.links.new(node_bg.outputs["Background"], node_out.inputs["Surface"])
    print("  World configured with Multiple Scattering Golden-Hour Sky.")

    # 2. Main Key Sun Lamp (Warm 3600K Sunset Sun)
    sun = bpy.data.objects.get("Sun_Daylight_Hero")
    if not sun:
        sun_data = bpy.data.lights.new(name="Sun_GoldenHour", type='SUN')
        sun = bpy.data.objects.new(name="Sun_GoldenHour", object_data=sun_data)
        scene.collection.objects.link(sun)
    else:
        sun_data = sun.data
    
    sun.rotation_euler = (math.radians(52.0), math.radians(12.0), math.radians(135.0))
    sun_data.energy = 4.2
    # Warm golden sunlight (Hex #FFDCB0 -> sRGB)
    sun_data.color = (1.0, 0.86, 0.69)
    sun_data.angle = math.radians(1.2) # Soft shadow edges
    print("  Warm golden sunlight calibrated.")

    # 3. Warm Interior Living & Balcony Illumination
    mat_glow_name = "Mat_Warm_Interior_Glow"
    if mat_glow_name in bpy.data.materials:
        mat_glow = bpy.data.materials[mat_glow_name]
    else:
        mat_glow = bpy.data.materials.new(mat_glow_name)
        mat_glow.use_nodes = True
    
    if mat_glow.node_tree:
        gnodes = mat_glow.node_tree.nodes
        gnodes.clear()
        g_out = gnodes.new(type="ShaderNodeOutputMaterial")
        g_emit = gnodes.new(type="ShaderNodeEmission")
        g_emit.inputs["Color"].default_value = (1.0, 0.78, 0.52, 1.0) # Warm halogen amber
        g_emit.inputs["Strength"].default_value = 2.5
        mat_glow.node_tree.links.new(g_emit.outputs["Emission"], g_out.inputs["Surface"])

    # Add interior point lights behind glazing to create depth
    for f in range(2, 8):
        l_name = f"Light_Interior_Floor_{f:02d}"
        if l_name not in bpy.data.objects:
            ldata = bpy.data.lights.new(name=l_name, type='POINT')
            ldata.color = (1.0, 0.82, 0.58)
            ldata.energy = 350.0
            ldata.shadow_soft_size = 1.2
            lobj = bpy.data.objects.new(name=l_name, object_data=ldata)
            lobj.location = (11.0, -8.0, 4.5 + (f - 1) * 3.3)
            scene.collection.objects.link(lobj)
    print("  Added warm interior apartment lighting.")

    # 4. Pergola Wood Louver Material
    mat_pergola_name = "Mat_Pergola_Timber"
    if mat_pergola_name in bpy.data.materials:
        mat_perg = bpy.data.materials[mat_pergola_name]
    else:
        mat_perg = bpy.data.materials.new(mat_pergola_name)
        mat_perg.use_nodes = True
    
    if mat_perg.node_tree:
        bsdf_p = mat_perg.node_tree.nodes.get("Principled BSDF")
        if bsdf_p:
            bsdf_p.inputs["Base Color"].default_value = (0.35, 0.22, 0.12, 1.0) # Rich architectural teak
            bsdf_p.inputs["Roughness"].default_value = 0.55

    for obj in bpy.data.objects:
        if "Pergola" in obj.name or "Crown" in obj.name:
            if obj.type == 'MESH':
                obj.data.materials.clear()
                obj.data.materials.append(mat_perg)

    # 5. Camera: Cam_Photo_Match_Hero_v4
    # Architectural two-point perspective matching the actual street view
    cam_name = "Cam_Photo_Match_Hero_v4"
    if cam_name in bpy.data.objects:
        cam_obj = bpy.data.objects[cam_name]
    else:
        cam_data = bpy.data.cameras.new(cam_name)
        cam_obj = bpy.data.objects.new(cam_name, cam_data)
        scene.collection.objects.link(cam_obj)
    
    # Camera position: situated across the street corner, with architectural vertical shift
    cam_obj.location = (25.5, -46.0, 3.8)
    cam_obj.rotation_euler = (math.radians(78.5), 0.0, math.radians(28.5))
    cam_obj.data.lens = 26.0 # Architectural wide angle
    cam_obj.data.shift_y = 0.32 # Vertical shift reveals entire tower up to pergola
    cam_obj.data.shift_x = -0.04
    cam_obj.data.clip_start = 0.1
    cam_obj.data.clip_end = 500.0
    
    scene.camera = cam_obj
    print("  Camera Cam_Photo_Match_Hero_v4 calibrated with architectural shift.")

    # Save master blend file
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print(f"Master Blender file updated: {blend_path}")

    # 6. Render high-res exterior still v004 (1200 x 800)
    scene.render.engine = 'CYCLES'
    if hasattr(scene, 'cycles'):
        scene.cycles.device = 'CPU'
        scene.cycles.samples = 16
        scene.cycles.use_denoising = True
        
    scene.render.resolution_x = 1200
    scene.render.resolution_y = 800
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = out_render
    
    print(f"Rendering v004 exterior photo-match still to {out_render}...")
    bpy.ops.render.render(write_still=True)
    print("Render v004 completed successfully!")

if __name__ == '__main__':
    calibrate_exterior_v004()
