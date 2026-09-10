# KH910 Rev A — Disposable Power Stage DRC

This report describes a disposable candidate. The staged PCB is not source-of-truth and must not be promoted unless every required route and validation passes.

## Routing result
```text
POWER_STAGE_OK /tmp/rev-a-power-stage.kicad_pcb
REMOVED_BYPASS_TRACKS 3
REMOVED_GPIO4_TRACKS 7
RAW_ROUTE_POINTS 300.95,154.35 301.25,154.25 302.25,154.25 302.25,157.00 297.75,157.00 297.75,155.00 295.75,155.00 295.75,136.50 297.75,136.50 297.75,135.00 307.00,135.00 307.23,134.89
LOCAL_SENSE_ROUTE_POINTS 205.43,135.75 206.00,135.75 206.00,134.75 209.50,134.75 209.50,135.75 210.07,135.75
GPIO_FRONT_ROUTE_POINTS 
SENSE_BOTTOM_ROUTE_POINTS 
SENSE_ROUTE_POINTS 207.49,131.97 207.25,132.00 207.25,132.75 205.50,132.75 205.50,135.50 205.43,135.75
SENSE_ROUTE_LAYER 4
PLUS12_ROUTE_POINTS 
PLUS12_ROUTE_LAYER -1
PLUS12_BOTTOM_ROUTE_POINTS 
GROUND_ROUTE_POINTS 208.43,135.75 208.50,136.00 208.50,138.50 213.25,138.50 213.57,138.60
GROUND_ROUTE_LAYER 6
GROUND_BOTTOM_ROUTE_POINTS 
ROUTE_STUDY_FAILURES no route for +12V from (207.075, 135.75) to (207.0, 163.1) on layer 2; no route for +12V from (207.075, 135.75) to (207.0, 163.1) on layer 4; no route for +12V from (207.075, 135.75) to (207.0, 163.1) on layer 6; no route for +12V from (207.075, 135.75) to (207.0, 163.1) on layer 0
```

## Source-board DRC
```text
** Drc report for ayab-esp32.kicad_pcb **
** Created on 2026-09-10T22:40:47+0000 **
** Report includes: Errors, Warnings **

** Found 0 DRC violations **

** Found 0 unconnected pads **

** Found 0 Footprint errors **

** End of Report **
```

## Staged-board DRC
```text
** Drc report for rev-a-power-stage.kicad_pcb **
** Created on 2026-09-10T22:40:48+0000 **
** Report includes: Errors, Warnings **

** Found 5 DRC violations **
[shorting_items]: Items shorting two nets (nets /AUX-CONNECTORS/AYAB_SDA and GND)
    Local override; error
    @(207.8200 mm, 136.6100 mm): Track [/AUX-CONNECTORS/AYAB_SDA] on F.Cu, length 5.3033 mm
    @(208.4250 mm, 135.7500 mm): Via [GND] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.1000 mm; actual 0.0523 mm)
    Local override; error
    @(207.0000 mm, 136.5000 mm): Track [/ESP32/HALL_L_ADC] on In1.Cu, length 4.2426 mm
    @(208.4250 mm, 135.7500 mm): Via [GND] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.1000 mm; actual 0.0523 mm)
    Local override; error
    @(207.0000 mm, 136.5000 mm): Track [/ESP32/HALL_L_ADC] on In1.Cu, length 4.2426 mm
    @(207.0750 mm, 135.7500 mm): Via [+12V] on F.Cu - B.Cu
[via_dangling]: Via is not connected or connected on only one layer
    Local override; warning
    @(207.0000 mm, 163.1000 mm): Via [+12V] on F.Cu - B.Cu
[via_dangling]: Via is not connected or connected on only one layer
    Local override; warning
    @(207.0750 mm, 135.7500 mm): Via [+12V] on F.Cu - B.Cu

** Found 1 unconnected pads **
[unconnected_items]: Missing connection between items
    Local override; error
    @(207.0000 mm, 163.1000 mm): Via [+12V] on F.Cu - B.Cu
    @(207.0750 mm, 135.7500 mm): Via [+12V] on F.Cu - B.Cu

** Found 0 Footprint errors **

** End of Report **
```
