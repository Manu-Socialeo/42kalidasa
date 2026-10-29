# Kalidasa 42 — Camera Path & Animation Notes

**Project:** Kalidasa 42 (Site No. 42, Kalidasa Road, Block-III, Jayalakshmipuram, Mysuru)  
**Animation Length:** 180 Frames @ 24 fps (7.5 seconds real-time / scrubbable scroll journey)  
**Master File:** `blender/kalidasa42_animated_v001.blend`  
**Preview Output:** `renders/preview/camera_path_preview.mp4`  

---

## 1. Sequence Architecture & Choreography

The camera journey is engineered to match the scroll-driven storytelling arc specified in the architectural mandate and the reference animation `kalidasa_video.mov`.

| Milestone | Frame Range | Camera Position (X, Y, Z) | Target Coordinates (X, Y, Z) | Focal Length | Narrative Architectural Focus |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Exterior Establishing Hero** | Frames 1 – 40 | `(24.0, -70.0, 8.0)` $\to$ `(22.0, -60.0, 14.0)` | `(5.0, 0.0, 32.0)` $\to$ `(4.0, 0.0, 34.0)` | 24mm | Low-angle perspective looking up from South-East driveway; emphasizes 67.7m height, entrance canopy, plinth, and rhythm of curved balconies. |
| **2. Upward Orbital Climb** | Frames 41 – 80 | `(8.0, -56.0, 30.0)` $\to$ `(-18.0, -48.0, 48.0)` | `(2.0, 0.0, 40.0)` $\to$ `(-2.0, 0.0, 48.0)` | 26mm – 28mm | Sweeping orbital ascent tracking the Southern facade; reveals vertical terracotta fins and undulating cantilever balustrades with continuous parallax. |
| **3. Rooftop Sky Lounge & Pool** | Frames 81 – 125 | `(-14.0, -32.0, 69.0)` $\to$ `(8.0, -26.0, 71.5)` | `(6.0, 2.0, 65.5)` $\to$ `(6.0, 0.0, 65.5)` | 30mm – 32mm | Crests the rooftop parapet at +71.5m; showcases 19th floor sky lounge glazing, cyan lap pool (11.8m × 4.0m), and pergola shading louvers against sky. |
| **4. Descending Balcony Approach** | Frames 126 – 162 | `(21.0, -22.0, 42.0)` $\to$ `(21.5, -12.5, 29.3)` | `(16.0, -7.0, 28.5)` $\to$ `(16.0, -6.0, 28.5)` | 26mm $\to$ 24mm | Dynamic helical descent homing in on Floor 08 ($Z = +27.60\text{ m}$ FFL); captures curved glass railing, bronze caps, and warm cove lighting. |
| **5. Balcony Threshold Glide** | Frames 163 – 180 | `(18.0, -8.5, 28.9)` $\to$ `(14.5, -5.5, 28.8)` | `(12.0, -3.0, 28.7)` $\to$ `(10.0, -1.5, 28.7)` | 22mm | Glides across the cantilevered balcony deck, through open sliding doors `SD1`, settling into the Statuario marble living room and dining zone. |

---

## 2. Mathematical Trajectory & Curve Smoothing

- **Trajectory Type:** Continuous 3D compound spline (Helical ascent $\to$ Cresting orbit $\to$ Helical descent $\to$ Linear dolly).
- **Interpolation:** 100% Bezier with automated continuous tangent handles (`handle_type = 'AUTO'`) ensuring zero angular jerks or sudden velocity discontinuities.
- **Orientation Control:** Track-To constraint anchored to `Cinematic_Cam_Target` empty with `TRACK_NEGATIVE_Z` and `UP_Y`, guaranteeing that the camera never rolls on its horizontal axis during complex vertical ascents.
- **Sensor & Optics:** 35mm full-frame digital sensor equivalent ($36\text{ mm} \times 24\text{ mm}$). Dynamic focal length shift (24mm $\to$ 32mm $\to$ 22mm) dynamically balances exterior vastness with interior intimacy.

---

## 3. Web Scroll Synchronization Profile

- In the final website implementation (Stage 10), the 180 frames will map directly to normalized viewport scroll:
  - $0.00 - 0.22$: Exterior Establishing (Milestone 1)
  - $0.22 - 0.45$: Orbital Facade Climb (Milestone 2)
  - $0.45 - 0.70$: Rooftop Sky Lounge & Pool (Milestone 3)
  - $0.70 - 0.90$: Balcony Descent (Milestone 4)
  - $0.90 - 1.00$: Interior Living Reveal (Milestone 5)
