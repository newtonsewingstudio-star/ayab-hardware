# KH910 Rev A — PCB Editing Method

Status: implementation rule for Rev A physical-layout work.

## Decision

Use KiCad's native `pcbnew` Python API for physical PCB edits wherever practical. Do not rely on direct `.kicad_pcb` text serialization for final placement/routing.

The existing text-patch scripts remain useful for diagnostics, staged comparisons, net-name inspection, and proving small metadata changes, but they are not the fabrication path for new copper geometry.

## Why this changed

The first solenoid fail-safe PCB attempt exposed two independent failure modes in hand-edited KiCad text:

1. A substring insertion helper matched a `zone` nested inside a footprint rather than a root-level board zone, so otherwise-valid track syntax was inserted inside the footprint definition and KiCad refused to load the board.
2. The text-level pad-coordinate helper used a conventional Cartesian rotation transform. KiCad board coordinates use the opposite rotation sense for this purpose; rotated footprints therefore produced incorrect physical pad coordinates. This sent routing toward the wrong ULN2003 and capacitor pads and misinterpreted the rotated Q805 SOT-23 pins.

These are tooling failures, not electrical-architecture failures.

## CI proof

`ayab-esp32/tools/probe_pcbnew_api.py` is exercised by `.github/workflows/kh910-rev-a-pcbnew-probe.yml` after installing the repository's KiCad 9 dependencies.

The probe requires KiCad itself to resolve these known physical pad positions:

- U302 pad 9: 124.005 mm, 141.800 mm
- C302 pad 1: 109.625 mm, 140.375 mm
- U201 pad 25 / GPIO21: 225.825 mm, 136.675 mm

It also runs a `ZONE_FILLER` pass in memory. The first CI probe passed on 2026-09-09.

## Rev A layout workflow

1. Keep schematic architecture authoritative.
2. Load the current board through `pcbnew`.
3. Resolve pads by footprint reference + pad number, never by hard-coded transformed coordinates.
4. Resolve nets by name and/or KiCad net objects.
5. Move/add footprints through KiCad objects.
6. Remove/reassign existing tracks using KiCad connectivity and geometry.
7. Add new tracks/vias through KiCad objects.
8. Refill zones through KiCad before DRC.
9. Save the board through KiCad.
10. Run direct DRC plus the repository jobset.
11. Compare new DRC findings with the pre-change baseline; do not treat pre-existing prototype-board findings as new Rev A failures.
12. Commit physical PCB changes only after the new circuitry has no unresolved shorts, clearance faults, or unintended unconnected items.

## Solenoid fail-safe sequencing

The fail-safe schematic remains part of Rev A. Its first physical placement should not be forced into the presently crowded right-side corridor.

Rev A already intends to replace the obsolete LM393-based carriage/Hall conditioning. Completing that redesign first is advantageous because it removes/reduces circuitry in the same general right-side region and creates cleaner placement/routing space for:

- Q805 high-side P-channel MOSFET,
- Q806 gate pull-down MOSFET,
- R820/R821/R822,
- TP703 switched-solenoid-rail test point.

Therefore the preferred sequence is:

1. complete the KH910 K/L + analog Hall conditioning redesign;
2. remove obsolete comparator circuitry and reconcile the PCB;
3. re-audit the freed board area;
4. place and route the hardware-default-OFF solenoid gate with `pcbnew`;
5. refill zones and run DRC.

## Fabrication rule

Do not fabricate the current PCB. The solenoid fail-safe schematic is intentional, but its final physical placement/routing is not yet accepted.
