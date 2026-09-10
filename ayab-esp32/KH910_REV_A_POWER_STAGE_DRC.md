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
SENSE_ROUTE_POINTS 207.49,131.97 207.75,132.00 208.00,132.00 208.00,131.25 208.75,131.25 208.75,122.00 214.00,122.00 214.00,121.75 224.25,121.75 224.25,118.75 261.25,118.75 261.25,123.00 263.00,123.00 263.00,124.75 265.25,124.75 265.25,127.50 269.75,127.50 269.75,133.75 287.75,133.75 287.75,134.00 308.25,134.00 308.25,135.75 307.50,135.75 307.50,137.25 302.50,137.25 302.50,146.50 292.50,146.50 292.50,146.75 292.00,146.75 292.00,152.75 285.75,152.75 285.75,161.75 256.75,161.75 256.75,159.75 225.75,159.75 225.75,159.00 224.18,159.00
SENSE_ROUTE_LAYER 6
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
** Created on 2026-09-10T23:05:40+0000 **
** Report includes: Errors, Warnings **

** Found 0 DRC violations **

** Found 0 unconnected pads **

** Found 0 Footprint errors **

** End of Report **
```

## Staged-board DRC
```text
** Drc report for rev-a-power-stage.kicad_pcb **
** Created on 2026-09-10T23:05:41+0000 **
** Report includes: Errors, Warnings **

** Found 7 DRC violations **
[copper_edge_clearance]: Board edge clearance violation
    Rule: board setup constraints edge; error
    @(247.7100 mm, 119.6791 mm): Segment on Edge.Cuts
    @(224.2500 mm, 118.7500 mm): Track [/ESP32/MACHINE_PWR_SENSE] on In2.Cu, length 37.0000 mm
[copper_edge_clearance]: Board edge clearance violation
    Rule: board setup constraints edge; error
    @(201.5727 mm, 121.6791 mm): Segment on Edge.Cuts
    @(214.0000 mm, 121.7500 mm): Track [/ESP32/MACHINE_PWR_SENSE] on In2.Cu, length 10.2500 mm
[copper_edge_clearance]: Board edge clearance violation
    Rule: board setup constraints edge; error
    @(201.5727 mm, 121.6791 mm): Segment on Edge.Cuts
    @(214.0000 mm, 122.0000 mm): Track [/ESP32/MACHINE_PWR_SENSE] on In2.Cu, length 0.2500 mm
[copper_edge_clearance]: Board edge clearance violation
    Rule: board setup constraints edge; error
    @(201.5727 mm, 121.6791 mm): Segment on Edge.Cuts
    @(224.2500 mm, 121.7500 mm): Track [/ESP32/MACHINE_PWR_SENSE] on In2.Cu, length 3.0000 mm
[items_not_allowed]: Items not allowed (keepout area 'antenna keepout')
    Rule: keepout area 'antenna keepout'; error
    @(224.2500 mm, 118.7500 mm): Track [/ESP32/MACHINE_PWR_SENSE] on In2.Cu, length 37.0000 mm
[items_not_allowed]: Items not allowed (keepout area 'antenna keepout')
    Rule: keepout area 'antenna keepout'; error
    @(214.0000 mm, 121.7500 mm): Track [/ESP32/MACHINE_PWR_SENSE] on In2.Cu, length 10.2500 mm
[items_not_allowed]: Items not allowed (keepout area 'antenna keepout')
    Rule: keepout area 'antenna keepout'; error
    @(224.2500 mm, 121.7500 mm): Track [/ESP32/MACHINE_PWR_SENSE] on In2.Cu, length 3.0000 mm

** Found 0 unconnected pads **

** Found 0 Footprint errors **

** End of Report **
```
