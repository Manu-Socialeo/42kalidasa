"""
Kalidasa 42 — Representative Apartment Interior
Stage 7: Models the documented typical 4BHK luxury residence (Floor 08, 368 m² net)
from sanction drawing DWG/NS/5692 Sheet 05, with internal partition walls, doors,
windows, living/dining staging, and exterior-to-interior camera transition.
"""

import bpy
import bmesh
import math
import os
import sys
import traceback

# ---------------------------------------------------------------------------
# ARCHITECTURAL CONSTANTS (Floor 08: Z = 27.60m FFL, Height = 3.30m)
# ---------------------------------------------------------------------------
Z_FFL = 27.60
CEILING_HEIGHT = 3.05 # Clear ceiling height beneath 0.25m slab
SLAB_THICKNESS = 0.25
WALL_THICKNESS = 0.20 # 200mm internal masonry/drywall partitions

BUILDING_LENGTH = 36.397
BUILDING_WIDTH = 16.000
BALCONY_CANTILEVER = 4.80

LOG_FILE = r"C:\Users\manpr\Documents\42 Kalidasa\scripts\interior_build.log"

def log(msg):
    print(msg, flush=True)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(str(msg) + "\n")
    except Exception:
        pass

def get_or_create_col(name, parent=None):
    if name in bpy.data.collections:
        col = bpy.data.collections[name]
    else:
        col = bpy.data.collections.new(name)
        if parent is None:
            bpy.context.scene.collection.children.link(col)
        else:
            parent.children.link(col)
    return col

def get_or_create_mat(name, color_rgba, roughness=0.4, metallic=0.0, emission_rgba=None, emission_strength=0.0):
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    if hasattr(mat, "node_tree") and mat.node_tree:
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            if "Base Color" in bsdf.inputs:
                bsdf.inputs['Base Color'].default_value = color_rgba
            if "Roughness" in bsdf.inputs:
                bsdf.inputs['Roughness'].default_value = roughness
            if "Metallic" in bsdf.inputs:
                bsdf.inputs['Metallic'].default_value = metallic
            if emission_rgba and "Emission Color" in bsdf.inputs:
                bsdf.inputs['Emission Color'].default_value = emission_rgba
                if "Emission Strength" in bsdf.inputs:
                    bsdf.inputs['Emission Strength'].default_value = emission_strength
    return mat

def create_cube(name, location, dimensions, material, collection):
    mesh = bpy.data.meshes.new(name + "_Mesh")
    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bm.to_mesh(mesh)
    bm.free()
    obj.location = location
    obj.scale = dimensions
    if material:
        obj.data.materials.append(material)
    return obj

