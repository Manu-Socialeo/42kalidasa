"""
KALIDASA 42 - Architectural Remodeling & Calibration v007
Faithfully sculpts the 3D Blender model to match the approved reference photograph:
1. Sweeping aerodynamic curved prow balconies with warm timber soffits
2. Recessed golden cove lighting glowing under every balcony
3. Sculptural curved roof crown / prow rising above the skyline
4. Fluted terracotta / copper architectural vertical spine on the right
5. Architectural exposed concrete facade with floor-to-ceiling warm glowing windows on the left
6. Natural tree canopy framing at the base (including autumn red accent tree)
7. Golden hour sunset lighting with warm rim light and two-point perspective camera
"""

import bpy
import bmesh
import math
import os

WORKSPACE = r"C:\Users\manpr\Documents\42 Kalidasa"
BLEND_PATH = os.path.join(WORKSPACE, "blender", "kalidasa42_animated_v001.blend")
RENDER_OUT = os.path.join(WORKSPACE, "renders", "preview", "exterior_photo_match_render_v007.png")
COMPARISON_OUT = os.path.join(WORKSPACE, "renders", "preview", "exterior_comparison_side_by_side_v007.png")
REF_PHOTO = os.path.join(WORKSPACE, "assets", "WhatsApp Image 2026-10-27 at 11.30.09 AM.jpeg")

