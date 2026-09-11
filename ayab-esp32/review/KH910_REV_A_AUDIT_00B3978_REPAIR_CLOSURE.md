# KH910 Rev A — Audit 00b3978 Repair Closure

Review date: 2026-09-11

This record addresses the final independent preorder audit of branch head `00b3978`. It is a CAD closure record, not fabrication authorization or assembled-board approval.

## P2 preorder conditions

### N4 — revision marking clearance: closed

`KH910 REV A 09/2026` moved from `(174.0, 161.2)` to `(180.0, 142.0)` on F.SilkS. Its previous location crossed R713/R714 pads. The new location is visibly clear beneath the display area in fresh native 2D and populated 3D front renders.

`validate_rev_a_manufacturing_metadata.py` no longer accepts a location merely because its coordinate matches. It now requires the complete text bounding box plus margin to remain:

- inside the board-edge bounds;
- clear of front pad and solder-mask regions;
- clear of front footprint courtyards;
- clear of footprint and board silkscreen.

### N11 — duplicated PCB object identities: closed

The eight newer cloned footprint instances `R820`, `R821`, `R822`, `TP703`, `Q805`, `C206`, `D206`, and `Q806` received unique deterministic UUIDs for their footprint roots and every nested field, graphic, text, and pad object. The older source objects retained their identities.

Before repair, the serialized board contained 137 repeated UUID groups and 183 excess uses, all associated with the copied footprint trees except four normal dimension/embedded-label pairs. After repair, no UUID repeats inside or between footprint trees remain. The only four repeated raw UUIDs are KiCad's intentional association between each User.1 dimension and its own embedded dimension text; they were preserved.

A normalized before/after source comparison confirms that the PCB changed only in footprint-tree object identities and the revision-label position. Footprint geometry, placement, layers, nets, pads, schematic paths, DNP flags, tracks, vias, zones, and board outline are unchanged. KiCad 9 DRC/parity and the topology checks independently confirm the electrical result.

The manufacturing validator now scans every UUID inside every serialized footprint tree and rejects any repeated identity, so both root and nested-copy regressions are covered.

## P3 qualifications

- N12: the KiCad 10 compatibility wording now accurately identifies inherited `Description` and `Datasheet` field overrides plus TP703's `Package` override. These are not represented as electrical or purchasing-identity failures.
- N13: the R215 loose current bound no longer infers resistor-element temperature from ambient. It uses the component's full rated -55 °C to +155 °C element-temperature range, ±1% tolerance, and ±100 ppm/°C TCR, giving a conservative 45.919 kΩ minimum. The resulting loose bounds are 0.261 mA at 12 V, 0.327 mA at 15 V, and 0.871 mA at 40 V, while explicitly not guaranteeing GPIO voltage or surge compliance.

## Reproduced local result

- KiCad 9.0.9: 0 DRC violations, 0 unconnected pads, 0 footprint errors, and 0 schematic-parity issues.
- KiCad 10.0.6: 0 board DRC violations, 0 unconnected pads, 0 footprint errors; ERC 0 errors and 0 warnings.
- Machine-sense, solenoid fail-safe, prototype presence, power parity, Hall parity, K/L parity, pin-map, and manufacturing validators pass.
- `FOOTPRINT_TREE_UUIDS_UNIQUE 6053` and `REVISION_LABEL_CLEARANCE_OK` are enforced outcomes.
- Fresh front copper/silkscreen and populated 3D renders were visually reviewed with no blocker found.

The relevant GitHub Actions run must pass on the pushed repair commit before this record is complete. Physical connector fit, real rail/transient measurements, ADC calibration, reset/brownout behavior, current, and thermal testing remain first-article gates before machine or solenoid operation.
