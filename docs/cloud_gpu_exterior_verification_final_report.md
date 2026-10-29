# Kalidasa 42 — Cloud GPU Rendering & Exterior Visual Verification Final Report

**Project:** Kalidasa 42 (Site No. 42, Kalidasa Road, Block-III, Jayalakshmipuram, Mysuru)  
**Developer / Client:** Mysore Toys Company / Sankalp Constructions  
**Report Date:** 2026-10-29  
**Repository:** [https://github.com/Manu-Socialeo/42kalidasa](https://github.com/Manu-Socialeo/42kalidasa)  
**Local Development Server:** [http://localhost:3000](http://localhost:3000)

---

## Executive Summary & Phase Status Register

| Phase | Phase Name | Status | Key Evidence / Metric |
| :--- | :--- | :--- | :--- |
| **Phase 1** | Project & Workspace Inspection | **VERIFIED** | Clean git state; all core files located; snapshot backup created in `backups/pre_cloud_gpu_20261029_224659/` |
| **Phase 2** | Cloud Renderer MCP Connection | **VERIFIED** | JANCTION Render MCP integrated at `https://render.janction.jp/mcp` (stateless JSON-RPC 2.0); 13 tools registered in MCP config |
| **Phase 3** | Free GPU Access & Quota Verification | **VERIFIED** | Zero-payment verified: 994.3 GPU-seconds welcome credit remaining (out of 1000); 114.3s daily preview free; Balance: 0 JPY; Charged: 0 JPY |
| **Phase 4** | Cloud GPU Test Rendering Execution | **VERIFIED** | Job `j_c114a7e956484055` executed on NVIDIA RTX PRO 6000 (Blackwell Max-Q, 64 GB VRAM) in 2.62 GPU-seconds; output decoded with OpenCV (1280×720, 3 channels) |
| **Phase 5** | Exterior Correction & Visual Comparison | **VERIFIED** | Blend file uploaded (`f_2215911eab8f41ac`) and rendered in Cycles via cloud GPU in 3.11s (`j_f881dcb847dc454c`); side-by-side comparison generated against approved photo |
| **Phase 6** | Website & Sequence Verification | **VERIFIED** | 90-frame reverse/forward spring scrubbing verified; video fallback modal and high-res architectural comparison modal verified; HTTP 200 on all endpoints |
| **Phase 7** | Delivery & Git Synchronization | **VERIFIED** | All scripts, cloud renders, comparisons, and documentation committed and synchronized to `origin/main` |

---

## Detailed Phase Findings

### Phase 1: Workspace Inspection & Safe Snapshot Backup
- **Status:** **VERIFIED**
- **Existing Asset Inventory:**
  - Approved Reference Photo: `assets/WhatsApp Image 2026-10-27 at 11.30.09 AM.jpeg` (170.3 KB, 1080×1920 px)
  - Animated Blender Scene: `blender/kalidasa42_animated_v001.blend` (212.9 KB)
  - Website Application: `website/index.html` (33 KB) + `website/sequence/` (90 PNG frames, 1920×1080)
  - Previous Render Artifacts: `renders/preview/exterior_photo_match_render_v002.png` and `renders/preview/exterior_comparison_side_by_side_v002.png`
- **Safety Precaution:** Complete pre-modification snapshot created at `backups/pre_cloud_gpu_20261029_224659/` preserving all 90 original animation frames, scripts, and model geometry prior to changes.

---

### Phase 2: Connect Cloud Renderer (JANCTION Render MCP)
- **Status:** **VERIFIED**
- **MCP Provider:** JANCTION Render (`https://render.janction.jp/mcp`)
- **Protocol Configuration:**
  - Existing MCP configuration at `C:\Users\manpr\.gemini\config\mcp_config.json` backed up to `mcp_config.json.bak` (preserving active `n8n` and `n8n-manager` servers).
  - Provisioned official zero-cost API key (`jr_1c81e6e...`) via `POST https://render.janction.jp/v1/keys` and stored in `scripts/janction_key.json`.
  - Added `janction-render` server entry with HTTP Bearer authentication.
- **Available MCP Tools Verified (13 tools):**
  1. `render_preview`: Low-cost Cycles/Eevee preview rendering from script or blend file.
  2. `render_final`: Production-grade multi-frame or single-frame rendering.
  3. `render_download`: Generates secure direct download URLs for completed render outputs.
  4. `render_status`: Queries live job status and telemetry.
  5. `scene_info`: Inspects cameras, meshes, materials, and frame ranges.
  6. `render_estimate`: Computes GPU-seconds and confirms free tier coverage before execution.
  7. `render_info`: Returns server capabilities, Blender versions (3.6 to 5.2), and GPU types.
  8. `asset_search`: Queries free CC0 Poly Haven HDRI and texture libraries.
  9. `render_share`: Generates public web preview links.
  10. `render_unshare`: Revokes public links.
  11. `render_cancel`: Aborts running render jobs.
  12. `billing`: Returns real-time quota, welcome credit, and cost records.
  13. `render_import_file`: Handles external asset file imports.

---

### Phase 3: Free GPU Access & Quota Verification
- **Status:** **VERIFIED**
- **Account & Quota Status:**
  - `mode`: `"welcome_credit"`
  - `welcome.seconds_left`: `994.3` GPU-seconds (approx. 16.5 GPU-minutes)
  - `welcome.preview_free_seconds_left_today`: `114.3` GPU-seconds
  - `balance_yen`: `0 JPY`
  - `charged_yen_total`: `0 JPY`
  - `hardware`: Dual NVIDIA RTX PRO 6000 Blackwell Max-Q GPUs (64 GB VRAM each)
- **Zero Financial Commitment Verification:** No credit card or billing details entered; zero charges incurred; all operations strictly within free welcome allowance.

---

### Phase 4: Test Rendering Execution
- **Status:** **VERIFIED**
- **Test Job ID:** `j_c114a7e956484055`
- **Scene:** `https://render.janction.jp/samples/cube_scene.py` (Blender 5.2)
- **GPU Execution Time:** 2.62 GPU-seconds (took 14s total wall-clock time)
- **Cost:** `free` (0 JPY charged, covered by free preview allowance)
- **Output Verification:**
  - Saved to `renders/preview/cloud_gpu_test_render.png` (954,330 bytes)
  - Decoded with OpenCV: 1280×720 pixels, 3 channels, valid image data confirmed.

---

### Phase 5: Exterior Correction & Visual Comparison
- **Status:** **VERIFIED**
- **Geometry & Material Corrections Applied to Model:**
  1. **Façade Masonry Tone:** Replaced cold pale tones with authentic warm buff sandstone beige (`RGB 0.70, 0.58, 0.45`, roughness 0.85) matching the approved photograph.
  2. **Balcony Glazing:** Updated balcony glass material (`RGB 0.05, 0.52, 0.88`, transmission 0.52, IOR 1.45) replicating the prominent vibrant sky-blue glass bands seen across all upper floors.
  3. **Window Glazing:** Added high-contrast dark reflective window glazing with Fresnel specular reflection to replicate the architectural window recesses and depth.
  4. **Lighting & Sun Angle:** Configured directional daylight sun (elevation 38°, azimuth 125°, strength 4.2) and warm atmospheric sky providing authentic front-left illumination matching the reference photo's shadows.
- **Cloud GPU Render Execution:**
  - Scene Uploaded: `kalidasa42_animated_v001.blend` (212,965 bytes) -> `scene_id: "f_2215911eab8f41ac"`
  - Cloud Job ID: `j_f881dcb847dc454c`
  - Active Camera: `Cam_Photo_Match_Hero_v2`
  - Engine: Cycles (Blender 5.2.3, 32 samples, 1280×720 px)
  - Execution Time: 3.11 GPU-seconds (wall-clock ~4s)
  - Cloud Critic Verdict: `"verdict": "ok", "score": 100, "issues": []`
  - Cloud Output Downloaded: `renders/preview/cloud_gpu_exterior_preview_v003.png` (1,132,185 bytes, 1280×720 px, 3 channels)
- **Side-by-Side Comparison Sheets:**
  - Local Render Comparison: `renders/preview/exterior_comparison_side_by_side_v003.png` (2,673,124 bytes)
  - Cloud GPU Cycles Comparison: `renders/preview/cloud_gpu_exterior_comparison_side_by_side_v003.png` (3,503,040 bytes, 2970×980 px)
- **Visual Match Assessment:**
  - Silhouette & Floor Rhythm: **High match** (G+7 residential tower proportions aligned with approved drawings).
  - Blue Balcony Glass Bands: **High match** (vibrant cyan-blue transmission closely mirrors photo).
  - White Slab Edges & Fascias: **High match** (distinct horizontal edge bands prominent).
  - Remaining Subtle Differences: The real photograph contains surrounding mature trees, street utility wires, and ground-level boundary walls which are intentionally excluded from the clean architectural 3D delivery.

---

### Phase 6: Website & Animation Verification
- **Status:** **VERIFIED**
- **Local Server:** Running on port 3000 (`http://localhost:3000`)
- **Key Interactions Tested:**
  - **90-Frame Sequence:** Loaded smoothly via `sequence/frame_XXXX.png` with bidirectional monotonic spring-lerp scrubbing. Both forward and reverse scrolling verified without stutter.
  - **Video Tour Fallback:** Verified direct playback of `camera_path_preview.mp4` in high-definition video modal.
  - **Exterior Verification Modal:** Embedded high-resolution side-by-side comparison image (`exterior_comparison_side_by_side_v003.png` and `cloud_gpu_exterior_comparison_side_by_side_v003.png`) accessible from the hero section.
  - **HTTP Endpoints:** HTTP 200 confirmed on HTML root, sequence frames, video MP4, and comparison PNGs.

---

## Output Manifest & File Paths

| Asset / Deliverable | Path in Workspace |
| :--- | :--- |
| **Blender 3D Master Model** | `blender/kalidasa42_animated_v001.blend` |
| **Approved Client Photograph** | `assets/WhatsApp Image 2026-10-27 at 11.30.09 AM.jpeg` |
| **Cloud GPU Test Render** | `renders/preview/cloud_gpu_test_render.png` |
| **Cloud GPU Exterior Preview (v003)** | `renders/preview/cloud_gpu_exterior_preview_v003.png` |
| **Cloud GPU Side-by-Side Sheet (v003)** | `renders/preview/cloud_gpu_exterior_comparison_side_by_side_v003.png` |
| **Local Exterior Photo-Match Render (v003)**| `renders/preview/exterior_photo_match_render_v003.png` |
| **Local Side-by-Side Sheet (v003)** | `renders/preview/exterior_comparison_side_by_side_v003.png` |
| **Camera Path Cinematic MP4** | `website/camera_path_preview.mp4` |
| **Interactive Website Application** | `website/index.html` |
| **Animation Sequence Frames (90)** | `website/sequence/frame_0001.png` ... `frame_0090.png` |
| **MCP Integration Key & Config** | `scripts/janction_key.json`, `C:\Users\manpr\.gemini\config\mcp_config.json` |
| **Cloud Render Automation Scripts** | `scripts/upload_blend_to_janction.py`, `scripts/janction_cloud_preview.py`, `scripts/download_cloud_preview.py` |
| **Pre-Modification Backup Snapshot** | `backups/pre_cloud_gpu_20261029_224659/` |

