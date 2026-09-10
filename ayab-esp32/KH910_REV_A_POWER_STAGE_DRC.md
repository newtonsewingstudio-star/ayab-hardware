# KH910 Rev A — Disposable Power Stage DRC

This report describes a disposable candidate. The staged PCB is not source-of-truth and must not be promoted unless every required route and validation passes.

## Routing result
```text
POWER_STAGE_OK /tmp/rev-a-power-stage.kicad_pcb
REMOVED_BYPASS_TRACKS 3
REMOVED_GPIO4_TRACKS 1
RAW_ROUTE_POINTS 300.95,154.35 301.25,154.25 302.25,154.25 302.25,157.00 297.75,157.00 297.75,155.00 295.75,155.00 295.75,136.50 297.75,136.50 297.75,135.00 307.00,135.00 307.23,134.89
LOCAL_SENSE_ROUTE_POINTS 224.18,159.00 224.18,157.00 229.32,157.00 229.32,159.00
GPIO_FRONT_ROUTE_POINTS reused-source-corridor
SENSE_BOTTOM_ROUTE_POINTS reused-source-corridor
SENSE_ROUTE_POINTS 
SENSE_ROUTE_LAYER -1
PLUS12_ROUTE_POINTS 225.82,159.00 225.82,163.10
PLUS12_ROUTE_LAYER 2
PLUS12_BOTTOM_ROUTE_POINTS 225.82,159.00 225.82,163.10
GROUND_ROUTE_POINTS 
GROUND_ROUTE_LAYER 2
GROUND_BOTTOM_ROUTE_POINTS 
ROUTE_STUDY_FAILURES no route for /ESP32/MACHINE_PWR_SENSE from (211.667, 159.717) to (224.175, 159.0) on layer 2; no route for /ESP32/MACHINE_PWR_SENSE from (211.667, 159.717) to (224.175, 159.0) on layer 4; no route for /ESP32/MACHINE_PWR_SENSE from (211.667, 159.717) to (224.175, 159.0) on layer 6; no route for /ESP32/MACHINE_PWR_SENSE from (211.667, 159.717) to (224.175, 159.0) on layer 0
```

## Source-board DRC
```text
** Drc report for ayab-esp32.kicad_pcb **
** Created on 2026-09-10T23:00:34+0000 **
** Report includes: Errors, Warnings **

** Found 0 DRC violations **

** Found 0 unconnected pads **

** Found 0 Footprint errors **

** End of Report **
```

## Staged-board DRC
```text
** Drc report for rev-a-power-stage.kicad_pcb **
** Created on 2026-09-10T23:00:35+0000 **
** Report includes: Errors, Warnings **

** Found 8 DRC violations **
[solder_mask_bridge]: Front solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(211.6670 mm, 159.7170 mm): Via [/ESP32/MACHINE_PWR_SENSE] on F.Cu - B.Cu
    @(212.5875 mm, 160.1374 mm): PTH pad 7 [/ESP32/EOL_R_N] of J701
[solder_mask_bridge]: Rear solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(211.6670 mm, 159.7170 mm): Via [/ESP32/MACHINE_PWR_SENSE] on F.Cu - B.Cu
    @(212.5875 mm, 160.1374 mm): PTH pad 7 [/ESP32/EOL_R_N] of J701
[clearance]: Clearance violation ( clearance 0.1000 mm; actual 0.0250 mm)
    Local override; error
    @(210.9674 mm, 151.8547 mm): Track [/ESP32/EOL_R_P] on B.Cu, length 9.4327 mm
    @(211.1674 mm, 158.7173 mm): Track [/ESP32/MACHINE_PWR_SENSE] on B.Cu, length 1.1176 mm
[shorting_items]: Items shorting two nets (nets /ESP32/EOL_R_N and /ESP32/MACHINE_PWR_SENSE)
    Local override; error
    @(197.2025 mm, 159.8050 mm): Track [/ESP32/EOL_R_N] on F.Cu, length 15.0526 mm
    @(211.6670 mm, 159.7170 mm): Via [/ESP32/MACHINE_PWR_SENSE] on F.Cu - B.Cu
[shorting_items]: Items shorting two nets (nets /ESP32/EOL_R_N and /ESP32/MACHINE_PWR_SENSE)
    Local override; error
    @(212.5875 mm, 160.1374 mm): PTH pad 7 [/ESP32/EOL_R_N] of J701
    @(211.6670 mm, 159.7170 mm): Via [/ESP32/MACHINE_PWR_SENSE] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.1000 mm; actual 0.0370 mm)
    Local override; error
    @(212.5875 mm, 160.1374 mm): PTH pad 7 [/ESP32/EOL_R_N] of J701
    @(211.1674 mm, 158.7173 mm): Track [/ESP32/MACHINE_PWR_SENSE] on B.Cu, length 1.1176 mm
[hole_clearance]: Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0120 mm)
    Rule: board setup constraints hole; error
    @(212.5875 mm, 160.1374 mm): PTH pad 7 [/ESP32/EOL_R_N] of J701
    @(211.6670 mm, 159.7170 mm): Via [/ESP32/MACHINE_PWR_SENSE] on F.Cu - B.Cu
[via_dangling]: Via is not connected or connected on only one layer
    Local override; warning
    @(224.1750 mm, 159.0000 mm): Via [/ESP32/MACHINE_PWR_SENSE] on F.Cu - B.Cu

** Found 1 unconnected pads **
[unconnected_items]: Missing connection between items
    Local override; error
    @(224.1750 mm, 159.0000 mm): Via [/ESP32/MACHINE_PWR_SENSE] on F.Cu - B.Cu
    @(211.1674 mm, 158.7173 mm): Track [/ESP32/MACHINE_PWR_SENSE] on B.Cu, length 1.1176 mm

** Found 0 Footprint errors **

** End of Report **
```
