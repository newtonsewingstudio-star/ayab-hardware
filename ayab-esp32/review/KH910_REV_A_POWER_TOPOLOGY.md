# KH910 Rev A — Prototype Power PCB Parity Audit

Read-only comparison of the schematic-derived Rev A power circuit with the physical PCB.

## Seed components

- R215: schematic `47k`; PCB present
- R216: schematic `10k`; PCB present
- TP603: schematic `3V3`; PCB present
- U403: schematic `LM66100DCKR`; PCB present
- U601: schematic `XL1509`; PCB present
- U602: schematic `XL1509`; PCB present

## Local power nets and directly attached components

- `/ESP32/MACHINE_PWR_SENSE`: `R215`, `R216`, `U201`
- `/PSU/3V3_SW`: `C613`, `C615`, `C617`, `C619`, `C621`, `L602`, `R609`, `R610`, `TP603`
- `/PSU/5V_SW`: `C612`, `C614`, `C616`, `C618`, `C620`, `L601`, `R608`, `TP602`, `U403`
- `Net-(D605-K)`: `D605`, `L601`, `U601`
- `Net-(D606-K)`: `D606`, `L602`, `U602`
- `Net-(U601-FB)`: `C614`, `R606`, `R608`, `U601`
- `Net-(U602-FB)`: `C615`, `R607`, `R609`, `U602`
- `unconnected-(U403-N/C-Pad4)`: `U403`

## Required PCB parity

- C612 `220u`: present
- C613 `220u`: present
- C614 `3n3`: present
- C615 `3n3`: present
- C616 `10u`: present
- C617 `10u`: present
- C618 `10u`: present
- C619 `10u`: present
- C620 `10u`: present
- C621 `10u`: present
- D605 `SS54`: present
- D606 `SS54`: present
- L601 `47uH`: present
- L602 `47uH`: present
- R215 `47k`: present
- R216 `10k`: present
- R606 `1k`: present
- R607 `1k`: present
- R608 `3k3`: present
- R609 `1k8`: present
- R610 `0R`: present
- TP602 `5V`: present
- TP603 `3V3`: present
- U201 `ESP32-S3-MINI-1`: present
- U403 `LM66100DCKR`: present
- U601 `XL1509`: present
- U602 `XL1509`: present

## Pin-level power topology

- R215.1: schematic `+12V`; matches
- R215.2: schematic `/ESP32/MACHINE_PWR_SENSE`; matches
- R216.1: schematic `/ESP32/MACHINE_PWR_SENSE`; matches
- R216.2: schematic `GND`; matches
- TP603.1: schematic `/PSU/3V3_SW`; matches
- U403.1: schematic `/PSU/5V_SW`; matches
- U403.2: schematic `GND`; matches
- U403.3: schematic `+5V`; matches
- U403.4: schematic `unconnected-(U403-N/C-Pad4)`; **PCB `unconnected`**
- U403.5: schematic `GND`; matches
- U403.6: schematic `+5V`; matches
- U601.1: schematic `+12V`; matches
- U601.2: schematic `Net-(D605-K)`; matches
- U601.3: schematic `Net-(U601-FB)`; matches
- U601.4: schematic `GND`; matches
- U601.5: schematic `GND`; matches
- U601.6: schematic `GND`; matches
- U601.7: schematic `GND`; matches
- U601.8: schematic `GND`; matches
- U602.1: schematic `+5V`; matches
- U602.2: schematic `Net-(D606-K)`; matches
- U602.3: schematic `Net-(U602-FB)`; matches
- U602.4: schematic `GND`; matches
- U602.5: schematic `GND`; matches
- U602.6: schematic `GND`; matches
- U602.7: schematic `GND`; matches
- U602.8: schematic `GND`; matches

## Preserved GPIO/control topology

- GPIO4 is machine-power sense: **PASS**
- active right end-stop remains on GPIO17: **PASS**
- J701.7 remains tied locally to U701.15: **PASS**

## Result

**BLOCKED:** the prototype power circuit is not fully represented on the PCB.
- Topology mismatch: `U403.4` expected `unconnected-(U403-N/C-Pad4)`, found `unconnected`
