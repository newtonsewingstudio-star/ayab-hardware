# KH910 Rev A — Disposable Power Stage DRC

This report describes a disposable candidate. The staged PCB is not source-of-truth and must not be promoted unless every required route and validation passes.

## Routing result
```text
POWER_STAGE_OK /tmp/rev-a-power-stage.kicad_pcb
REMOVED_BYPASS_TRACKS 3
REMOVED_GPIO4_TRACKS 1
RAW_ROUTE_POINTS 300.95,154.35 301.25,154.25 302.25,154.25 302.25,157.00 297.75,157.00 297.75,155.00 295.75,155.00 295.75,136.50 297.75,136.50 297.75,135.00 307.00,135.00 307.23,134.89
LOCAL_SENSE_ROUTE_POINTS 
GPIO_FRONT_ROUTE_POINTS reused-source-corridor
SENSE_BOTTOM_ROUTE_POINTS reused-source-corridor
SENSE_ROUTE_POINTS 
SENSE_ROUTE_LAYER -1
PLUS12_ROUTE_POINTS 
PLUS12_ROUTE_LAYER -1
PLUS12_BOTTOM_ROUTE_POINTS 
GROUND_ROUTE_POINTS 
GROUND_ROUTE_LAYER 2
GROUND_BOTTOM_ROUTE_POINTS 
ROUTE_STUDY_FAILURES no route for /ESP32/MACHINE_PWR_SENSE from (211.1674, 158.717302) to (205.675, 160.0) on layer 2 | no route for +12V from (207.325, 160.0) to (207.325, 163.1) on layer 2
```

## Source-board DRC
```text
** Drc report for ayab-esp32.kicad_pcb **
** Created on 2026-09-10T22:52:00+0000 **
** Report includes: Errors, Warnings **

** Found 0 DRC violations **

** Found 0 unconnected pads **

** Found 0 Footprint errors **

** End of Report **
```

## Staged-board DRC
```text
** Drc report for rev-a-power-stage.kicad_pcb **
** Created on 2026-09-10T22:52:01+0000 **
** Report includes: Errors, Warnings **

** Found 3 DRC violations **
[solder_mask_bridge]: Rear solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(210.9674 mm, 151.8547 mm): Track [/ESP32/EOL_R_P] on B.Cu, length 9.4327 mm
    @(210.8250 mm, 160.0000 mm): Pad 2 [GND] of R216 on B.Cu
[shorting_items]: Items shorting two nets (nets GND and /ESP32/EOL_R_P)
    Local override; error
    @(210.8250 mm, 160.0000 mm): Pad 2 [GND] of R216 on B.Cu
    @(210.9674 mm, 151.8547 mm): Track [/ESP32/EOL_R_P] on B.Cu, length 9.4327 mm
[track_dangling]: Track has unconnected end
    Local override; warning
    @(211.1674 mm, 158.7173 mm): Track [/ESP32/MACHINE_PWR_SENSE] on B.Cu, length 6.7798 mm

** Found 4 unconnected pads **
[unconnected_items]: Missing connection between items
    Local override; error
    @(210.8250 mm, 160.0000 mm): Pad 2 [GND] of R216 on B.Cu
    @(201.9999 mm, 155.2550 mm): Track [GND] on F.Cu, length 0.0130 mm
[unconnected_items]: Missing connection between items
    Local override; error
    @(116.0625 mm, 161.2000 mm): Pad 2 [+12V] of Q805 on F.Cu
    @(207.3250 mm, 160.0000 mm): Pad 1 [+12V] of R215 on B.Cu
[unconnected_items]: Missing connection between items
    Local override; error
    @(205.6750 mm, 160.0000 mm): Pad 2 [/ESP32/MACHINE_PWR_SENSE] of R215 on B.Cu
    @(209.1750 mm, 160.0000 mm): Pad 1 [/ESP32/MACHINE_PWR_SENSE] of R216 on B.Cu
[unconnected_items]: Missing connection between items
    Local override; error
    @(209.1750 mm, 160.0000 mm): Pad 1 [/ESP32/MACHINE_PWR_SENSE] of R216 on B.Cu
    @(211.1674 mm, 158.7173 mm): Track [/ESP32/MACHINE_PWR_SENSE] on B.Cu, length 6.7798 mm

** Found 0 Footprint errors **

** End of Report **
```
