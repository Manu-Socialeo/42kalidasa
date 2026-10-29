import bpy

print("=== COLLECTIONS ===")
for c in bpy.data.collections:
    print(f"Collection: {c.name} (objects: {len(c.objects)})")

print("\n=== MESH OBJECTS ===")
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        mats = [slot.material.name for slot in obj.material_slots if slot.material]
        print(f"Mesh: {obj.name:<32} | loc: ({obj.location.x:.1f}, {obj.location.y:.1f}, {obj.location.z:.1f}) | dims: ({obj.dimensions.x:.1f}, {obj.dimensions.y:.1f}, {obj.dimensions.z:.1f}) | mats: {mats}")

print("\n=== CAMERAS & LIGHTS ===")
for obj in bpy.data.objects:
    if obj.type in ['CAMERA', 'LIGHT', 'EMPTY']:
        print(f"{obj.type:<8}: {obj.name:<28} | loc: ({obj.location.x:.1f}, {obj.location.y:.1f}, {obj.location.z:.1f})")

print("\n=== MATERIALS & BSDF NODES ===")
for mat in bpy.data.materials:
    if mat.node_tree:
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            col = bsdf.inputs["Base Color"].default_value
            rough = bsdf.inputs["Roughness"].default_value
            met = bsdf.inputs["Metallic"].default_value
            print(f"Mat: {mat.name:<28} | color: ({col[0]:.2f}, {col[1]:.2f}, {col[2]:.2f}, {col[3]:.2f}) | rough: {rough:.2f} | met: {met:.2f}")

