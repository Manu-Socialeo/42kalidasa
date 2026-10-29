"""
Stage 2: Environment and Blender capability verification script.
"""

import os
import subprocess
import sys
import json
import shutil
import platform
import time

def run_env_check():
    report = {
        "stage": 2,
        "name": "Environment and Blender capability check",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "os": platform.platform(),
        "python_version": sys.version,
        "tools": {},
        "acceptance_checks": {},
        "issues": []
    }
    
    # 1. Disk space
    total, used, free = shutil.disk_usage("C:\\")
    report["disk_space_gb"] = {
        "total": round(total / (1024**3), 2),
        "used": round(used / (1024**3), 2),
        "free": round(free / (1024**3), 2)
    }
    
    # 2. Node & npm
    try:
        node_v = subprocess.check_output(["node", "-v"], text=True).strip()
        npm_v = subprocess.check_output(["npm", "-v"], text=True).strip()
        report["tools"]["node"] = node_v
        report["tools"]["npm"] = npm_v
    except Exception as e:
        report["issues"].append(f"Node check error: {e}")
        
    # 3. Blender Executable
    blender_path = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
    if not os.path.exists(blender_path):
        report["status"] = "failed"
        report["issues"].append(f"Blender not found at {blender_path}")
        print("BLENDER NOT FOUND")
        sys.exit(1)
        
    report["tools"]["blender_path"] = blender_path
    try:
        blender_v_out = subprocess.check_output([blender_path, "-v"], text=True)
        report["tools"]["blender_version"] = blender_v_out.splitlines()[0]
    except Exception as e:
        report["issues"].append(f"Blender version check error: {e}")
        
    # 4. Smoke test: minimal .blend and low-res render
    test_blend = r"C:\Users\manpr\Documents\42 Kalidasa\blender\stage2_test.blend"
    test_render = r"C:\Users\manpr\Documents\42 Kalidasa\renders\preview\stage2_test.png"
    
    smoke_py = f"""
import bpy
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.mesh.primitive_cube_add(size=2.0, location=(0, 0, 1))
bpy.ops.object.camera_add(location=(5, -5, 4))
cam = bpy.context.active_object
cam.rotation_euler = (1.0, 0.0, 0.785)
bpy.context.scene.camera = cam

bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))

bpy.context.scene.render.engine = 'BLENDER_EEVEE'
bpy.context.scene.render.resolution_x = 320
bpy.context.scene.render.resolution_y = 240
bpy.context.scene.render.filepath = r'{test_render}'

bpy.ops.wm.save_as_mainfile(filepath=r'{test_blend}')
bpy.ops.render.render(write_still=True)
print('STAGE2_SMOKE_TEST_OK')
"""
    cmd = [blender_path, "-b", "--python-expr", smoke_py]
    res = subprocess.run(cmd, capture_output=True, text=True)
    
    blend_ok = os.path.exists(test_blend) and os.path.getsize(test_blend) > 0
    render_ok = os.path.exists(test_render) and os.path.getsize(test_render) > 0
    
    report["acceptance_checks"]["blender_cli_works"] = (res.returncode == 0)
    report["acceptance_checks"]["test_blend_created"] = blend_ok
    report["acceptance_checks"]["test_render_created"] = render_ok
    report["acceptance_checks"]["environment_limitations_recorded"] = True
    
    # Limitations recorded:
    # Optix / CUDA GPU on MX250 driver is sm_60 incompatible, CPU raytracing / EEVEE fallback is standard
    report["environment_limitations"] = [
        "NVIDIA GeForce MX250 driver uses sm_60 which requires CPU rendering for Cycles or EEVEE for viewport",
        "Cycles CPU with 4 cores is primary raytracing engine; EEVEE is available for real-time viewport stills"
    ]
    
    if blend_ok and render_ok:
        report["status"] = "passed"
    else:
        report["status"] = "failed"
        
    out_path = r"C:\Users\manpr\Documents\42 Kalidasa\reports\stage_02_report.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print("Stage 2 Check completed:", report["status"])

if __name__ == "__main__":
    run_env_check()

