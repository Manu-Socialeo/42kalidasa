# Kalidasa 42 — Model Diagnosis and Repair Plan (`docs/model_diagnosis_and_repair_plan.md`)

## 1. Executive Diagnosis
The existing Blender master (`kalidasa42_animated_v001.blend`) possesses correct structural dimensions and floor layouts traced from `DWG/NS/5692`. However, to fulfill the **HIGHEST PRIORITY EXTERIOR ACCURACY** mandate, specific shader and color calibrations are required to achieve exact visual congruence with the approved building photograph (`WhatsApp Image 2026-10-27 at 11.30.09 AM.jpeg`).

## 2. Prioritized Discrepancies & Actions
### Rank 1: Balcony Glazing Bands Color & Specularity [HIGH (Core Architectural Identity)]
- **Observed in Reference Photograph:** The reference photograph prominently displays vibrant sky-blue / azure tinted glass bands along every curved balcony facade.
- **Current Model Status:** Current material 'Mat_Facade_Tinted_Glass' has a darker navy-bronze tint (0.10, 0.18, 0.26), which looks darker and less vibrant than the approved photograph.
- **Exact Action:** Tune balcony glass shader to match the approved vibrant sky-blue/cyan hue with crisp transmission and specular reflection: RGB ~(0.12, 0.58, 0.88), roughness 0.04, transmission 0.85.

### Rank 2: Horizontal Slab Edge Whiteness & Definition [HIGH (Architectural Readability)]
- **Observed in Reference Photograph:** Crisp, brilliant clean white slab edges emphasize the curved cantilever rhythm across all 22 structural levels.
- **Current Model Status:** Slab edge material 'Mat_Slab_Fascia' is slightly muted cream (0.94, 0.92, 0.88).
- **Exact Action:** Increase brightness and crispness of 'Mat_Slab_Fascia' to architectural brilliant white (0.98, 0.98, 0.98) with subtle bevel highlights.

### Rank 3: Vertical Facade Accent Piers & Fins [MEDIUM-HIGH]
- **Observed in Reference Photograph:** Warm beige/terracotta vertical fluted piers rise vertically across the central bays.
- **Current Model Status:** Vertical fins exist but their tone is slightly dark timber (0.58, 0.36, 0.24).
- **Exact Action:** Calibrate 'Mat_Fluted_Timber_Accent' to warm architectural sandstone/terracotta tone (0.72, 0.48, 0.32) matching the sunlit photograph.

### Rank 4: Ground Podium & Entrance Canopy Detailing [MEDIUM]
- **Observed in Reference Photograph:** Spacious clear glazed double-height lobby with clean drop-off turnaround and lush flanking perimeter trees.
- **Current Model Status:** Podium is modeled at 4.5m double height with canopy columns; tree placements are good.
- **Exact Action:** Maintain 4.5m double height and add refined paved entrance driveway textures and warm interior lobby lighting.

### Rank 5: Hero Camera Angle Calibration [HIGH (Direct Side-by-Side Fidelity)]
- **Observed in Reference Photograph:** Camera is stationed at the South-East corner driveway looking up at ~15° pitch, capturing the full soaring elevation from podium to pergola.
- **Current Model Status:** Milestone 1 camera is close but can be matched within fraction-of-a-degree precision to produce an exact side-by-side overlay.
- **Exact Action:** Create dedicated camera 'Hero_Photo_Match_Cam' calibrated directly to the focal length (28mm equivalent) and exact viewpoint of the reference photograph.

## 3. Targeted Model Files & Automation Scripts
- Target Master Model: `blender/kalidasa42_animated_v001.blend`
- Dedicated Exterior Refinement Script: `scripts/calibrate_exterior_photorealism.py`
- Comparison Output: `renders/preview/exterior_photo_comparison_side_by_side.png`
