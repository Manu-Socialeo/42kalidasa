"""
KALIDASA 42 - Architectural Blueprint Match Reconstruction (v003 Final)
Faithfully reconstructs the 3D model using the user's uploaded blueprints:
- Typical Floor Plan (Floors 1-18) living room balcony & prow cantilever
- 19th Floor Plan (Amenities, Gym, 11.8x4.0m Swimming Pool, Sculptural Roof Crown)
- Removes foreground tree obstructions
- Calibrates 2-point architectural camera to frame the full 67.7m tower from street plinth to roof
"""

import bpy
import bmesh
import math
import os

WORKSPACE = r"C:\Users\manpr\Documents\42 Kalidasa"
BASE_BLEND = os.path.join(WORKSPACE, "blender", "kalidasa42_corrected_v002.blend")
OUT_BLEND = os.path.join(WORKSPACE, "blender", "kalidasa42_corrected_v003.blend")
RENDER_OUT = os.path.join(WORKSPACE, "renders", "preview", "kalidasa42_corrected_v003.png")

print(f"Loading base blend: {BASE_BLEND}...")
bpy.ops.wm.open_mainfile(filepath=BASE_BLEND)
scene = bpy.context.scene

# 1. Hide all obstructive foreground trees
for obj in bpy.data.objects:
    if 'Tree_FG' in obj.name or 'Tree_Canopy_Right' in obj.name or 'Tree_Trunk_Right' in obj.name:
        obj.hide_render = True
    elif 'Tree_Canopy_Left' in obj.name or 'Tree_Trunk_Left' in obj.name:
        # Keep background street trees along the driveway
        obj.hide_render = False

# 2. Materials
mat_slab = bpy.data.materials.get("Mat_Slab_Fascia")
mat_soffit = bpy.data.materials.get("Mat_Feature_Timber_Paneling")
mat_cove = bpy.data.materials.get("Mat_Warm_Cove_Glow")
mat_glass = bpy.data.materials.get("Mat_Facade_Tinted_Glass")
mat_bronze = bpy.data.materials.get("Mat_Champagne_Bronze")
mat_concrete = bpy.data.materials.get("Mat_Precast_Concrete")
mat_water = bpy.data.materials.get("Mat_Pool_Water_Cyan") or bpy.data.materials.new("Mat_Pool_Water_Cyan")
if mat_water.node_tree:
    bw = mat_water.node_tree.nodes.get("Principled BSDF")
    if bw:
        bw.inputs["Base Color"].default_value = (0.05, 0.55, 0.75, 1.0)
        bw.inputs["Roughness"].default_value = 0.05
        if "Transmission Weight" in bw.inputs:
            bw.inputs["Transmission Weight"].default_value = 0.90
        elif "Transmission" in bw.inputs:
            bw.inputs["Transmission"].default_value = 0.90

col_balconies = bpy.data.collections.get("04_Curved_Balconies") or scene.collection

# 3. Typical Balcony 2D Coordinates (Floors 1 to 18)
# Shifted by -7.0m in Y to align with the building's South facade at Y = -8.0
typical_balcony_raw = [
    (13.48, 6.55), (14.43, 4.72), (15.75, 2.16), (17.35, 1.79), (17.32, 1.06),
    (17.32, 0.33), (17.32, -0.40), (17.50, -0.77), (17.69, -1.13), (17.87, -1.50),
    (18.02, -1.87), (18.09, -2.23), (18.16, -2.60), (18.09, -2.96), (18.05, -3.33),
    (17.91, -3.69), (17.72, -4.06), (17.43, -4.43), (17.32, -4.79), (16.50, -5.20),
    (14.00, -5.50), (6.085, -5.50), (6.085, 2.00), (13.48, 6.55)
]
# Apply offset: Y -> Y - 7.0m so prow projects from Y = -8.0 down to Y = -12.50m
typical_balcony_pts = [(p[0], p[1] - 7.0) for p in typical_balcony_raw]
typical_outer_curve = typical_balcony_pts[:-3]

# 4. 19th Floor Pool Deck Coordinates
pool_deck_raw = [
    (12.84, 6.71), (13.69, 5.61), (15.30, 3.05), (15.89, 1.94), (16.47, 1.21),
    (16.84, 0.48), (17.21, -0.26), (17.57, -0.99), (17.98, -1.72), (18.20, -2.83),
    (18.16, -3.19), (18.09, -3.56), (17.72, -4.29), (17.39, -4.66), (16.88, -5.03),
    (15.00, -5.30), (6.085, -5.30), (6.085, 3.00), (12.84, 6.71)
]
pool_deck_pts = [(p[0], p[1] - 7.0) for p in pool_deck_raw]
pool_deck_outer_curve = pool_deck_pts[:-3]

