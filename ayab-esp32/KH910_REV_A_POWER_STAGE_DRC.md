# KH910 Rev A — Disposable Power Stage DRC

This report describes a disposable candidate. The staged PCB is not source-of-truth and must not be promoted unless every required route and validation passes.

## Routing result
```text
POWER_STAGE_OK /tmp/rev-a-power-stage.kicad_pcb
REMOVED_BYPASS_TRACKS 3
REMOVED_GPIO4_TRACKS 2
RAW_ROUTE_POINTS 300.95,154.35 301.25,154.25 302.25,154.25 302.25,157.00 297.75,157.00 297.75,155.00 295.75,155.00 295.75,136.50 297.75,136.50 297.75,135.00 307.00,135.00 307.23,134.89
LOCAL_SENSE_ROUTE_POINTS 205.43,135.75 206.00,135.75 206.00,134.75 209.50,134.75 209.50,135.75 210.07,135.75
GPIO_FRONT_ROUTE_POINTS 
SENSE_BOTTOM_ROUTE_POINTS 
SENSE_ROUTE_POINTS 207.49,131.97 207.25,132.00 207.25,132.75 205.50,132.75 205.50,135.50 205.43,135.75
SENSE_ROUTE_LAYER 4
PLUS12_ROUTE_POINTS 207.07,137.00 207.00,137.25 207.00,144.00 205.00,144.00 205.00,163.00 206.75,163.00 207.00,163.10
PLUS12_ROUTE_LAYER 4
PLUS12_BOTTOM_ROUTE_POINTS 207.07,135.75 207.07,137.00
GROUND_ROUTE_POINTS 208.43,134.50 208.50,134.75 208.50,138.50 213.25,138.50 213.57,138.60
GROUND_ROUTE_LAYER 6
GROUND_BOTTOM_ROUTE_POINTS 208.43,135.75 208.43,134.50
ROUTE_STUDY_FAILURES 
```

## Source-board DRC
```text
** Drc report for ayab-esp32.kicad_pcb **
** Created on 2026-09-10T22:38:06+0000 **
** Report includes: Errors, Warnings **

** Found 0 DRC violations **

** Found 0 unconnected pads **

** Found 0 Footprint errors **

** End of Report **
```

## Staged-board DRC
```text
** Drc report for rev-a-power-stage.kicad_pcb **
** Created on 2026-09-10T22:38:07+0000 **
** Report includes: Errors, Warnings **

** Found 9 DRC violations **
[shorting_items]: Items shorting two nets (nets /ESP32/MACHINE_PWR_SENSE and GND)
    Local override; error
    @(206.0000 mm, 134.7500 mm): Track [/ESP32/MACHINE_PWR_SENSE] on B.Cu, length 3.5000 mm
    @(208.4250 mm, 134.5000 mm): Via [GND] on F.Cu - B.Cu
[shorting_items]: Items shorting two nets (nets /ESP32/HALL_L_ADC and GND)
    Local override; error
    @(207.0000 mm, 136.5000 mm): Track [/ESP32/HALL_L_ADC] on In1.Cu, length 4.2426 mm
    @(208.4250 mm, 134.5000 mm): Via [GND] on F.Cu - B.Cu
[tracks_crossing]: Tracks crossing
    Local override; error
    @(206.0000 mm, 134.7500 mm): Track [/ESP32/MACHINE_PWR_SENSE] on B.Cu, length 3.5000 mm
    @(208.4250 mm, 135.7500 mm): Track [GND] on B.Cu, length 1.2500 mm
[shorting_items]: Items shorting two nets (nets +12V and /AUX-CONNECTORS/AYAB_SCL)
    Local override; error
    @(207.0750 mm, 137.0000 mm): Via [+12V] on F.Cu - B.Cu
    @(136.3400 mm, 137.1900 mm): Track [/AUX-CONNECTORS/AYAB_SCL] on F.Cu, length 72.7300 mm
[clearance]: Clearance violation ( clearance 0.1000 mm; actual 0.0806 mm)
    Local override; error
    @(207.0750 mm, 137.0000 mm): Via [+12V] on F.Cu - B.Cu
    @(207.0000 mm, 136.5000 mm): Track [/ESP32/HALL_L_ADC] on In1.Cu, length 4.2426 mm
[clearance]: Clearance violation ( clearance 0.1000 mm; actual 0.0400 mm)
    Local override; error
    @(207.0750 mm, 137.0000 mm): Via [+12V] on F.Cu - B.Cu
    @(136.7600 mm, 136.6100 mm): Track [/AUX-CONNECTORS/AYAB_SDA] on F.Cu, length 71.0600 mm
[clearance]: Clearance violation ( clearance 0.1000 mm; actual 0.0806 mm)
    Local override; error
    @(207.0750 mm, 137.0000 mm): Via [+12V] on F.Cu - B.Cu
    @(94.0000 mm, 136.5000 mm): Track [/ESP32/HALL_L_ADC] on In1.Cu, length 113.0000 mm
[track_dangling]: Track has unconnected end
    Local override; warning
    @(217.6700 mm, 136.0557 mm): Track [/ESP32/EOL_R_N] on B.Cu, length 3.7557 mm
[track_dangling]: Track has unconnected end
    Local override; warning
    @(205.5000 mm, 135.5000 mm): Track [/ESP32/MACHINE_PWR_SENSE] on In1.Cu, length 0.2610 mm

** Found 1 unconnected pads **
[unconnected_items]: Missing connection between items
    Local override; error
    @(205.5000 mm, 135.5000 mm): Track [/ESP32/MACHINE_PWR_SENSE] on In1.Cu, length 0.2610 mm
    @(205.4250 mm, 135.7500 mm): Track [/ESP32/MACHINE_PWR_SENSE] on B.Cu, length 0.5750 mm

** Found 0 Footprint errors **

** End of Report **
```