def build_kalidasa42_interior():
    try:
        if os.path.exists(LOG_FILE):
            os.remove(LOG_FILE)
    except Exception:
        pass

    log("=== STARTING KALIDASA 42 REPRESENTATIVE INTERIOR (FLOOR 08) ===")
    
    try:
        facade_blend = r"C:\Users\manpr\Documents\42 Kalidasa\blender\kalidasa42_facade_v001.blend"
        if os.path.exists(facade_blend):
            log(f"Loading facade blend: {facade_blend}")
            bpy.ops.wm.open_mainfile(filepath=facade_blend)
        else:
            log("Warning: Facade blend not found, creating clean scene.")
            bpy.ops.wm.read_factory_settings(use_empty=True)

        scene = bpy.context.scene
        scene.unit_settings.system = 'METRIC'
        scene.unit_settings.scale_length = 1.0
        scene.unit_settings.length_unit = 'METERS'

        # Ensure World exists
        if scene.world is None:
            scene.world = bpy.data.worlds.new("World")
        scene.world.use_nodes = True
        bg = scene.world.node_tree.nodes.get("Background")
        if bg:
            bg.inputs['Color'].default_value = (0.75, 0.85, 0.98, 1.0)
            bg.inputs['Strength'].default_value = 1.2

        log("Creating interior materials...")
        mat_marble = get_or_create_mat("Mat_Italian_Statuario_Marble", (0.93, 0.92, 0.90, 1.0), roughness=0.18, metallic=0.05)
        mat_int_wall = get_or_create_mat("Mat_Interior_Plaster_Neutral", (0.88, 0.86, 0.83, 1.0), roughness=0.60)
        mat_feature_wall = get_or_create_mat("Mat_Feature_Timber_Paneling", (0.50, 0.32, 0.20, 1.0), roughness=0.35)
        mat_ceiling = get_or_create_mat("Mat_Ceiling_Gypsum", (0.95, 0.95, 0.95, 1.0), roughness=0.80)
        mat_fabric_sofa = get_or_create_mat("Mat_Sofa_Boucle_Fabric", (0.82, 0.80, 0.76, 1.0), roughness=0.75)
        mat_timber_table = get_or_create_mat("Mat_Smoked_Oak_Table", (0.22, 0.16, 0.12, 1.0), roughness=0.30)
        mat_chair_cushion = get_or_create_mat("Mat_Dining_Chair_Cushion", (0.35, 0.32, 0.30, 1.0), roughness=0.55)
        mat_warm_interior_light = get_or_create_mat("Mat_Warm_Downlight_Emission", (1.0, 0.92, 0.78, 1.0), roughness=0.9, emission_rgba=(1.0, 0.88, 0.65, 1.0), emission_strength=8.0)
        mat_brass = get_or_create_mat("Mat_Brushed_Brass_Accents", (0.75, 0.60, 0.32, 1.0), roughness=0.25, metallic=0.85)
        mat_bronze = get_or_create_mat("Mat_Champagne_Bronze", (0.24, 0.21, 0.19, 1.0), roughness=0.25, metallic=0.80)

        # Collections
        col_interior = get_or_create_col("09_Apartment_Interior_L08")
        col_furniture = get_or_create_col("10_Living_Dining_Furniture", parent=col_interior)
        col_int_lighting = get_or_create_col("11_Interior_Lighting", parent=col_interior)

        log("Building floor slab finishes & ceiling...")
        create_cube("Floor_08_Marble_Flooring", (0, 0, Z_FFL + 0.01), (BUILDING_LENGTH - 0.3, BUILDING_WIDTH - 0.3, 0.02), mat_marble, col_interior)
        create_cube("Floor_08_False_Ceiling", (0, 0, Z_FFL + CEILING_HEIGHT), (BUILDING_LENGTH - 0.3, BUILDING_WIDTH - 0.3, 0.08), mat_ceiling, col_interior)

        w_z = Z_FFL + CEILING_HEIGHT / 2.0
        w_h = CEILING_HEIGHT

        log("Building internal partition walls (DWG/NS/5692 Sheet 05)...")
        # (A) Grand Living & Dining Zone (8.50m x 6.20m, South-East corner)
        create_cube("Wall_Living_West_Foyer", (BUILDING_LENGTH/2 - 8.50, -BUILDING_WIDTH/2 + 3.10, w_z), (WALL_THICKNESS, 6.20, w_h), mat_int_wall, col_interior)
        create_cube("Wall_Living_North_Feature", (BUILDING_LENGTH/2 - 4.25, -BUILDING_WIDTH/2 + 6.20, w_z), (8.50, WALL_THICKNESS, w_h), mat_feature_wall, col_interior)

        # (B) Family Lounge / Informal Living (4.00m x 5.80m)
        create_cube("Wall_Informal_Living_West", (BUILDING_LENGTH/2 - 12.50, -BUILDING_WIDTH/2 + 2.90, w_z), (WALL_THICKNESS, 5.80, w_h), mat_int_wall, col_interior)

        # (C) Entrance Foyer (1.50m x 2.40m) & Private Lift Lobby (5.60m x 2.50m)
        create_cube("Wall_Foyer_North", (BUILDING_LENGTH/2 - 10.0, -BUILDING_WIDTH/2 + 2.40, w_z), (3.0, WALL_THICKNESS, w_h), mat_int_wall, col_interior)
        
        # (D) Kitchen (3.60m x 6.40m) & Utility (4.40m x 3.90m)
        create_cube("Wall_Kitchen_Divider", (-2.0, -BUILDING_WIDTH/2 + 3.20, w_z), (WALL_THICKNESS, 6.40, w_h), mat_int_wall, col_interior)
        create_cube("Wall_Kitchen_North", (-3.80, -BUILDING_WIDTH/2 + 6.40, w_z), (3.60, WALL_THICKNESS, w_h), mat_int_wall, col_interior)

        # (E) Master Bedroom Suite (5.00m x 4.00m, North-East flank)
        create_cube("Wall_MBR_South_Corridor", (BUILDING_LENGTH/2 - 2.50, BUILDING_WIDTH/2 - 4.00, w_z), (5.00, WALL_THICKNESS, w_h), mat_int_wall, col_interior)
        create_cube("Wall_MBR_West_WIW", (BUILDING_LENGTH/2 - 5.00, BUILDING_WIDTH/2 - 2.00, w_z), (WALL_THICKNESS, 4.00, w_h), mat_int_wall, col_interior)
        create_cube("Wall_Master_Bath_Divider", (BUILDING_LENGTH/2 - 2.00, BUILDING_WIDTH/2 - 1.80, w_z), (4.00, WALL_THICKNESS, w_h), mat_int_wall, col_interior)

        # (F) Bedrooms 2, 3, 4 partitions (Western wing)
        create_cube("Wall_Bedrooms_Central_Corridor", (-10.0, 0.0, w_z), (16.0, WALL_THICKNESS, w_h), mat_int_wall, col_interior)
        create_cube("Wall_Bed2_Divider", (-6.0, BUILDING_WIDTH/4, w_z), (WALL_THICKNESS, BUILDING_WIDTH/2, w_h), mat_int_wall, col_interior)
        create_cube("Wall_Bed3_Divider", (-11.0, BUILDING_WIDTH/4, w_z), (WALL_THICKNESS, BUILDING_WIDTH/2, w_h), mat_int_wall, col_interior)

        log("Staging living & dining furniture...")
        sofa_x = BUILDING_LENGTH/2 - 4.5
        sofa_y = -BUILDING_WIDTH/2 + 3.2
        create_cube("Living_Sectional_Sofa_Base", (sofa_x, sofa_y, Z_FFL + 0.22), (3.6, 1.1, 0.44), mat_fabric_sofa, col_furniture)
        create_cube("Living_Sectional_Sofa_L_Wing", (sofa_x - 1.25, sofa_y - 0.75, Z_FFL + 0.22), (1.1, 1.5, 0.44), mat_fabric_sofa, col_furniture)
        create_cube("Living_Sectional_Sofa_Backrest", (sofa_x, sofa_y + 0.45, Z_FFL + 0.50), (3.6, 0.25, 0.40), mat_fabric_sofa, col_furniture)

        create_cube("Living_Coffee_Table", (sofa_x + 0.2, sofa_y - 0.8, Z_FFL + 0.20), (1.4, 0.8, 0.40), mat_marble, col_furniture)
        create_cube("Living_Media_Console", (BUILDING_LENGTH/2 - 4.25, -BUILDING_WIDTH/2 + 6.00, Z_FFL + 0.25), (4.0, 0.45, 0.50), mat_timber_table, col_furniture)
        create_cube("Living_OLED_Screen", (BUILDING_LENGTH/2 - 4.25, -BUILDING_WIDTH/2 + 6.08, Z_FFL + 1.40), (2.2, 0.05, 1.25), mat_bronze, col_furniture)

        dining_x = BUILDING_LENGTH/2 - 2.8
        dining_y = -BUILDING_WIDTH/2 + 1.8
        create_cube("Dining_Table_Top", (dining_x, dining_y, Z_FFL + 0.75), (2.6, 1.1, 0.06), mat_timber_table, col_furniture)
        create_cube("Dining_Table_Base_L", (dining_x - 0.9, dining_y, Z_FFL + 0.36), (0.15, 0.7, 0.70), mat_brass, col_furniture)
        create_cube("Dining_Table_Base_R", (dining_x + 0.9, dining_y, Z_FFL + 0.36), (0.15, 0.7, 0.70), mat_brass, col_furniture)

        for c_i in range(4):
            cx = dining_x - 0.9 + (c_i * 0.6)
            create_cube(f"Chair_S_{c_i}", (cx, dining_y - 0.75, Z_FFL + 0.25), (0.45, 0.45, 0.50), mat_chair_cushion, col_furniture)
            create_cube(f"Chair_N_{c_i}", (cx, dining_y + 0.75, Z_FFL + 0.25), (0.45, 0.45, 0.50), mat_chair_cushion, col_furniture)

        balc_chair_x = BUILDING_LENGTH/2 + 1.8
        balc_chair_y = -BUILDING_WIDTH/2 - 1.8
        create_cube("Balcony_Lounge_Armchair_1", (balc_chair_x, balc_chair_y, Z_FFL + 0.40), (0.9, 0.9, 0.75), mat_fabric_sofa, col_furniture)
        create_cube("Balcony_Lounge_Armchair_2", (balc_chair_x - 1.6, balc_chair_y - 0.8, Z_FFL + 0.40), (0.9, 0.9, 0.75), mat_fabric_sofa, col_furniture)
        create_cube("Balcony_Drinks_Table", (balc_chair_x - 0.8, balc_chair_y - 1.2, Z_FFL + 0.25), (0.6, 0.6, 0.50), mat_brass, col_furniture)

        log("Setting up interior lighting without operator dependencies...")
        downlight_locs = [
            (sofa_x, sofa_y, Z_FFL + CEILING_HEIGHT - 0.05),
            (sofa_x + 1.5, sofa_y, Z_FFL + CEILING_HEIGHT - 0.05),
            (sofa_x - 1.5, sofa_y, Z_FFL + CEILING_HEIGHT - 0.05),
            (dining_x, dining_y, Z_FFL + CEILING_HEIGHT - 0.05),
            (dining_x + 1.0, dining_y, Z_FFL + CEILING_HEIGHT - 0.05),
            (dining_x - 1.0, dining_y, Z_FFL + CEILING_HEIGHT - 0.05)
        ]
        for dl_idx, dl_pos in enumerate(downlight_locs):
            create_cube(f"Downlight_Spot_{dl_idx}", dl_pos, (0.15, 0.15, 0.02), mat_warm_interior_light, col_int_lighting)
            
            # Point lights using pure bpy.data API
            light_data = bpy.data.lights.new(name=f"Point_Light_DL_{dl_idx}", type='POINT')
            light_data.energy = 80.0
            light_data.color = (1.0, 0.88, 0.70)
            light_obj = bpy.data.objects.new(name=f"Point_Light_DL_{dl_idx}", object_data=light_data)
            light_obj.location = (dl_pos[0], dl_pos[1], dl_pos[2] - 0.15)
            col_int_lighting.objects.link(light_obj)

        log("Creating transition camera...")
        cam_loc = (BUILDING_LENGTH/2 + 3.2, -BUILDING_WIDTH/2 - 2.8, Z_FFL + 1.55)
        cam_target_loc = (sofa_x + 0.5, sofa_y + 0.5, Z_FFL + 1.40)

        # Pure bpy.data camera creation
        cam_data = bpy.data.cameras.new(name="Interior_Balcony_Transition_Camera")
        cam_data.lens = 22
        cam_data.clip_start = 0.1
        cam_data.clip_end = 500.0
        cam_obj = bpy.data.objects.new(name="Interior_Balcony_Transition_Camera", object_data=cam_data)
        cam_obj.location = cam_loc
        col_int_lighting.objects.link(cam_obj)
        scene.camera = cam_obj

        # Pure bpy.data empty creation
        target_empty = bpy.data.objects.new(name="Target_Interior_Living", object_data=None)
        target_empty.empty_display_type = 'PLAIN_AXES'
        target_empty.location = cam_target_loc
        col_int_lighting.objects.link(target_empty)

        track = cam_obj.constraints.new(type='TRACK_TO')
        track.target = target_empty
        track.track_axis = 'TRACK_NEGATIVE_Z'
        track.up_axis = 'UP_Y'

        log("Saving project...")
        blend_output = r"C:\Users\manpr\Documents\42 Kalidasa\blender\kalidasa42_interior_v001.blend"
        os.makedirs(os.path.dirname(blend_output), exist_ok=True)
        bpy.ops.wm.save_as_mainfile(filepath=blend_output)
        log(f"Saved interior model to: {blend_output}")

        log("Rendering interior review preview (1920x1080)...")
        review_output = r"C:\Users\manpr\Documents\42 Kalidasa\renders\preview\interior_review.png"
        scene.render.engine = 'BLENDER_EEVEE'
        scene.render.resolution_x = 1920
        scene.render.resolution_y = 1080
        scene.render.resolution_percentage = 100
        scene.render.image_settings.file_format = 'PNG'
        scene.render.filepath = review_output

        bpy.ops.render.render(write_still=True)

        if os.path.exists(blend_output) and os.path.getsize(blend_output) > 0:
            log(f"VERIFIED: Blend file size = {os.path.getsize(blend_output)/1024:.1f} KB")
        else:
            log("ERROR: Blend file was not saved!")
            sys.exit(1)

        if os.path.exists(review_output) and os.path.getsize(review_output) > 0:
            log(f"VERIFIED: Interior render size = {os.path.getsize(review_output)/1024:.1f} KB")
        else:
            log("ERROR: Interior render was not created!")
            sys.exit(1)

        log("=== REPRESENTATIVE APARTMENT INTERIOR COMPLETED SUCCESSFULLY ===")
    except Exception as e:
        log(f"FATAL ERROR in build_kalidasa42_interior: {e}")
        log(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    build_kalidasa42_interior()
