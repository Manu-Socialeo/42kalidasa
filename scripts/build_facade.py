"""
Kalidasa 42 — High-Fidelity Facade and Site Modeling (Camera & Landscape Perfected)
Stage 6: Procedural architectural detailing, modular fenestration, curved glass balustrades,
vertical facade fins, entrance canopy, rooftop pool, and PBR shaders calibrated to reference image.
"""

import bpy
import bmesh
import math
import os
import sys

BUILDING_LENGTH = 36.397
BUILDING_WIDTH = 16.000
SLAB_THICKNESS = 0.250
BALCONY_CANTILEVER = 4.80
BALCONY_ARC_LENGTH = 12.115

LEVELS = [
    {"name": "Lower_Basement_B2", "z_ffl": -6.90, "height": 3.30, "type": "basement"},
    {"name": "Upper_Basement_B1", "z_ffl": -3.60, "height": 3.60, "type": "basement"},
    {"name": "Ground_Floor",      "z_ffl":  0.00, "height": 4.50, "type": "ground"},
    {"name": "Floor_01",          "z_ffl":  4.50, "height": 3.30, "type": "residential_art"},
    {"name": "Floor_02",          "z_ffl":  7.80, "height": 3.30, "type": "typical_4bhk"},
    {"name": "Floor_03",          "z_ffl": 11.10, "height": 3.30, "type": "typical_4bhk"},
    {"name": "Floor_04",          "z_ffl": 14.40, "height": 3.30, "type": "typical_4bhk"},
    {"name": "Floor_05",          "z_ffl": 17.70, "height": 3.30, "type": "typical_4bhk"},
    {"name": "Floor_06",          "z_ffl": 21.00, "height": 3.30, "type": "typical_4bhk"},
    {"name": "Floor_07",          "z_ffl": 24.30, "height": 3.30, "type": "typical_4bhk"},
    {"name": "Floor_08",          "z_ffl": 27.60, "height": 3.30, "type": "typical_4bhk"},
    {"name": "Floor_09",          "z_ffl": 30.90, "height": 3.30, "type": "typical_4bhk"},
    {"name": "Floor_10",          "z_ffl": 34.20, "height": 3.30, "type": "typical_4bhk"},
    {"name": "Floor_11",          "z_ffl": 37.50, "height": 3.30, "type": "typical_4bhk"},
    {"name": "Floor_12",          "z_ffl": 40.80, "height": 3.30, "type": "typical_4bhk"},
    {"name": "Floor_13",          "z_ffl": 44.10, "height": 3.30, "type": "typical_4bhk"},
    {"name": "Floor_14",          "z_ffl": 47.40, "height": 3.30, "type": "typical_4bhk"},
    {"name": "Floor_15",          "z_ffl": 50.70, "height": 3.30, "type": "typical_4bhk"},
    {"name": "Floor_16",          "z_ffl": 54.00, "height": 3.30, "type": "typical_4bhk"},
    {"name": "Floor_17_Refuge",   "z_ffl": 57.30, "height": 3.30, "type": "refuge_2bhk"},
    {"name": "Floor_18",          "z_ffl": 60.60, "height": 3.30, "type": "typical_4bhk"},
    {"name": "Floor_19_Clubhouse","z_ffl": 63.90, "height": 3.30, "type": "clubhouse_pool"},
    {"name": "Floor_Terrace",     "z_ffl": 67.20, "height": 3.00, "type": "terrace"}
]

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

def create_cylinder(name, location, radius, depth, material, collection):
    mesh = bpy.data.meshes.new(name + "_Mesh")
    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=16, radius1=radius, radius2=radius, depth=depth)
    bm.to_mesh(mesh)
    bm.free()
    obj.location = location
    if material:
        obj.data.materials.append(material)
    return obj

