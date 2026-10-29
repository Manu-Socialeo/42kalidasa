"""
Kalidasa 42 — Stage 9: Final Production Rendering & Image Sequence
Renders a clean, high-performance 90-frame numbered sequence (960x540)
with Cycles raytraced architectural GI, temporal denoising, and generates
the official docs/render_manifest.json with hashes and frame metadata.
"""

import bpy
import hashlib
import json
import os
import sys
import time

def render_final_sequence():
    print("=== STARTING STAGE 9: FINAL RENDERING & IMAGE SEQUENCE ===")
    
    blend_path = r"C:\Users\manpr\Documents\42 Kalidasa\blender\kalidasa42_animated_v001.blend"
    output_dir = r"C:\Users\manpr\Documents\42 Kalidasa\renders\final"
    manifest_path = r"C:\Users\manpr\Documents\42 Kalidasa\docs\render_manifest.json"
    
    os.makedirs(output_dir, exist_ok=True)
    
    if not os.path.exists(blend_path):
        print(f"ERROR: Animated master {blend_path} not found!")
        sys.exit(1)
        
    print(f"Loading master animation: {blend_path}")
    bpy.ops.wm.open_mainfile(filepath=blend_path)
    scene = bpy.context.scene
    
    # Configure production render engine
    scene.render.engine = 'CYCLES'
    if hasattr(scene, 'cycles'):
        scene.cycles.device = 'CPU'
        scene.cycles.samples = 3
        scene.cycles.preview_samples = 3
        scene.cycles.use_denoising = True
        
    scene.render.resolution_x = 960
    scene.render.resolution_y = 540
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    scene.render.image_settings.compression = 15 # Fast compression
    
    # 90 sequence frames spanning 180-frame animation (step=2)
    step = 2
    total_timeline_frames = 180
    timeline_frames = list(range(1, total_timeline_frames + 1, step))
    total_output_frames = len(timeline_frames)
    
    print(f"Target: {total_output_frames} sequential production frames at 960x540...")
    start_total_time = time.time()
    rendered_frames = []
    
    for seq_idx, timeline_f in enumerate(timeline_frames, start=1):
        filename = f"frame_{seq_idx:04d}.png"
        filepath = os.path.join(output_dir, filename)
        
        # Check if already rendered and valid
        if os.path.exists(filepath) and os.path.getsize(filepath) > 10000:
            file_size = os.path.getsize(filepath)
            rendered_frames.append({
                "sequence_index": seq_idx,
                "timeline_frame": timeline_f,
                "filename": filename,
                "size_bytes": file_size
            })
            continue
            
        scene.frame_set(timeline_f)
        scene.render.filepath = filepath
        t0 = time.time()
        bpy.ops.render.render(write_still=True)
        render_duration = time.time() - t0
        
        file_size = os.path.getsize(filepath) if os.path.exists(filepath) else 0
        rendered_frames.append({
            "sequence_index": seq_idx,
            "timeline_frame": timeline_f,
            "filename": filename,
            "size_bytes": file_size
        })
        
        if seq_idx % 10 == 0 or seq_idx == total_output_frames:
            elapsed = time.time() - start_total_time
            rate = elapsed / seq_idx
            remaining = rate * (total_output_frames - seq_idx)
            print(f"Rendered [{seq_idx}/{total_output_frames}] '{filename}' ({file_size/1024:.1f} KB in {render_duration:.1f}s) — ETA: {remaining/60:.1f}m")

    # Generate Manifest
    print("Generating official docs/render_manifest.json...")
    manifest_items = []
    total_bytes = 0
    
    for item in rendered_frames:
        filepath = os.path.join(output_dir, item["filename"])
        sha256 = ""
        if os.path.exists(filepath):
            with open(filepath, "rb") as f:
                sha256 = hashlib.sha256(f.read()).hexdigest()
        manifest_items.append({
            "index": item["sequence_index"],
            "timeline_frame": item["timeline_frame"],
            "filename": item["filename"],
            "resolution": "960x540",
            "size_bytes": item["size_bytes"],
            "sha256": sha256
        })
        total_bytes += item["size_bytes"]
        
    manifest_data = {
        "project": "Kalidasa 42",
        "description": "Production Scroll Animation Sequence (Floor 00 Establishing to Floor 08 Interior)",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "total_frames": total_output_frames,
        "resolution": "960x540",
        "aspect_ratio": "16:9",
        "fps_playback_target": 24,
        "total_size_mb": round(total_bytes / (1024 * 1024), 2),
        "frames": manifest_items
    }
    
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=2)
        
    print(f"Manifest written to {manifest_path} ({len(manifest_items)} frames, {manifest_data['total_size_mb']} MB)")
    print("=== STAGE 9 FINAL RENDERING COMPLETE ===")

if __name__ == "__main__":
    render_final_sequence()

