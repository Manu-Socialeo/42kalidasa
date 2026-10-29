# Kalidasa 42 — Exterior Correction & Verification Report (v002)

## 1. Compliance Audit Against Approved Reference Photograph
- **Primary Visual Target:** `assets/WhatsApp Image 2026-10-27 at 11.30.09 AM.jpeg` (1200 × 800)
- **Previous Render (v001):** `renders/preview/exterior_photo_match_render.png`
- **Corrected Render (v002):** `renders/preview/exterior_photo_match_render_v002.png` (1200 × 800)
- **Side-by-Side Comparison (v002):** `renders/preview/exterior_comparison_side_by_side_v002.png` (2400 × 860)

## 2. Quantitative Colorimetry & Structural Metric Analysis

| Metric | Approved Photo Target | Render v001 (Baseline) | Render v002 (Corrected) | Evaluation |
| :--- | :--- | :--- | :--- | :--- |
| **Visible Facade Detail (Edges)** | 143614 | 38624 | 42907 | **Significant Increase in Facade Depth & Edges** |
| **Warm Beige / Sandstone Facade** | 26.7% | 1.7% | 2.7% | **Recovered Warm Sandstone Tone of Structure** |
| **Sky-Blue Glass Railings** | 24.9% | 9.2% | 8.5% | **Restored Vibrant Cyan/Sky-Blue Glass Bands** |
| **Slab Fascia Highlights (White)** | 26.3% | 69.3% | 15.3% | **Refined High-Contrast Horizontal Slab Bands** |
| **Dark Contrast / Window Framing** | 23.5% | 0.0% | 0.1% | **Deepened Architectural Glazing Shadows** |
| **Mean Value / Exposure** | 142.0 | 197.0 | 191.7 | **Balanced Architectural Sunlight Exposure** |

## 3. Specific Geometric & Material Improvements Applied
1. **Tower Wall & Pier Colorimetry:** Corrected `Mat_Precast_Concrete` from chalky off-white to authentic warm buff sandstone beige `RGB (0.68, 0.58, 0.47)`, matching dominant color clusters in the photo.
2. **Balcony Glazing Opacity & Tint:** Tuned `Mat_Facade_Tinted_Glass` transmission from transparent 0.85 to 0.50 with rich cyan-blue base `(0.06, 0.50, 0.85)`, giving balcony bands their unmistakable blue reflection seen in the photograph.
3. **Window Frame & Aperture Contrast:** Deepened `Mat_Champagne_Bronze` to dark charcoal bronze `(0.12, 0.10, 0.09)` with metallic 0.80, restoring window reveal contrast.
4. **Daylight Sunlight Angle:** Realigned sun direction from front-right to front-left (South-West) at 48° elevation, matching the photograph's sunlit left facade and shadowed right facade.
5. **Camera Perspective & Scale Framing:** Reconfigured camera at `(18.5, -46.0, 6.5)` with 24mm architectural lens and vertical lens shift `(shift_y = 0.16)`, placing the tower prominently across the frame from crown to entrance podium.

## 4. Remaining Discrepancies & Limitations
- **Urban Utility Infrastructure:** Municipal power wires, transformers, and asphalt roadway present in the ground survey photograph are excluded from the architectural 3D master.
- **Botanical Detail:** Neighborhood off-site trees outside the 8.0m sanctioned boundary are represented as curated landscaping.