def create_organic_canopy(name, location, scale_xyz, material, collection):
    mesh = bpy.data.meshes.new(name + "_Mesh")
    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=2, radius=1.0)
    bm.to_mesh(mesh)
    bm.free()
    obj.location = location
    obj.scale = scale_xyz
    if material:
        obj.data.materials.append(material)
    return obj

def create_detailed_balcony(name, z_bottom, thickness, collection, mat_slab, mat_soffit, mat_glass, mat_bronze, mat_glow):
    mesh = bpy.data.meshes.new(name + "_Slab_Mesh")
    obj = bpy.data.objects.new(name + "_Slab", mesh)
    collection.objects.link(obj)
    
    bm = bmesh.new()
    x_base = BUILDING_LENGTH / 2.0
    y_base = -BUILDING_WIDTH / 2.0
    
    pts = []
    pts.append((x_base - 12.115, y_base))
    pts.append((x_base, y_base))
    pts.append((x_base, y_base + 7.0))
    pts.append((x_base + BALCONY_CANTILEVER, y_base + 7.0))
    
    r = 3.6
    cx = x_base + BALCONY_CANTILEVER - r
    cy = y_base - BALCONY_CANTILEVER + r
    segments = 12
    for i in range(segments + 1):
        angle = math.radians(0 - (90.0 * i / segments))
        pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
        
    pts.append((x_base - 12.115, y_base - BALCONY_CANTILEVER))
    
    v_bottom = [bm.verts.new((px, py, z_bottom)) for px, py in pts]
    f_bottom = bm.faces.new(v_bottom)
    
    extrude = bmesh.ops.extrude_face_region(bm, geom=[f_bottom])
    v_top = [v for v in extrude['geom'] if isinstance(v, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, vec=(0, 0, thickness), verts=v_top)
    
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    
    if mat_slab:
        obj.data.materials.append(mat_slab)
        
    # Curved Glass Railing
    rail_mesh = bpy.data.meshes.new(name + "_Glass_Rail_Mesh")
    rail_obj = bpy.data.objects.new(name + "_Glass_Rail", rail_mesh)
    collection.objects.link(rail_obj)
    
    bm_r = bmesh.new()
    outer_pts = pts[3:]
    v_rb = [bm_r.verts.new((px, py, z_bottom + thickness)) for px, py in outer_pts]
    v_rt = [bm_r.verts.new((px, py, z_bottom + thickness + 1.15)) for px, py in outer_pts]
    
    for j in range(len(outer_pts) - 1):
        bm_r.faces.new([v_rb[j], v_rb[j+1], v_rt[j+1], v_rt[j]])
        
    bmesh.ops.recalc_face_normals(bm_r, faces=bm_r.faces)
    bm_r.to_mesh(rail_mesh)
    bm_r.free()
    if mat_glass:
        rail_obj.data.materials.append(mat_glass)

    # Top Cap Handrail (Champagne Bronze)
    cap_mesh = bpy.data.meshes.new(name + "_Handrail_Cap_Mesh")
    cap_obj = bpy.data.objects.new(name + "_Handrail_Cap", cap_mesh)
    collection.objects.link(cap_obj)
    
    bm_c = bmesh.new()
    cap_h = 0.06
    v_cb = [bm_c.verts.new((px, py, z_bottom + thickness + 1.15)) for px, py in outer_pts]
    v_ct = [bm_c.verts.new((px, py, z_bottom + thickness + 1.15 + cap_h)) for px, py in outer_pts]
    for k in range(len(outer_pts) - 1):
        bm_c.faces.new([v_cb[k], v_cb[k+1], v_ct[k+1], v_ct[k]])
    bmesh.ops.recalc_face_normals(bm_c, faces=bm_c.faces)
    bm_c.to_mesh(cap_mesh)
    bm_c.free()
    if mat_bronze:
        cap_obj.data.materials.append(mat_bronze)

    # Warm LED Cove Lighting Strip
    glow_mesh = bpy.data.meshes.new(name + "_Cove_Glow_Mesh")
    glow_obj = bpy.data.objects.new(name + "_Cove_Glow", glow_mesh)
    collection.objects.link(glow_obj)
    
    bm_g = bmesh.new()
    v_gb = [bm_g.verts.new((px * 0.98, py * 0.98, z_bottom - 0.02)) for px, py in outer_pts]
    v_gt = [bm_g.verts.new((px * 0.98, py * 0.98, z_bottom + 0.02)) for px, py in outer_pts]
    for m in range(len(outer_pts) - 1):
        bm_g.faces.new([v_gb[m], v_gb[m+1], v_gt[m+1], v_gt[m]])
    bmesh.ops.recalc_face_normals(bm_g, faces=bm_g.faces)
    bm_g.to_mesh(glow_mesh)
    bm_g.free()
    if mat_glow:
        glow_obj.data.materials.append(mat_glow)

    return obj

def create_window_unit(name, loc, width, height, mat_frame, mat_glass, collection):
    frame = create_cube(name + "_Frame", loc, (width, 0.12, height), mat_frame, collection)
    pane = create_cube(name + "_Glass", (loc[0], loc[1] + 0.01, loc[2]), (width - 0.10, 0.02, height - 0.10), mat_glass, collection)
    return frame, pane

def build_kalidasa42_facade():
    print("=== BUILDING KALIDASA 42 REFINED HIGH-FIDELITY FACADE & SITE ===")
    
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = 'METRIC'
    scene.unit_settings.scale_length = 1.0
    scene.unit_settings.length_unit = 'METERS'

    # PBR Materials
    mat_concrete = get_or_create_mat("Mat_Precast_Concrete", (0.78, 0.75, 0.70, 1.0), roughness=0.45)
    mat_fluted = get_or_create_mat("Mat_Fluted_Timber_Accent", (0.58, 0.36, 0.24, 1.0), roughness=0.40)
    mat_slab_edge = get_or_create_mat("Mat_Slab_Fascia", (0.94, 0.92, 0.88, 1.0), roughness=0.30)
    mat_soffit = get_or_create_mat("Mat_Timber_Soffit", (0.65, 0.45, 0.28, 1.0), roughness=0.50)
    mat_bronze = get_or_create_mat("Mat_Champagne_Bronze", (0.24, 0.21, 0.19, 1.0), roughness=0.25, metallic=0.80)
    mat_glass = get_or_create_mat("Mat_Facade_Tinted_Glass", (0.10, 0.18, 0.26, 0.40), roughness=0.06, metallic=0.35)
    mat_glow = get_or_create_mat("Mat_Warm_Cove_Glow", (1.0, 0.88, 0.65, 1.0), roughness=0.9, emission_rgba=(1.0, 0.85, 0.55, 1.0), emission_strength=4.5)
    mat_pool = get_or_create_mat("Mat_Pool_Water_Cyan", (0.05, 0.62, 0.78, 0.75), roughness=0.08)
    mat_driveway = get_or_create_mat("Mat_Driveway_Paved", (0.20, 0.20, 0.21, 1.0), roughness=0.70)
    mat_grass = get_or_create_mat("Mat_Lush_Landscape", (0.16, 0.30, 0.12, 1.0), roughness=0.85)
    mat_foliage = get_or_create_mat("Mat_Tree_Foliage", (0.14, 0.26, 0.10, 1.0), roughness=0.6)
    mat_red_foliage = get_or_create_mat("Mat_Autumn_Accent_Tree", (0.62, 0.14, 0.12, 1.0), roughness=0.6)
    mat_trunk = get_or_create_mat("Mat_Tree_Trunk", (0.22, 0.16, 0.10, 1.0), roughness=0.8)

    # Collections
    col_site = get_or_create_col("01_Site_Landscape")
    col_structure = get_or_create_col("02_Superstructure")
    col_slabs = get_or_create_col("03_Floor_Slabs")
    col_balconies = get_or_create_col("04_Curved_Balconies")
    col_fenestration = get_or_create_col("05_Fenestration_Glazing")
    col_fins = get_or_create_col("06_Architectural_Fins")
    col_roof = get_or_create_col("07_Rooftop_Clubhouse")
    col_lighting = get_or_create_col("08_Lighting_And_Cameras")

    # Site Ground Plane & Driveway
    create_cube("Master_Site_Plane", (0, 0, -1.0), (140.0, 120.0, 0.5), mat_grass, col_site)
    create_cube("Fire_Driveway_8M", (0, 0, -0.45), (BUILDING_LENGTH + 18.0, BUILDING_WIDTH + 18.0, 0.1), mat_driveway, col_site)
    create_cube("Ground_Plinth_Slab", (0, 0, -0.25), (BUILDING_LENGTH + 1.2, BUILDING_WIDTH + 1.2, 0.5), mat_concrete, col_site)

    # Balanced Perimeter Trees Framing the Base & Sides
    # Left flanking trees (framing bottom-left)
    for t_idx, (tx, ty, tz, s_xy, s_z) in enumerate([
        (-24.0, -28.0, 1.0, 6.0, 5.5),
        (-14.0, -32.0, 1.0, 5.0, 4.5),
        (-32.0, -18.0, 1.0, 6.5, 6.0),
        (-5.0,  -35.0, 0.5, 4.0, 3.5)
    ]):
        create_cylinder(f"Tree_Trunk_Left_{t_idx}", (tx, ty, tz), 0.25, 4.0, mat_trunk, col_site)
        create_organic_canopy(f"Tree_Canopy_Left_{t_idx}", (tx, ty, tz + 3.0), (s_xy, s_xy, s_z), mat_foliage, col_site)

    # Right flanking trees (Autumn red accent tree + green canopy framing bottom-right)
    create_cylinder("Tree_Trunk_Right_Red", (25.0, -18.0, 1.0), 0.25, 4.5, mat_trunk, col_site)
    create_organic_canopy("Tree_Canopy_Right_Red", (25.0, -18.0, 4.0), (5.5, 5.5, 5.0), mat_red_foliage, col_site)

    create_cylinder("Tree_Trunk_Right_Green", (32.0, -12.0, 1.0), 0.30, 5.0, mat_trunk, col_site)
    create_organic_canopy("Tree_Canopy_Right_Green", (32.0, -12.0, 4.5), (6.0, 6.0, 5.5), mat_foliage, col_site)

    # Ground Floor Double-Height Curtain Wall & Entrance (4.50m)
    create_cube("Ground_Lobby_Glazing", (0, 0, 2.25), (BUILDING_LENGTH - 0.4, BUILDING_WIDTH - 0.4, 4.50 - SLAB_THICKNESS), mat_glass, col_fenestration)
    create_cube("Ground_Entrance_Canopy", (0, -BUILDING_WIDTH/2 - 2.8, 3.8), (6.5, 3.2, 0.25), mat_bronze, col_structure)
    create_cylinder("Canopy_Support_Col_1", (-2.8, -BUILDING_WIDTH/2 - 4.0, 1.9), 0.15, 3.8, mat_bronze, col_structure)
    create_cylinder("Canopy_Support_Col_2", ( 2.8, -BUILDING_WIDTH/2 - 4.0, 1.9), 0.15, 3.8, mat_bronze, col_structure)
    create_cube("Entrance_Portal_Frame", (0, -BUILDING_WIDTH/2 - 0.1, 1.7), (3.2, 0.3, 3.4), mat_bronze, col_structure)

    # Vertical Shear Wall Core
    core_z_mid = (-6.90 + 70.20) / 2.0
    core_h = 77.10
    create_cube("Tower_Vertical_Shear_Core", (-2.0, 1.0, core_z_mid), (12.2, 8.2, core_h), mat_fluted, col_structure)

    # Floors 1 to 18
    for lvl in LEVELS:
        z = lvl["z_ffl"]
        h = lvl["height"]
        name = lvl["name"]
        ltype = lvl["type"]

        create_cube(f"Slab_{name}", (0, 0, z + SLAB_THICKNESS/2), (BUILDING_LENGTH, BUILDING_WIDTH, SLAB_THICKNESS), mat_slab_edge, col_slabs)

        if ltype in ["residential_art", "typical_4bhk", "refuge_2bhk"]:
            create_cube(f"Walls_{name}", (0, 0, z + h/2), (BUILDING_LENGTH - 0.2, BUILDING_WIDTH - 0.2, h - SLAB_THICKNESS), mat_concrete, col_structure)

            # Curved Cantilever Balconies
            create_detailed_balcony(f"Balcony_Living_{name}", z, SLAB_THICKNESS, col_balconies, mat_slab_edge, mat_soffit, mat_glass, mat_bronze, mat_glow)

            # SD1 Sliding Door to Balcony
            sd1_x = BUILDING_LENGTH/2 - 2.5
            sd1_y = -BUILDING_WIDTH/2 + 0.05
            create_cube(f"Door_SD1_{name}", (sd1_x, sd1_y, z + 1.25), (3.4, 0.15, 2.4), mat_glass, col_fenestration)
            create_cube(f"Door_SD1_Frame_{name}", (sd1_x, sd1_y, z + 1.25), (3.45, 0.16, 2.45), mat_bronze, col_fenestration)

            # Windows W4 & W1
            create_window_unit(f"Win_W4_{name}", (-8.0, -BUILDING_WIDTH/2 + 0.05, z + 1.65), 3.0, 1.5, mat_bronze, mat_glass, col_fenestration)
            create_window_unit(f"Win_W1_{name}", (-14.0, -BUILDING_WIDTH/2 + 0.05, z + 1.65), 1.5, 1.5, mat_bronze, mat_glass, col_fenestration)

            # Rear Balconies
            mb_x = -BUILDING_LENGTH/2 + 2.6
            mb_y = BUILDING_WIDTH/2 + 1.05
            create_cube(f"Balcony_MBR_{name}", (mb_x, mb_y, z + SLAB_THICKNESS/2), (5.2, 2.1, SLAB_THICKNESS), mat_slab_edge, col_balconies)
            create_cube(f"Rail_MBR_{name}", (mb_x, mb_y + 1.0, z + 0.65), (5.2, 0.05, 1.15), mat_glass, col_balconies)

            b2_x = BUILDING_LENGTH/2 - 2.7
            b2_y = BUILDING_WIDTH/2 + 1.2
            create_cube(f"Balcony_Bed2_{name}", (b2_x, b2_y, z + SLAB_THICKNESS/2), (5.4, 2.4, SLAB_THICKNESS), mat_slab_edge, col_balconies)
            create_cube(f"Rail_Bed2_{name}", (b2_x, b2_y + 1.15, z + 0.65), (5.4, 0.05, 1.15), mat_glass, col_balconies)

        elif ltype == "clubhouse_pool":
            create_cube("Clubhouse_Gym_Glazing", (-BUILDING_LENGTH/4, 0, z + h/2), (18.0, 14.0, h - SLAB_THICKNESS), mat_glass, col_roof)
            create_cube("Clubhouse_Frame_Mullions", (-BUILDING_LENGTH/4, 0, z + h/2), (18.1, 14.1, h - SLAB_THICKNESS + 0.05), mat_bronze, col_roof)
            
            create_cube("Pool_Platform_Deck", (BUILDING_LENGTH/4, 0, z + 0.6), (15.2, 12.2, 1.2), mat_concrete, col_roof)
            create_cube("Swimming_Pool_Water_Body", (BUILDING_LENGTH/4, 0, z + 0.85), (11.8, 4.0, 0.8), mat_pool, col_roof)
            create_cube("Pool_Safety_Glass_Rail", (BUILDING_LENGTH/4, -6.1, z + 1.7), (15.2, 0.06, 1.15), mat_glass, col_roof)

        elif ltype == "terrace":
            create_cube("Elevator_Headrooms", (-2.0, 1.0, z + 1.50), (12.5, 8.5, 3.0), mat_concrete, col_roof)
            create_cube("Rooftop_Pergola_Perimeter", (0, 0, z + 3.0), (BUILDING_LENGTH + 0.5, BUILDING_WIDTH + 0.5, 0.35), mat_bronze, col_roof)
            
            for luv_i in range(12):
                lx = -BUILDING_LENGTH/2 + 2.0 + (luv_i * 3.0)
                create_cube(f"Pergola_Louver_{luv_i}", (lx, 0, z + 3.0), (0.15, BUILDING_WIDTH, 0.30), mat_bronze, col_roof)

    # Vertical Architectural Fins
    for fin_idx, fin_x in enumerate([-16.0, -10.5, -4.5, 5.0]):
        create_cube(f"Vertical_Facade_Fin_{fin_idx}", (fin_x, -BUILDING_WIDTH/2 - 0.25, 35.85), (0.35, 0.50, 62.70), mat_fluted, col_fins)

    # Lighting Setup (Warm Golden Hour)
    bpy.ops.object.light_add(type='SUN', location=(80, -90, 65))
    sun = bpy.context.active_object
    sun.name = "Sun_Golden_Hour"
    sun.data.energy = 5.5
    sun.data.angle = math.radians(2.0)
    sun.rotation_euler = (math.radians(65), math.radians(10), math.radians(35))
    col_lighting.objects.link(sun)
    scene.collection.objects.unlink(sun)

    # Sky Environment Lighting
    if scene.world is None:
        scene.world = bpy.data.worlds.new("World")
    world = scene.world
    if hasattr(world, "node_tree") and world.node_tree:
        bg = world.node_tree.nodes.get("Background")
        if bg:
            bg.inputs['Color'].default_value = (0.76, 0.84, 0.96, 1.0)
            bg.inputs['Strength'].default_value = 0.85

    # HERO CAMERA (OPTIMAL ESTABLISHING ANGLE - DRAMATIC LOW-ANGLE PERSPECTIVE)
    bpy.ops.object.camera_add(location=(22.0, -68.0, 9.0))
    cam = bpy.context.active_object
    cam.name = "Hero_Establishing_Camera"
    cam.data.lens = 24 # 24mm architectural wide-angle
    cam.data.clip_end = 1500.0
    
    target_pos = (BUILDING_LENGTH/2 - 6.0, -BUILDING_WIDTH/2 + 2.0, 35.0)
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=target_pos)
    cam_target = bpy.context.active_object
    cam_target.name = "Cam_Target_Hero_Corner"
    col_lighting.objects.link(cam_target)
    scene.collection.objects.unlink(cam_target)

    track = cam.constraints.new(type='TRACK_TO')
    track.target = cam_target
    track.track_axis = 'TRACK_NEGATIVE_Z'
    track.up_axis = 'UP_Y'
    
    col_lighting.objects.link(cam)
    scene.collection.objects.unlink(cam)
    scene.camera = cam

    # Save Project
    blend_output = r"C:\Users\manpr\Documents\42 Kalidasa\blender\kalidasa42_facade_v001.blend"
    os.makedirs(os.path.dirname(blend_output), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=blend_output)
    print(f"Saved refined facade model to: {blend_output}")

    # Render High-Resolution Facade Review (1920 x 1080)
    review_output = r"C:\Users\manpr\Documents\42 Kalidasa\renders\preview\facade_review.png"
    scene.render.engine = 'BLENDER_EEVEE'
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = review_output
    
    print(f"Rendering refined facade review to {review_output}...")
    bpy.ops.render.render(write_still=True)

    print("=== REFINED FACADE AND SITE MODELING COMPLETE ===")

if __name__ == "__main__":
    build_kalidasa42_facade()
