# KH910 Rev A — Controlled One-Off Prototype Manufacturing Profile

Status: pre-order CAD constraint for the corrected revision that contains this document. This is not a fabrication package.

## Board construction

- One PCB only; no daughterboard or stacked-board requirement.
- Four copper layers, FR-4, 1.6062 mm modeled finished thickness (order as nominal 1.6 mm).
- Outer copper: at least 35 µm / 1 oz finished. Inner copper must not be less than the board house's standard 0.5 oz offering.
- Through-hole vias are permitted. Blind, buried, and microvias are not required by this design.
- Finished-hole plating and annular rings must meet IPC Class 2 or the board house's equivalent controlled prototype process.

## Enforced CAD minima

The KiCad project now rejects geometry below these values:

| Constraint | Minimum |
|---|---:|
| Copper-to-copper clearance | 0.10 mm |
| Track width | 0.10 mm |
| Copper-to-board-edge clearance | 0.25 mm |
| Finished through-hole drill | 0.20 mm |
| Via annular width | 0.05 mm |
| Via diameter | 0.30 mm |
| Hole-to-hole clearance | 0.25 mm |

Two zone-only GND stitching vias at the upper antenna recess were moved 0.30 mm inward so the 0.25 mm copper-edge rule passes. The controlled KiCad 9 DRC must report 0 violations, 0 unconnected pads, and 0 footprint/parity errors with these limits active.

## Ordering restrictions

- Select a board-house capability that meets or improves every minimum above; do not allow automatic relaxation.
- Do not let the board house substitute connector footprints, diode polarity, resistor values, DNP status, or manufacturer/order identifiers.
- The custom connector and specialty-footprint libraries are pinned in the repository. Their placed pads are compared against those pinned definitions by `tools/validate_rev_a_manufacturing_metadata.py`.
- D205/D206 use the deliberately accepted 0603 land pattern documented by the independent audit. Assembly must follow the new rear-side cathode/anode silk cues and the schematic, not a generic diode preview.
- No Gerber, drill, placement, BOM, or other manufacturing output is authorized by this profile.

## Mechanical evidence and remaining physical gate

The native board outline, central slot, mounting holes, connector rows, critical front/back placements, and both populated 3D sides were reviewed. Same-side critical component overlap was not found. The source contains the exact custom connector pad geometry used by DRC and assembly review.

CAD and photographs cannot prove connector mating force, housing height, chassis clearance, or underside tool access. Those items remain a first-article inspection gate after the one-off PCB is assembled. Any mismatch stops machine installation and solenoid testing; it does not authorize a footprint change without a new DRC/parity/audit cycle.
