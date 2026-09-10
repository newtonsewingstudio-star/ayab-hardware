# KH910 Rev A — Disposable Power Stage DRC

This report describes a disposable candidate. The staged PCB is not source-of-truth and must not be promoted unless every required route and validation passes.

## Routing result
```text
POWER_STAGE_OK /tmp/rev-a-power-stage.kicad_pcb
REMOVED_BYPASS_TRACKS 3
REMOVED_GPIO4_TRACKS 7
RAW_ROUTE_POINTS 300.95,154.35 301.25,154.25 302.25,154.25 302.25,157.00 297.75,157.00 297.75,155.00 295.75,155.00 295.75,136.50 297.75,136.50 297.75,135.00 307.00,135.00 307.23,134.89
LOCAL_SENSE_ROUTE_POINTS 224.18,159.00 224.18,157.00 229.32,157.00 229.32,159.00
GPIO_FRONT_ROUTE_POINTS reused-source-corridor
SENSE_BOTTOM_ROUTE_POINTS reused-source-corridor
SENSE_ROUTE_POINTS 207.49,131.97 207.50,132.25 207.50,145.50 208.00,145.50 208.00,146.25 214.75,146.25 214.75,147.50 223.25,147.50 223.25,147.50 223.25,159.00 224.18,159.00
SENSE_ROUTE_LAYER In2.Cu,In2.Cu,In2.Cu,In2.Cu,In2.Cu,In2.Cu,In2.Cu,In2.Cu,B.Cu,B.Cu,B.Cu
PLUS12_ROUTE_POINTS 225.82,159.00 225.82,163.10
PLUS12_ROUTE_LAYER 2
PLUS12_BOTTOM_ROUTE_POINTS 225.82,159.00 225.82,163.10
GROUND_ROUTE_POINTS 
GROUND_ROUTE_LAYER 2
GROUND_BOTTOM_ROUTE_POINTS 
ROUTE_STUDY_FAILURES 
```

## Source-board DRC
```text
** Drc report for ayab-esp32.kicad_pcb **
** Created on 2026-09-10T23:15:49+0000 **
** Report includes: Errors, Warnings **

** Found 0 DRC violations **

** Found 0 unconnected pads **

** Found 0 Footprint errors **

** End of Report **
```

## Staged-board DRC
```text
** Drc report for rev-a-power-stage.kicad_pcb **
** Created on 2026-09-10T23:15:50+0000 **
** Report includes: Errors, Warnings **

** Found 0 DRC violations **

** Found 0 unconnected pads **

** Found 0 Footprint errors **

** End of Report **
```
