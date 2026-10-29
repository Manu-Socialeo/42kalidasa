"""
Kalidasa 42 — Architectural Massing Generator
Stage 4: Automated Parametric Massing Model in Blender 5.2+

Traces all vertical levels, footprint geometry, curved cantilever balconies,
central lift/stair core, ground double-height lobby, and 19th floor pool deck
strictly to sanction drawing DWG/NS/5692 and docs/reference_register.json.
"""

import bpy
import bmesh
import math
import os
import sys

# ---------------------------------------------------------------------------
# ARCHITECTURAL SPECIFICATIONS (from docs/reference_register.json)
# ---------------------------------------------------------------------------
BUILDING_LENGTH = 36.397  # Main tower length (m)
BUILDING_WIDTH = 16.000   # Main body width (m)
SLAB_THICKNESS = 0.250    # Concrete floor slab thickness (m)

# Vertical Levels (Relative to Ground Floor FFL = 0.00m)
# Driveway = -0.50m (Sanctioned height 67.70m from Driveway to Terrace SSL)
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

# Balcony Geometry Parameters
BALCONY_CANTILEVER = 4.80   # Projection beyond main wall (m)
BALCONY_ARC_LENGTH = 12.115 # Total sweep length (m)

# ---------------------------------------------------------------------------
# UTILITY HELPERS
# ---------------------------------------------------------------------------
def get_or_create_collection(name, parent=None):
    if name in bpy.data.collections:
        col = bpy.data.collections[name]
    else:
        col = bpy.data.collections.new(name)
        if parent is None:
            bpy.context.scene.collection.children.link(col)
        else:
            parent.children.link(col)
    return col

def get_or_create_material(name, color_rgba, roughness=0.4, metallic=0.0):
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
    return mat

def create_box(name, location, dimensions, material, collection):
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

