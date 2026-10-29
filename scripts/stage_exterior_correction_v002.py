"""
Exterior Correction & Visual Verification v002
Calibrates geometry materials, daylight sun direction, and camera framing
to match the approved building photograph.
"""

import bpy
import os
import math

def apply_exterior_corrections():
    workspace = r"C:\Users\manpr\Documents\42 Kalidasa"
    blend_path = os.path.join(workspace, "blender", "kalidasa42_animated_v001.blend")
    render_out = os.path.join(workspace, "renders", "preview", "exterior_photo_match_render_v002.png")
    
    print(f"Opening {blend_path}...")
    bpy.ops.wm.open_mainfile(filepath=blend_path)
    scene = bpy.context.scene
    
    print("Applying evidence-based material corrections...")
    
    # 1. Mat_Precast_Concrete -> Warm Sandstone / Buff Beige (dominant facade color in photo)
    if "Mat_Precast_Concrete" in bpy.data.materials:
        mat = bpy.data.materials["Mat_Precast_Concrete"]
        if mat.node_tree:
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                # RGB values matching Color 2 & 5 from photo K-Means (165, 142, 118 / 255 -> ~0.65, 0.56, 0.46)
                bsdf.inputs["Base Color"].default_value = (0.68, 0.58, 0.47, 1.0)
                bsdf.inputs["Roughness"].default_value = 0.42
                bsdf.inputs["Metallic"].default_value = 0.02
                print("  Updated Mat_Precast_Concrete to warm sandstone beige.")
                
    # 2. Mat_Fluted_Timber_Accent -> Warm Terracotta / Sandstone Accent Piers
    if "Mat_Fluted_Timber_Accent" in bpy.data.materials:
        mat = bpy.data.materials["Mat_Fluted_Timber_Accent"]
        if mat.node_tree:
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                bsdf.inputs["Base Color"].default_value = (0.60, 0.44, 0.30, 1.0)
                bsdf.inputs["Roughness"].default_value = 0.35
                bsdf.inputs["Metallic"].default_value = 0.05
                print("  Updated Mat_Fluted_Timber_Accent.")

    # 3. Mat_Slab_Fascia -> Crisp Brilliant White Horizontal Bands
    if "Mat_Slab_Fascia" in bpy.data.materials:
        mat = bpy.data.materials["Mat_Slab_Fascia"]
        if mat.node_tree:
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                bsdf.inputs["Base Color"].default_value = (0.98, 0.98, 0.98, 1.0)
                bsdf.inputs["Roughness"].default_value = 0.18
                bsdf.inputs["Metallic"].default_value = 0.0
                print("  Updated Mat_Slab_Fascia to brilliant white.")

    # 4. Mat_Facade_Tinted_Glass -> Vibrant Sky-Blue / Cyan Balcony Glass Bands
    # Crucial fix: Transmission tuned to 0.50 so vibrant sky-blue pigment has solid presence
    if "Mat_Facade_Tinted_Glass" in bpy.data.materials:
        mat = bpy.data.materials["Mat_Facade_Tinted_Glass"]
        if mat.node_tree:
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                # Vibrant cyan-blue matching photo balcony reflections
                bsdf.inputs["Base Color"].default_value = (0.06, 0.50, 0.85, 1.0)
                bsdf.inputs["Roughness"].default_value = 0.02
                bsdf.inputs["Metallic"].default_value = 0.05
                if "Transmission Weight" in bsdf.inputs:
                    bsdf.inputs["Transmission Weight"].default_value = 0.50
                elif "Transmission" in bsdf.inputs:
                    bsdf.inputs["Transmission"].default_value = 0.50
                if "IOR" in bsdf.inputs:
                    bsdf.inputs["IOR"].default_value = 1.52
                print("  Updated Mat_Facade_Tinted_Glass to vibrant reflective sky-blue.")

    # 5. Mat_Champagne_Bronze -> Deep Architectural Bronze / Charcoal Frames
    if "Mat_Champagne_Bronze" in bpy.data.materials:
        mat = bpy.data.materials["Mat_Champagne_Bronze"]
        if mat.node_tree:
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                # Dark charcoal bronze for crisp window and balustrade contrast
                bsdf.inputs["Base Color"].default_value = (0.12, 0.10, 0.09, 1.0)
                bsdf.inputs["Roughness"].default_value = 0.28
                bsdf.inputs["Metallic"].default_value = 0.80
                print("  Updated Mat_Champagne_Bronze to deep architectural bronze.")

    # 6. Lighting: Sun Direction matching photo (sunlit from front-left / South-West)
    sun = bpy.data.objects.get("Sun_Golden_Hour") or bpy.data.objects.get("Sun_Daylight")
    if not sun:
        sun_data = bpy.data.lights.new("Sun_Photoreal", type='SUN')
        sun = bpy.data.objects.new("Sun_Photoreal", sun_data)
        scene.collection.objects.link(sun)
    
    sun.location = (-45.0, -70.0, 65.0)
    sun.rotation_euler = (math.radians(48.0), math.radians(12.0), math.radians(-32.0))
    sun.data.energy = 4.8
    sun.data.color = (1.0, 0.96, 0.90)
    print("  Sun light calibrated to front-left sunlit angle.")

    # 7. World Environment Sky
    if scene.world and scene.world.node_tree:
        bg = scene.world.node_tree.nodes.get("Background")
        if bg:
            # Soft daylight blue ambient fill matching photo sky
            bg.inputs["Color"].default_value = (0.55, 0.68, 0.82, 1.0)
            bg.inputs["Strength"].default_value = 1.1
            print("  World environment sky updated to soft daylight blue fill.")

    # 8. Camera Framing: Cam_Photo_Match_Hero_v2
    cam_name = "Cam_Photo_Match_Hero_v2"
    if cam_name in bpy.data.objects:
        cam_obj = bpy.data.objects[cam_name]
    else:
        cam_data = bpy.data.cameras.new(cam_name + "_Data")
        cam_obj = bpy.data.objects.new(cam_name, cam_data)
        scene.collection.objects.link(cam_obj)
        
    # Closer distance so building fills the frame vertically & horizontally
    cam_obj.location = (18.5, -46.0, 6.5)
    cam_obj.data.lens = 24.0
    cam_obj.data.shift_y = 0.16  # Architectural vertical rise
    cam_obj.data.shift_x = -0.04
    cam_obj.data.clip_end = 2000.0
    
    target_name = "Target_Photo_Match_v2"
    if target_name in bpy.data.objects:
        target_obj = bpy.data.objects[target_name]
    else:
        target_obj = bpy.data.objects.new(target_name, None)
        scene.collection.objects.link(target_obj)
    target_obj.location = (8.0, -2.0, 30.0)
    
    # Configure Track To constraint
    cam_obj.constraints.clear()
    track = cam_obj.constraints.new(type='TRACK_TO')
    track.target = target_obj
    track.track_axis = 'TRACK_NEGATIVE_Z'
    track.up_axis = 'UP_Y'
    
    scene.camera = cam_obj
    print(f"  Camera {cam_name} configured at {cam_obj.location} tracking {target_obj.location}.")

    # Save updated blend file
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print(f"Master Blender file saved: {blend_path}")

    # 9. Render new exterior still
    scene.render.engine = 'CYCLES'
    if hasattr(scene, 'cycles'):
        scene.cycles.device = 'CPU'
        scene.cycles.samples = 14
        scene.cycles.use_denoising = True
        
    scene.render.resolution_x = 1200
    scene.render.resolution_y = 800
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = render_out
    
    print(f"Rendering v002 exterior still to {render_out}...")
    bpy.ops.render.render(write_still=True)
    print(f"Render complete: {render_out}")

if __name__ == "__main__":
    apply_exterior_corrections()

