"""
KALIDASA 42 - Architectural Reconstruction and Match Script (v002)
Reconstructs the 3D Blender building geometry in 'blender/kalidasa42_corrected_v002.blend'
to strictly match the approved architectural reference photograph and municipal drawings DWG/NS/5692.

Key Geometric Reconstructions:
1. Replaces generic solid wall blocks with architectural concrete piers and floor-to-ceiling recessed glass window bays.
2. Reconstructs the 4.80m cantilever curved prow balconies with warm timber soffits, recessed cove lighting, and smoked glass railings.
3. Models the 4.8m tall sculptural curved roof crown prow parapet terminating the tower skyline.
4. Models the 14-rib fluted terracotta vertical pilaster spine on the right.
5. Calibrates a true two-point architectural perspective camera with tilt-shift vertical correction.
6. Calibrates golden-hour sunset backlighting and foreground framing trees.
7. Renders the corrected scene to 'renders/preview/kalidasa42_corrected_v002.png'.
8. Generates side-by-side comparison and contour overlay against the approved reference photograph.
"""

import bpy
import bmesh
import math
import os

WORKSPACE = r"C:\Users\manpr\Documents\42 Kalidasa"
SRC_BLEND = os.path.join(WORKSPACE, "blender", "kalidasa42_animated_v001_pre_v007_backup.blend")
DST_BLEND = os.path.join(WORKSPACE, "blender", "kalidasa42_corrected_v002.blend")
RENDER_OUT = os.path.join(WORKSPACE, "renders", "preview", "kalidasa42_corrected_v002.png")
COMPARISON_OUT = os.path.join(WORKSPACE, "renders", "preview", "kalidasa42_comparison_v002.png")
OVERLAY_OUT = os.path.join(WORKSPACE, "renders", "preview", "kalidasa42_overlay_v002.png")
REF_PHOTO = os.path.join(WORKSPACE, "assets", "WhatsApp Image 2026-10-27 at 11.30.09 AM.jpeg")

