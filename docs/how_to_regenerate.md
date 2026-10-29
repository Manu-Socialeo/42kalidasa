# Kalidasa 42 — Pipeline Reproduction Guide (`how_to_regenerate.md`)

This document provides exact, automated, headless command-line instructions to regenerate every 3D model, camera animation, production render sequence, and web experience from scratch.

---

## 1. Environment & Prerequisites

- **Operating System:** Windows 10/11
- **Blender Version:** Blender 5.2.3 LTS (or newer)  
  *Default Path:* `C:\Program Files\Blender Foundation\Blender 5.2\blender.exe`
- **Node.js:** v20+ / v24+ with npm
- **Python:** Python 3.10+ with `opencv-python` (`pip install opencv-python`)

---

## 2. Directory Structure

```
C:\Users\manpr\Documents\42 Kalidasa\
├── assets/          # Official municipal PDFs, certificates, launch photos, reference video
├── references/      # Curated visual design intent and camera path references
├── plans/           # Drawing DWG / NS / 5692 Sheets 01 to 06
├── scripts/         # Production headless automation Python scripts
├── blender/         # Parametric Blender master files (.blend)
├── renders/
│   ├── preview/     # Review renders, elevation checks, MP4 preview
│   └── final/       # 90 production frames (frame_0001.png to frame_0090.png)
├── website/         # Production scroll-driven canvas application
├── docs/            # Architecture specifications, validation logs, manifests
└── backups/         # Code and model version backups
```

---

## 3. Step-by-Step Regeneration Commands

Run all commands from PowerShell in the workspace root: `C:\Users\manpr\Documents\42 Kalidasa`.

### Step 1: Blender Automation Smoke Test (Stage 3)
Verifies headless Blender execution and camera pipeline.
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b --python "scripts\blender_smoke_test.py"
```
*Outputs:* `blender\smoke_test.blend`, `renders\preview\smoke_test.png`

---

### Step 2: Build Parametric Architectural Massing (Stage 4)
Generates all 22 structural levels, double-height lobby, and 4.8m curved cantilevers.
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b --python "scripts\build_massing.py"
```
*Outputs:* `blender\kalidasa42_massing_v001.blend`, `renders\preview\massing_v001_preview.png`

---

### Step 3: Validate Massing Orthographic Elevations (Stage 5)
Renders 5 elevation validation views (Front, Rear, Left, Right, Aerial) to verify zero tolerance against `DWG/NS/5692`.
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b --python "scripts\validate_massing.py"
```
*Outputs:* `renders\preview\massing_front.png`, `massing_rear.png`, `massing_left.png`, `massing_right.png`, `massing_aerial.png`

---

### Step 4: Model High-Fidelity Facade & Site (Stage 6)
Adds curved bronze glass balustrades, terracotta fins, ground canopy, rooftop pool, and pergola louvers.
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b --python "scripts\build_facade.py"
```
*Outputs:* `blender\kalidasa42_facade_v001.blend`, `renders\preview\facade_review.png`

---

### Step 5: Model Representative 4BHK Interior (Stage 7)
Constructs Floor 08 (Z = +27.60m) partition layout, Statuario marble floors, furniture, downlights, and sliding threshold.
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b --python "scripts\build_interior.py"
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b --python "scripts\render_interior_review.py"
```
*Outputs:* `blender\kalidasa42_interior_v001.blend`, `renders\preview\interior_review.png`

---

### Step 6: Configure Animated Camera & Preview Video (Stage 8)
Applies the 5-milestone camera trajectory, smooth Bezier curves, and renders the MP4 preview.
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b --python "scripts\animate_camera.py"
python "scripts\compile_video.py"
```
*Outputs:* `blender\kalidasa42_animated_v001.blend`, `renders\preview\camera_path_preview.mp4`

---

### Step 7: Render Production Sequence & Manifest (Stage 9)
Renders all 90 production frames (960x540) with Cycles raytraced architectural GI and generates cryptographic manifest.
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b --python "scripts\render_final_sequence.py"
```
*Outputs:* `renders\final\frame_0001.png` to `frame_0090.png`, `docs\render_manifest.json`

---

### Step 8: Deploy & Launch Interactive Web Experience (Stage 10)
Copies the latest frames to the website sequence cache and serves the web application.
```powershell
Copy-Item "renders\final\frame_*.png" -Destination "website\sequence\" -Force
cd website
npx serve -l 3000 .
```
*Outputs:* Open `http://localhost:3000` or double-click `website\index.html`.

