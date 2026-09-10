# KH910 Rev A — Disposable Power Stage DRC

This report describes a disposable candidate. The staged PCB is not source-of-truth and must not be promoted unless every required route and validation passes.

## Routing result
```text
POWER_STAGE_OK /tmp/rev-a-power-stage.kicad_pcb
REMOVED_BYPASS_TRACKS 3
REMOVED_GPIO4_TRACKS 1
RAW_ROUTE_POINTS 300.95,154.35 301.25,154.25 302.25,154.25 302.25,157.00 297.75,157.00 297.75,155.00 295.75,155.00 295.75,136.50 297.75,136.50 297.75,135.00 307.00,135.00 307.23,134.89
LOCAL_SENSE_ROUTE_POINTS 208.82,160.00 208.82,158.25 203.68,158.25 203.68,160.00
GPIO_FRONT_ROUTE_POINTS reused-source-corridor
SENSE_BOTTOM_ROUTE_POINTS reused-source-corridor
SENSE_ROUTE_POINTS 211.17,158.72 211.40,158.95 211.40,161.75 208.82,161.75 208.82,160.00
SENSE_ROUTE_LAYER 2
PLUS12_ROUTE_POINTS 205.32,160.00 205.32,163.10
PLUS12_ROUTE_LAYER 2
PLUS12_BOTTOM_ROUTE_POINTS 205.32,160.00 205.32,163.10
GROUND_ROUTE_POINTS 
GROUND_ROUTE_LAYER 2
GROUND_BOTTOM_ROUTE_POINTS 
ROUTE_STUDY_FAILURES 
```

## Source-board DRC
```text
** Drc report for ayab-esp32.kicad_pcb **
** Created on 2026-09-10T22:54:14+0000 **
** Report includes: Errors, Warnings **

** Found 0 DRC violations **

** Found 0 unconnected pads **

** Found 0 Footprint errors **

** End of Report **
```

## Staged-board DRC
```text
** Drc report for rev-a-power-stage.kicad_pcb **
** Created on 2026-09-10T22:54:16+0000 **
** Report includes: Errors, Warnings **

** Found 6 DRC violations **
[tracks_crossing]: Tracks crossing
    Local override; error
    @(205.3250 mm, 160.0000 mm): Track [+12V] on B.Cu, length 3.1000 mm
    @(215.8000 mm, 162.0000 mm): Track [SOLENOID_PWR_EN] on B.Cu, length 89.8000 mm
[shorting_items]: Items shorting two nets (nets /ESP32/MACHINE_PWR_SENSE and SOLENOID_PWR_EN)
    Local override; error
    @(211.4000 mm, 161.7500 mm): Track [/ESP32/MACHINE_PWR_SENSE] on B.Cu, length 2.5750 mm
    @(215.8000 mm, 162.0000 mm): Track [SOLENOID_PWR_EN] on B.Cu, length 89.8000 mm
[tracks_crossing]: Tracks crossing
    Local override; error
    @(211.4000 mm, 158.9500 mm): Track [/ESP32/MACHINE_PWR_SENSE] on B.Cu, length 2.8000 mm
    @(210.9674 mm, 161.2874 mm): Track [/ESP32/EOL_R_P] on B.Cu, length 2.0964 mm
[clearance]: Clearance violation ( clearance 0.1000 mm; actual 0.0250 mm)
    Local override; error
    @(211.1674 mm, 158.7173 mm): Track [/ESP32/MACHINE_PWR_SENSE] on B.Cu, length 0.3290 mm
    @(210.9674 mm, 151.8547 mm): Track [/ESP32/EOL_R_P] on B.Cu, length 9.4327 mm
[shorting_items]: Items shorting two nets (nets /ESP32/MACHINE_PWR_SENSE and SOLENOID_PWR_EN)
    Local override; error
    @(211.4000 mm, 158.9500 mm): Track [/ESP32/MACHINE_PWR_SENSE] on B.Cu, length 2.8000 mm
    @(215.8000 mm, 162.0000 mm): Track [SOLENOID_PWR_EN] on B.Cu, length 89.8000 mm
[shorting_items]: Items shorting two nets (nets SOLENOID_PWR_EN and /ESP32/MACHINE_PWR_SENSE)
    Local override; error
    @(215.8000 mm, 162.0000 mm): Track [SOLENOID_PWR_EN] on B.Cu, length 89.8000 mm
    @(208.8250 mm, 161.7500 mm): Track [/ESP32/MACHINE_PWR_SENSE] on B.Cu, length 1.7500 mm

** Found 1 unconnected pads **
[unconnected_items]: Missing connection between items
    Local override; error
    @(201.9999 mm, 155.2550 mm): Track [GND] on F.Cu, length 0.0130 mm
    @(207.1750 mm, 160.0000 mm): Pad 2 [GND] of R216 on B.Cu

** Found 0 Footprint errors **

** End of Report **
```
