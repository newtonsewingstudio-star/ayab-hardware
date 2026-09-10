# KH910 Rev A — Disposable Power Stage DRC

This report describes a disposable candidate. The staged PCB is not source-of-truth and must not be promoted unless every required route and validation passes.

## Routing result
```text
POWER_STAGE_OK /tmp/rev-a-power-stage.kicad_pcb
REMOVED_BYPASS_TRACKS 3
REMOVED_GPIO4_TRACKS 1
RAW_ROUTE_POINTS 300.95,154.35 301.25,154.25 302.25,154.25 302.25,157.00 297.75,157.00 297.75,155.00 295.75,155.00 295.75,136.50 297.75,136.50 297.75,135.00 307.00,135.00 307.23,134.89
LOCAL_SENSE_ROUTE_POINTS 217.68,159.00 217.68,157.00 222.82,157.00 222.82,159.00
GPIO_FRONT_ROUTE_POINTS reused-source-corridor
SENSE_BOTTOM_ROUTE_POINTS reused-source-corridor
SENSE_ROUTE_POINTS 211.17,158.72 213.00,158.70 214.00,159.00 217.68,159.00
SENSE_ROUTE_LAYER 2
PLUS12_ROUTE_POINTS 219.32,159.00 219.32,163.10
PLUS12_ROUTE_LAYER 2
PLUS12_BOTTOM_ROUTE_POINTS 219.32,159.00 219.32,163.10
GROUND_ROUTE_POINTS 
GROUND_ROUTE_LAYER 2
GROUND_BOTTOM_ROUTE_POINTS 
ROUTE_STUDY_FAILURES 
```

## Source-board DRC
```text
** Drc report for ayab-esp32.kicad_pcb **
** Created on 2026-09-10T22:55:59+0000 **
** Report includes: Errors, Warnings **

** Found 0 DRC violations **

** Found 0 unconnected pads **

** Found 0 Footprint errors **

** End of Report **
```

## Staged-board DRC
```text
** Drc report for rev-a-power-stage.kicad_pcb **
** Created on 2026-09-10T22:56:01+0000 **
** Report includes: Errors, Warnings **

** Found 6 DRC violations **
[solder_mask_bridge]: Rear solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(222.4000 mm, 155.4000 mm): Track [SOLENOID_PWR_EN] on B.Cu, length 9.3338 mm
    @(219.3250 mm, 159.0000 mm): Pad 1 [+12V] of R215 on B.Cu
[tracks_crossing]: Tracks crossing
    Local override; error
    @(217.6750 mm, 157.0000 mm): Track [/ESP32/MACHINE_PWR_SENSE] on B.Cu, length 5.1500 mm
    @(222.4000 mm, 155.4000 mm): Track [SOLENOID_PWR_EN] on B.Cu, length 9.3338 mm
[shorting_items]: Items shorting two nets (nets /ESP32/EOL_R_P and /ESP32/MACHINE_PWR_SENSE)
    Local override; error
    @(213.8700 mm, 160.4812 mm): Track [/ESP32/EOL_R_P] on B.Cu, length 1.6263 mm
    @(214.0000 mm, 159.0000 mm): Track [/ESP32/MACHINE_PWR_SENSE] on B.Cu, length 3.6750 mm
[clearance]: Clearance violation ( clearance 0.1000 mm; actual 0.0250 mm)
    Local override; error
    @(211.1674 mm, 158.7173 mm): Track [/ESP32/MACHINE_PWR_SENSE] on B.Cu, length 1.8327 mm
    @(210.9674 mm, 151.8547 mm): Track [/ESP32/EOL_R_P] on B.Cu, length 9.4327 mm
[clearance]: Clearance violation ( clearance 0.1000 mm; actual 0.0198 mm)
    Local override; error
    @(214.0000 mm, 159.0000 mm): Track [/ESP32/MACHINE_PWR_SENSE] on B.Cu, length 3.6750 mm
    @(213.8700 mm, 158.8549 mm): Track [/ESP32/EOL_R_P] on B.Cu, length 1.7784 mm
[tracks_crossing]: Tracks crossing
    Local override; error
    @(213.0000 mm, 158.7000 mm): Track [/ESP32/MACHINE_PWR_SENSE] on B.Cu, length 1.0440 mm
    @(213.8700 mm, 160.4812 mm): Track [/ESP32/EOL_R_P] on B.Cu, length 1.6263 mm

** Found 0 unconnected pads **

** Found 0 Footprint errors **

** End of Report **
```
