# KH910 Rev A — PCB Visual Sanity Review

Review date: 2026-09-11

Verdict: **PASS for the corrected pre-order CAD revision, with no visual blocker found.** This is not a post-assembly mechanical or thermal sign-off. KiCad DRC remains authoritative for numeric clearance and connectivity.

## Views reviewed

- `KH910_REV_A_TOP.png`
- `KH910_REV_A_BOTTOM.png`
- `KH910_REV_A_TOP_COPPER.svg` / `.png`
- `KH910_REV_A_BOTTOM_COPPER.svg` / `.png`

## Findings

- The single-board outline, six upstream 2.2 mm/M2 mounting holes, long central slot, and upper edge cutouts remain intact.
- The ESP32 antenna region remains free of the new power-sense route.
- U403 is placed on the bottom side in an open region near the existing power section; its short local traces enter the pads without acute slivers or visible edge encroachment.
- R215/R216 are paired on the bottom side with a short local divider connection and clear pad access.
- D205/D206/C206 form a compact bottom-side protection cluster beside the existing GPIO4 divider route. Their sense traces enter from the net-correct side of each 0603 footprint, stay clear of the nearby ground via, and do not form the ground-plane island rejected in the preceding disposable layout.
- The protection cluster overlaps the top-side buzzer only in X/Y projection. Both assemblies are surface-mount on opposite board faces, so the PCB separates them physically; same-side courtyards remain clear and hand access is available from the bottom for a one-off build.
- The reused GPIO4 escape remains localized at U201, and the new sense route changes layers at one clear through-via rather than crossing dense surface fanout.
- The raw 12 V divider branch is short, and no new high-voltage trace is routed through USB/ESP32 antenna circuitry.
- Copper pours remain continuous around the new work, with no obvious orphan islands, unintended neck-down on the shared solenoid trunk, or silkscreen obscuring a new assembly pad.
- Connector rows, test points, and existing solenoid-gate placement remain unobstructed.
- The obsolete `C:900,965,270` connector-family legend was removed because it crossed the new gate at its old location and obscured J401/J406 when moved. The connector references remain the assembly identifiers.
- The obsolete `v0.1 rev A 02/24` badge was removed and replaced with `KH910 REV A 09/2026`. The revision text is now at (174.0, 161.2) on F.SilkS, clear of the J406 badge and readable in the fresh front render.
- New front-side `SOLENOID GATE` and `TP703 SW` labels identify the safety-critical gate and switched-rail test point without covering pads.
- New rear-side `D205 K=3V3` and `D206 A=GND` labels make both machine-sense clamp orientations explicit at assembly.
- Two GND stitching vias beside the antenna recess were shifted inward; the resulting board passes the explicit 0.25 mm copper-to-edge rule.
- All 165 repository-relative component models now resolve from `ayab-library/packages3D`; fresh native top and bottom renders were checked together with the 2D copper/silk and fabrication/courtyard views. Physical housing height and chassis fit remain first-article checks rather than inferred 3D guarantees.
- The pinned custom connector pads match every placed custom-footprint instance. Housing fit, mating force, chassis clearance, and underside tool access remain first-article physical checks.

No AYAB-ESP32 release fabrication files were produced as part of this review. Historical Gerbers for a different legacy interface remain elsewhere in the repository and are outside this release.
