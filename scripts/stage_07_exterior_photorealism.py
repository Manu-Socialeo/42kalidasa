"""
Stage 7: Exterior Materials and Photorealism Calibration (Blender portion)
Calibrates PBR shaders (sky-blue glass bands, crisp white slab edges, warm beige piers),
matches daylight sun angle, and renders the exact matching viewpoint.
"""

import bpy
import os
import sys

def calibrate_exterior():
    workspace = r"C:\Users\manpr\Documents\42 Kalidasa"
    blend_path = os.path.join(workspace, "blender", "kalidasa42_animated_v001.blend")
    render_out = os.path.join(workspace, "renders", "preview", "exterior_photo_match_render.png")
    
    bpy.ops.wm.open_mainfile(filepath=blend_path)
    scene = bpy.context.scene
    
    print("Calibrating materials to match approved building photograph...")
    
    # 1. Mat_Facade_Tinted_Glass -> Vibrant Sky-Blue Balcony Bands
    if "Mat_Facade_Tinted_Glass" in bpy.data.materials:
        mat_glass = bpy.data.materials["Mat_Facade_Tinted_Glass"]
        if mat_glass.node_tree:
            bsdf = mat_glass.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                bsdf.inputs["Base Color"].default_value = (0.10, 0.52, 0.86, 0.45)
                bsdf.inputs["Roughness"].default_value = 0.03
                bsdf.inputs["Metallic"].default_value = 0.10
                if "Transmission Weight" in bsdf.inputs:
                    bsdf.inputs["Transmission Weight"].default_value = 0.85
                elif "Transmission" in bsdf.inputs:
                    bsdf.inputs["Transmission"].default_value = 0.85
                if "IOR" in bsdf.inputs:
                    bsdf.inputs["IOR"].default_value = 1.52
                    
    # 2. Mat_Slab_Fascia -> Crisp White Slab Edges
    if "Mat_Slab_Fascia" in bpy.data.materials:
        mat_slab = bpy.data.materials["Mat_Slab_Fascia"]
        if mat_slab.node_tree:
            bsdf = mat_slab.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                bsdf.inputs["Base Color"].default_value = (0.98, 0.98, 0.98, 1.0)
                bsdf.inputs["Roughness"].default_value = 0.22
                bsdf.inputs["Metallic"].default_value = 0.02
                
    # 3. Mat_Fluted_Timber_Accent -> Warm Sandstone/Beige Vertical Accent Piers
    if "Mat_Fluted_Timber_Accent" in bpy.data.materials:
        mat_accent = bpy.data.materials["Mat_Fluted_Timber_Accent"]
        if mat_accent.node_tree:
            bsdf = mat_accent.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                bsdf.inputs["Base Color"].default_value = (0.74, 0.52, 0.36, 1.0)
                bsdf.inputs["Roughness"].default_value = 0.35
                bsdf.inputs["Metallic"].default_value = 0.05
                
    # 4. Mat_Precast_Concrete -> Off-White Architectural Concrete
    if "Mat_Precast_Concrete" in bpy.data.materials:
        mat_conc = bpy.data.materials["Mat_Precast_Concrete"]
        if mat_conc.node_tree:
            bsdf = mat_conc.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                bsdf.inputs["Base Color"].default_value = (0.86, 0.84, 0.81, 1.0)
                bsdf.inputs["Roughness"].default_value = 0.45
                
    # 5. Sun & Daylight Environment Calibration
    sun = bpy.data.lights.get("Sun_Daylight")
    if sun:
        sun.energy = 4.2
        sun.color = (1.0, 0.95, 0.88)
        
    # 6. Configure Camera matching exact perspective of reference photo
    cam_name = "Cam_Photo_Match_Hero"
    if cam_name in bpy.data.objects:
        cam_obj = bpy.data.objects[cam_name]
    else:
        cam_data = bpy.data.cameras.new(cam_name + "_Data")
        cam_obj = bpy.data.objects.new(cam_name, cam_data)
        scene.collection.objects.link(cam_obj)
        
    cam_obj.location = (25.0, -68.0, 8.5)
    cam_obj.data.lens = 26.0
    cam_obj.data.clip_end = 2000.0
    
    target_name = "Target_Photo_Match"
    if target_name in bpy.data.objects:
        target_obj = bpy.data.objects[target_name]
    else:
        target_obj = bpy.data.objects.new(target_name, None)
        scene.collection.objects.link(target_obj)
    target_obj.location = (4.0, 0.0, 32.0)
    
    track = None
    for c in cam_obj.constraints:
        if c.type == 'TRACK_TO':
            track = c
            break
    if track is None:
        track = cam_obj.constraints.new(type='TRACK_TO')
    track.target = target_obj
    track.track_axis = 'TRACK_NEGATIVE_Z'
    track.up_axis = 'UP_Y'
    
    scene.camera = cam_obj
    
    # Save calibrated master
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print(f"Master blend updated with calibrated exterior shaders: {blend_path}")
    
    # 7. Render high-res exterior still (1200 x 800)
    scene.render.engine = 'CYCLES'
    if hasattr(scene, 'cycles'):
        scene.cycles.device = 'CPU'
        scene.cycles.samples = 12
        scene.cycles.use_denoising = True
        
    scene.render.resolution_x = 1200
    scene.render.resolution_y = 800
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = render_out
    
    print(f"Rendering calibrated exterior still to: {render_out}...")
    bpy.ops.render.render(write_still=True)
    print("Blender render complete.")

if __name__ == "__main__":
    calibrate_exterior()