def run_remodel():
    print(f"Loading {BLEND_PATH}...")
    bpy.ops.wm.open_mainfile(filepath=BLEND_PATH)
    scene = bpy.context.scene

    # -------------------------------------------------------------
    # 1. PBR Materials Calibration
    # -------------------------------------------------------------
    # A. Warm Timber Soffit (underside of balconies)
    mat_soffit = bpy.data.materials.get("Mat_Feature_Timber_Paneling") or bpy.data.materials.new("Mat_Feature_Timber_Paneling")
    mat_soffit.use_nodes = True
    bsdf = mat_soffit.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (0.38, 0.22, 0.12, 1.0) # Rich warm teak/amber timber
        bsdf.inputs["Roughness"].default_value = 0.45
        bsdf.inputs["Metallic"].default_value = 0.05

    # B. Balcony Cove Light Emission
    mat_cove = bpy.data.materials.get("Mat_Warm_Cove_Glow") or bpy.data.materials.new("Mat_Warm_Cove_Glow")
    mat_cove.use_nodes = True
    bsdf_c = mat_cove.node_tree.nodes.get("Principled BSDF")
    if bsdf_c:
        bsdf_c.inputs["Base Color"].default_value = (1.0, 0.85, 0.60, 1.0)
        if "Emission Color" in bsdf_c.inputs:
            bsdf_c.inputs["Emission Color"].default_value = (1.0, 0.85, 0.60, 1.0)
        if "Emission Strength" in bsdf_c.inputs:
            bsdf_c.inputs["Emission Strength"].default_value = 4.5

    # C. Balcony Glass: Transparent smoked bronze/grey architectural glass
    mat_glass = bpy.data.materials.get("Mat_Facade_Tinted_Glass") or bpy.data.materials.new("Mat_Facade_Tinted_Glass")
    mat_glass.use_nodes = True
    bsdf_g = mat_glass.node_tree.nodes.get("Principled BSDF")
    if bsdf_g:
        bsdf_g.inputs["Base Color"].default_value = (0.75, 0.70, 0.65, 1.0)
        bsdf_g.inputs["Roughness"].default_value = 0.02
        if "Transmission Weight" in bsdf_g.inputs:
            bsdf_g.inputs["Transmission Weight"].default_value = 0.88
        elif "Transmission" in bsdf_g.inputs:
            bsdf_g.inputs["Transmission"].default_value = 0.88
        if "IOR" in bsdf_g.inputs:
            bsdf_g.inputs["IOR"].default_value = 1.52

    # D. Handrail Cap: Champagne bronze
    mat_bronze = bpy.data.materials.get("Mat_Champagne_Bronze") or bpy.data.materials.new("Mat_Champagne_Bronze")
    mat_bronze.use_nodes = True
    bsdf_b = mat_bronze.node_tree.nodes.get("Principled BSDF")
    if bsdf_b:
        bsdf_b.inputs["Base Color"].default_value = (0.28, 0.22, 0.17, 1.0)
        bsdf_b.inputs["Roughness"].default_value = 0.30
        bsdf_b.inputs["Metallic"].default_value = 0.85

    # E. Balcony Slab Fascia / Edge: Refined architectural off-white stone
    mat_slab = bpy.data.materials.get("Mat_Slab_Fascia") or bpy.data.materials.new("Mat_Slab_Fascia")
    mat_slab.use_nodes = True
    bsdf_s = mat_slab.node_tree.nodes.get("Principled BSDF")
    if bsdf_s:
        bsdf_s.inputs["Base Color"].default_value = (0.85, 0.82, 0.78, 1.0)
        bsdf_s.inputs["Roughness"].default_value = 0.35

    # F. Fluted Terracotta Vertical Spine
    mat_terracotta = bpy.data.materials.get("Mat_Terracotta_Spine") or bpy.data.materials.new("Mat_Terracotta_Spine")
    mat_terracotta.use_nodes = True
    bsdf_t = mat_terracotta.node_tree.nodes.get("Principled BSDF")
    if bsdf_t:
        bsdf_t.inputs["Base Color"].default_value = (0.44, 0.23, 0.15, 1.0)
        bsdf_t.inputs["Roughness"].default_value = 0.65
        bsdf_t.inputs["Metallic"].default_value = 0.10

    # G. Left Facade Exposed Concrete
    mat_concrete = bpy.data.materials.get("Mat_Precast_Concrete") or bpy.data.materials.new("Mat_Precast_Concrete")
    mat_concrete.use_nodes = True
    bsdf_conc = mat_concrete.node_tree.nodes.get("Principled BSDF")
    if bsdf_conc:
        bsdf_conc.inputs["Base Color"].default_value = (0.50, 0.46, 0.41, 1.0)
        bsdf_conc.inputs["Roughness"].default_value = 0.78

    # H. Interior Warm Room Illumination (Floor-to-ceiling windows)
    mat_interior = bpy.data.materials.get("Mat_Interior_Glow_Window") or bpy.data.materials.new("Mat_Interior_Glow_Window")
    mat_interior.use_nodes = True
    bsdf_in = mat_interior.node_tree.nodes.get("Principled BSDF")
    if bsdf_in:
        bsdf_in.inputs["Base Color"].default_value = (1.0, 0.88, 0.68, 1.0)
        if "Emission Color" in bsdf_in.inputs:
            bsdf_in.inputs["Emission Color"].default_value = (1.0, 0.88, 0.68, 1.0)
        if "Emission Strength" in bsdf_in.inputs:
            bsdf_in.inputs["Emission Strength"].default_value = 2.2

    # -------------------------------------------------------------
    # 2. Reshape Curved Balconies to Sweeping Aerodynamic Prow
    # -------------------------------------------------------------
    col_balconies = bpy.data.collections.get("04_Curved_Balconies")
    if not col_balconies:
        col_balconies = bpy.data.collections.new("04_Curved_Balconies")
        scene.collection.children.link(col_balconies)

    # Floor levels 1 to 18
    # FFL heights from 4.5m up to 60.6m in steps of 3.3m
    floors = [
        ("Floor_01", 4.50), ("Floor_02", 7.80), ("Floor_03", 11.10), ("Floor_04", 14.40),
        ("Floor_05", 17.70), ("Floor_06", 21.00), ("Floor_07", 24.30), ("Floor_08", 27.60),
        ("Floor_09", 30.90), ("Floor_10", 34.20), ("Floor_11", 37.50), ("Floor_12", 40.80),
        ("Floor_13", 44.10), ("Floor_14", 47.40), ("Floor_15", 50.70), ("Floor_16", 54.00),
        ("Floor_17_Refuge", 57.30), ("Floor_18", 60.60)
    ]

    # Generate aerodynamic curved prow curve
    # The corner prow is on the right of the South facade:
    # X ranges from ~6.0m to ~22.5m, Y ranges from -13.5m to -7.5m
    x_anchor = 6.0
    y_anchor = -7.5
    prow_apex_x = 22.2
    prow_apex_y = -12.8
    cantilever_thickness = 0.28

    def generate_prow_polygon():
        pts = []
        pts.append((x_anchor, y_anchor))
        # Straight wall back connection
        pts.append((x_anchor, y_anchor - 2.8))
        # Smooth outward curve to prow
        # Spline curve points towards apex
        n_seg = 20
        # Curved transition towards prow apex
        for i in range(n_seg + 1):
            t = i / float(n_seg)
            # Cubic bezier or elliptical parameterization
            # Start at (x_anchor, y_anchor - 2.8), sweep out to apex (prow_apex_x, prow_apex_y), then wrap back to (prow_apex_x - 3.5, y_anchor)
            # Angle from 270 deg around to 45 deg
            ang = math.radians(240.0 - t * 185.0)
            rx = 8.5
            ry = 4.6
            cx = prow_apex_x - rx
            cy = prow_apex_y + ry
            px = cx + rx * math.cos(ang)
            py = cy + ry * math.sin(ang)
            pts.append((px, py))
        pts.append((prow_apex_x - 4.0, y_anchor))
        return pts

    prow_pts = generate_prow_polygon()

    for fl_name, z_fl in floors:
        slab_obj_name = f"Balcony_Living_{fl_name}_Slab"
        glass_obj_name = f"Balcony_Living_{fl_name}_Glass_Rail"
        cap_obj_name = f"Balcony_Living_{fl_name}_Handrail_Cap"
        cove_obj_name = f"Balcony_Living_{fl_name}_Cove_Glow"

        # Remove old meshes if existing
        for obj_name in [slab_obj_name, glass_obj_name, cap_obj_name, cove_obj_name]:
            old_obj = bpy.data.objects.get(obj_name)
            if old_obj:
                bpy.data.objects.remove(old_obj, do_unlink=True)

        # 1. Slab with warm timber soffit + white fascia
        mesh_slab = bpy.data.meshes.new(slab_obj_name + "_Mesh")
        slab_obj = bpy.data.objects.new(slab_obj_name, mesh_slab)
        col_balconies.objects.link(slab_obj)

        bm = bmesh.new()
        v_bot = [bm.verts.new((p[0], p[1], z_fl)) for p in prow_pts]
        f_bot = bm.faces.new(v_bot)
        ext = bmesh.ops.extrude_face_region(bm, geom=[f_bot])
        v_top = [v for v in ext['geom'] if isinstance(v, bmesh.types.BMVert)]
        bmesh.ops.translate(bm, vec=(0, 0, cantilever_thickness), verts=v_top)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        
        # Material slot 0: Fascia/top, Slot 1: Soffit
        slab_obj.data.materials.append(mat_slab)
        slab_obj.data.materials.append(mat_soffit)
        f_bot.material_index = 1 # Bottom face has warm timber soffit!
        
        bm.to_mesh(mesh_slab)
        bm.free()

        # 2. Outer curved perimeter for Glass Rail, Handrail Cap, and Cove Glow
        outer_curve = prow_pts[1:-1] # The projected perimeter

        # 3. Glass Rail
        mesh_glass = bpy.data.meshes.new(glass_obj_name + "_Mesh")
        glass_obj = bpy.data.objects.new(glass_obj_name, mesh_glass)
        col_balconies.objects.link(glass_obj)
        bm_g = bmesh.new()
        v_gb = [bm_g.verts.new((p[0], p[1], z_fl + cantilever_thickness)) for p in outer_curve]
        v_gt = [bm_g.verts.new((p[0], p[1], z_fl + cantilever_thickness + 1.15)) for p in outer_curve]
        for idx in range(len(outer_curve) - 1):
            bm_g.faces.new([v_gb[idx], v_gb[idx+1], v_gt[idx+1], v_gt[idx]])
        bmesh.ops.recalc_face_normals(bm_g, faces=bm_g.faces)
        bm_g.to_mesh(mesh_glass)
        bm_g.free()
        glass_obj.data.materials.append(mat_glass)

        # 4. Handrail Cap (Champagne Bronze)
        mesh_cap = bpy.data.meshes.new(cap_obj_name + "_Mesh")
        cap_obj = bpy.data.objects.new(cap_obj_name, mesh_cap)
        col_balconies.objects.link(cap_obj)
        bm_c = bmesh.new()
        cap_h = 0.05
        v_cb = [bm_c.verts.new((p[0], p[1], z_fl + cantilever_thickness + 1.15)) for p in outer_curve]
        v_ct = [bm_c.verts.new((p[0], p[1], z_fl + cantilever_thickness + 1.15 + cap_h)) for p in outer_curve]
        for idx in range(len(outer_curve) - 1):
            bm_c.faces.new([v_cb[idx], v_cb[idx+1], v_ct[idx+1], v_ct[idx]])
        bmesh.ops.recalc_face_normals(bm_c, faces=bm_c.faces)
        bm_c.to_mesh(mesh_cap)
        bm_c.free()
        cap_obj.data.materials.append(mat_bronze)

        # 5. Recessed Golden Cove Light Strip under balcony
        mesh_cove = bpy.data.meshes.new(cove_obj_name + "_Mesh")
        cove_obj = bpy.data.objects.new(cove_obj_name, mesh_cove)
        col_balconies.objects.link(cove_obj)
        bm_cv = bmesh.new()
        # Offset slightly inward along the soffit perimeter
        v_cvb = [bm_cv.verts.new((p[0]*0.985, p[1]*0.985, z_fl - 0.02)) for p in outer_curve]
        v_cvt = [bm_cv.verts.new((p[0]*0.985, p[1]*0.985, z_fl + 0.01)) for p in outer_curve]
        for idx in range(len(outer_curve) - 1):
            bm_cv.faces.new([v_cvb[idx], v_cvb[idx+1], v_cvt[idx+1], v_cvt[idx]])
        bmesh.ops.recalc_face_normals(bm_cv, faces=bm_cv.faces)
        bm_cv.to_mesh(mesh_cove)
        bm_cv.free()
        cove_obj.data.materials.append(mat_cove)

    print(f"Reshaped {len(floors)} curved prow balconies with timber soffits and cove glows.")

    # -------------------------------------------------------------
    # 3. Sculptural Curved Roof Crown / Prow
    # -------------------------------------------------------------
    crown_name = "Tower_Sculptural_Roof_Crown"
    old_crown = bpy.data.objects.get(crown_name)
    if old_crown:
        bpy.data.objects.remove(old_crown, do_unlink=True)

    mesh_crown = bpy.data.meshes.new(crown_name + "_Mesh")
    crown_obj = bpy.data.objects.new(crown_name, mesh_crown)
    col_balconies.objects.link(crown_obj)

    bm_cr = bmesh.new()
    z_roof = 63.90
    crown_h = 4.80 # 4.8m tall sculptural crown rising gracefully above top floor
    v_cr_b = [bm_cr.verts.new((p[0], p[1], z_roof)) for p in prow_pts]
    v_cr_t = [bm_cr.verts.new((p[0], p[1], z_roof + crown_h)) for p in prow_pts]
    for idx in range(len(prow_pts) - 1):
        bm_cr.faces.new([v_cr_b[idx], v_cr_b[idx+1], v_cr_t[idx+1], v_cr_t[idx]])
    bmesh.ops.recalc_face_normals(bm_cr, faces=bm_cr.faces)
    bm_cr.to_mesh(mesh_crown)
    bm_cr.free()
    crown_obj.data.materials.append(mat_concrete)
    print("Sculptural roof crown created successfully.")

    # -------------------------------------------------------------
    # 4. Fluted Terracotta Vertical Spine (Right Edge Behind Balconies)
    # -------------------------------------------------------------
    spine_name = "Tower_Fluted_Terracotta_Spine"
    old_spine = bpy.data.objects.get(spine_name)
    if old_spine:
        bpy.data.objects.remove(old_spine, do_unlink=True)

    mesh_spine = bpy.data.meshes.new(spine_name + "_Mesh")
    spine_obj = bpy.data.objects.new(spine_name, mesh_spine)
    col_balconies.objects.link(spine_obj)

    bm_sp = bmesh.new()
    # Fluted vertical pilaster strip along the right boundary: X ~ 22.0, Y from -12.5 to -6.5, Z from 0.0 to 68.7m
    spine_x = 22.2
    y_start = -11.5
    y_end = -6.0
    ribs = 14
    for r in range(ribs):
        yr = y_start + (y_end - y_start) * (r / float(ribs))
        # Small projecting fluted rib
        bmesh.ops.create_cube(bm_sp, size=1.0)
        # Scale and position rib
        rib_verts = bm_sp.verts[-8:]
        for v in rib_verts:
            v.co.x = spine_x + v.co.x * 0.25
            v.co.y = yr + v.co.y * 0.20
            v.co.z = 34.35 + v.co.z * 68.7
    bmesh.ops.recalc_face_normals(bm_sp, faces=bm_sp.faces)
    bm_sp.to_mesh(mesh_spine)
    bm_sp.free()
    spine_obj.data.materials.append(mat_terracotta)
    print("Fluted terracotta vertical spine created.")

    # -------------------------------------------------------------
    # 5. Left Facade Window Bays with Warm Interior Illumination
    # -------------------------------------------------------------
    # Floor-to-ceiling glowing window panels on the left facade (X from -18.0 to +4.0)
    for fl_name, z_fl in floors:
        win_panel_name = f"Window_Interior_Glow_{fl_name}"
        old_win = bpy.data.objects.get(win_panel_name)
        if old_win:
            bpy.data.objects.remove(old_win, do_unlink=True)
            
        mesh_w = bpy.data.meshes.new(win_panel_name + "_Mesh")
        obj_w = bpy.data.objects.new(win_panel_name, mesh_w)
        col_balconies.objects.link(obj_w)
        
        bm_w = bmesh.new()
        # Bay 1 (X: -16.0 to -10.0), Bay 2 (X: -8.0 to -2.0)
        for x_start, x_end in [(-16.0, -10.0), (-8.0, -2.0)]:
            v1 = bm_w.verts.new((x_start, -7.85, z_fl + 0.1))
            v2 = bm_w.verts.new((x_end,   -7.85, z_fl + 0.1))
            v3 = bm_w.verts.new((x_end,   -7.85, z_fl + 3.0))
            v4 = bm_w.verts.new((x_start, -7.85, z_fl + 3.0))
            bm_w.faces.new([v1, v2, v3, v4])
            
        bmesh.ops.recalc_face_normals(bm_w, faces=bm_w.faces)
        bm_w.to_mesh(mesh_w)
        bm_w.free()
        obj_w.data.materials.append(mat_interior)

    # -------------------------------------------------------------
    # 6. Foreground Framing Foliage (Green Canopies + Autumn Red Maple)
    # -------------------------------------------------------------
    # Material for Autumn Red Tree on lower right
    mat_red_tree = bpy.data.materials.get("Mat_Autumn_Accent_Tree") or bpy.data.materials.new("Mat_Autumn_Accent_Tree")
    mat_red_tree.use_nodes = True
    bsdf_rt = mat_red_tree.node_tree.nodes.get("Principled BSDF")
    if bsdf_rt:
        bsdf_rt.inputs["Base Color"].default_value = (0.45, 0.08, 0.06, 1.0) # Deep autumnal crimson red
        bsdf_rt.inputs["Roughness"].default_value = 0.85

    mat_green_tree = bpy.data.materials.get("Mat_Tree_Foliage") or bpy.data.materials.new("Mat_Tree_Foliage")
    mat_green_tree.use_nodes = True
    bsdf_gt = mat_green_tree.node_tree.nodes.get("Principled BSDF")
    if bsdf_gt:
        bsdf_gt.inputs["Base Color"].default_value = (0.12, 0.18, 0.08, 1.0) # Deep natural foliage green
        bsdf_gt.inputs["Roughness"].default_value = 0.80

    col_landscape = bpy.data.collections.get("01_Site_Landscape") or bpy.data.collections.new("01_Site_Landscape")

    # Add foreground trees framing the shot
    trees = [
        ("Tree_Foreground_Left_01",  (-18.0, -38.0, 5.0), 9.0, mat_green_tree),
        ("Tree_Foreground_Left_02",  (-8.0,  -42.0, 4.0), 7.5, mat_green_tree),
        ("Tree_Foreground_Right_Red", (24.0,  -40.0, 6.0), 8.5, mat_red_tree), # Autumn red maple on right!
        ("Tree_Foreground_Right_Green",(32.0, -44.0, 7.0), 9.5, mat_green_tree),
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
        o_t.hide_viewport = False

    # -------------------------------------------------------------
    # 7. World Sky & Dusk Lighting Calibration
    # -------------------------------------------------------------
    world = scene.world
    if world and world.node_tree:
        for node in world.node_tree.nodes:
            if node.type == 'BACKGROUND':
                node.inputs["Strength"].default_value = 0.55
            elif node.type == 'TEX_SKY':
                node.sun_elevation = math.radians(14.0) # Golden dusk sunset
                node.sun_rotation = math.radians(125.0)  # Setting behind left, casting rim light
                node.sun_intensity = 0.85
                if hasattr(node, 'turbidity'):
                    node.turbidity = 3.8 # Soft haze

    # Sun lamp
    sun = bpy.data.objects.get("Sun_Daylight_Hero") or bpy.data.objects.get("Sun_GoldenHour")
    if sun:
        sun.data.energy = 2.4
        sun.data.color = (1.0, 0.78, 0.58) # Warm golden sunset
        sun.data.angle = math.radians(2.0)
        sun.rotation_euler = (math.radians(65.0), math.radians(15.0), math.radians(125.0))

    # Color management
    if hasattr(scene, 'view_settings'):
        scene.view_settings.view_transform = 'AgX'
        scene.view_settings.look = 'AgX - Medium High Contrast'
        scene.view_settings.exposure = -0.35

    # -------------------------------------------------------------
    # 8. Perfectly Calibrated Two-Point Architectural Hero Camera
    # -------------------------------------------------------------
    cam_name = "Cam_Photo_Match_Hero_v7"
    if cam_name in bpy.data.objects:
        cam_obj = bpy.data.objects[cam_name]
    else:
        cam_data = bpy.data.cameras.new(cam_name)
        cam_obj = bpy.data.objects.new(cam_name, cam_data)
        scene.collection.objects.link(cam_obj)

    # Positioned at street corner (~52m back, looking up with shift_y to keep vertical lines upright)
    cam_obj.location = (22.5, -52.0, 6.0)
    # Rotation: upright roll, slight upward pitch with shift-lens
    cam_obj.rotation_euler = (math.radians(82.5), 0.0, math.radians(22.0))
    cam_obj.data.lens = 32.0 # Natural architectural focal length
    cam_obj.data.shift_y = 0.38 # Vertical perspective correction keeps columns straight
    cam_obj.data.shift_x = -0.04 # Centers building elegantly

    scene.camera = cam_obj

    # Save master blend
    bpy.ops.wm.save_as_mainfile(filepath=BLEND_PATH)
    print(f"Master file saved: {BLEND_PATH}")

    # -------------------------------------------------------------
    # 9. Render Local Preview v007
    # -------------------------------------------------------------
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

    print(f"Rendering v007 preview to {RENDER_OUT}...")
    bpy.ops.render.render(write_still=True)
    print(f"Render complete: {RENDER_OUT}")

    # -------------------------------------------------------------
    # 10. Generate Side-by-Side Comparison
    # -------------------------------------------------------------
    from PIL import Image, ImageDraw, ImageFont

    ref_img = Image.open(REF_PHOTO).convert('RGB').resize((600, 800), Image.Resampling.LANCZOS)
    ren_img = Image.open(RENDER_OUT).convert('RGB').resize((600, 800), Image.Resampling.LANCZOS)

    canvas = Image.new('RGB', (1200, 840), (20, 22, 26))
    canvas.paste(ref_img, (0, 40))
    canvas.paste(ren_img, (600, 40))

    draw = ImageDraw.Draw(canvas)
    draw.text((20, 10), "APPROVED REFERENCE ARCHITECTURE", fill=(255, 255, 255))
    draw.text((620, 10), "KALIDASA 42 - REMODELED ARCHITECTURE (v007)", fill=(255, 215, 0))

    canvas.save(COMPARISON_OUT)
    print(f"Comparison image generated: {COMPARISON_OUT}")

if __name__ == "__main__":
    run_remodel()

