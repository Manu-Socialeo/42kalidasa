# Kalidasa 42 — Cinematic Storyboard (`docs/camera_storyboard.md`)

## 1. Timeline & Video Correspondence Matrix

| Beat | Milestone | Timeline Frames | Video Timestamp | Camera Position | Optics | Observed Action |
| :---: | :--- | :---: | :---: | :--- | :---: | :--- |
| 1 | **Exterior Hero Establishing** | 1 - 40 | 0.0s - 4.5s | `(24.0, -70.0, 8.0) -> (22.0, -60.0, 14.0)` | 24mm | Ground-level perspective looking up at 67.7m tower with landscaped driveway and double-height entrance canopy. |
| 2 | **Orbital Facade Ascent** | 41 - 80 | 4.5s - 9.5s | `(8.0, -56.0, 30.0) -> (-18.0, -48.0, 48.0)` | 26mm - 28mm | Smooth orbital climb revealing rhythmic curved cantilever balconies, sky-blue glazing bands, and vertical terracotta fins. |
| 3 | **Rooftop Sky Lounge & Lap Pool** | 81 - 125 | 9.5s - 15.0s | `(-14.0, -32.0, 69.0) -> (8.0, -26.0, 71.5)` | 30mm - 32mm | Cresting parapet at +71.5m to reveal 19th-floor clubhouse glazing, 11.8m x 4.0m cyan lap pool, and pergola louvers. |
| 4 | **Balcony Descent (Floor 08)** | 126 - 162 | 15.0s - 21.0s | `(21.0, -22.0, 42.0) -> (21.5, -12.5, 29.3)` | 26mm -> 24mm | Helical diving descent targeting the 8th floor cantilevered curved deck, warm soffit cove lighting, and bronze handrails. |
| 5 | **Balcony Threshold Glide into Grand Living** | 163 - 180 | 21.0s - 26.85s | `(18.0, -8.5, 28.9) -> (14.5, -5.5, 28.8)` | 22mm | Gliding past sliding glass doors SD1 across continuous Italian Statuario marble floors into living/dining suite. |

## 2. Motion Quality & Interpolation Verification
- **Interpolation:** Native continuous 3D Bezier splines (`handle_type = 'AUTO'`).
- **Zero Discontinuity Check:** Verified forward and backward motion without sudden angular snaps or wall-clipping artifacts.
- **Orientation:** Track-To constraint anchored to target empty prevents horizontal roll during high-angle climbs.
