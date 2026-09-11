# KH910 Rev A — Final Preorder Audit Repair Closure

Review date: 2026-09-11

This record closes the ten repair-order findings reported against commit `032c31c`. It documents CAD and source-validation work only. It does not authorize fabrication, claim surge certification, or replace first-article bring-up.

## Finding dispositions

| Audit item | Disposition | Evidence in the corrected source |
|---|---|---|
| N1 — D605/D606 ordering identity | Closed | Both SS54 rectifiers now identify MDD part `SS54`, LCSC `C22452`, with the SS54 datasheet. The LED code `C2290` is prohibited for these rectifier positions by the manufacturing validator; actual indicator LEDs legitimately retain it. D204 was normalized to the same identity. |
| N2 — footprint schematic paths | Closed | R213/R214 now have their native ESP32-sheet paths. R735–R738 now point to their current connector-sheet symbols. Exact paths are enforced by `validate_rev_a_manufacturing_metadata.py`. |
| N3 — inner copper ambiguity | Closed | The modeled stackup is 35 µm outer / 17.5 µm inner copper. The core was adjusted so modeled thickness remains 1.6062 mm. The manufacturing profile requires at least these copper weights. |
| N4 — revision silk overlap | Closed | `KH910 REV A 09/2026` moved to `(174.0, 161.2)` on F.SilkS. Fresh front copper/silk and 3D renders show it clear of J406. The coordinate is validator-controlled. |
| N5 — clamp-current overclaim | Closed | The validator and fail-safe review now distinguish conditional 3.6 V-node calculations from deliberately loose current bounds and explicitly state that neither proves GPIO voltage or surge compliance. |
| N6 — unresolved 3D models | Closed | All 165 project-local model references were rebased to the repository library and resolve. The remaining model is from KiCad's standard library. Fresh top and bottom native renders load the board models. |
| N7 — critical-part metadata | Closed | D204/D205/D206/D601/D605/D606 now carry explicit device descriptions and datasheets; D601 also carries its MBF package metadata. These fields are checked automatically. |
| N8 — fabrication-output wording | Closed | Review language now says no AYAB-ESP32 release fabrication output was generated and separately acknowledges unrelated historical Gerbers elsewhere in the repository. |
| N9 — KiCad 10 annotation warning | Closed | Stale foreign-project instance blocks and duplicate power-symbol references were removed. KiCad 10.0.6 ERC reports 0 errors and 0 warnings, without the annotation warning. A before/after netlist comparison retained 152 nets with no connectivity differences. |
| N10 — M3/M2 mismatch | Closed | All six board and schematic mounting values now say M2, matching the inherited `MountingHole_2.2mm_M2_DIN965_Pad` footprint and 2.2 mm drills. The geometry was not enlarged or otherwise changed. |

## Local validation reproduced after repair

- KiCad 9.0.9 PCB DRC with schematic parity: 0 violations, 0 unconnected items, 0 schematic parity issues.
- KiCad 10.0.6 board DRC: 0 violations, 0 unconnected items.
- KiCad 10.0.6 ERC: 0 errors, 0 warnings.
- KiCad 10.0.6 supplemental board-to-schematic field comparison reports inherited local `Description` overrides only; it reports no geometry or connectivity fault and is not counted as the KiCad 9 controlled parity gate.
- GPIO/pin-map, Hall parity, KL parity, power parity, prototype parity, machine-sense protection, solenoid gate source, solenoid PCB fail-safe, and manufacturing-metadata checks pass.
- Fresh top, bottom, top-copper/silk, and bottom-copper/silk views received a visual sanity review with no visible blocker.

The relevant GitHub Actions run must still pass for the pushed repair commit before this closure is considered complete. Physical connector fit, rail/transient measurements, ADC calibration, reset/brownout behavior, current, and thermal tests remain post-assembly gates for the first one-off prototype.
