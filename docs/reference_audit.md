# Kalidasa 42 — Architectural Reference Audit Report

**Date:** 2026-10-29  
**Stage:** 02 — Architectural Reference Audit  
**Status:** ✅ COMPLETE  

---

## 1. Executive Summary

A comprehensive architectural audit was performed using official municipal sanction drawings (`Sectional Drawing of the apartments.pdf`, Drawing No. `DWG / NS / 5692`, Sheets 01 to 06) and the verified high-resolution facade reference render from `assets/WhatsApp Image 2026-10-27 at 11.30.09 AM.jpeg`.

All vertical elevations, structural levels, footprint boundaries, typical unit floor plans, opening schedules, and site setbacks have been extracted and cross-referenced with exact source sheet numbers.

---

## 2. Document Hierarchy & Source Verification

| Document | Authority | Content |
|---|---|---|
| **DWG / NS / 5692 (Sheet 01/06)** | Official Municipal Sanction | Site Plan, setbacks, coverage, FAR, openings schedule |
| **DWG / NS / 5692 (Sheet 02/06)** | Official Municipal Sanction | Lower Basement (B2) plan, ramps, parking bays (23 nos) |
| **DWG / NS / 5692 (Sheet 03/06)** | Official Municipal Sanction | Upper Basement (B1) plan, service equipment, parking (19 nos) |
| **DWG / NS / 5692 (Sheet 04/06)** | Official Municipal Sanction | Ground Floor plan, double-height reception, business lounge |
| **DWG / NS / 5692 (Sheet 05/06)** | Official Municipal Sanction | Typical 4BHK plan (floors 2–16 & 18), 1st floor plan, 17th refuge floor, 19th clubhouse & pool plan, terrace |
| **DWG / NS / 5692 (Sheet 06/06)** | Official Municipal Sanction | Section - A (full vertical dimension chain) and Exterior Elevation |
| **WhatsApp Image 2026-10-27 (Assets)** | Design Intent Reference | Photorealistic exterior rendering for facade materials, glass tint, lighting |
| **WhatsApp Video .mov (Assets)** | Motion / Camera Reference | 26-second reference camera trajectory |

---

## 3. Site and Master Dimensions

- **Total Site Area:** 3,137.69 m²
- **Road Widening Area:** 96.31 m²
- **Net Plot Area:** 3,041.38 m²
- **Ground Footprint Area:** 404.81 m² (Ground Coverage = 12.90%, permissible = 60.0%)
- **Total Sanctioned FAR Area:** 7,012.08 m² (FAR = 2.235, permissible = 2.25)
- **Total Units:** 19 residential units (exclusive full-floor apartments)
- **Boundary Perimeters:**
  - South (5th Cross Road, 12m wide): 75.10 m
  - East (Kalidasa Main Road, 20m widening to 24m): 48.00 m
  - North-East Chamfer (11th Cross Road): 24.90 m
  - North (Private Site): 32.00 m
  - West (Private Site): 45.20 m
- **Setbacks:**
  - Front (East): 16.00 m building setback / 8.00 m fire driveway
  - South: 16.00 m building setback / 8.00 m fire driveway
  - North: 9.00 m building setback / 8.00 m fire driveway
  - West (Rear): 8.00 m fire driveway
  - Basement Boundary Setback: 3.00 m perimeter offset

---

## 4. Vertical Levels and Floor Heights (Datum: Mean Sea Level relative)

| Level | FFL (m) | Floor-to-Floor Height (m) | Function & Features |
|---|---|---|---|
| **Lower Basement (B2)** | +91.40 | 3.30 | Parking for 23 cars, driver toilet, STP, sump |
| **Upper Basement (B1)** | +94.70 | 3.60 | Parking for 19 cars, pump room, utility shafts |
| **Driveway Grade** | +97.80 | -- | Outer fire driveway and circulation perimeter |
| **Ground Floor** | +98.30 | **4.50** | Plinth (+0.50m above drive), Grand double-height Lobby, Business Center, Porch |
| **1st Floor** | +102.80 | 3.30 | Residence 01 (4BHK with Art Gallery, 349.34 m²) |
| **2nd – 16th Floors (15 floors)** | +106.10 to +152.30 | 3.30 each | Typical full-floor 4BHK units (368.06 m² net each) |
| **17th Floor (Refuge)** | +155.60 | 3.30 | Residence 17 (2BHK) + Open-to-sky Refuge Terrace (4.5m × 6.2m) |
| **18th Floor** | +158.90 | 3.30 | Typical full-floor 4BHK unit (368.06 m² net) |
| **19th Floor (Clubhouse)** | +162.20 | 3.30 | Multipurpose Hall, Gym, Pool Deck (+163.4m), 11.8m × 4.0m Lap Pool |
| **Terrace Level** | +165.50 (SSL) | 3.00 | Open terrace, pool cutout, staircase & lift headrooms |
| **Top of Roof / Parapet** | +168.50 | 1.50 | Rooftop pergola / architectural crown |
| **Lightning Arrestor** | +170.00 | -- | Highest physical element (+71.70m above Ground FFL) |

