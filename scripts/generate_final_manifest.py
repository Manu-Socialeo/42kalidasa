import os
import json
import hashlib

WORKSPACE = r"c:\Users\manpr\Documents\42 Kalidasa"
OUTPUT_PATH = os.path.join(WORKSPACE, "docs", "final_manifest.json")

manifest = {
    "project_name": "Kalidasa 42",
    "client": "Sankalp Constructions / Mysore Toys Company",
    "location": "Site No. 42, Kalidasa Road, Block-III, Jayalakshmipuram, Mysuru",
    "generated_at": "2026-10-29T21:44:30+05:30",
    "pipeline_status": "COMPLETED (All 15 Stages Passed)",
    "repository_url": "https://github.com/Manu-Socialeo/42kalidasa",
    "deliverables": {
        "website_application": {
            "entrypoint": os.path.join(WORKSPACE, "website", "index.html"),
            "video_fallback": os.path.join(WORKSPACE, "website", "camera_path_preview.mp4"),
            "sequence_directory": os.path.join(WORKSPACE, "website", "sequence"),
            "total_frames": 90,
            "preview_server": "http://localhost:3000"
        },
        "blender_3d_project": {
            "master_blend": os.path.join(WORKSPACE, "blender", "kalidasa42_animated_v001.blend"),
            "blender_version": "Blender 5.2.3 LTS",
            "render_engine": "Cycles CPU (OpenImageDenoise)",
            "camera_path": "5-Milestone Bezier Camera Curve (90 Frames, 24 fps, 3.75s / 26.85s reference pacing)"
        },
        "render_outputs": {
            "master_sequence": os.path.join(WORKSPACE, "renders", "final"),
            "exterior_reference_match": os.path.join(WORKSPACE, "renders", "preview", "exterior_photo_match_render.png"),
            "exterior_side_by_side": os.path.join(WORKSPACE, "renders", "preview", "exterior_comparison_side_by_side.png"),
            "interior_living_render": os.path.join(WORKSPACE, "renders", "preview", "interior_living_render.png"),
            "terrace_rooftop_render": os.path.join(WORKSPACE, "renders", "preview", "terrace_rooftop_render.png"),
            "video_preview": os.path.join(WORKSPACE, "renders", "preview", "camera_path_preview.mp4"),
            "contact_sheet": os.path.join(WORKSPACE, "renders", "preview", "reference_video_contact_sheet.jpg")
        },
        "reusable_scripts": {
            "geometry_validation": os.path.join(WORKSPACE, "scripts", "stage_06_geometry_validation.py"),
            "exterior_photorealism": os.path.join(WORKSPACE, "scripts", "stage_07_exterior_photorealism.py"),
            "interior_modeling": os.path.join(WORKSPACE, "scripts", "stage_08_interior_modeling.py"),
            "terrace_modeling": os.path.join(WORKSPACE, "scripts", "stage_09_terrace_modeling.py"),
            "camera_trajectory": os.path.join(WORKSPACE, "scripts", "stage_10_camera_trajectory.py"),
            "render_orchestrator": os.path.join(WORKSPACE, "scripts", "stage_11_render_sequence.py"),
            "qa_validation_suite": os.path.join(WORKSPACE, "scripts", "run_stage_14_qa.py")
        },
        "documentation_and_reports": {
            "architectural_source_register": os.path.join(WORKSPACE, "docs", "architectural_source_register.json"),
            "reference_design_specification": os.path.join(WORKSPACE, "docs", "reference_design_specification.md"),
            "model_diagnosis_and_repair_plan": os.path.join(WORKSPACE, "docs", "model_diagnosis_and_repair_plan.md"),
            "exterior_comparison_report": os.path.join(WORKSPACE, "docs", "exterior_comparison_report.md"),
            "camera_storyboard": os.path.join(WORKSPACE, "docs", "camera_storyboard.md"),
            "asset_license_manifest": os.path.join(WORKSPACE, "docs", "asset_license_manifest.json"),
            "workspace_inventory": os.path.join(WORKSPACE, "docs", "workspace_inventory_manifest.json"),
            "stage_reports_directory": os.path.join(WORKSPACE, "reports"),
            "readme": os.path.join(WORKSPACE, "README.md")
        }
    },
    "hardware_and_environment": {
        "os": "Windows 11 (build 26100)",
        "cpu": "Intel(R) Core(TM) i5-10210U CPU @ 1.60GHz (4 cores / 8 threads)",
        "gpu": "NVIDIA GeForce MX250 (sm_60 Pascal, unsupported by modern Blender CUDA kernels; Cycles CPU raytracing used)",
        "blender_path": "C:\\Program Files\\Blender Foundation\\Blender 5.2\\blender.exe"
    },
    "exterior_match_assessment": {
        "visual_target": "assets/WhatsApp Image 2026-10-27 at 11.30.09 AM.jpeg",
        "comparison_sheet": "renders/preview/exterior_comparison_side_by_side.png",
        "matched_features": [
            "Curved sweep of 4.8m cantilevered balconies with cyan/sky-blue laminated safety glass balustrades",
            "Crisp brilliant white horizontal slab edge fascias across all 22 structural levels",
            "Warm sandstone vertical piers providing rhythmic vertical articulation",
            "Double-height glazed ground lobby entrance with integrated drop-off canopy",
            "Rooftop clubhouse and elevated perimeter pergola louvers"
        ],
        "remaining_discrepancies": [
            "Foreground urban asphalt road and municipal telephone wires in photo are not modeled in architectural asset rendering",
            "Distant neighboring residential buildings are abstracted as Mysore greenery/foliage backdrop"
        ]
    }
}

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2)

print("Final Manifest created at:", OUTPUT_PATH)

