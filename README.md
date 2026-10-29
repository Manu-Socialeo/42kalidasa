# 42 Kalidasa — Architectural 3D & Scroll-Driven Web Experience

> **Mysuru's Defining Vertical Estate**  
> Site No. 42, Kalidasa Road, Block-III, Jayalakshmipuram, Mysuru  
> Developer / Client: Sankalp Constructions & Mysore Toys Company  
> Sanction Drawing: `DWG / NS / 5692` (Sheets 01 to 06)  
> Total Certified Valuation: ₹ 49.89 Crores | Structural Construction Cost: ₹ 43.00 Crores  

---

## Executive Summary & Visual Ground Truth

This repository contains the complete autonomous reconstruction of **Kalidasa 42**, executed according to `kalidasa42_autonomous_master_pipeline_FINAL.json` across all 15 sequential stages.

### Highest Priority Visual Target: Exterior Accuracy
The primary visual ground truth for exterior rendering is the client-approved building photograph (`assets/WhatsApp Image 2026-10-27 at 11.30.09 AM.jpeg`).
- **Curved Balconies:** Sweeping 4.8m cantilevered curved profiles with sky-blue / cyan laminated safety glass balustrades (`Mat_Facade_Tinted_Glass`).
- **Slab Fascias:** Crisp brilliant-white horizontal slab edge fascias (`Mat_Slab_Fascia`) continuously separating all 22 structural levels (2 Basements + Ground + 19 Floors).
- **Vertical Articulation:** Warm beige / sandstone vertical structural piers (`Mat_Fluted_Timber_Accent`) providing rhythmic facade depth.
- **Side-by-Side Comparison:** See [`renders/preview/exterior_comparison_side_by_side_v003.png`](file:///c:/Users/manpr/Documents/42%20Kalidasa/renders/preview/exterior_comparison_side_by_side_v003.png) (2400×860 px) and detailed analysis in [`docs/exterior_comparison_report_v002.md`](file:///c:/Users/manpr/Documents/42%20Kalidasa/docs/exterior_comparison_report_v002.md).

---

## Architectural Ground Truth & Compliance

All building parameters are strictly traced to certified municipal sanction drawings (`DWG / NS / 5692`) and the consulting engineer's valuation report. No speculative or undocumented amenities (e.g. helipads, tennis courts, private marinas) have been fabricated.

| Parameter | Sanctioned Specification | Reference Drawing / Source |
| :--- | :--- | :--- |
| **Total Height** | 67.70 meters | DWG / NS / 5692 (Sheet 04 - Elevation) |
| **Vertical Levels** | 2 Basements + Ground + 19 Floors | DWG / NS / 5692 (Sheet 05 - Section) |
| **Site Area & Coverage** | 3,604.80 m² (12.90% footprint ground coverage) | DWG / NS / 5692 (Sheet 01 - Site Plan) |
| **Floor Area Ratio (FAR)**| 2.235 (Sanctioned) | Sheet 01 & Valuation Report |
| **Typical 4BHK Residence**| 368.06 m² net internal area (Level 08) | DWG / NS / 5692 (Sheet 02 - Typical Plan) |
| **Curved Balcony Arc** | 12.11m arc length with 4.80m cantilever | DWG / NS / 5692 (Sheet 02) |
| **Rooftop Lap Pool** | 11.80m × 4.00m at +65.50m FFL | DWG / NS / 5692 (Sheet 06 - Terrace Plan) |
| **Perimeter Fire Driveway**| 8.00m clear setback around boundary | DWG / NS / 5692 (Sheet 01) |

---

## Key Deliverables & Directory Layout

```text
42 Kalidasa/
├── website/                                 # Production web application
│   ├── index.html                           # Semantic HTML5, interactive canvas & ARIA modals
│   ├── camera_path_preview.mp4              # 941.8 KB H.264 video fallback
│   └── sequence/                            # 90 rendered WebP/PNG frames (frame_0001 to frame_0090)
├── blender/                                 # Editable 3D master project
│   ├── kalidasa42_animated_v001.blend       # Rigged animated master scene (Cycles CPU denoised)
│   ├── kalidasa42_master_v001.blend         # Base architectural model
│   └── stage2_test.blend                    # Capability verification smoke test
├── renders/                                 # Visual masters & comparison sheets
│   ├── final/                               # 90 master PNG frames (960x540)
│   └── preview/
│       ├── exterior_photo_match_render.png  # Calibrated render from reference camera angle
│       ├── exterior_comparison_side_by_side.png # Direct side-by-side photo comparison
│       ├── interior_living_render.png       # 4BHK living salon render
│       ├── terrace_rooftop_render.png       # Level 19 pool & pergola render
│       ├── camera_path_preview.mp4          # 26.85s preview video
│       └── reference_video_contact_sheet.jpg# Reference video contact sheet
├── scripts/                                 # Reusable automation pipeline
│   ├── stage_06_geometry_validation.py      # Metric scale & tolerance validator
│   ├── stage_07_exterior_photorealism.py    # Material calibration & photo-match camera
│   ├── stage_08_interior_modeling.py        # 4BHK interior layout generator
│   ├── stage_09_terrace_modeling.py         # Rooftop pool & pergola builder
│   ├── stage_10_camera_trajectory.py        # 5-milestone camera curve generator
│   ├── stage_11_render_sequence.py          # Frame render orchestrator
│   └── run_stage_14_qa.py                   # Automated QA test suite
├── docs/                                    # Architectural registers & specifications
│   ├── final_manifest.json                  # Complete deliverable manifest
│   ├── asset_license_manifest.json          # Open-source and proprietary license register
│   ├── architectural_source_register.json   # Full municipal drawing parameter trace
│   ├── exterior_comparison_report.md        # Facade match vs photograph
│   ├── reference_design_specification.md    # Art direction & video breakdown
│   ├── model_diagnosis_and_repair_plan.md   # Initial audit & geometry fixes
│   └── camera_storyboard.md                 # 5-milestone shot storyboard
└── reports/                                 # Verifiable stage reports (Stages 01 to 15)
    ├── stage_01_report.json to stage_15_report.json
```

---

## Local Setup & Preview Instructions

### 1. Web Experience
The web application is pure zero-dependency modern HTML5, CSS3, and ES6 JavaScript.
To run the local preview server:

```powershell
# From the workspace root:
python -m http.server 3000 --directory "website"
```
Then open:
👉 **`http://localhost:3000`**

#### Interactive Web Features:
- **Scroll-Controlled Flythrough:** Scroll down or up to scrub through the 90-frame camera journey with spring-lerp damping (bidirectional monotonic scrub).
- **Milestone Navigation:** Click any of the 5 HUD milestone dots (`01 Superstructure`, `02 Cantilevers`, `03 Horizon Club`, `04 Sky Terrace`, `05 Grand Living`) to smooth-scroll directly to that architectural phase.
- **Timeline Scrubber:** Drag the bottom range slider to instantly jump to any frame (1 to 90).
- **Keyboard Navigation:** Use `ArrowDown` / `ArrowRight` (step forward), `ArrowUp` / `ArrowLeft` (step back), `Home` (start), `End` (finish).
- **Architectural Sanctions Dialog:** Click the `Architectural Sanctions` button in the header to view municipal engineering data (`DWG / NS / 5692`).
- **Cinematic Tour Fallback:** Click `Play Cinematic Tour` in the header to play the standalone 26.85s H.264 video.
- **Accessibility & Reduced Motion:** Respects `prefers-reduced-motion: reduce` by presenting stationary high-contrast narrative cards.

---

### 2. 3D Blender Automation & Re-rendering
The project was authored and verified in **Blender 5.2.3 LTS**.

```powershell
# Run the geometry scale check:
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b "blender\kalidasa42_animated_v001.blend" -P "scripts\stage_06_geometry_validation.py"

# Re-render the exterior photo match still:
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b "blender\kalidasa42_animated_v001.blend" -P "scripts\stage_07_exterior_photorealism.py"

# Re-run automated Stage 14 QA test suite:
python scripts\run_stage_14_qa.py
```

---

## Hardware Environment & Render Configuration

- **Host Operating System:** Windows 11 (64-bit)
- **CPU:** Intel(R) Core(TM) i5-10210U CPU @ 1.60GHz (4 physical cores / 8 logical threads)
- **GPU:** NVIDIA GeForce MX250 (sm_60 Pascal architecture). Modern Blender 5.2.3 CUDA/OptiX kernels require sm_70+; therefore, all procedural rendering has been configured with **Cycles CPU Raytracing + OpenImageDenoise**, ensuring 100% crash-free stability across headless rendering runs.

---

## Deployment Instructions

### Static Web Hosting (Production Ready)
The `website/` folder is a self-contained static package ready for immediate deployment on any modern CDN or static web host (Vercel, Cloudflare Pages, Netlify, AWS S3 / CloudFront, GitHub Pages).

#### Example: Deploying to GitHub Pages
1. In repository settings, navigate to **Pages**.
2. Set Build and deployment source to **Deploy from a branch**.
3. Select `main` branch and `/website` folder.
4. Save to deploy.

---

## Autonomous Pipeline Audit Trail

All 15 pipeline stages from `kalidasa42_autonomous_master_pipeline_FINAL.json` have passed all acceptance checks:
- [x] **Stage 01: Workspace inventory and backups** (`reports/stage_01_report.json`)
- [x] **Stage 02: Environment and Blender capability check** (`reports/stage_02_report.json`)
- [x] **Stage 03: Reference video and image analysis** (`reports/stage_03_report.json`)
- [x] **Stage 04: Architectural document audit** (`reports/stage_04_report.json`)
- [x] **Stage 05: Existing project audit and model diagnosis** (`reports/stage_05_report.json`)
- [x] **Stage 06: Geometry correction and scale validation** (`reports/stage_06_report.json`)
- [x] **Stage 07: Exterior materials and photorealism** (`reports/stage_07_report.json`)
- [x] **Stage 08: Interior design and modelling** (`reports/stage_08_report.json`)
- [x] **Stage 09: Terrace, pool and amenity verification** (`reports/stage_09_report.json`)
- [x] **Stage 10: Camera journey and animation blocking** (`reports/stage_10_report.json`)
- [x] **Stage 11: Final render and asset optimisation** (`reports/stage_11_report.json`)
- [x] **Stage 12: Website reconstruction** (`reports/stage_12_report.json`)
- [x] **Stage 13: Scroll-controlled animation integration** (`reports/stage_13_report.json`)
- [x] **Stage 14: Quality assurance and performance** (`reports/stage_14_qa_report.json`)
- [x] **Stage 15: Packaging and handoff** (`reports/stage_15_report.json`)

---
*Autonomous execution completed by Antigravity under Google DeepMind Advanced Agentic Coding.*
