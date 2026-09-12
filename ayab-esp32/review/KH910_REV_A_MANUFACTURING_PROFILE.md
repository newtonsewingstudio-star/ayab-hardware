# KH910 Rev A — Controlled One-Off Prototype Manufacturing Profile

Status: pre-order CAD constraint for the corrected revision that contains this document. This is not a fabrication package.

## Board construction

- One PCB only; no daughterboard or stacked-board requirement.
- Four copper layers, FR-4, 1.6062 mm modeled finished thickness (order as nominal 1.6 mm).
- Controlled stackup: 35 µm / 1 oz nominal copper on F.Cu and B.Cu; 17.5 µm / 0.5 oz nominal copper on In1.Cu and In2.Cu. Do not accept thinner copper on any layer.
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

The manufacturing validator additionally requires every serialized footprint-tree UUID—including nested pads, fields, text, and graphics—to be unique. It also checks the complete revision-marking bounding box with margin against the native board outline, front pad/mask regions, footprint courtyards, and other silkscreen. These are explicit preorder source-integrity checks because native DRC alone does not detect copied object identities or guarantee useful marking placement.

## Ordering restrictions

- Select a board-house capability that meets or improves every minimum above; do not allow automatic relaxation.
- Do not let the board house substitute connector footprints, diode polarity, resistor values, DNP status, or manufacturer/order identifiers.
- The custom connector and specialty-footprint libraries are pinned in the repository. Their placed pads are compared against those pinned definitions by `tools/validate_rev_a_manufacturing_metadata.py`.
- D205/D206 use the deliberately accepted 0603 land pattern documented by the independent audit. Assembly must follow the new rear-side cathode/anode silk cues and the schematic, not a generic diode preview.
- D204/D605/D606 are MDD SS54 SMA Schottky rectifiers, orderable as LCSC C22452. C2290 is an LED and is prohibited for those three rectifier positions; the board's actual indicator LEDs legitimately retain C2290.
- No Gerber, drill, placement, BOM, or other manufacturing output is authorized by this profile.

## Assembly-release preflight

The frozen population contains 153 fitted BOM references: 133 SMD and 20 through-hole. Every fitted item is present in placement data. All but five fitted specialty machine connectors have an LCSC identifier.

The five connectors without LCSC identifiers are J403/J405 `HNC2-2.5P-10DS(02)`, J404 `HNC2-2.5P-8DS(02)`, J408 `HNC2-2.5P-3DS(02)`, and the non-KH910 J406 `A2506WV-10P`. For the KH910 prototype, J403/J404/J405/J408 must be sourced exactly and either consigned to the assembler or installed afterward. They must not be silently substituted with a generic 2.5 mm header because mating and housing geometry are part of the machine interface. J406 may remain part of the general multi-machine population, but it is not a KH910 mating connector.

The controlled supplier record, dated stock observations, substitution rules, spare quantities, and manufacturer-installation decision path are in [`KH910_REV_A_CONNECTOR_SOURCING.md`](KH910_REV_A_CONNECTOR_SOURCING.md). The preferred path is an exact-MPN New Parts Request or Global Sourcing match. Consignment is supported but may be poor value for a one-off; qualified local installation remains the controlled fallback. No order-specific manufacturer BOM may be released until the exact private/global/consigned part identifiers are known and explicitly matched.

The JLC BOM and placement converters are regression-tested against the current ten-column KiCad BOM, legacy AYAB BOM formats, KiCad placement files with and without a footer, and top/bottom layer conversion. This preflight does not constitute component-stock confirmation; availability and every proposed substitution must be reviewed at quote time.

## Mechanical evidence and remaining physical gate

The native board outline, central slot, mounting holes, connector rows, and critical front/back placements were reviewed. All 165 repository-supplied model references resolve through `${KIPRJMOD}/../ayab-library/packages3D`; the one remaining model uses KiCad's standard 3D library. Fresh top and bottom native renders are supporting visual evidence, while 2D fabrication/courtyard views remain authoritative for pad and body-outline checks. Same-side critical component overlap was not found. The source contains the exact custom connector pad geometry used by DRC and assembly review.

All six grounded chassis holes retain the upstream AYAB-ESP32 geometry: `MountingHole_2.2mm_M2_DIN965_Pad` with a 2.2 mm drill. Their value is corrected to M2. This release therefore requires M2 hardware; an M3 screw is not compatible and must not be forced through the board.

CAD and photographs cannot prove connector mating force, housing height, chassis clearance, or underside tool access. Those items remain a first-article inspection gate after the one-off PCB is assembled. Any mismatch stops machine installation and solenoid testing; it does not authorize a footprint change without a new DRC/parity/audit cycle.