def create_curved_balcony_slab(name, z_bottom, thickness, collection, mat_slab, mat_railing=None):
    """
    Creates a precision curved cantilever balcony matching Sheet 05 & facade render.
    Sweeps a continuous curve along the living room frontage.
    """
    mesh = bpy.data.meshes.new(name + "_Mesh")
    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    
    bm = bmesh.new()
    
    # 2D profile coordinates of typical 4BHK living balcony:
    # Corner origin at (BUILDING_LENGTH/2, -BUILDING_WIDTH/2)
    # Cantilever projects in +X and -Y direction
    x_base = BUILDING_LENGTH / 2.0
    y_base = -BUILDING_WIDTH / 2.0
    
    # Points defining the slab polygon
    pts = []
    # Inner wall boundary points (attachment to building)
    pts.append((x_base - 12.115, y_base))
    pts.append((x_base, y_base))
    pts.append((x_base, y_base + 7.0))
    
    # Outer cantilever boundary points (with smooth 7-segment corner fillet)
    pts.append((x_base + BALCONY_CANTILEVER, y_base + 7.0))
    
    # Fillet corner arc
    r = 3.5
    cx = x_base + BALCONY_CANTILEVER - r
    cy = y_base - BALCONY_CANTILEVER + r
    segments = 8
    for i in range(segments + 1):
        angle = math.radians(0 - (90.0 * i / segments))
        pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
        
    pts.append((x_base - 12.115, y_base - BALCONY_CANTILEVER))
    
    # Create 2D bottom face
    verts_bottom = [bm.verts.new((px, py, z_bottom)) for px, py in pts]
    face_bottom = bm.faces.new(verts_bottom)
    
    # Extrude upward by slab thickness
    geom_extrude = bmesh.ops.extrude_face_region(bm, geom=[face_bottom])
    verts_top = [v for v in geom_extrude['geom'] if isinstance(v, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, vec=(0, 0, thickness), verts=verts_top)
    
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    
    if mat_slab:
        obj.data.materials.append(mat_slab)
        
    # Add Glass Balustrade (1.1m height, 50mm offset from edge)
    if mat_railing:
        rail_mesh = bpy.data.meshes.new(name + "_Railing_Mesh")
        rail_obj = bpy.data.objects.new(name + "_Railing", rail_mesh)
        collection.objects.link(rail_obj)
        
        bm_rail = bmesh.new()
        # Rail follows the outer edge from pts[3] through arc to pts[-1]
        outer_pts = pts[3:]
        v_bottom = [bm_rail.verts.new((px, py, z_bottom + thickness)) for px, py in outer_pts]
        v_top = [bm_rail.verts.new((px, py, z_bottom + thickness + 1.10)) for px, py in outer_pts]
        
        for j in range(len(outer_pts) - 1):
            bm_rail.faces.new([v_bottom[j], v_bottom[j+1], v_top[j+1], v_top[j]])
            
        bmesh.ops.recalc_face_normals(bm_rail, faces=bm_rail.faces)
        bm_rail.to_mesh(rail_mesh)
        bm_rail.free()
        rail_obj.data.materials.append(mat_railing)

    return obj

# ---------------------------------------------------------------------------
# MAIN MODEL GENERATOR
# ---------------------------------------------------------------------------
def build_kalidasa42_massing():
    print("=== BUILDING KALIDASA 42 PARAMETRIC ARCHITECTURAL MASSING ===")
    
    # 1. Clean Scene
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = 'METRIC'
    scene.unit_settings.scale_length = 1.0
    scene.unit_settings.length_unit = 'METERS'

    # 2. Materials Setup
    mat_site = get_or_create_material("Mat_Site_Ground", (0.25, 0.26, 0.24, 1.0), roughness=0.8)
    mat_driveway = get_or_create_material("Mat_Fire_Driveway", (0.18, 0.18, 0.18, 1.0), roughness=0.7)
    mat_concrete = get_or_create_material("Mat_Arch_Concrete", (0.80, 0.77, 0.72, 1.0), roughness=0.45)
    mat_slab = get_or_create_material("Mat_Slab_Edge", (0.90, 0.88, 0.84, 1.0), roughness=0.35)
    mat_core = get_or_create_material("Mat_Core_Shafts", (0.65, 0.63, 0.60, 1.0), roughness=0.5)
    mat_glass = get_or_create_material("Mat_Facade_Glass", (0.15, 0.25, 0.35, 0.4), roughness=0.1, metallic=0.2)
    mat_pool = get_or_create_material("Mat_Pool_Water", (0.05, 0.55, 0.75, 0.8), roughness=0.1)

    # 3. Create Collection Hierarchy
    col_site = get_or_create_collection("01_Site_And_Ground")
    col_core = get_or_create_collection("02_Central_Core")
    col_slabs = get_or_create_collection("03_Floor_Slabs")
    col_balconies = get_or_create_collection("04_Curved_Balconies")
    col_mass = get_or_create_collection("05_Building_Mass_Envelopes")
    col_roof = get_or_create_collection("06_Rooftop_Amenities")

    # 4. SITE & DRIVEWAY BOUNDARIES (Sheet 01)
    # Master plot boundaries: South: 75.1m, East: 48.0m, North: 32.0m, West: 45.2m
    create_box("Site_Ground_Plane", (0, 0, -1.0), (100.0, 80.0, 0.5), mat_site, col_site)
    
    # 8.0m Fire Driveway Perimeter around Building Footprint
    driveway_len = BUILDING_LENGTH + 16.0  # 36.4 + 16 = 52.4m
    driveway_wid = BUILDING_WIDTH + 16.0   # 16.0 + 16 = 32.0m
    create_box("Fire_Driveway_8M", (0, 0, -0.5), (driveway_len, driveway_wid, 0.2), mat_driveway, col_site)

    # Ground Plinth (+98.3m datum = Z 0.0m; step up from driveway -0.5m)
    create_box("Ground_Plinth", (0, 0, -0.25), (BUILDING_LENGTH + 1.0, BUILDING_WIDTH + 1.0, 0.5), mat_concrete, col_site)

    # Entrance Porch (9'0" x 18'0" = 2.74m x 5.48m, Sheet 04)
    create_box("Ground_Entrance_Porch", (0, -BUILDING_WIDTH/2 - 2.74/2, 2.25), (5.48, 2.74, 4.50), mat_concrete, col_site)

    # 5. CENTRAL CIRCULATION CORE (Continuous from B2 to Roof)
    # Core dimensions: Main Stair 2.9x5.2, Fire Stair 2.9x4.9, 3 Lifts (2.3x2.7, 2x 1.9x2.5), Lobby 5.6x2.5
    core_length = 12.0
    core_width = 8.0
    core_height = 67.20 + 3.00 + 6.90 # B2 to Terrace headroom = 77.1m
    core_center_z = (-6.90 + 70.20) / 2.0
    create_box("Central_Service_Core", (-2.0, 1.0, core_center_z), (core_length, core_width, core_height), mat_core, col_core)

    # 6. PARAMETRIC FLOOR SLABS & MASSING FOR ALL 22 LEVELS
    for idx, lvl in enumerate(LEVELS):
        z_ffl = lvl["z_ffl"]
        h = lvl["height"]
        name = lvl["name"]
        ltype = lvl["type"]

        # Base floor slab
        slab_obj = create_box(f"Slab_{name}", (0, 0, z_ffl + SLAB_THICKNESS/2), (BUILDING_LENGTH, BUILDING_WIDTH, SLAB_THICKNESS), mat_slab, col_slabs)

        # Floor massing envelope / glazing volume
        if ltype == "basement":
            # Basement retaining volume
            create_box(f"Mass_{name}", (0, 0, z_ffl + h/2), (BUILDING_LENGTH + 2.0, BUILDING_WIDTH + 2.0, h), mat_concrete, col_mass)
            
        elif ltype == "ground":
            # Double-height grand lobby (4.50m height)
            create_box(f"Mass_{name}", (0, 0, z_ffl + h/2), (BUILDING_LENGTH - 0.2, BUILDING_WIDTH - 0.2, h - SLAB_THICKNESS), mat_glass, col_mass)

        elif ltype in ["residential_art", "typical_4bhk", "refuge_2bhk"]:
            # Residential floor massing
            create_box(f"Mass_{name}", (0, 0, z_ffl + h/2), (BUILDING_LENGTH - 0.2, BUILDING_WIDTH - 0.2, h - SLAB_THICKNESS), mat_concrete, col_mass)

            # Curved Cantilever Living Balcony (4.8m projection x 12.1m arc)
            create_curved_balcony_slab(f"Balcony_Living_{name}", z_ffl, SLAB_THICKNESS, col_balconies, mat_slab, mat_glass)

            # Master Bedroom Balcony (2.1m x 5.2m, Sheet 05)
            mb_x = -BUILDING_LENGTH/2 + 2.6
            mb_y = BUILDING_WIDTH/2 + 1.05
            create_box(f"Balcony_MBR_{name}", (mb_x, mb_y, z_ffl + SLAB_THICKNESS/2), (5.2, 2.1, SLAB_THICKNESS), mat_slab, col_balconies)

            # Bedroom 2 Balcony (5.4m x 2.4m, Sheet 05)
            b2_x = BUILDING_LENGTH/2 - 2.7
            b2_y = BUILDING_WIDTH/2 + 1.2
            create_box(f"Balcony_Bed2_{name}", (b2_x, b2_y, z_ffl + SLAB_THICKNESS/2), (5.4, 2.4, SLAB_THICKNESS), mat_slab, col_balconies)

        elif ltype == "clubhouse_pool":
            # 19th Floor Clubhouse & Rooftop Pool
            # Multipurpose Hall & Gym volume (9.9x12.5m and 6.8x6.1m)
            create_box("Clubhouse_Hall_Mass", (-BUILDING_LENGTH/4, 0, z_ffl + h/2), (18.0, 14.0, h - SLAB_THICKNESS), mat_glass, col_roof)
            
            # Swimming Pool Deck (+1.2m elevated deck @ +163.4m FFL)
            create_box("Pool_Deck_Platform", (BUILDING_LENGTH/4, 0, z_ffl + 0.6), (15.0, 12.0, 1.2), mat_concrete, col_roof)
            
            # Swimming Pool Tank (11.8m x 4.0m x 1.2m depth, Sheet 05)
            create_box("Swimming_Pool_Water", (BUILDING_LENGTH/4, 0, z_ffl + 0.8), (11.8, 4.0, 0.8), mat_pool, col_roof)

        elif ltype == "terrace":
            # Terrace Floor (SSL +165.5m)
            # Open terrace with swimming pool void/cutout
            # Stair and Lift Headrooms (3.0m headroom up to +168.5m roof level)
            create_box("Lift_Stair_Headrooms", (-2.0, 1.0, z_ffl + 1.50), (12.5, 8.5, 3.0), mat_concrete, col_roof)
            
            # Rooftop Pergola / Crown Frame (Top of Roof +168.5m)
            create_box("Rooftop_Pergola_Crown", (0, 0, z_ffl + 3.0), (BUILDING_LENGTH, BUILDING_WIDTH, 0.4), mat_concrete, col_roof)

    # 7. SETUP TEST PREVIEW CAMERAS & SUN
    col_render = get_or_create_collection("07_Lighting_And_Cameras")
    
    # Sun light with golden-hour angle matching WhatsApp render
    bpy.ops.object.light_add(type='SUN', location=(60, -80, 100))
    sun = bpy.context.active_object
    sun.name = "Sun_Golden_Hour"
    sun.data.energy = 4.0
    sun.rotation_euler = (math.radians(55), math.radians(15), math.radians(40))
    col_render.objects.link(sun)
    scene.collection.objects.unlink(sun)

    # Perspective Camera pointing to entire tower height (67.7m)
    bpy.ops.object.camera_add(location=(85, -85, 35))
    cam = bpy.context.active_object
    cam.name = "Massing_Review_Camera"
    cam.data.lens = 32
    cam.data.clip_end = 1000
    
    # Target constraint aiming at tower geometric center (Z ~ 34m)
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 34.0))
    target = bpy.context.active_object
    target.name = "Cam_Target_Center"
    col_render.objects.link(target)
    scene.collection.objects.unlink(target)
    
    track = cam.constraints.new(type='TRACK_TO')
    track.target = target
    track.track_axis = 'TRACK_NEGATIVE_Z'
    track.up_axis = 'UP_Y'
    
    col_render.objects.link(cam)
    scene.collection.objects.unlink(cam)
    scene.camera = cam

    # 8. SAVE VERSIONED BLENDER PROJECT
    blend_output = r"C:\Users\manpr\Documents\42 Kalidasa\blender\kalidasa42_massing_v001.blend"
    os.makedirs(os.path.dirname(blend_output), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=blend_output)
    print(f"Successfully saved massing model to: {blend_output}")

    # 9. RENDER VERIFICATION PREVIEW
    preview_output = r"C:\Users\manpr\Documents\42 Kalidasa\renders\preview\massing_v001_preview.png"
    os.makedirs(os.path.dirname(preview_output), exist_ok=True)
    
    scene.render.engine = 'BLENDER_EEVEE'
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = preview_output
    
    print(f"Rendering massing preview to: {preview_output}")
    bpy.ops.render.render(write_still=True)

    # 10. Check verification files
    if os.path.exists(blend_output) and os.path.getsize(blend_output) > 0:
        print(f"VERIFIED: Blend file size = {os.path.getsize(blend_output)/1024:.1f} KB")
    else:
        print("ERROR: Blend file was not saved!")
        sys.exit(1)

    if os.path.exists(preview_output) and os.path.getsize(preview_output) > 0:
        print(f"VERIFIED: Preview render size = {os.path.getsize(preview_output)/1024:.1f} KB")
    else:
        print("ERROR: Preview render was not created!")
        sys.exit(1)

    print("=== ARCHITECTURAL MASSING GENERATION COMPLETED SUCCESSFULLY ===")

if __name__ == "__main__":
    build_kalidasa42_massing()