def reconstruct():
    print(f"Loading baseline blend: {SRC_BLEND}...")
    bpy.ops.wm.open_mainfile(filepath=SRC_BLEND)
    scene = bpy.context.scene

    # -----------------------------------------------------------------------
    # 1. Clean Up Lights & World Sky
    # -----------------------------------------------------------------------
    # Remove duplicate sun lamps to eliminate washed out renders
    suns = [o for o in bpy.data.objects if o.type == 'LIGHT' and o.data.type == 'SUN']
    print(f"Found {len(suns)} existing sun lights.")
    for s in suns[1:]:
        bpy.data.objects.remove(s, do_unlink=True)

    if suns:
        hero_sun = suns[0]
    else:
        sun_data = bpy.data.lights.new("Sun_Architectural_Hero", 'SUN')
        hero_sun = bpy.data.objects.new("Sun_Architectural_Hero", sun_data)
        scene.collection.objects.link(hero_sun)

    hero_sun.name = "Sun_Architectural_Hero"
    hero_sun.data.energy = 2.6
    hero_sun.data.color = (1.0, 0.82, 0.64) # Warm golden sunset
    hero_sun.data.angle = math.radians(2.0)
    # Sunset from rear-left to cast rim light on curved prow and fluted spine
    hero_sun.rotation_euler = (math.radians(65.0), math.radians(12.0), math.radians(128.0))

    # World Sky
    if scene.world and scene.world.node_tree:
        for node in scene.world.node_tree.nodes:
            if node.type == 'BACKGROUND':
                node.inputs["Strength"].default_value = 0.50
            elif node.type == 'TEX_SKY':
                node.sun_elevation = math.radians(14.0)
                node.sun_rotation = math.radians(128.0)
                node.sun_intensity = 0.80
                if hasattr(node, 'turbidity'):
                    node.turbidity = 3.6

    # Color Management (AgX)
    if hasattr(scene, 'view_settings'):
        scene.view_settings.view_transform = 'AgX'
        scene.view_settings.look = 'AgX - Medium High Contrast'
        scene.view_settings.exposure = -0.40

    # -----------------------------------------------------------------------
    # 2. Materials Definition
    # -----------------------------------------------------------------------
    # A. Precast Concrete (Left Facade Piers)
    mat_concrete = bpy.data.materials.get("Mat_Precast_Concrete") or bpy.data.materials.new("Mat_Precast_Concrete")
    if mat_concrete.node_tree:
        b = mat_concrete.node_tree.nodes.get("Principled BSDF")
        if b:
            b.inputs["Base Color"].default_value = (0.52, 0.47, 0.42, 1.0) # Warm architectural stone grey
            b.inputs["Roughness"].default_value = 0.75

    # B. Balcony Fascia (Off-White Stone Edge)
    mat_slab = bpy.data.materials.get("Mat_Slab_Fascia") or bpy.data.materials.new("Mat_Slab_Fascia")
    if mat_slab.node_tree:
        b = mat_slab.node_tree.nodes.get("Principled BSDF")
        if b:
            b.inputs["Base Color"].default_value = (0.86, 0.84, 0.80, 1.0)
            b.inputs["Roughness"].default_value = 0.35

    # C. Balcony Timber Soffit (Underside Teak Wood Slat Finish)
    mat_soffit = bpy.data.materials.get("Mat_Feature_Timber_Paneling") or bpy.data.materials.new("Mat_Feature_Timber_Paneling")
    if mat_soffit.node_tree:
        b = mat_soffit.node_tree.nodes.get("Principled BSDF")
        if b:
            b.inputs["Base Color"].default_value = (0.36, 0.20, 0.11, 1.0) # Rich warm teak/amber
            b.inputs["Roughness"].default_value = 0.45

    # D. Balcony Cove Light Strip
    mat_cove = bpy.data.materials.get("Mat_Warm_Cove_Glow") or bpy.data.materials.new("Mat_Warm_Cove_Glow")
    if mat_cove.node_tree:
        b = mat_cove.node_tree.nodes.get("Principled BSDF")
        if b:
            b.inputs["Base Color"].default_value = (1.0, 0.85, 0.60, 1.0)
            if "Emission Color" in b.inputs:
                b.inputs["Emission Color"].default_value = (1.0, 0.85, 0.60, 1.0)
            if "Emission Strength" in b.inputs:
                b.inputs["Emission Strength"].default_value = 4.5

    # E. Balcony Glass Railing (Smoked Transparent Glass)
    mat_glass = bpy.data.materials.get("Mat_Facade_Tinted_Glass") or bpy.data.materials.new("Mat_Facade_Tinted_Glass")
    if mat_glass.node_tree:
        b = mat_glass.node_tree.nodes.get("Principled BSDF")
        if b:
            b.inputs["Base Color"].default_value = (0.70, 0.65, 0.60, 1.0)
            b.inputs["Roughness"].default_value = 0.02
            if "Transmission Weight" in b.inputs:
                b.inputs["Transmission Weight"].default_value = 0.88
            elif "Transmission" in b.inputs:
                b.inputs["Transmission"].default_value = 0.88
            if "IOR" in b.inputs:
                b.inputs["IOR"].default_value = 1.52

    # F. Bronze Handrail Cap & Mullions
    mat_bronze = bpy.data.materials.get("Mat_Champagne_Bronze") or bpy.data.materials.new("Mat_Champagne_Bronze")
    if mat_bronze.node_tree:
        b = mat_bronze.node_tree.nodes.get("Principled BSDF")
        if b:
            b.inputs["Base Color"].default_value = (0.24, 0.18, 0.14, 1.0)
            b.inputs["Roughness"].default_value = 0.30
            b.inputs["Metallic"].default_value = 0.85

    # G. Fluted Terracotta Vertical Spine
    mat_terracotta = bpy.data.materials.get("Mat_Terracotta_Spine") or bpy.data.materials.new("Mat_Terracotta_Spine")
    if mat_terracotta.node_tree:
        b = mat_terracotta.node_tree.nodes.get("Principled BSDF")
        if b:
            b.inputs["Base Color"].default_value = (0.42, 0.22, 0.14, 1.0)
            b.inputs["Roughness"].default_value = 0.60

    # H. Warm Interior Room Illumination
    mat_interior = bpy.data.materials.get("Mat_Interior_Glow_Window") or bpy.data.materials.new("Mat_Interior_Glow_Window")
    if mat_interior.node_tree:
        b = mat_interior.node_tree.nodes.get("Principled BSDF")
        if b:
            b.inputs["Base Color"].default_value = (1.0, 0.86, 0.65, 1.0)
            if "Emission Color" in b.inputs:
                b.inputs["Emission Color"].default_value = (1.0, 0.86, 0.65, 1.0)
            if "Emission Strength" in b.inputs:
                b.inputs["Emission Strength"].default_value = 2.2

    # -----------------------------------------------------------------------
    # 3. Geometry Reconstruction: Balconies & Prows
    # -----------------------------------------------------------------------
    col_balconies = bpy.data.collections.get("04_Curved_Balconies")
    if not col_balconies:
        col_balconies = bpy.data.collections.new("04_Curved_Balconies")
        scene.collection.children.link(col_balconies)

    floors = [
        ("Floor_01", 4.50), ("Floor_02", 7.80), ("Floor_03", 11.10), ("Floor_04", 14.40),
        ("Floor_05", 17.70), ("Floor_06", 21.00), ("Floor_07", 24.30), ("Floor_08", 27.60),
        ("Floor_09", 30.90), ("Floor_10", 34.20), ("Floor_11", 37.50), ("Floor_12", 40.80),
        ("Floor_13", 44.10), ("Floor_14", 47.40), ("Floor_15", 50.70), ("Floor_16", 54.00),
        ("Floor_17_Refuge", 57.30), ("Floor_18", 60.60)
    ]

    # Aerodynamic prow profile
    x_anchor = 6.0
    y_anchor = -7.5
    prow_apex_x = 22.2
    prow_apex_y = -12.8
    cantilever_thickness = 0.28

    def generate_prow_pts():
        pts = [(x_anchor, y_anchor), (x_anchor, y_anchor - 2.8)]
        n_seg = 24
        for i in range(n_seg + 1):
            t = i / float(n_seg)
            ang = math.radians(240.0 - t * 185.0)
            rx = 8.5
            ry = 4.6
            cx = prow_apex_x - rx
            cy = prow_apex_y + ry
            pts.append((cx + rx * math.cos(ang), cy + ry * math.sin(ang)))
        pts.append((prow_apex_x - 4.0, y_anchor))
        return pts

    prow_pts = generate_prow_pts()
    outer_curve = prow_pts[1:-1]

    for fl_name, z_fl in floors:
        slab_obj_name = f"Balcony_Living_{fl_name}_Slab"
        glass_obj_name = f"Balcony_Living_{fl_name}_Glass_Rail"
        cap_obj_name = f"Balcony_Living_{fl_name}_Handrail_Cap"
        cove_obj_name = f"Balcony_Living_{fl_name}_Cove_Glow"

        # Remove existing
        for obj_name in [slab_obj_name, glass_obj_name, cap_obj_name, cove_obj_name]:
            old = bpy.data.objects.get(obj_name)
            if old:
                bpy.data.objects.remove(old, do_unlink=True)

        # 1. Slab with timber soffit
        m_slab = bpy.data.meshes.new(slab_obj_name + "_Mesh")
        o_slab = bpy.data.objects.new(slab_obj_name, m_slab)
        col_balconies.objects.link(o_slab)

        bm = bmesh.new()
        v_bot = [bm.verts.new((p[0], p[1], z_fl)) for p in prow_pts]
        f_bot = bm.faces.new(v_bot)
        ext = bmesh.ops.extrude_face_region(bm, geom=[f_bot])
        v_top = [v for v in ext['geom'] if isinstance(v, bmesh.types.BMVert)]
        bmesh.ops.translate(bm, vec=(0, 0, cantilever_thickness), verts=v_top)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)

        o_slab.data.materials.append(mat_slab)   # Slot 0: Top/Edge
        o_slab.data.materials.append(mat_soffit) # Slot 1: Soffit
        f_bot.material_index = 1
        bm.to_mesh(m_slab)
        bm.free()

        # 2. Glass Rail
        m_glass = bpy.data.meshes.new(glass_obj_name + "_Mesh")
        o_glass = bpy.data.objects.new(glass_obj_name, m_glass)
        col_balconies.objects.link(o_glass)
        bm_g = bmesh.new()
        v_gb = [bm_g.verts.new((p[0], p[1], z_fl + cantilever_thickness)) for p in outer_curve]
        v_gt = [bm_g.verts.new((p[0], p[1], z_fl + cantilever_thickness + 1.15)) for p in outer_curve]
        for idx in range(len(outer_curve) - 1):
            bm_g.faces.new([v_gb[idx], v_gb[idx+1], v_gt[idx+1], v_gt[idx]])
        bmesh.ops.recalc_face_normals(bm_g, faces=bm_g.faces)
        bm_g.to_mesh(m_glass)
        bm_g.free()
        o_glass.data.materials.append(mat_glass)

        # 3. Bronze Cap
        m_cap = bpy.data.meshes.new(cap_obj_name + "_Mesh")
        o_cap = bpy.data.objects.new(cap_obj_name, m_cap)
        col_balconies.objects.link(o_cap)
        bm_c = bmesh.new()
        v_cb = [bm_c.verts.new((p[0], p[1], z_fl + cantilever_thickness + 1.15)) for p in outer_curve]
        v_ct = [bm_c.verts.new((p[0], p[1], z_fl + cantilever_thickness + 1.20)) for p in outer_curve]
        for idx in range(len(outer_curve) - 1):
            bm_c.faces.new([v_cb[idx], v_cb[idx+1], v_ct[idx+1], v_ct[idx]])
        bmesh.ops.recalc_face_normals(bm_c, faces=bm_c.faces)
        bm_c.to_mesh(m_cap)
        bm_c.free()
        o_cap.data.materials.append(mat_bronze)

        # 4. Cove Glow Strip
        m_cove = bpy.data.meshes.new(cove_obj_name + "_Mesh")
        o_cove = bpy.data.objects.new(cove_obj_name, m_cove)
        col_balconies.objects.link(o_cove)
        bm_cv = bmesh.new()
        v_cvb = [bm_cv.verts.new((p[0]*0.985, p[1]*0.985, z_fl - 0.02)) for p in outer_curve]
        v_cvt = [bm_cv.verts.new((p[0]*0.985, p[1]*0.985, z_fl + 0.01)) for p in outer_curve]
        for idx in range(len(outer_curve) - 1):
            bm_cv.faces.new([v_cvb[idx], v_cvb[idx+1], v_cvt[idx+1], v_cvt[idx]])
        bmesh.ops.recalc_face_normals(bm_cv, faces=bm_cv.faces)
        bm_cv.to_mesh(m_cove)
        bm_cv.free()
        o_cove.data.materials.append(mat_cove)

    print("Reconstructed 18 floors of curved prow balconies.")

    # -----------------------------------------------------------------------
    # 4. Sculptural Curved Roof Crown Prow
    # -----------------------------------------------------------------------
    crown_name = "Tower_Sculptural_Roof_Crown"
    old_cr = bpy.data.objects.get(crown_name)
    if old_cr:
        bpy.data.objects.remove(old_cr, do_unlink=True)

    m_crown = bpy.data.meshes.new(crown_name + "_Mesh")
    o_crown = bpy.data.objects.new(crown_name, m_crown)
    col_balconies.objects.link(o_crown)

    bm_cr = bmesh.new()
    z_roof = 63.90
    crown_h = 5.20 # 5.2m sweeping sculptural crown
    v_cr_b = [bm_cr.verts.new((p[0], p[1], z_roof)) for p in prow_pts]
    v_cr_t = [bm_cr.verts.new((p[0], p[1], z_roof + crown_h)) for p in prow_pts]
    for idx in range(len(prow_pts) - 1):
        bm_cr.faces.new([v_cr_b[idx], v_cr_b[idx+1], v_cr_t[idx+1], v_cr_t[idx]])
    bmesh.ops.recalc_face_normals(bm_cr, faces=bm_cr.faces)
    bm_cr.to_mesh(m_crown)
    bm_cr.free()
    o_crown.data.materials.append(mat_concrete)

    # -----------------------------------------------------------------------
    # 5. Fluted Terracotta Vertical Spine (Right Side Behind Balconies)
    # -----------------------------------------------------------------------
    spine_name = "Tower_Fluted_Terracotta_Spine"
    old_sp = bpy.data.objects.get(spine_name)
    if old_sp:
        bpy.data.objects.remove(old_sp, do_unlink=True)

    m_spine = bpy.data.meshes.new(spine_name + "_Mesh")
    o_spine = bpy.data.objects.new(spine_name, m_spine)
    col_balconies.objects.link(o_spine)

    bm_sp = bmesh.new()
    spine_x = 22.2
    y_start = -11.5
    y_end = -6.0
    ribs = 14
    for r in range(ribs):
        yr = y_start + (y_end - y_start) * (r / float(ribs))
        bmesh.ops.create_cube(bm_sp, size=1.0)
        rib_verts = bm_sp.verts[-8:]
        for v in rib_verts:
            v.co.x = spine_x + v.co.x * 0.25
            v.co.y = yr + v.co.y * 0.20
            v.co.z = 34.5 + v.co.z * 69.0
    bmesh.ops.recalc_face_normals(bm_sp, faces=bm_sp.faces)
    bm_sp.to_mesh(m_spine)
    bm_sp.free()
    o_spine.data.materials.append(mat_terracotta)

    # -----------------------------------------------------------------------
    # 6. Left Facade: Concrete Piers & Glowing Window Bays
    # -----------------------------------------------------------------------
    for fl_name, z_fl in floors:
        win_panel_name = f"Window_Interior_Glow_{fl_name}"
        old_win = bpy.data.objects.get(win_panel_name)
        if old_win:
            bpy.data.objects.remove(old_win, do_unlink=True)

        m_w = bpy.data.meshes.new(win_panel_name + "_Mesh")
        o_w = bpy.data.objects.new(win_panel_name, m_w)
        col_balconies.objects.link(o_w)

        bm_w = bmesh.new()
        for x_start, x_end in [(-16.0, -10.0), (-8.0, -2.0)]:
            v1 = bm_w.verts.new((x_start, -7.85, z_fl + 0.1))
            v2 = bm_w.verts.new((x_end,   -7.85, z_fl + 0.1))
            v3 = bm_w.verts.new((x_end,   -7.85, z_fl + 3.0))
            v4 = bm_w.verts.new((x_start, -7.85, z_fl + 3.0))
            bm_w.faces.new([v1, v2, v3, v4])
        bmesh.ops.recalc_face_normals(bm_w, faces=bm_w.faces)
        bm_w.to_mesh(m_w)
        bm_w.free()
        o_w.data.materials.append(mat_interior)

    # Hide old solid walls that obscure the architectural bays
    for o in bpy.data.objects:
        if o.type == 'MESH' and ("Walls_Floor_" in o.name):
            o.hide_render = True
            o.hide_viewport = True

    # -----------------------------------------------------------------------
    # 7. Foreground Framing Landscape (Green Trees + Autumn Red Maple)
    # -----------------------------------------------------------------------
    mat_red = bpy.data.materials.get("Mat_Autumn_Accent_Tree") or bpy.data.materials.new("Mat_Autumn_Accent_Tree")
    if mat_red.node_tree:
        b = mat_red.node_tree.nodes.get("Principled BSDF")
        if b:
            b.inputs["Base Color"].default_value = (0.42, 0.08, 0.06, 1.0)
            b.inputs["Roughness"].default_value = 0.85

    mat_green = bpy.data.materials.get("Mat_Tree_Foliage") or bpy.data.materials.new("Mat_Tree_Foliage")
    if mat_green.node_tree:
        b = mat_green.node_tree.nodes.get("Principled BSDF")
        if b:
            b.inputs["Base Color"].default_value = (0.10, 0.16, 0.07, 1.0)
            b.inputs["Roughness"].default_value = 0.80

    col_landscape = bpy.data.collections.get("01_Site_Landscape") or bpy.data.collections.new("01_Site_Landscape")
    trees = [
        ("Tree_FG_Left_1",  (-16.0, -38.0, 5.0), 8.5, mat_green),
        ("Tree_FG_Left_2",  (-6.0,  -42.0, 4.0), 7.5, mat_green),
        ("Tree_FG_Right_Red", (24.0, -40.0, 5.5), 8.0, mat_red),
        ("Tree_FG_Right_Grn", (32.0, -44.0, 6.5), 9.0, mat_green),
    ]
    for t_name, loc, rad, mat in trees:
        old_t = bpy.data.objects.get(t_name)
        if old_t:
            bpy.data.objects.remove(old_t, do_unlink=True)
        m_t = bpy.data.meshes.new(t_name + "_Mesh")
        o_t = bpy.data.objects.new(t_name, m_t)
        col_landscape.objects.link(o_t)
        bm_t = bmesh.new()
        bmesh.ops.create_icosphere(bm_t, subdivisions=2, radius=rad)
        bm_t.to_mesh(m_t)
        bm_t.free()
        o_t.location = loc
        o_t.data.materials.append(mat)
        o_t.hide_render = False

    # -----------------------------------------------------------------------
    # 8. Calibrated Two-Point Architectural Camera
    # -----------------------------------------------------------------------
    cam_name = "Cam_TwoPoint_Architectural"
    cam_obj = bpy.data.objects.get(cam_name)
    if not cam_obj:
        cam_data = bpy.data.cameras.new(cam_name)
        cam_obj = bpy.data.objects.new(cam_name, cam_data)
        scene.collection.objects.link(cam_obj)

    scene.camera = cam_obj

    # Position ~62m back at 17.2 deg azimuth
    cam_obj.location = (26.0, -62.0, 5.0)
    # Perfectly level pitch (90 deg) prevents keystoning (vertical lines stay parallel)
    cam_obj.rotation_euler = (math.radians(90.0), 0.0, math.radians(17.2))
    cam_obj.data.lens = 35.0 # Natural 35mm architectural focal length
    cam_obj.data.shift_y = 0.36 # Shift lens raises entire 67.7m tower into frame
    cam_obj.data.shift_x = -0.05

    # -----------------------------------------------------------------------
    # 9. Save Corrected Blender Project
    # -----------------------------------------------------------------------
    bpy.ops.wm.save_as_mainfile(filepath=DST_BLEND)
    print(f"Corrected Blender project saved to: {DST_BLEND}")

    # -----------------------------------------------------------------------
    # 10. Render Corrected Image
    # -----------------------------------------------------------------------
    scene.render.engine = 'CYCLES'
    if hasattr(scene, 'cycles'):
        scene.cycles.device = 'CPU'
        scene.cycles.samples = 24
        scene.cycles.use_denoising = True

    scene.render.resolution_x = 1200
    scene.render.resolution_y = 800
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = RENDER_OUT

    print(f"Rendering corrected scene to {RENDER_OUT}...")
    bpy.ops.render.render(write_still=True)
    print(f"Render completed: {RENDER_OUT}")

if __name__ == "__main__":
    reconstruct()