> [!NOTE]  
> **Sanctioned Height Verification:**  
> Driveway level (+97.80m) to Terrace Slab (+165.50m) = **67.70 m**, precisely matching the title block specification: `BUILDING HEIGHT : 67.70M`.

---

## 5. Typical Apartment Architecture (2nd to 16th & 18th Floors)

- **Footprint:** Overall building envelope length is 36.397 m by ~16.00 m body width.
- **Cantilever Balcony:** Sweeping curved balcony extending 4.80 m beyond the primary column line across a 12.115 m arc length.
- **Room Dimensions (Internal Clear):**
  - Living & Dining: 8.50 m × 6.20 m with sliding glass door `SD1` (3.40m × 2.40m)
  - Grand Curved Balcony: 4.80 m × 7.00 m
  - Master Bedroom: 5.00 m × 4.00 m with attached Walk-in-Wardrobe (3.10 m × 1.80 m), Master Bath (4.00 m × 1.80 m), and Private Balcony (2.10 m × 5.20 m)
  - Bedroom 2: 4.10 m × 4.40 m with Attached Bath (1.60 m × 2.80 m) and Balcony (5.40 m × 2.40 m)
  - Bedroom 3: 4.00 m × 4.40 m with Attached Bath (1.60 m × 2.80 m)
  - Bedroom 4: 3.70 m × 4.40 m with Powder Bath (1.50 m × 2.80 m)
  - Informal Living / Family Lounge: 4.00 m × 5.80 m
  - Kitchen: 3.60 m × 6.40 m with Utility & Drying Yard (4.40 m × 3.90 m)
  - Maid's Room: 1.70 m × 2.20 m with independent toilet
  - Puja Room: 1.60 m × 1.50 m
  - Private Lift Lobby: 5.60 m × 2.50 m opening directly from dual 10-passenger high-speed elevators and one 15-passenger stretcher/fire service lift.

---

## 6. Fenestration & Opening Schedule (From Sheet 01)

- **Sliding Glass Doors:**
  - `SD1`: 3400 × 2400 mm (Living to primary balcony)
  - `SD1A`: 2930 × 2400 mm
  - `SD2`: 2400 × 2400 mm (Bedrooms to balconies)
- **Windows:**
  - `W1`: 1500 × 1500 mm (Sill: 900 mm, Lintel: 2400 mm)
  - `W4`: 3000 × 1500 mm (Sill: 900 mm, Lintel: 2400 mm)
  - `W5`: 2400 × 1500 mm (Sill: 900 mm, Lintel: 2400 mm)
  - `BW1`: 1800 × 1950 mm Bay Window (Sill: 450 mm, Lintel: 2400 mm)
- **Curtain Glazing:**
  - `GL3`: 6400 × 2400 mm
  - `GL4`: 1800 × 2400 mm
  - `GL4A`: 4100 × 2400 mm
  - `GL7`: 2150 × 3400 mm
  - `GL14`: 6000 × 2400 mm (Gym overlooking pool)

---

## 7. Confirmed Facts vs. Presentation Assumptions

### Confirmed Architectural Facts
1. Building levels (2B+G+19+Terrace) and exact heights (Ground = 4.5m, upper typical = 3.3m).
2. Boundary lines, setbacks, and driveway circulation (8.0m wide fire driveway).
3. Exact unit layout and partition dimensions for typical 4BHK floor.
4. Total building height of 67.70 m.
5. Rooftop amenities: 11.8m × 4.0m pool on the 19th floor with double-height volume open to terrace above.

### Presentation Assumptions (To be calibrated in 3D)
1. Balcony curvature spline tangent points (derived from CAD outline and facade render).
2. PBR shader settings for textured exposed concrete, warm timber soffits, and champagne-bronze mullions matching the reference render.
3. Landscape perimeter planting style and ground illumination warmth (golden hour / dusk setup).

---

## 8. Stage 2 Acceptance Checklist

- [x] All major vertical levels and floor-to-floor heights traced to Sheet 06.
- [x] Boundary footprint and setbacks extracted from Sheet 01.
- [x] Representative apartment layout selected (Typical 4BHK, 2nd–16th & 18th floors).
- [x] Conflicting height values evaluated and reconciled with MCC building bylaw definitions.
- [x] Reference register, unknowns register, and audit log fully documented.

