"""
Exterior Correction & Visual Verification Iteration v003
Applies deep architectural contrast, dedicated window glazing material,
crisp slab fascia highlights, and calibrated sun/shadow ratio.
"""

import bpy
import os
import math

def apply_exterior_corrections_v003():
    workspace = r"C:\Users\manpr\Documents\42 Kalidasa"
    blend_path = os.path.join(workspace, "blender", "kalidasa42_animated_v001.blend")
    render_out = os.path.join(workspace, "renders", "preview", "exterior_photo_match_render_v003.png")
    
    print(f"Opening {blend_path} for iteration v003...")
    bpy.ops.wm.open_mainfile(filepath=blend_path)
    scene = bpy.context.scene
    
    # 1. Dedicated Window Glazing Material: Mat_Window_Glazing_Reflective
    # Dark reflective architectural glass matching photo window reveals
    mat_win_name = "Mat_Window_Glazing_Reflective"
    if mat_win_name in bpy.data.materials:
        mat_win = bpy.data.materials[mat_win_name]
    else:
        mat_win = bpy.data.materials.new(mat_win_name)
        mat_win.use_nodes = True
        
    if mat_win.node_tree:
        bsdf = mat_win.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            # Deep reflective charcoal with crisp sky reflection
            bsdf.inputs["Base Color"].default_value = (0.02, 0.03, 0.05, 1.0)
            bsdf.inputs["Roughness"].default_value = 0.02
            bsdf.inputs["Metallic"].default_value = 0.20
            if "Transmission Weight" in bsdf.inputs:
                bsdf.inputs["Transmission Weight"].default_value = 0.15
            elif "Transmission" in bsdf.inputs:
                bsdf.inputs["Transmission"].default_value = 0.15
            if "IOR" in bsdf.inputs:
                bsdf.inputs["IOR"].default_value = 1.55
                
    # Assign Mat_Window_Glazing_Reflective to all window glass objects
    win_glass_count = 0
    for obj in bpy.data.objects:
        if obj.type == 'MESH' and ("Win_" in obj.name or "Window" in obj.name) and "Glass" in obj.name:
            if obj.data.materials:
                obj.data.materials[0] = mat_win
            else:
                obj.data.materials.append(mat_win)
            win_glass_count += 1
    print(f"  Assigned dark reflective window glazing to {win_glass_count} window panes.")

    # 2. Refine Balcony Glass: Mat_Facade_Tinted_Glass
    # Pure vibrant cyan/sky-blue laminated glass on curved balustrades
    if "Mat_Facade_Tinted_Glass" in bpy.data.materials:
        mat_balc = bpy.data.materials["Mat_Facade_Tinted_Glass"]
        if mat_balc.node_tree:
            bsdf = mat_balc.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                # Vibrant sky-blue matching photo balcony reflections
                bsdf.inputs["Base Color"].default_value = (0.05, 0.52, 0.88, 1.0)
                bsdf.inputs["Roughness"].default_value = 0.015
                bsdf.inputs["Metallic"].default_value = 0.08
                if "Transmission Weight" in bsdf.inputs:
                    bsdf.inputs["Transmission Weight"].default_value = 0.52
                elif "Transmission" in bsdf.inputs:
                    bsdf.inputs["Transmission"].default_value = 0.52
                if "IOR" in bsdf.inputs:
                    bsdf.inputs["IOR"].default_value = 1.52

    # 3. Refine Warm Sandstone Walls: Mat_Precast_Concrete
    if "Mat_Precast_Concrete" in bpy.data.materials:
        mat_conc = bpy.data.materials["Mat_Precast_Concrete"]
        if mat_conc.node_tree:
            bsdf = mat_conc.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                # Rich buff sandstone beige
                bsdf.inputs["Base Color"].default_value = (0.70, 0.58, 0.45, 1.0)
                bsdf.inputs["Roughness"].default_value = 0.40
                bsdf.inputs["Metallic"].default_value = 0.02

    # 4. Refine Crisp White Slab Fascia: Mat_Slab_Fascia
    if "Mat_Slab_Fascia" in bpy.data.materials:
        mat_slab = bpy.data.materials["Mat_Slab_Fascia"]
        if mat_slab.node_tree:
            bsdf = mat_slab.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                bsdf.inputs["Base Color"].default_value = (0.98, 0.98, 0.98, 1.0)
                bsdf.inputs["Roughness"].default_value = 0.15
                bsdf.inputs["Metallic"].default_value = 0.0

    # 5. Lighting: High-contrast architectural sunlight + subtle sky ambient
    sun = bpy.data.objects.get("Sun_Photoreal") or bpy.data.objects.get("Sun_Golden_Hour") or bpy.data.objects.get("Sun_Daylight")
    if sun:
        sun.location = (-42.0, -68.0, 62.0)
        sun.rotation_euler = (math.radians(50.0), math.radians(10.0), math.radians(-30.0))
        sun.data.energy = 5.6
        sun.data.color = (1.0, 0.96, 0.89)
        sun.data.angle = math.radians(1.5)  # Soft realistic sun shadow penumbra

    # Sky World: Reduce flat fill to allow deep shadows under slabs & reveals
    if scene.world and scene.world.node_tree:
        bg = scene.world.node_tree.nodes.get("Background")
        if bg:
            bg.inputs["Color"].default_value = (0.50, 0.65, 0.82, 1.0)
            bg.inputs["Strength"].default_value = 0.45
            print("  Calibrated world ambient strength to 0.45 for rich shadow depth.")

    # 6. Camera: Cam_Photo_Match_Hero_v2
    cam_obj = bpy.data.objects.get("Cam_Photo_Match_Hero_v2")
    if cam_obj:
        cam_obj.location = (17.8, -44.5, 6.2)
        cam_obj.data.lens = 23.5
        cam_obj.data.shift_y = 0.17
        cam_obj.data.shift_x = -0.03
        
        target_obj = bpy.data.objects.get("Target_Photo_Match_v2")
        if target_obj:
            target_obj.location = (8.5, -2.5, 31.0)
            
    # Save updated blend file
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print(f"Master Blender file saved: {blend_path}")

    # 7. Render high-res exterior still v003 (1200 x 800)
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
    
    print(f"Rendering v003 exterior still to {render_out}...")
    bpy.ops.render.render(write_still=True)
    print(f"Render v003 complete: {render_out}")

if __name__ == "__main__":
    apply_exterior_corrections_v003()