floors = [
    ("Floor_01", 4.50), ("Floor_02", 7.80), ("Floor_03", 11.10), ("Floor_04", 14.40),
    ("Floor_05", 17.70), ("Floor_06", 21.00), ("Floor_07", 24.30), ("Floor_08", 27.60),
    ("Floor_09", 30.90), ("Floor_10", 34.20), ("Floor_11", 37.50), ("Floor_12", 40.80),
    ("Floor_13", 44.10), ("Floor_14", 47.40), ("Floor_15", 50.70), ("Floor_16", 54.00),
    ("Floor_17_Refuge", 57.30), ("Floor_18", 60.60)
]
slab_thickness = 0.28

# Rebuild Floors 1 to 18
for fl_name, z_fl in floors:
    slab_name = f"Balcony_Living_{fl_name}_Slab"
    glass_name = f"Balcony_Living_{fl_name}_Glass_Rail"
    cap_name = f"Balcony_Living_{fl_name}_Handrail_Cap"
    cove_name = f"Balcony_Living_{fl_name}_Cove_Glow"

    for oname in [slab_name, glass_name, cap_name, cove_name]:
        old = bpy.data.objects.get(oname)
        if old:
            bpy.data.objects.remove(old, do_unlink=True)

    # Slab with Timber Soffit
    m_s = bpy.data.meshes.new(slab_name + "_Mesh")
    o_s = bpy.data.objects.new(slab_name, m_s)
    col_balconies.objects.link(o_s)
    bm = bmesh.new()
    vb = [bm.verts.new((p[0], p[1], z_fl)) for p in typical_balcony_pts]
    fb = bm.faces.new(vb)
    ext = bmesh.ops.extrude_face_region(bm, geom=[fb])
    vt = [v for v in ext['geom'] if isinstance(v, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, vec=(0, 0, slab_thickness), verts=vt)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    o_s.data.materials.append(mat_slab)
    o_s.data.materials.append(mat_soffit)
    fb.material_index = 1
    bm.to_mesh(m_s)
    bm.free()

    # Glass Railing
    m_g = bpy.data.meshes.new(glass_name + "_Mesh")
    o_g = bpy.data.objects.new(glass_name, m_g)
    col_balconies.objects.link(o_g)
    bm_g = bmesh.new()
    vgb = [bm_g.verts.new((p[0], p[1], z_fl + slab_thickness)) for p in typical_outer_curve]
    vgt = [bm_g.verts.new((p[0], p[1], z_fl + slab_thickness + 1.15)) for p in typical_outer_curve]
    for idx in range(len(typical_outer_curve) - 1):
        bm_g.faces.new([vgb[idx], vgb[idx+1], vgt[idx+1], vgt[idx]])
    bmesh.ops.recalc_face_normals(bm_g, faces=bm_g.faces)
    bm_g.to_mesh(m_g)
    bm_g.free()
    o_g.data.materials.append(mat_glass)

    # Handrail Cap
    m_c = bpy.data.meshes.new(cap_name + "_Mesh")
    o_c = bpy.data.objects.new(cap_name, m_c)
    col_balconies.objects.link(o_c)
    bm_c = bmesh.new()
    vcb = [bm_c.verts.new((p[0], p[1], z_fl + slab_thickness + 1.15)) for p in typical_outer_curve]
    vct = [bm_c.verts.new((p[0], p[1], z_fl + slab_thickness + 1.20)) for p in typical_outer_curve]
    for idx in range(len(typical_outer_curve) - 1):
        bm_c.faces.new([vcb[idx], vcb[idx+1], vct[idx+1], vct[idx]])
    bmesh.ops.recalc_face_normals(bm_c, faces=bm_c.faces)
    bm_c.to_mesh(m_c)
    bm_c.free()
    o_c.data.materials.append(mat_bronze)

    # Cove Glow
    m_cv = bpy.data.meshes.new(cove_name + "_Mesh")
    o_cv = bpy.data.objects.new(cove_name, m_cv)
    col_balconies.objects.link(o_cv)
    bm_cv = bmesh.new()
    vcvb = [bm_cv.verts.new((p[0]*0.99, p[1]*0.99, z_fl - 0.02)) for p in typical_outer_curve]
    vcvt = [bm_cv.verts.new((p[0]*0.99, p[1]*0.99, z_fl + 0.01)) for p in typical_outer_curve]
    for idx in range(len(typical_outer_curve) - 1):
        bm_cv.faces.new([vcvb[idx], vcvb[idx+1], vcvt[idx+1], vcvt[idx]])
    bmesh.ops.recalc_face_normals(bm_cv, faces=bm_cv.faces)
    bm_cv.to_mesh(m_cv)
    bm_cv.free()
    o_cv.data.materials.append(mat_cove)

print("Constructed 18 floors of blueprint-accurate balconies.")

# 5. Reconstruct 19th Floor Pool Deck & Swimming Pool
z_19 = 63.90
deck_name = "Pool_Deck_Floor_19_Slab"
deck_rail_name = "Pool_Deck_Floor_19_Glass_Rail"
pool_name = "Swimming_Pool_Water_Body"

for oname in [deck_name, deck_rail_name, pool_name]:
    old = bpy.data.objects.get(oname)
    if old:
        bpy.data.objects.remove(old, do_unlink=True)

# Pool Deck Slab
m_d = bpy.data.meshes.new(deck_name + "_Mesh")
o_d = bpy.data.objects.new(deck_name, m_d)
col_balconies.objects.link(o_d)
bm_d = bmesh.new()
v_db = [bm_d.verts.new((p[0], p[1], z_19)) for p in pool_deck_pts]
f_db = bm_d.faces.new(v_db)
ext_d = bmesh.ops.extrude_face_region(bm_d, geom=[f_db])
v_dt = [v for v in ext_d['geom'] if isinstance(v, bmesh.types.BMVert)]
bmesh.ops.translate(bm_d, vec=(0, 0, slab_thickness), verts=v_dt)
bmesh.ops.recalc_face_normals(bm_d, faces=bm_d.faces)
o_d.data.materials.append(mat_slab)
o_d.data.materials.append(mat_soffit)
f_db.material_index = 1
bm_d.to_mesh(m_d)
bm_d.free()

# Pool Deck Railing
m_dr = bpy.data.meshes.new(deck_rail_name + "_Mesh")
o_dr = bpy.data.objects.new(deck_rail_name, m_dr)
col_balconies.objects.link(o_dr)
bm_dr = bmesh.new()
v_drb = [bm_dr.verts.new((p[0], p[1], z_19 + slab_thickness)) for p in pool_deck_outer_curve]
v_drt = [bm_dr.verts.new((p[0], p[1], z_19 + slab_thickness + 1.15)) for p in pool_deck_outer_curve]
for idx in range(len(pool_deck_outer_curve) - 1):
    bm_dr.faces.new([v_drb[idx], v_drb[idx+1], v_drt[idx+1], v_drt[idx]])
bmesh.ops.recalc_face_normals(bm_dr, faces=bm_dr.faces)
bm_dr.to_mesh(m_dr)
bm_dr.free()
o_dr.data.materials.append(mat_glass)

# Swimming Pool (11.8m x 4.0m)
m_p = bpy.data.meshes.new(pool_name + "_Mesh")
o_p = bpy.data.objects.new(pool_name, m_p)
col_balconies.objects.link(o_p)
bm_p = bmesh.new()
px1, px2 = 6.0, 17.8
py1, py2 = -12.0, -8.0
vp1 = bm_p.verts.new((px1, py1, z_19 + 0.15))
vp2 = bm_p.verts.new((px2, py1, z_19 + 0.15))
vp3 = bm_p.verts.new((px2, py2, z_19 + 0.15))
vp4 = bm_p.verts.new((px1, py2, z_19 + 0.15))
bm_p.faces.new([vp1, vp2, vp3, vp4])
bmesh.ops.recalc_face_normals(bm_p, faces=bm_p.faces)
bm_p.to_mesh(m_p)
bm_p.free()
o_p.data.materials.append(mat_water)

# 6. Sculptural Curved Roof Crown Prow
crown_name = "Tower_Sculptural_Roof_Crown"
old_cr = bpy.data.objects.get(crown_name)
if old_cr:
    bpy.data.objects.remove(old_cr, do_unlink=True)

m_cr = bpy.data.meshes.new(crown_name + "_Mesh")
o_cr = bpy.data.objects.new(crown_name, m_cr)
col_balconies.objects.link(o_cr)
bm_cr = bmesh.new()
crown_h = 4.80
v_crb = [bm_cr.verts.new((p[0], p[1], z_19)) for p in pool_deck_pts]
v_crt = [bm_cr.verts.new((p[0], p[1], z_19 + crown_h)) for p in pool_deck_pts]
for idx in range(len(pool_deck_pts) - 1):
    bm_cr.faces.new([v_crb[idx], v_crb[idx+1], v_crt[idx+1], v_crt[idx]])
bmesh.ops.recalc_face_normals(bm_cr, faces=bm_cr.faces)
bm_cr.to_mesh(m_cr)
bm_cr.free()
o_cr.data.materials.append(mat_concrete)

# 7. Fluted Terracotta / Bronze Spine Flush on East Balcony Edge
old_sp = bpy.data.objects.get("Tower_Fluted_Terracotta_Spine")
if old_sp:
    bpy.data.objects.remove(old_sp, do_unlink=True)

m_sp = bpy.data.meshes.new("Tower_Fluted_Terracotta_Spine_Mesh")
o_sp = bpy.data.objects.new("Tower_Fluted_Terracotta_Spine", m_sp)
col_balconies.objects.link(o_sp)
bm_sp = bmesh.new()
v1 = bm_sp.verts.new((18.10, -9.60, 0.0))
v2 = bm_sp.verts.new((18.45, -9.60, 0.0))
v3 = bm_sp.verts.new((18.45, -0.45, 0.0))
v4 = bm_sp.verts.new((18.10, -0.45, 0.0))
f_sp = bm_sp.faces.new([v1, v2, v3, v4])
ext_sp = bmesh.ops.extrude_face_region(bm_sp, geom=[f_sp])
vt_sp = [v for v in ext_sp['geom'] if isinstance(v, bmesh.types.BMVert)]
bmesh.ops.translate(bm_sp, vec=(0, 0, 69.10), verts=vt_sp)
bmesh.ops.recalc_face_normals(bm_sp, faces=bm_sp.faces)
bm_sp.to_mesh(m_sp)
bm_sp.free()
o_sp.data.materials.append(mat_bronze)

# 8. Architectural Two-Point Camera Calibration
cam = bpy.data.objects.get("Cam_TwoPoint_Architectural")
if not cam:
    cam_data = bpy.data.cameras.new("Cam_TwoPoint_Architectural")
    cam = bpy.data.objects.new("Cam_TwoPoint_Architectural", cam_data)
    scene.collection.objects.link(cam)

scene.camera = cam

# Station camera at South-East corner:
cam.location = (52.0, -78.0, 12.0)
dx = 4.0 - 52.0
dy = -4.0 - (-78.0)
yaw = math.atan2(-dx, dy)

cam.rotation_euler = (math.radians(90), 0.0, yaw) # Perfect 2-point perspective
cam.data.type = 'PERSP'
cam.data.lens = 42.0 # Telephoto architectural lens
cam.data.shift_x = 0.03 # Centered framing
cam.data.shift_y = 0.40 # Level elevation showing plinth to roof crown

# 9. Lighting Setup
sun = bpy.data.objects.get("Sun_Architectural_Hero")
if sun:
    sun.rotation_euler = (math.radians(65), math.radians(12), math.radians(128))
    sun.data.energy = 2.6
    sun.data.color = (1.0, 0.85, 0.70)

# Save blend
bpy.ops.wm.save_as_mainfile(filepath=OUT_BLEND)
print(f"Saved: {OUT_BLEND}")

# 10. Cycles Render
scene.render.engine = 'CYCLES'
if hasattr(scene, 'cycles'):
    scene.cycles.device = 'CPU'
    scene.cycles.samples = 32
    scene.cycles.use_denoising = True

scene.render.resolution_x = 1200
scene.render.resolution_y = 800
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.filepath = RENDER_OUT

print(f"Rendering blueprint match v003 to: {RENDER_OUT}...")
bpy.ops.render.render(write_still=True)
print("Render complete!")

# Sync to master blend
master_path = os.path.join(WORKSPACE, "blender", "kalidasa42_animated_v001.blend")
bpy.ops.wm.save_as_mainfile(filepath=master_path)
print(f"Master blend synced: {master_path}")

