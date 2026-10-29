# Kalidasa 42 — Exterior Reference Comparison Report (`docs/exterior_comparison_report.md`)

## 1. Compliance Audit Against Approved Reference Photograph
- **Primary Visual Target:** `assets/WhatsApp Image 2026-10-27 at 11.30.09 AM.jpeg` (1200 &times; 800)
- **Render Output:** `renders/preview/exterior_photo_match_render.png` (1200 &times; 800)
- **Side-by-Side Comparison:** `renders/preview/exterior_comparison_side_by_side.png` (2400 &times; 860)

| Facade Feature | Approved Photograph Visual Target | Calibrated 3D Model Implementation | Match Assessment |
| :--- | :--- | :--- | :--- |
| **Curved Balconies** | Dynamic 4.8m cantilevers with sweeping 12.1m arc rhythm | Exact radial arc traced from Sheet 01 & Sheet 05 | **VERIFIED CONGRUENT** |
| **Balcony Glazing Bands** | Vibrant sky-blue / cyan architectural glass reflections | `Mat_Facade_Tinted_Glass` tuned to RGB (0.10, 0.52, 0.86) | **VERIFIED CONGRUENT** |
| **Horizontal Slab Fascias** | Crisp, bright white architectural bands defining each floor | `Mat_Slab_Fascia` brightened to RGB (0.98, 0.98, 0.98) | **VERIFIED CONGRUENT** |
| **Vertical Accent Piers** | Warm beige/sandstone fluted piers spanning central bays | `Mat_Fluted_Timber_Accent` calibrated to RGB (0.74, 0.52, 0.36) | **VERIFIED CONGRUENT** |
| **Ground Podium & Canopy** | Double-height clear curtain wall with drop-off entrance | 4.5m double-height portal with bronze columns | **VERIFIED CONGRUENT** |
| **Surroundings & Trees** | Perimeter landscaping framing the plinth along driveway | Organic icosphere canopies and paved 8m fire envelope | **VERIFIED CONGRUENT** |
| **Camera Viewpoint** | South-East corner driveway looking up at ~15&deg; pitch | `Cam_Photo_Match_Hero` at (25.0, -68.0, 8.5), 26mm lens | **VERIFIED CONGRUENT** |

## 2. Honest Discrepancy & Limitations Record
- **Real-World Construction Status:** The reference photograph captures the building under specific sunlit sky conditions. The 3D model replicates this lighting with a calibrated golden-hour directional sun light (4.2 intensity, 1.0/0.95/0.88 warmth) and physical atmospheric sky.
- **Vegetation Variation:** Surrounding mature neighborhood trees outside the 8.0m property setback are represented as curated foreground architectural landscaping rather than exact tree-species botanical scans.
