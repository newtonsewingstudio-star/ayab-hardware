# KH910 Rev A — Disposable Power Stage DRC

This report describes a disposable candidate. The staged PCB is not source-of-truth and must not be promoted unless every required route and validation passes.

## Routing result
```text
POWER_STAGE_OK /tmp/rev-a-power-stage.kicad_pcb
REMOVED_BYPASS_TRACKS 3
REMOVED_GPIO4_TRACKS 5
RAW_ROUTE_POINTS 300.95,154.35 301.25,154.25 302.25,154.25 302.25,157.00 297.75,157.00 297.75,155.00 295.75,155.00 295.75,136.50 297.75,136.50 297.75,135.00 307.00,135.00 307.23,134.89
LOCAL_SENSE_ROUTE_POINTS 205.43,135.75 206.00,135.75 206.00,134.75 209.50,134.75 209.50,135.75 210.07,135.75
GPIO_FRONT_ROUTE_POINTS 
SENSE_BOTTOM_ROUTE_POINTS 
SENSE_ROUTE_POINTS 
SENSE_ROUTE_LAYER -1
PLUS12_ROUTE_POINTS 
PLUS12_ROUTE_LAYER -1
PLUS12_BOTTOM_ROUTE_POINTS 
GROUND_ROUTE_POINTS 206.18,135.00 206.50,135.00 206.50,134.75 207.00,134.75 207.00,138.50 213.25,138.50 213.57,138.60
GROUND_ROUTE_LAYER 6
GROUND_BOTTOM_ROUTE_POINTS 
ROUTE_STUDY_FAILURES no route for /ESP32/MACHINE_PWR_SENSE from (217.125, 129.675) to (205.425, 135.75) on layer 2; no route for /ESP32/MACHINE_PWR_SENSE from (217.125, 129.675) to (205.425, 135.75) on layer 4; no route for /ESP32/MACHINE_PWR_SENSE from (217.125, 129.675) to (205.425, 135.75) on layer 6; no route for /ESP32/MACHINE_PWR_SENSE from (217.125, 129.675) to (205.425, 135.75) on layer 0 | no route for +12V from (207.075, 135.75) to (206.075, 135.75) on layer 2 | no route for +12V from (206.075, 135.75) to (207.0, 163.1) on layer 2; no route for +12V from (206.075, 135.75) to (207.0, 163.1) on layer 4; no route for +12V from (206.075, 135.75) to (207.0, 163.1) on layer 6; no route for +12V from (206.075, 135.75) to (207.0, 163.1) on layer 0 | no route for GND from (208.425, 135.75) to (206.175, 135.0) on layer 2
```

## Source-board DRC
```text
** Drc report for ayab-esp32.kicad_pcb **
** Created on 2026-09-10T22:32:49+0000 **
** Report includes: Errors, Warnings **

** Found 0 DRC violations **

** Found 0 unconnected pads **

** Found 0 Footprint errors **

** End of Report **
```

## Staged-board DRC
```text
** Drc report for rev-a-power-stage.kicad_pcb **
** Created on 2026-09-10T22:32:51+0000 **
** Report includes: Errors, Warnings **

** Found 719 DRC violations **
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(224.1100 mm, 147.7800 mm): Via [/ESP32/USB_M] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(224.1250 mm, 137.9700 mm): Via [/ESP32/USB_M] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(232.9000 mm, 133.9200 mm): Via [GND] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(224.9750 mm, 137.9700 mm): Via [/ESP32/USB_P] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(224.9700 mm, 147.3100 mm): Via [/ESP32/USB_P] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(240.5300 mm, 131.4400 mm): Via [/ESP32/BUZZER] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(239.8100 mm, 150.3100 mm): Via [/ESP32/BUZZER] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(215.2100 mm, 127.9500 mm): Via [/ESP32/BOOT0] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(206.3600 mm, 131.9300 mm): Via [/ESP32/EOL_R_P] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(208.7307 mm, 131.9980 mm): Via [/ESP32/ENC_A] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(218.1000 mm, 134.1400 mm): Via [/ESP32/ENC_B] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(210.1000 mm, 131.9900 mm): Via [/ESP32/ENC_BP] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(227.9800 mm, 128.4100 mm): Via [/ESP32/nRST] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(228.6200 mm, 134.2000 mm): Via [Net-(U201-SPIIO7/GPIO36/FSPICLK/SUBSPICLK)] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(89.7678 mm, 132.0780 mm): Via [/BROTHER-CONNECTORS/EOL_L] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(87.1900 mm, 134.1100 mm): Via [/BROTHER-CONNECTORS/EOL_L] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(236.7300 mm, 145.6400 mm): Via [/BROTHER-CONNECTORS/ENC_V2] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(236.7200 mm, 148.9300 mm): Via [/BROTHER-CONNECTORS/ENC_V2] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(235.8700 mm, 145.6400 mm): Via [/BROTHER-CONNECTORS/ENC_V1] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(235.8700 mm, 148.4100 mm): Via [/BROTHER-CONNECTORS/ENC_V1] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(237.6600 mm, 145.6500 mm): Via [/BROTHER-CONNECTORS/ENC_BELTPHASE] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(237.6600 mm, 148.9400 mm): Via [/BROTHER-CONNECTORS/ENC_BELTPHASE] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(239.2200 mm, 145.6500 mm): Via [/BROTHER-CONNECTORS/EOL_R_N] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(220.9700 mm, 134.1500 mm): Via [/BROTHER-CONNECTORS/EOL_R_N] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(238.4500 mm, 145.6300 mm): Via [/BROTHER-CONNECTORS/EOL_R_S] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(221.6700 mm, 134.1400 mm): Via [/BROTHER-CONNECTORS/EOL_R_S] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(221.5750 mm, 137.9600 mm): Via [/AUX-CONNECTORS/I2C_SCL] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(221.6100 mm, 146.7700 mm): Via [/AUX-CONNECTORS/I2C_SCL] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(220.7250 mm, 137.9500 mm): Via [/AUX-CONNECTORS/I2C_SDA] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(220.7300 mm, 146.2200 mm): Via [/AUX-CONNECTORS/I2C_SDA] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(227.9800 mm, 132.2200 mm): Via [/ESP32/ESP39] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(227.9700 mm, 131.3400 mm): Via [/ESP32/ESP40] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(227.9800 mm, 130.5500 mm): Via [/ESP32/ESP41] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(227.9800 mm, 129.6800 mm): Via [/ESP32/ESP42] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(220.2900 mm, 134.1600 mm): Via [/ESP32/ESP14] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(222.3000 mm, 134.1200 mm): Via [SOLENOID_PWR_EN] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(219.5500 mm, 134.1300 mm): Via [/ESP32/HALL_L_ADC] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(218.8000 mm, 134.1300 mm): Via [/ESP32/HALL_R_ADC] on F.Cu - B.Cu
[starved_thermal]: Thermal relief connection to zone incomplete (layer F.Cu; zone min spoke count 2; actual 1)
    Local override; error
    @(307.5294 mm, 130.6000 mm): Zone [/PSU/5V_SW] on F.Cu, priority 5
    @(307.9200 mm, 131.3950 mm): Pad 2 [/PSU/5V_SW] of C614 on F.Cu
[starved_thermal]: Thermal relief connection to zone incomplete (layer F.Cu; zone min spoke count 2; actual 1)
    Local override; error
    @(312.6794 mm, 124.0250 mm): Zone [GND] on F.Cu, priority 5
    @(309.6900 mm, 129.8900 mm): Pad 2 [GND] of C620 on F.Cu
[starved_thermal]: Thermal relief connection to zone incomplete (layer F.Cu; zone min spoke count 2; actual 1)
    Local override; error
    @(307.5294 mm, 130.6000 mm): Zone [/PSU/5V_SW] on F.Cu, priority 5
    @(306.3800 mm, 131.4450 mm): Pad 2 [/PSU/5V_SW] of R608 on F.Cu
[starved_thermal]: Thermal relief connection to zone incomplete (layer F.Cu; 1 spokes connected to isolated island)
    Local override; error
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
    @(288.4300 mm, 145.1700 mm): PTH pad 2 [GND] of J405
[starved_thermal]: Thermal relief connection to zone incomplete (layer B.Cu; 1 spokes connected to isolated island)
    Local override; error
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
    @(76.8200 mm, 127.9400 mm): PTH pad 2 [GND] of J408
[starved_thermal]: Thermal relief connection to zone incomplete (layer B.Cu; zone min spoke count 2; actual 1)
    Local override; error
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
    @(208.4250 mm, 135.7500 mm): Pad 2 [GND] of R216 on B.Cu
[starved_thermal]: Thermal relief connection to zone incomplete (layer F.Cu; zone min spoke count 2; actual 1)
    Local override; error
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
    @(280.7775 mm, 133.3400 mm): Pad 1 [GND] of D604 on F.Cu
[starved_thermal]: Thermal relief connection to zone incomplete (layer F.Cu; zone min spoke count 2; actual 1)
    Local override; error
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
    @(254.6000 mm, 156.0400 mm): Pad A12 [GND] of J501 on F.Cu
[starved_thermal]: Thermal relief connection to zone incomplete (layer F.Cu; zone min spoke count 2; actual 1)
    Local override; error
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
    @(254.6000 mm, 156.0400 mm): Pad B1 [GND] of J501 on F.Cu
[starved_thermal]: Thermal relief connection to zone incomplete (layer F.Cu; 1 spokes connected to isolated island)
    Local override; error
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
    @(255.6700 mm, 156.9550 mm): PTH pad S1 [GND] of J501
[starved_thermal]: Thermal relief connection to zone incomplete (layer F.Cu; zone min spoke count 2; actual 1)
    Local override; error
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
    @(211.5750 mm, 123.0750 mm): Pad 2 [GND] of C205 on F.Cu
[starved_thermal]: Thermal relief connection to zone incomplete (layer F.Cu; zone min spoke count 2; actual 1)
    Local override; error
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
    @(231.1250 mm, 125.4250 mm): Pad 43 [GND] of U201 on F.Cu
[starved_thermal]: Thermal relief connection to zone incomplete (layer F.Cu; zone min spoke count 2; actual 1)
    Local override; error
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
    @(217.1250 mm, 136.6750 mm): Pad 63 [GND] of U201 on F.Cu
[drill_out_of_range]: Hole size out of range (board setup constraints min hole 0.3000 mm; actual 0.2000 mm)
    Rule: netclass 'Default'; error
    @(224.1100 mm, 147.7800 mm): Via [/ESP32/USB_M] on F.Cu - B.Cu
[drill_out_of_range]: Hole size out of range (board setup constraints min hole 0.3000 mm; actual 0.2000 mm)
    Rule: netclass 'Default'; error
    @(224.1250 mm, 137.9700 mm): Via [/ESP32/USB_M] on F.Cu - B.Cu
[drill_out_of_range]: Hole size out of range (board setup constraints min hole 0.3000 mm; actual 0.2000 mm)
    Rule: netclass 'Default'; error
    @(232.9000 mm, 133.9200 mm): Via [GND] on F.Cu - B.Cu
[drill_out_of_range]: Hole size out of range (board setup constraints min hole 0.3000 mm; actual 0.2000 mm)
    Rule: netclass 'Default'; error
    @(224.9750 mm, 137.9700 mm): Via [/ESP32/USB_P] on F.Cu - B.Cu
[drill_out_of_range]: Hole size out of range (board setup constraints min hole 0.3000 mm; actual 0.2000 mm)
    Rule: netclass 'Default'; error
    @(224.9700 mm, 147.3100 mm): Via [/ESP32/USB_P] on F.Cu - B.Cu
[drill_out_of_range]: Hole size out of range (board setup constraints min hole 0.3000 mm; actual 0.2000 mm)
    Rule: netclass 'Default'; error
    @(240.5300 mm, 131.4400 mm): Via [/ESP32/BUZZER] on F.Cu - B.Cu
[drill_out_of_range]: Hole size out of range (board setup constraints min hole 0.3000 mm; actual 0.2000 mm)
    Rule: netclass 'Default'; error
    @(239.8100 mm, 150.3100 mm): Via [/ESP32/BUZZER] on F.Cu - B.Cu
[drill_out_of_range]: Hole size out of range (board setup constraints min hole 0.3000 mm; actual 0.2000 mm)
    Rule: netclass 'Default'; error
    @(215.2100 mm, 127.9500 mm): Via [/ESP32/BOOT0] on F.Cu - B.Cu
[drill_out_of_range]: Hole size out of range (board setup constraints min hole 0.3000 mm; actual 0.2000 mm)
    Rule: netclass 'Default'; error
    @(206.3600 mm, 131.9300 mm): Via [/ESP32/EOL_R_P] on F.Cu - B.Cu
[drill_out_of_range]: Hole size out of range (board setup constraints min hole 0.3000 mm; actual 0.2000 mm)
    Rule: netclass 'Default'; error
    @(208.7307 mm, 131.9980 mm): Via [/ESP32/ENC_A] on F.Cu - B.Cu
[drill_out_of_range]: Hole size out of range (board setup constraints min hole 0.3000 mm; actual 0.2000 mm)
    Rule: netclass 'Default'; error
    @(218.1000 mm, 134.1400 mm): Via [/ESP32/ENC_B] on F.Cu - B.Cu
[drill_out_of_range]: Hole size out of range (board setup constraints min hole 0.3000 mm; actual 0.2000 mm)
    Rule: netclass 'Default'; error
    @(210.1000 mm, 131.9900 mm): Via [/ESP32/ENC_BP] on F.Cu - B.Cu
[drill_out_of_range]: Hole size out of range (board setup constraints min hole 0.3000 mm; actual 0.2000 mm)
    Rule: netclass 'Default'; error
    @(227.9800 mm, 128.4100 mm): Via [/ESP32/nRST] on F.Cu - B.Cu
[drill_out_of_range]: Hole size out of range (board setup constraints min hole 0.3000 mm; actual 0.2000 mm)
    Rule: netclass 'Default'; error
    @(228.6200 mm, 134.2000 mm): Via [Net-(U201-SPIIO7/GPIO36/FSPICLK/SUBSPICLK)] on F.Cu - B.Cu
[drill_out_of_range]: Hole size out of range (board setup constraints min hole 0.3000 mm; actual 0.2000 mm)
    Rule: netclass 'Default'; error
    @(89.7678 mm, 132.0780 mm): Via [/BROTHER-CONNECTORS/EOL_L] on F.Cu - B.Cu
[drill_out_of_range]: Hole size out of range (board setup constraints min hole 0.3000 mm; actual 0.2000 mm)
    Rule: netclass 'Default'; error
    @(87.1900 mm, 134.1100 mm): Via [/BROTHER-CONNECTORS/EOL_L] on F.Cu - B.Cu
[drill_out_of_range]: Hole size out of range (board setup constraints min hole 0.3000 mm; actual 0.2000 mm)
    Rule: netclass 'Default'; error
    @(236.7300 mm, 145.6400 mm): Via [/BROTHER-CONNECTORS/ENC_V2] on F.Cu - B.Cu
[drill_out_of_range]: Hole size out of range (board setup constraints min hole 0.3000 mm; actual 0.2000 mm)
    Rule: netclass 'Default'; error
    @(236.7200 mm, 148.9300 mm): Via [/BROTHER-CONNECTORS/ENC_V2] on F.Cu - B.Cu
[drill_out_of_range]: Hole size out of range (board setup constraints min hole 0.3000 mm; actual 0.2000 mm)
    Rule: netclass 'Default'; error
    @(235.8700 mm, 145.6400 mm): Via [/BROTHER-CONNECTORS/ENC_V1] on F.Cu - B.Cu
[drill_out_of_range]: Hole size out of range (board setup constraints min hole 0.3000 mm; actual 0.2000 mm)
    Rule: netclass 'Default'; error
    @(235.8700 mm, 148.4100 mm): Via [/BROTHER-CONNECTORS/ENC_V1] on F.Cu - B.Cu
[drill_out_of_range]: Hole size out of range (board setup constraints min hole 0.3000 mm; actual 0.2000 mm)
    Rule: netclass 'Default'; error
    @(237.6600 mm, 145.6500 mm): Via [/BROTHER-CONNECTORS/ENC_BELTPHASE] on F.Cu - B.Cu
[drill_out_of_range]: Hole size out of range (board setup constraints min hole 0.3000 mm; actual 0.2000 mm)
    Rule: netclass 'Default'; error
    @(237.6600 mm, 148.9400 mm): Via [/BROTHER-CONNECTORS/ENC_BELTPHASE] on F.Cu - B.Cu
[drill_out_of_range]: Hole size out of range (board setup constraints min hole 0.3000 mm; actual 0.2000 mm)
    Rule: netclass 'Default'; error
    @(239.2200 mm, 145.6500 mm): Via [/BROTHER-CONNECTORS/EOL_R_N] on F.Cu - B.Cu
[drill_out_of_range]: Hole size out of range (board setup constraints min hole 0.3000 mm; actual 0.2000 mm)
    Rule: netclass 'Default'; error
    @(220.9700 mm, 134.1500 mm): Via [/BROTHER-CONNECTORS/EOL_R_N] on F.Cu - B.Cu
[drill_out_of_range]: Hole size out of range (board setup constraints min hole 0.3000 mm; actual 0.2000 mm)
    Rule: netclass 'Default'; error
    @(238.4500 mm, 145.6300 mm): Via [/BROTHER-CONNECTORS/EOL_R_S] on F.Cu - B.Cu
[drill_out_of_range]: Hole size out of range (board setup constraints min hole 0.3000 mm; actual 0.2000 mm)
    Rule: netclass 'Default'; error
    @(221.6700 mm, 134.1400 mm): Via [/BROTHER-CONNECTORS/EOL_R_S] on F.Cu - B.Cu
[drill_out_of_range]: Hole size out of range (board setup constraints min hole 0.3000 mm; actual 0.2000 mm)
    Rule: netclass 'Default'; error
    @(221.5750 mm, 137.9600 mm): Via [/AUX-CONNECTORS/I2C_SCL] on F.Cu - B.Cu
[drill_out_of_range]: Hole size out of range (board setup constraints min hole 0.3000 mm; actual 0.2000 mm)
    Rule: netclass 'Default'; error
    @(221.6100 mm, 146.7700 mm): Via [/AUX-CONNECTORS/I2C_SCL] on F.Cu - B.Cu
[drill_out_of_range]: Hole size out of range (board setup constraints min hole 0.3000 mm; actual 0.2000 mm)
    Rule: netclass 'Default'; error
    @(220.7250 mm, 137.9500 mm): Via [/AUX-CONNECTORS/I2C_SDA] on F.Cu - B.Cu
[drill_out_of_range]: Hole size out of range (board setup constraints min hole 0.3000 mm; actual 0.2000 mm)
    Rule: netclass 'Default'; error
    @(220.7300 mm, 146.2200 mm): Via [/AUX-CONNECTORS/I2C_SDA] on F.Cu - B.Cu
[drill_out_of_range]: Hole size out of range (board setup constraints min hole 0.3000 mm; actual 0.2000 mm)
    Rule: netclass 'Default'; error
    @(227.9800 mm, 132.2200 mm): Via [/ESP32/ESP39] on F.Cu - B.Cu
[drill_out_of_range]: Hole size out of range (board setup constraints min hole 0.3000 mm; actual 0.2000 mm)
    Rule: netclass 'Default'; error
    @(227.9700 mm, 131.3400 mm): Via [/ESP32/ESP40] on F.Cu - B.Cu
[drill_out_of_range]: Hole size out of range (board setup constraints min hole 0.3000 mm; actual 0.2000 mm)
    Rule: netclass 'Default'; error
    @(227.9800 mm, 130.5500 mm): Via [/ESP32/ESP41] on F.Cu - B.Cu
[drill_out_of_range]: Hole size out of range (board setup constraints min hole 0.3000 mm; actual 0.2000 mm)
    Rule: netclass 'Default'; error
    @(227.9800 mm, 129.6800 mm): Via [/ESP32/ESP42] on F.Cu - B.Cu
[drill_out_of_range]: Hole size out of range (board setup constraints min hole 0.3000 mm; actual 0.2000 mm)
    Rule: netclass 'Default'; error
    @(220.2900 mm, 134.1600 mm): Via [/ESP32/ESP14] on F.Cu - B.Cu
[drill_out_of_range]: Hole size out of range (board setup constraints min hole 0.3000 mm; actual 0.2000 mm)
    Rule: netclass 'Default'; error
    @(222.3000 mm, 134.1200 mm): Via [SOLENOID_PWR_EN] on F.Cu - B.Cu
[drill_out_of_range]: Hole size out of range (board setup constraints min hole 0.3000 mm; actual 0.2000 mm)
    Rule: netclass 'Default'; error
    @(219.5500 mm, 134.1300 mm): Via [/ESP32/HALL_L_ADC] on F.Cu - B.Cu
[drill_out_of_range]: Hole size out of range (board setup constraints min hole 0.3000 mm; actual 0.2000 mm)
    Rule: netclass 'Default'; error
    @(218.8000 mm, 134.1300 mm): Via [/ESP32/HALL_R_ADC] on F.Cu - B.Cu
[copper_edge_clearance]: Board edge clearance violation (board setup constraints edge clearance 0.5000 mm; actual 0.4476 mm)
    Rule: board setup constraints edge; error
    @(249.7100 mm, 116.1609 mm): Segment on Edge.Cuts
    @(270.1000 mm, 117.0200 mm): Via [GND] on F.Cu - B.Cu
[copper_edge_clearance]: Board edge clearance violation (board setup constraints edge clearance 0.5000 mm; actual 0.1809 mm)
    Rule: board setup constraints edge; error
    @(201.5727 mm, 121.6791 mm): Segment on Edge.Cuts
    @(244.7100 mm, 122.2600 mm): Via [GND] on F.Cu - B.Cu
[copper_edge_clearance]: Board edge clearance violation (board setup constraints edge clearance 0.5000 mm; actual 0.2009 mm)
    Rule: board setup constraints edge; error
    @(201.5727 mm, 121.6791 mm): Segment on Edge.Cuts
    @(237.8200 mm, 122.2800 mm): Via [GND] on F.Cu - B.Cu
[copper_edge_clearance]: Board edge clearance violation (board setup constraints edge clearance 0.5000 mm; actual 0.4790 mm)
    Rule: board setup constraints edge; error
    @(343.3493 mm, 164.2140 mm): Segment on Edge.Cuts
    @(68.3200 mm, 160.9200 mm): Track [+12V] on B.Cu, length 3.0830 mm
[copper_edge_clearance]: Board edge clearance violation (board setup constraints edge clearance 0.5000 mm; actual 0.4790 mm)
    Rule: board setup constraints edge; error
    @(343.3493 mm, 164.2140 mm): Segment on Edge.Cuts
    @(70.5000 mm, 163.1000 mm): Track [+12V] on B.Cu, length 233.0300 mm
[copper_edge_clearance]: Board edge clearance violation (board setup constraints edge clearance 0.5000 mm; actual 0.4790 mm)
    Rule: board setup constraints edge; error
    @(343.3493 mm, 164.2140 mm): Segment on Edge.Cuts
    @(303.5300 mm, 163.1000 mm): Track [+12V] on B.Cu, length 4.1861 mm
[copper_edge_clearance]: Board edge clearance violation (board setup constraints edge clearance 0.5000 mm; actual 0.4654 mm)
    Rule: board setup constraints edge; error
    @(194.0128 mm, 140.4204 mm): Arc on Edge.Cuts
    @(196.4900 mm, 137.9300 mm): Track [/BROTHER-CONNECTORS/SOL_7] on B.Cu, length 49.1724 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(142.7050 mm, 130.7100 mm): Track [/BROTHER-CONNECTORS/EOL_R_S] on B.Cu, length 14.7220 mm
    @(140.3650 mm, 130.9100 mm): Track [/BROTHER-CONNECTORS/EOL_R_N] on B.Cu, length 77.3650 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(145.0450 mm, 130.5100 mm): Track [SOLENOID_PWR_EN] on B.Cu, length 73.6450 mm
    @(221.6700 mm, 134.1400 mm): Track [/BROTHER-CONNECTORS/EOL_R_S] on B.Cu, length 4.8508 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1884 mm)
    Local override; error
    @(302.4900 mm, 139.5400 mm): Track [/BROTHER-CONNECTORS/SOL_7] on F.Cu, length 5.7417 mm
    @(306.7600 mm, 143.1900 mm): Track [/BROTHER-CONNECTORS/SOL_6] on F.Cu, length 17.2900 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1750 mm)
    Local override; error
    @(224.2900 mm, 147.7600 mm): Track [/ESP32/USB_M] on F.Cu, length 17.3900 mm
    @(224.9700 mm, 147.3100 mm): Via [/ESP32/USB_P] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1392 mm)
    Local override; error
    @(239.2200 mm, 145.6500 mm): Via [/BROTHER-CONNECTORS/EOL_R_N] on F.Cu - B.Cu
    @(238.4500 mm, 145.6300 mm): Track [/BROTHER-CONNECTORS/EOL_R_S] on In2.Cu, length 1.7864 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1318 mm)
    Local override; error
    @(264.9200 mm, 139.5400 mm): Track [/BROTHER-CONNECTORS/SOL_7] on F.Cu, length 37.5700 mm
    @(263.1000 mm, 140.8200 mm): Track [/BROTHER-CONNECTORS/SOL_6] on F.Cu, length 2.3617 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1615 mm)
    Local override; error
    @(216.5300 mm, 138.4400 mm): Track [/BROTHER-CONNECTORS/SOL_0] on F.Cu, length 7.3932 mm
    @(224.1250 mm, 137.9700 mm): Via [/ESP32/USB_M] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1821 mm)
    Local override; error
    @(236.1250 mm, 134.9200 mm): Track [+3V3] on F.Cu, length 1.8950 mm
    @(236.3600 mm, 134.1800 mm): Track [/ESP32/YEL] on F.Cu, length 0.7600 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1350 mm)
    Local override; error
    @(240.5300 mm, 131.4400 mm): Via [/ESP32/BUZZER] on F.Cu - B.Cu
    @(236.5450 mm, 131.0300 mm): Track [/AUX-CONNECTORS/AYAB_TX] on F.Cu, length 7.2050 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1600 mm)
    Local override; error
    @(324.0500 mm, 143.1900 mm): Track [/BROTHER-CONNECTORS/SOL_6] on F.Cu, length 6.1660 mm
    @(306.5500 mm, 143.6000 mm): Track [/BROTHER-CONNECTORS/SOL_7] on F.Cu, length 19.5900 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1932 mm)
    Local override; error
    @(93.9400 mm, 120.3600 mm): PTH pad 1 [/AUX-CONNECTORS/MCP_SCL] of J806
    @(92.5300 mm, 119.6200 mm): Track [/AUX-CONNECTORS/I2C_VBUS] on F.Cu, length 1.2728 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1722 mm)
    Local override; error
    @(98.7000 mm, 128.2675 mm): Pad 2 [Net-(Q804-S)] of Q804 on F.Cu
    @(97.3300 mm, 128.2675 mm): Track [+3V3] on F.Cu, length 1.6405 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1932 mm)
    Local override; error
    @(231.1250 mm, 136.6750 mm): Track [GND] on F.Cu, length 1.5910 mm
    @(231.1250 mm, 135.6250 mm): Pad 31 [/ESP32/YEL] of U201 on F.Cu
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1813 mm)
    Local override; error
    @(218.1800 mm, 142.9600 mm): Track [/BROTHER-CONNECTORS/SOL_7] on F.Cu, length 2.4607 mm
    @(218.1800 mm, 142.3500 mm): Track [/BROTHER-CONNECTORS/SOL_6] on F.Cu, length 2.1637 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(205.9722 mm, 141.0250 mm): Track [/AUX-CONNECTORS/AYAB_CS] on F.Cu, length 2.4395 mm
    @(207.7800 mm, 139.5000 mm): Track [/AUX-CONNECTORS/AYAB_COPI] on F.Cu, length 6.3200 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1821 mm)
    Local override; error
    @(237.4650 mm, 133.5800 mm): Track [+3V3] on F.Cu, length 4.4750 mm
    @(237.7550 mm, 132.7850 mm): Track [/ESP32/YEL] on F.Cu, length 1.9728 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(210.7056 mm, 142.9600 mm): Track [/BROTHER-CONNECTORS/SOL_7] on F.Cu, length 7.4744 mm
    @(211.5962 mm, 142.3350 mm): Via [/BROTHER-CONNECTORS/SOL_6] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1319 mm)
    Local override; error
    @(197.2025 mm, 155.2550 mm): Track [GND] on F.Cu, length 4.7974 mm
    @(199.0919 mm, 154.5981 mm): Via [+3V3] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(212.4695 mm, 141.7100 mm): Track [/BROTHER-CONNECTORS/SOL_5] on B.Cu, length 10.5395 mm
    @(211.5962 mm, 142.3350 mm): Via [/BROTHER-CONNECTORS/SOL_6] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(210.7006 mm, 142.9550 mm): Via [/BROTHER-CONNECTORS/SOL_7] on F.Cu - B.Cu
    @(211.5912 mm, 142.3300 mm): Track [/BROTHER-CONNECTORS/SOL_6] on B.Cu, length 9.8312 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(212.3500 mm, 139.3000 mm): Track [/AUX-CONNECTORS/AYAB_CS] on F.Cu, length 0.6930 mm
    @(207.7800 mm, 139.5000 mm): Track [/AUX-CONNECTORS/AYAB_COPI] on F.Cu, length 6.3200 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1738 mm)
    Local override; error
    @(101.8800 mm, 126.6675 mm): Pad 2 [/AUX-CONNECTORS/I2C_VBUS] of J804 on F.Cu
    @(102.2400 mm, 127.9800 mm): Track [+3V3] on F.Cu, length 1.3294 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(231.1250 mm, 133.9250 mm): Pad 33 [unconnected-(U201-SPIDQS/GPIO37/FSPIQ/SUBSPIQ-Pad33)] of U201 on F.Cu
    @(232.9000 mm, 133.5000 mm): Track [GND] on F.Cu, length 4.9700 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1500 mm)
    Local override; error
    @(219.5000 mm, 140.4200 mm): Track [/BROTHER-CONNECTORS/SOL_5] on F.Cu, length 43.4100 mm
    @(218.1800 mm, 142.3500 mm): Track [/BROTHER-CONNECTORS/SOL_6] on F.Cu, length 2.1637 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(207.7800 mm, 139.5000 mm): Track [/AUX-CONNECTORS/AYAB_COPI] on F.Cu, length 6.3200 mm
    @(207.6972 mm, 139.3000 mm): Track [/AUX-CONNECTORS/AYAB_CS] on F.Cu, length 4.6528 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1510 mm)
    Local override; error
    @(95.1800 mm, 128.2575 mm): Pad 2 [Net-(Q803-S)] of Q803 on F.Cu
    @(95.0000 mm, 127.0975 mm): Track [+3V3] on F.Cu, length 1.6405 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1813 mm)
    Local override; error
    @(212.5195 mm, 141.7600 mm): Track [/BROTHER-CONNECTORS/SOL_5] on F.Cu, length 5.6405 mm
    @(218.1800 mm, 142.3500 mm): Track [/BROTHER-CONNECTORS/SOL_6] on F.Cu, length 2.1637 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1652 mm)
    Local override; error
    @(121.9375 mm, 160.2500 mm): Pad 3 [Net-(Q805-G)] of Q806 on F.Cu
    @(239.8350 mm, 152.8850 mm): Track [GND] on F.Cu, length 3.0052 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(204.5500 mm, 141.0250 mm): Track [/AUX-CONNECTORS/AYAB_CS] on F.Cu, length 1.4222 mm
    @(205.2550 mm, 142.0250 mm): Track [/AUX-CONNECTORS/AYAB_COPI] on F.Cu, length 3.5709 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1600 mm)
    Local override; error
    @(321.9600 mm, 142.7800 mm): Track [/BROTHER-CONNECTORS/SOL_5] on F.Cu, length 5.5861 mm
    @(306.7600 mm, 143.1900 mm): Track [/BROTHER-CONNECTORS/SOL_6] on F.Cu, length 17.2900 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(215.7500 mm, 137.8500 mm): Track [/AUX-CONNECTORS/AYAB_COPI] on F.Cu, length 1.9600 mm
    @(215.8328 mm, 138.0500 mm): Track [/AUX-CONNECTORS/AYAB_SCK] on F.Cu, length 2.1800 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1807 mm)
    Local override; error
    @(175.7900 mm, 154.6700 mm): Via [GND] on F.Cu - B.Cu
    @(170.5493 mm, 155.3007 mm): Track [/BROTHER-CONNECTORS/ENC_BELTPHASE] on F.Cu, length 7.4882 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1200 mm)
    Local override; error
    @(215.8000 mm, 125.9400 mm): Track [+3V3] on In2.Cu, length 22.9200 mm
    @(225.7750 mm, 126.9600 mm): Via [GND] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1391 mm)
    Local override; error
    @(175.8200 mm, 151.4341 mm): Via [GND] on F.Cu - B.Cu
    @(187.5900 mm, 150.7700 mm): Track [/BROTHER-CONNECTORS/SOL_F] on B.Cu, length 77.0048 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1813 mm)
    Local override; error
    @(218.1600 mm, 141.7600 mm): Track [/BROTHER-CONNECTORS/SOL_5] on F.Cu, length 1.8950 mm
    @(218.1800 mm, 142.3500 mm): Track [/BROTHER-CONNECTORS/SOL_6] on F.Cu, length 2.1637 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(214.1000 mm, 139.5000 mm): Track [/AUX-CONNECTORS/AYAB_COPI] on F.Cu, length 2.3335 mm
    @(215.8328 mm, 138.0500 mm): Track [/AUX-CONNECTORS/AYAB_SCK] on F.Cu, length 2.1800 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1297 mm)
    Local override; error
    @(207.8200 mm, 136.6100 mm): Track [/AUX-CONNECTORS/AYAB_SDA] on F.Cu, length 5.3033 mm
    @(210.9249 mm, 134.3249 mm): Via [+3V3] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(215.8000 mm, 125.9400 mm): Track [+3V3] on In2.Cu, length 22.9200 mm
    @(224.1250 mm, 126.9400 mm): Via [GND] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1500 mm)
    Local override; error
    @(262.9100 mm, 140.4200 mm): Track [/BROTHER-CONNECTORS/SOL_5] on F.Cu, length 2.3476 mm
    @(219.7100 mm, 140.8200 mm): Track [/BROTHER-CONNECTORS/SOL_6] on F.Cu, length 43.3900 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(217.7100 mm, 137.8500 mm): Track [/AUX-CONNECTORS/AYAB_COPI] on F.Cu, length 0.6576 mm
    @(215.8328 mm, 138.0500 mm): Track [/AUX-CONNECTORS/AYAB_SCK] on F.Cu, length 2.1800 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1581 mm)
    Local override; error
    @(207.8200 mm, 136.6100 mm): Track [/AUX-CONNECTORS/AYAB_SDA] on F.Cu, length 5.3033 mm
    @(210.9200 mm, 132.6500 mm): Via [+3V3] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1519 mm)
    Local override; error
    @(91.7878 mm, 139.8780 mm): Track [/ESP32/HALL_L_ADC] on F.Cu, length 4.0379 mm
    @(93.0700 mm, 139.1100 mm): Via [GND] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(209.9327 mm, 133.2000 mm): Track [/ESP32/ENC_A] on B.Cu, length 5.1645 mm
    @(210.9200 mm, 132.6500 mm): Via [+3V3] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1819 mm)
    Local override; error
    @(91.5200 mm, 139.0900 mm): Track [+5V] on In2.Cu, length 2.2910 mm
    @(93.0700 mm, 139.1100 mm): Via [GND] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1327 mm)
    Local override; error
    @(210.0750 mm, 135.7500 mm): Pad 1 [/ESP32/MACHINE_PWR_SENSE] of R216 on B.Cu
    @(210.9500 mm, 136.3100 mm): Via [+3V3] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1672 mm)
    Local override; error
    @(303.1300 mm, 138.3700 mm): Track [/BROTHER-CONNECTORS/SOL_4] on F.Cu, length 5.6569 mm
    @(302.9300 mm, 138.7600 mm): Track [/BROTHER-CONNECTORS/SOL_5] on F.Cu, length 5.6851 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(207.8628 mm, 139.7000 mm): Track [/AUX-CONNECTORS/AYAB_SCK] on F.Cu, length 6.3200 mm
    @(207.7800 mm, 139.5000 mm): Track [/AUX-CONNECTORS/AYAB_COPI] on F.Cu, length 6.3200 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1250 mm)
    Local override; error
    @(224.9750 mm, 137.9700 mm): Via [/ESP32/USB_P] on F.Cu - B.Cu
    @(223.9282 mm, 138.4450 mm): Track [/BROTHER-CONNECTORS/SOL_0] on F.Cu, length 38.0368 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1672 mm)
    Local override; error
    @(303.1300 mm, 138.3700 mm): Track [/BROTHER-CONNECTORS/SOL_4] on F.Cu, length 5.6569 mm
    @(264.5700 mm, 138.7600 mm): Track [/BROTHER-CONNECTORS/SOL_5] on F.Cu, length 38.3600 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(207.6972 mm, 139.3000 mm): Track [/AUX-CONNECTORS/AYAB_CS] on F.Cu, length 4.6528 mm
    @(205.2550 mm, 142.0250 mm): Track [/AUX-CONNECTORS/AYAB_COPI] on F.Cu, length 3.5709 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1800 mm)
    Local override; error
    @(268.0600 mm, 150.4800 mm): Track [/AUX-CONNECTORS/I2C_SDA] on F.Cu, length 8.9000 mm
    @(274.5300 mm, 151.1100 mm): Via [+3V3] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1600 mm)
    Local override; error
    @(303.1300 mm, 138.3700 mm): Track [/BROTHER-CONNECTORS/SOL_4] on F.Cu, length 5.6569 mm
    @(306.9500 mm, 142.7800 mm): Track [/BROTHER-CONNECTORS/SOL_5] on F.Cu, length 15.0100 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(205.9700 mm, 143.3700 mm): Track [/AUX-CONNECTORS/AYAB_SCK] on F.Cu, length 1.7772 mm
    @(205.2550 mm, 142.0250 mm): Track [/AUX-CONNECTORS/AYAB_COPI] on F.Cu, length 3.5709 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1750 mm)
    Local override; error
    @(112.1750 mm, 162.6500 mm): Track [+12V] on F.Cu, length 3.8875 mm
    @(125.8250 mm, 159.2000 mm): Pad 2 [Net-(Q806-G)] of R821 on F.Cu
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1550 mm)
    Local override; error
    @(210.9800 mm, 128.1800 mm): Track [+3V3] on In2.Cu, length 8.1000 mm
    @(210.1000 mm, 131.9900 mm): Via [/ESP32/ENC_BP] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(211.6112 mm, 142.3500 mm): Track [/BROTHER-CONNECTORS/SOL_6] on F.Cu, length 6.5688 mm
    @(212.4845 mm, 141.7250 mm): Via [/BROTHER-CONNECTORS/SOL_5] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(213.3152 mm, 141.1000 mm): Track [/BROTHER-CONNECTORS/SOL_4] on B.Cu, length 11.1852 mm
    @(212.4845 mm, 141.7250 mm): Via [/BROTHER-CONNECTORS/SOL_5] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(207.8628 mm, 139.7000 mm): Track [/AUX-CONNECTORS/AYAB_SCK] on F.Cu, length 6.3200 mm
    @(205.2550 mm, 142.0250 mm): Track [/AUX-CONNECTORS/AYAB_COPI] on F.Cu, length 3.5709 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(205.9700 mm, 141.5928 mm): Track [/AUX-CONNECTORS/AYAB_SCK] on F.Cu, length 2.6769 mm
    @(207.7800 mm, 139.5000 mm): Track [/AUX-CONNECTORS/AYAB_COPI] on F.Cu, length 6.3200 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1884 mm)
    Local override; error
    @(303.1300 mm, 138.3700 mm): Track [/BROTHER-CONNECTORS/SOL_4] on F.Cu, length 5.6569 mm
    @(303.3600 mm, 137.9800 mm): Track [/BROTHER-CONNECTORS/SOL_3] on F.Cu, length 5.6003 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1450 mm)
    Local override; error
    @(303.4000 mm, 136.0200 mm): Track [+5V] on F.Cu, length 1.2700 mm
    @(304.0600 mm, 136.7900 mm): Track [/BROTHER-CONNECTORS/SOL_0] on F.Cu, length 5.4164 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1300 mm)
    Local override; error
    @(213.3452 mm, 141.1300 mm): Track [/BROTHER-CONNECTORS/SOL_4] on F.Cu, length 4.8048 mm
    @(214.1269 mm, 140.4750 mm): Via [/BROTHER-CONNECTORS/SOL_3] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(215.8328 mm, 138.0500 mm): Track [/AUX-CONNECTORS/AYAB_SCK] on F.Cu, length 2.1800 mm
    @(216.3700 mm, 138.6000 mm): Via [/BROTHER-CONNECTORS/SOL_0] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1250 mm)
    Local override; error
    @(303.3600 mm, 136.0200 mm): Track [+5V] on F.Cu, length 0.0283 mm
    @(263.6200 mm, 136.7900 mm): Track [/BROTHER-CONNECTORS/SOL_0] on F.Cu, length 40.4400 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1350 mm)
    Local override; error
    @(234.4900 mm, 131.4600 mm): Pad 2 [/AUX-CONNECTORS/UART_TX] of R819 on F.Cu
    @(236.4500 mm, 132.1200 mm): Track [/ESP32/BUZZER] on F.Cu, length 2.5300 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1400 mm)
    Local override; error
    @(264.3900 mm, 138.3700 mm): Track [/BROTHER-CONNECTORS/SOL_4] on F.Cu, length 38.7400 mm
    @(264.5700 mm, 138.7600 mm): Track [/BROTHER-CONNECTORS/SOL_5] on F.Cu, length 38.3600 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(215.7500 mm, 137.8500 mm): Track [/AUX-CONNECTORS/AYAB_COPI] on F.Cu, length 1.9600 mm
    @(214.1828 mm, 139.7000 mm): Track [/AUX-CONNECTORS/AYAB_SCK] on F.Cu, length 2.3335 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1250 mm)
    Local override; error
    @(302.0500 mm, 136.0200 mm): Track [+5V] on F.Cu, length 0.0283 mm
    @(263.6200 mm, 136.7900 mm): Track [/BROTHER-CONNECTORS/SOL_0] on F.Cu, length 40.4400 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(236.1400 mm, 131.4600 mm): Pad 1 [/AUX-CONNECTORS/AYAB_TX] of R819 on F.Cu
    @(237.1300 mm, 131.4400 mm): Track [/ESP32/BUZZER] on F.Cu, length 0.9617 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1550 mm)
    Local override; error
    @(240.0000 mm, 144.4000 mm): Track [/BROTHER-CONNECTORS/EOL_R_N] on B.Cu, length 0.2000 mm
    @(240.5300 mm, 131.4400 mm): Track [/ESP32/BUZZER] on B.Cu, length 14.1600 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1743 mm)
    Local override; error
    @(218.2000 mm, 140.4800 mm): Track [/BROTHER-CONNECTORS/SOL_3] on F.Cu, length 1.2587 mm
    @(219.2800 mm, 140.0000 mm): Track [/BROTHER-CONNECTORS/SOL_4] on F.Cu, length 43.4800 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(201.7800 mm, 129.0800 mm): Track [/ESP32/BOOT0] on B.Cu, length 13.9300 mm
    @(227.2000 mm, 129.2800 mm): Track [/ESP32/nRST] on B.Cu, length 36.7850 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1450 mm)
    Local override; error
    @(300.7500 mm, 136.0200 mm): Track [+5V] on F.Cu, length 1.3000 mm
    @(263.6200 mm, 136.7900 mm): Track [/BROTHER-CONNECTORS/SOL_0] on F.Cu, length 40.4400 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(214.2800 mm, 129.0800 mm): Track [/ESP32/BOOT0] on B.Cu, length 12.5000 mm
    @(227.2000 mm, 129.2800 mm): Track [/ESP32/nRST] on B.Cu, length 36.7850 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(227.2000 mm, 129.2800 mm): Track [/ESP32/nRST] on B.Cu, length 36.7850 mm
    @(215.2100 mm, 128.1500 mm): Track [/ESP32/BOOT0] on B.Cu, length 1.3152 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1142 mm)
    Local override; error
    @(211.9250 mm, 135.3250 mm): Pad 1 [+3V3] of R814 on F.Cu
    @(209.0700 mm, 137.1900 mm): Track [/AUX-CONNECTORS/AYAB_SCL] on F.Cu, length 3.8184 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1530 mm)
    Local override; error
    @(262.7600 mm, 140.0000 mm): Track [/BROTHER-CONNECTORS/SOL_4] on F.Cu, length 2.3052 mm
    @(264.5700 mm, 138.7600 mm): Track [/BROTHER-CONNECTORS/SOL_5] on F.Cu, length 38.3600 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1450 mm)
    Local override; error
    @(295.5000 mm, 131.4400 mm): Track [+5V] on F.Cu, length 6.4771 mm
    @(263.6200 mm, 136.7900 mm): Track [/BROTHER-CONNECTORS/SOL_0] on F.Cu, length 40.4400 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(211.1674 mm, 151.9375 mm): Track [/ESP32/EOL_R_N] on B.Cu, length 9.1961 mm
    @(217.4700 mm, 145.3521 mm): Track [/ESP32/EOL_R_P] on B.Cu, length 9.1961 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(214.9315 mm, 133.6000 mm): Track [/ESP32/EOL_R_P] on B.Cu, length 3.5900 mm
    @(217.6700 mm, 136.0557 mm): Track [/ESP32/EOL_R_N] on B.Cu, length 3.7557 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(208.0300 mm, 133.6000 mm): Track [/ESP32/EOL_R_P] on B.Cu, length 6.9015 mm
    @(217.6700 mm, 136.0557 mm): Track [/ESP32/EOL_R_N] on B.Cu, length 3.7557 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1743 mm)
    Local override; error
    @(214.1319 mm, 140.4800 mm): Track [/BROTHER-CONNECTORS/SOL_3] on F.Cu, length 4.0681 mm
    @(218.1500 mm, 141.1300 mm): Track [/BROTHER-CONNECTORS/SOL_4] on F.Cu, length 1.5981 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(212.5875 mm, 160.1374 mm): Track [/ESP32/EOL_R_N] on B.Cu, length 2.0083 mm
    @(210.9674 mm, 151.8547 mm): Track [/ESP32/EOL_R_P] on B.Cu, length 9.4327 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(217.4700 mm, 136.1385 mm): Track [/ESP32/EOL_R_P] on B.Cu, length 9.2135 mm
    @(217.6700 mm, 136.0557 mm): Track [/ESP32/EOL_R_N] on B.Cu, length 3.7557 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1450 mm)
    Local override; error
    @(302.0900 mm, 136.0200 mm): Track [+5V] on F.Cu, length 1.2700 mm
    @(263.6200 mm, 136.7900 mm): Track [/BROTHER-CONNECTORS/SOL_0] on F.Cu, length 40.4400 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(211.1674 mm, 158.7173 mm): Track [/ESP32/EOL_R_N] on B.Cu, length 6.7798 mm
    @(217.4700 mm, 145.3521 mm): Track [/ESP32/EOL_R_P] on B.Cu, length 9.1961 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(211.1674 mm, 151.9375 mm): Track [/ESP32/EOL_R_N] on B.Cu, length 9.1961 mm
    @(212.5875 mm, 150.8002 mm): Track [/ESP32/ENC_A] on B.Cu, length 1.7172 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1300 mm)
    Local override; error
    @(216.5300 mm, 138.4400 mm): Track [/BROTHER-CONNECTORS/SOL_0] on F.Cu, length 7.3932 mm
    @(221.5750 mm, 137.9600 mm): Via [/AUX-CONNECTORS/I2C_SCL] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1600 mm)
    Local override; error
    @(319.8700 mm, 142.3700 mm): Track [/BROTHER-CONNECTORS/SOL_4] on F.Cu, length 5.0063 mm
    @(306.9500 mm, 142.7800 mm): Track [/BROTHER-CONNECTORS/SOL_5] on F.Cu, length 15.0100 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(214.9315 mm, 133.6000 mm): Track [/ESP32/EOL_R_P] on B.Cu, length 3.5900 mm
    @(217.6700 mm, 145.4349 mm): Track [/ESP32/EOL_R_N] on B.Cu, length 9.3792 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(215.0972 mm, 133.2000 mm): Track [/ESP32/ENC_A] on B.Cu, length 3.9214 mm
    @(217.6700 mm, 136.0557 mm): Track [/ESP32/EOL_R_N] on B.Cu, length 3.7557 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(209.9327 mm, 133.2000 mm): Track [/ESP32/ENC_A] on B.Cu, length 5.1645 mm
    @(217.6700 mm, 136.0557 mm): Track [/ESP32/EOL_R_N] on B.Cu, length 3.7557 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1250 mm)
    Local override; error
    @(302.0700 mm, 136.0400 mm): Track [+5V] on F.Cu, length 0.0283 mm
    @(263.6200 mm, 136.7900 mm): Track [/BROTHER-CONNECTORS/SOL_0] on F.Cu, length 40.4400 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(211.1674 mm, 151.9375 mm): Track [/ESP32/EOL_R_N] on B.Cu, length 9.1961 mm
    @(217.8700 mm, 145.5177 mm): Track [/ESP32/ENC_A] on B.Cu, length 7.4706 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1800 mm)
    Local override; error
    @(303.3600 mm, 137.9800 mm): Track [/BROTHER-CONNECTORS/SOL_3] on F.Cu, length 5.6003 mm
    @(307.1300 mm, 142.3700 mm): Track [/BROTHER-CONNECTORS/SOL_4] on F.Cu, length 12.7400 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(214.1700 mm, 131.9900 mm): Track [/ESP32/ENC_BP] on B.Cu, length 5.5154 mm
    @(215.0972 mm, 133.2000 mm): Track [/ESP32/ENC_A] on B.Cu, length 3.9214 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(217.8700 mm, 135.9728 mm): Track [/ESP32/ENC_A] on B.Cu, length 9.5449 mm
    @(217.6700 mm, 136.0557 mm): Track [/ESP32/EOL_R_N] on B.Cu, length 3.7557 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1400 mm)
    Local override; error
    @(220.7250 mm, 137.9500 mm): Via [/AUX-CONNECTORS/I2C_SDA] on F.Cu - B.Cu
    @(216.5300 mm, 138.4400 mm): Track [/BROTHER-CONNECTORS/SOL_0] on F.Cu, length 7.3932 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(214.1700 mm, 131.9900 mm): Track [/ESP32/ENC_BP] on B.Cu, length 5.5154 mm
    @(218.2700 mm, 135.6200 mm): Track [/ESP32/ENC_B] on B.Cu, length 14.9700 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1450 mm)
    Local override; error
    @(263.6200 mm, 136.7900 mm): Track [/BROTHER-CONNECTORS/SOL_0] on F.Cu, length 40.4400 mm
    @(300.0800 mm, 136.0200 mm): Track [+5V] on F.Cu, length 0.6300 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1100 mm)
    Local override; error
    @(212.5195 mm, 141.7600 mm): Track [/BROTHER-CONNECTORS/SOL_5] on F.Cu, length 5.6405 mm
    @(213.3402 mm, 141.1250 mm): Via [/BROTHER-CONNECTORS/SOL_4] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(213.5875 mm, 150.0831 mm): Track [/ESP32/ENC_BP] on B.Cu, length 3.9743 mm
    @(212.5875 mm, 152.5174 mm): PTH pad 1 [/ESP32/ENC_A] of J701
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(213.3402 mm, 141.1250 mm): Via [/BROTHER-CONNECTORS/SOL_4] on F.Cu - B.Cu
    @(214.1019 mm, 140.5000 mm): Track [/BROTHER-CONNECTORS/SOL_3] on B.Cu, length 11.7319 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(214.1700 mm, 131.9900 mm): Track [/ESP32/ENC_BP] on B.Cu, length 5.5154 mm
    @(217.8700 mm, 135.9728 mm): Track [/ESP32/ENC_A] on B.Cu, length 9.5449 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(218.0700 mm, 145.6006 mm): Track [/ESP32/ENC_BP] on B.Cu, length 6.3392 mm
    @(217.8700 mm, 135.9728 mm): Track [/ESP32/ENC_A] on B.Cu, length 9.5449 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1520 mm)
    Local override; error
    @(220.7300 mm, 146.2200 mm): Via [/AUX-CONNECTORS/I2C_SDA] on F.Cu - B.Cu
    @(218.9100 mm, 147.3300 mm): Track [/BROTHER-CONNECTORS/SOL_F] on F.Cu, length 4.1790 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(215.0972 mm, 133.2000 mm): Track [/ESP32/ENC_A] on B.Cu, length 3.9214 mm
    @(218.0700 mm, 135.8900 mm): Track [/ESP32/ENC_BP] on B.Cu, length 9.7106 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1813 mm)
    Local override; error
    @(218.2000 mm, 140.4800 mm): Track [/BROTHER-CONNECTORS/SOL_3] on F.Cu, length 1.2587 mm
    @(214.9000 mm, 139.8500 mm): Track [/BROTHER-CONNECTORS/SOL_2] on F.Cu, length 3.3200 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1250 mm)
    Local override; error
    @(263.6200 mm, 136.7900 mm): Track [/BROTHER-CONNECTORS/SOL_0] on F.Cu, length 40.4400 mm
    @(303.3800 mm, 136.0400 mm): Track [+5V] on F.Cu, length 0.0283 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1268 mm)
    Local override; error
    @(231.1250 mm, 123.7250 mm): Track [/ESP32/nRST] on F.Cu, length 4.4477 mm
    @(231.1250 mm, 124.5750 mm): Pad 44 [/ESP32/BOOT1] of U201 on F.Cu
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(145.1650 mm, 120.3000 mm): Track [/ESP32/ESP39] on B.Cu, length 14.1563 mm
    @(145.0450 mm, 130.5100 mm): Track [SOLENOID_PWR_EN] on B.Cu, length 73.6450 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(226.0700 mm, 130.3100 mm): Track [/ESP32/ESP39] on B.Cu, length 2.7011 mm
    @(226.7400 mm, 130.1100 mm): Track [/ESP32/ESP40] on B.Cu, length 69.2250 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1475 mm)
    Local override; error
    @(227.2000 mm, 129.2800 mm): Track [/ESP32/nRST] on B.Cu, length 36.7850 mm
    @(227.6900 mm, 129.1400 mm): Track [Net-(U201-SPIIO7/GPIO36/FSPICLK/SUBSPICLK)] on B.Cu, length 0.4808 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(218.6900 mm, 130.5100 mm): Track [SOLENOID_PWR_EN] on B.Cu, length 5.1053 mm
    @(155.1750 mm, 130.3100 mm): Track [/ESP32/ESP39] on B.Cu, length 70.8950 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1500 mm)
    Local override; error
    @(303.3600 mm, 137.9800 mm): Track [/BROTHER-CONNECTORS/SOL_3] on F.Cu, length 5.6003 mm
    @(264.0200 mm, 137.5800 mm): Track [/BROTHER-CONNECTORS/SOL_2] on F.Cu, length 39.5900 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1250 mm)
    Local override; error
    @(263.6200 mm, 136.7900 mm): Track [/BROTHER-CONNECTORS/SOL_0] on F.Cu, length 40.4400 mm
    @(300.7300 mm, 136.0400 mm): Track [+5V] on F.Cu, length 0.0283 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1475 mm)
    Local override; error
    @(227.9800 mm, 128.5000 mm): Track [/ESP32/nRST] on B.Cu, length 1.1031 mm
    @(227.6900 mm, 129.1400 mm): Track [Net-(U201-SPIIO7/GPIO36/FSPICLK/SUBSPICLK)] on B.Cu, length 0.4808 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(227.3400 mm, 129.9100 mm): Track [/ESP32/ESP41] on B.Cu, length 67.4850 mm
    @(227.9700 mm, 131.3400 mm): Track [/ESP32/ESP40] on B.Cu, length 1.7395 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(227.3500 mm, 129.4800 mm): Track [Net-(U201-SPIIO7/GPIO36/FSPICLK/SUBSPICLK)] on B.Cu, length 48.4200 mm
    @(190.4150 mm, 129.2800 mm): Track [/ESP32/nRST] on B.Cu, length 14.2128 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.0850 mm)
    Local override; error
    @(217.1250 mm, 129.6750 mm): Via [/ESP32/MACHINE_PWR_SENSE] on F.Cu - B.Cu
    @(226.7400 mm, 130.1100 mm): Track [/ESP32/ESP40] on B.Cu, length 69.2250 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(155.1750 mm, 130.3100 mm): Track [/ESP32/ESP39] on B.Cu, length 70.8950 mm
    @(157.5150 mm, 130.1100 mm): Track [/ESP32/ESP40] on B.Cu, length 13.8734 mm
[shorting_items]: Items shorting two nets (nets /ESP32/ESP41 and /ESP32/MACHINE_PWR_SENSE)
    Local override; error
    @(227.3400 mm, 129.9100 mm): Track [/ESP32/ESP41] on B.Cu, length 67.4850 mm
    @(217.1250 mm, 129.6750 mm): Via [/ESP32/MACHINE_PWR_SENSE] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(159.8550 mm, 129.9100 mm): Track [/ESP32/ESP41] on B.Cu, length 13.5906 mm
    @(226.7400 mm, 130.1100 mm): Track [/ESP32/ESP40] on B.Cu, length 69.2250 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1400 mm)
    Local override; error
    @(303.1300 mm, 138.3700 mm): Track [/BROTHER-CONNECTORS/SOL_4] on F.Cu, length 5.6569 mm
    @(264.2200 mm, 137.9800 mm): Track [/BROTHER-CONNECTORS/SOL_3] on F.Cu, length 39.1400 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1250 mm)
    Local override; error
    @(263.6200 mm, 136.7900 mm): Track [/BROTHER-CONNECTORS/SOL_0] on F.Cu, length 40.4400 mm
    @(300.7100 mm, 136.0200 mm): Track [+5V] on F.Cu, length 0.0283 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1300 mm)
    Local override; error
    @(162.1650 mm, 129.6800 mm): Track [/ESP32/ESP42] on B.Cu, length 65.8150 mm
    @(227.9800 mm, 130.5500 mm): Track [/ESP32/ESP41] on B.Cu, length 0.9051 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1300 mm)
    Local override; error
    @(227.3400 mm, 129.9100 mm): Track [/ESP32/ESP41] on B.Cu, length 67.4850 mm
    @(152.7850 mm, 120.3000 mm): Track [/ESP32/ESP42] on B.Cu, length 13.2653 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1450 mm)
    Local override; error
    @(182.7700 mm, 151.4400 mm): Via [+5V] on F.Cu - B.Cu
    @(187.5900 mm, 150.7700 mm): Track [/BROTHER-CONNECTORS/SOL_F] on B.Cu, length 77.0048 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1900 mm)
    Local override; error
    @(185.6500 mm, 156.5700 mm): Track [/IO CONDITIONING/EOL_L_L] on F.Cu, length 3.6200 mm
    @(185.9400 mm, 156.2800 mm): Track [/IO CONDITIONING/EOL_L_K] on F.Cu, length 1.7678 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(227.6900 mm, 129.1400 mm): Track [Net-(U201-SPIIO7/GPIO36/FSPICLK/SUBSPICLK)] on B.Cu, length 0.4808 mm
    @(162.1650 mm, 129.6800 mm): Track [/ESP32/ESP42] on B.Cu, length 65.8150 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1329 mm)
    Local override; error
    @(220.0000 mm, 133.2000 mm): Track [/BROTHER-CONNECTORS/EOL_R_N] on In2.Cu, length 1.3577 mm
    @(220.2900 mm, 134.1600 mm): Via [/ESP32/ESP14] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(217.2400 mm, 131.1100 mm): Track [/ESP32/ESP14] on B.Cu, length 79.2150 mm
    @(129.7550 mm, 120.3000 mm): Track [/BROTHER-CONNECTORS/EOL_R_N] on B.Cu, length 15.0048 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1050 mm)
    Local override; error
    @(214.1319 mm, 140.4800 mm): Track [/BROTHER-CONNECTORS/SOL_3] on F.Cu, length 4.0681 mm
    @(214.9000 mm, 139.8500 mm): Via [/BROTHER-CONNECTORS/SOL_2] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(220.2900 mm, 134.1600 mm): Track [/ESP32/ESP14] on B.Cu, length 4.3134 mm
    @(140.3650 mm, 130.9100 mm): Track [/BROTHER-CONNECTORS/EOL_R_N] on B.Cu, length 77.3650 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1900 mm)
    Local override; error
    @(184.0100 mm, 156.2800 mm): Track [/IO CONDITIONING/EOL_L_K] on F.Cu, length 1.9300 mm
    @(184.6500 mm, 157.5700 mm): Track [/IO CONDITIONING/EOL_L_L] on F.Cu, length 1.4142 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1884 mm)
    Local override; error
    @(303.1300 mm, 138.3700 mm): Track [/BROTHER-CONNECTORS/SOL_4] on F.Cu, length 5.6569 mm
    @(307.3200 mm, 141.9400 mm): Track [/BROTHER-CONNECTORS/SOL_3] on F.Cu, length 10.4800 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(299.0500 mm, 155.6500 mm): Pad 4 [<no net>] of U403 on B.Cu
    @(298.5000 mm, 156.2500 mm): Track [+5V] on B.Cu, length 1.9000 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1900 mm)
    Local override; error
    @(185.6500 mm, 156.5700 mm): Track [/IO CONDITIONING/EOL_L_L] on F.Cu, length 3.6200 mm
    @(184.0100 mm, 156.2800 mm): Track [/IO CONDITIONING/EOL_L_K] on F.Cu, length 1.9300 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1813 mm)
    Local override; error
    @(218.2200 mm, 139.8500 mm): Track [/BROTHER-CONNECTORS/SOL_2] on F.Cu, length 0.9334 mm
    @(219.0900 mm, 139.5900 mm): Track [/BROTHER-CONNECTORS/SOL_3] on F.Cu, length 43.5200 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(227.3500 mm, 129.4800 mm): Track [Net-(U201-SPIIO7/GPIO36/FSPICLK/SUBSPICLK)] on B.Cu, length 48.4200 mm
    @(227.9800 mm, 128.5000 mm): Track [/ESP32/nRST] on B.Cu, length 1.1031 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(178.9300 mm, 129.4800 mm): Track [Net-(U201-SPIIO7/GPIO36/FSPICLK/SUBSPICLK)] on B.Cu, length 14.4957 mm
    @(162.1650 mm, 129.6800 mm): Track [/ESP32/ESP42] on B.Cu, length 65.8150 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1268 mm)
    Local override; error
    @(225.8250 mm, 136.6750 mm): Track [SOLENOID_PWR_EN] on F.Cu, length 3.6133 mm
    @(224.9750 mm, 136.6750 mm): Pad 24 [/ESP32/USB_P] of U201 on F.Cu
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1743 mm)
    Local override; error
    @(218.8800 mm, 139.1900 mm): Track [/BROTHER-CONNECTORS/SOL_2] on F.Cu, length 43.5300 mm
    @(262.6100 mm, 139.5900 mm): Track [/BROTHER-CONNECTORS/SOL_3] on F.Cu, length 2.2769 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1475 mm)
    Local override; error
    @(227.9800 mm, 128.5000 mm): Track [/ESP32/nRST] on B.Cu, length 1.1031 mm
    @(228.1700 mm, 129.1400 mm): Track [Net-(U201-SPIIO7/GPIO36/FSPICLK/SUBSPICLK)] on B.Cu, length 0.4800 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1800 mm)
    Local override; error
    @(307.1300 mm, 142.3700 mm): Track [/BROTHER-CONNECTORS/SOL_4] on F.Cu, length 12.7400 mm
    @(317.8000 mm, 141.9400 mm): Track [/BROTHER-CONNECTORS/SOL_3] on F.Cu, length 4.3982 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1846 mm)
    Local override; error
    @(222.3000 mm, 134.1200 mm): Via [SOLENOID_PWR_EN] on F.Cu - B.Cu
    @(223.2750 mm, 135.7450 mm): Track [/BROTHER-CONNECTORS/EOL_R_S] on F.Cu, length 2.2698 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1800 mm)
    Local override; error
    @(234.4750 mm, 134.9200 mm): Pad 2 [Net-(U201-SPIIO7/GPIO36/FSPICLK/SUBSPICLK)] of R201 on F.Cu
    @(234.9950 mm, 135.6250 mm): Track [/ESP32/YEL] on F.Cu, length 3.8700 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1803 mm)
    Local override; error
    @(222.3000 mm, 134.1200 mm): Via [SOLENOID_PWR_EN] on F.Cu - B.Cu
    @(221.6700 mm, 134.1400 mm): Via [/BROTHER-CONNECTORS/EOL_R_S] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1941 mm)
    Local override; error
    @(214.9000 mm, 139.8500 mm): Via [/BROTHER-CONNECTORS/SOL_2] on F.Cu - B.Cu
    @(214.1269 mm, 140.4750 mm): Via [/BROTHER-CONNECTORS/SOL_3] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(214.9000 mm, 139.8500 mm): Track [/BROTHER-CONNECTORS/SOL_2] on B.Cu, length 12.4000 mm
    @(214.1269 mm, 140.4750 mm): Via [/BROTHER-CONNECTORS/SOL_3] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1846 mm)
    Local override; error
    @(218.6900 mm, 130.5100 mm): Track [SOLENOID_PWR_EN] on B.Cu, length 5.1053 mm
    @(221.6700 mm, 134.1400 mm): Via [/BROTHER-CONNECTORS/EOL_R_S] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(218.2400 mm, 130.7100 mm): Track [/BROTHER-CONNECTORS/EOL_R_S] on B.Cu, length 75.5350 mm
    @(134.8350 mm, 120.3000 mm): Track [SOLENOID_PWR_EN] on B.Cu, length 14.4391 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1821 mm)
    Local override; error
    @(236.1250 mm, 134.9200 mm): Track [+3V3] on F.Cu, length 1.8950 mm
    @(237.7550 mm, 132.7850 mm): Track [/ESP32/YEL] on F.Cu, length 1.9728 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(155.1750 mm, 130.3100 mm): Track [/ESP32/ESP39] on B.Cu, length 70.8950 mm
    @(145.0450 mm, 130.5100 mm): Track [SOLENOID_PWR_EN] on B.Cu, length 73.6450 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1500 mm)
    Local override; error
    @(218.2000 mm, 140.4800 mm): Track [/BROTHER-CONNECTORS/SOL_3] on F.Cu, length 1.2587 mm
    @(218.8800 mm, 139.1900 mm): Track [/BROTHER-CONNECTORS/SOL_2] on F.Cu, length 43.5300 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1884 mm)
    Local override; error
    @(218.2200 mm, 139.8500 mm): Track [/BROTHER-CONNECTORS/SOL_2] on F.Cu, length 0.9334 mm
    @(215.6230 mm, 139.2250 mm): Track [/BROTHER-CONNECTORS/SOL_1] on F.Cu, length 2.6020 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1268 mm)
    Local override; error
    @(230.0750 mm, 136.6750 mm): Pad 30 [unconnected-(U201-GPIO48/SPICLK_N/SUBSPICLK_N_DIFF-Pad30)] of U201 on F.Cu
    @(230.1400 mm, 137.5900 mm): Track [/ESP32/GRN] on F.Cu, length 1.2940 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1400 mm)
    Local override; error
    @(303.6100 mm, 137.5800 mm): Track [/BROTHER-CONNECTORS/SOL_2] on F.Cu, length 5.6144 mm
    @(263.8100 mm, 137.1900 mm): Track [/BROTHER-CONNECTORS/SOL_1] on F.Cu, length 40.0600 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1884 mm)
    Local override; error
    @(302.4900 mm, 139.5400 mm): Track [/BROTHER-CONNECTORS/SOL_7] on F.Cu, length 5.7417 mm
    @(302.7200 mm, 139.1500 mm): Track [/BROTHER-CONNECTORS/SOL_6] on F.Cu, length 5.7134 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(214.9000 mm, 139.8500 mm): Track [/BROTHER-CONNECTORS/SOL_2] on F.Cu, length 3.3200 mm
    @(215.6230 mm, 139.2250 mm): Via [/BROTHER-CONNECTORS/SOL_1] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1500 mm)
    Local override; error
    @(264.0200 mm, 137.5800 mm): Track [/BROTHER-CONNECTORS/SOL_2] on F.Cu, length 39.5900 mm
    @(264.2200 mm, 137.9800 mm): Track [/BROTHER-CONNECTORS/SOL_3] on F.Cu, length 39.1400 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1900 mm)
    Local override; error
    @(186.4200 mm, 159.0200 mm): Track [Net-(J702-Pin_7)] on F.Cu, length 4.9225 mm
    @(187.1900 mm, 160.1100 mm): PTH pad 8 [Net-(J702-Pin_8)] of J702
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1813 mm)
    Local override; error
    @(211.6112 mm, 142.3500 mm): Track [/BROTHER-CONNECTORS/SOL_6] on F.Cu, length 6.5688 mm
    @(218.1800 mm, 142.9600 mm): Track [/BROTHER-CONNECTORS/SOL_7] on F.Cu, length 2.4607 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1400 mm)
    Local override; error
    @(307.3200 mm, 141.9400 mm): Track [/BROTHER-CONNECTORS/SOL_3] on F.Cu, length 10.4800 mm
    @(315.6900 mm, 141.5500 mm): Track [/BROTHER-CONNECTORS/SOL_2] on F.Cu, length 3.8467 mm
[shorting_items]: Items shorting two nets (nets /ESP32/MACHINE_PWR_SENSE and SOLENOID_12V_SW)
    Local override; error
    @(217.1250 mm, 129.6750 mm): Via [/ESP32/MACHINE_PWR_SENSE] on F.Cu - B.Cu
    @(215.6000 mm, 130.8000 mm): Track [SOLENOID_12V_SW] on In1.Cu, length 7.3539 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1500 mm)
    Local override; error
    @(219.0900 mm, 139.5900 mm): Track [/BROTHER-CONNECTORS/SOL_3] on F.Cu, length 43.5200 mm
    @(262.4100 mm, 139.1900 mm): Track [/BROTHER-CONNECTORS/SOL_2] on F.Cu, length 2.2769 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1800 mm)
    Local override; error
    @(264.9200 mm, 139.5400 mm): Track [/BROTHER-CONNECTORS/SOL_7] on F.Cu, length 37.5700 mm
    @(264.9850 mm, 139.9700 mm): Track [/BROTHER-CONNECTORS/SOL_8] on F.Cu, length 37.2000 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1900 mm)
    Local override; error
    @(303.8700 mm, 137.1900 mm): Track [/BROTHER-CONNECTORS/SOL_1] on F.Cu, length 5.5437 mm
    @(307.5800 mm, 141.5500 mm): Track [/BROTHER-CONNECTORS/SOL_2] on F.Cu, length 8.1100 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(263.2400 mm, 141.2200 mm): Track [/BROTHER-CONNECTORS/SOL_7] on F.Cu, length 2.3759 mm
    @(264.9850 mm, 139.9700 mm): Track [/BROTHER-CONNECTORS/SOL_8] on F.Cu, length 37.2000 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1557 mm)
    Local override; error
    @(214.9000 mm, 139.8500 mm): Via [/BROTHER-CONNECTORS/SOL_2] on F.Cu - B.Cu
    @(215.6230 mm, 139.2250 mm): Via [/BROTHER-CONNECTORS/SOL_1] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(214.9000 mm, 139.8500 mm): Via [/BROTHER-CONNECTORS/SOL_2] on F.Cu - B.Cu
    @(215.6230 mm, 139.2250 mm): Track [/BROTHER-CONNECTORS/SOL_1] on B.Cu, length 13.0280 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.0450 mm)
    Local override; error
    @(227.2000 mm, 129.2800 mm): Track [/ESP32/nRST] on B.Cu, length 36.7850 mm
    @(217.1250 mm, 129.6750 mm): Via [/ESP32/MACHINE_PWR_SENSE] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1672 mm)
    Local override; error
    @(303.8700 mm, 137.1900 mm): Track [/BROTHER-CONNECTORS/SOL_1] on F.Cu, length 5.5437 mm
    @(304.0600 mm, 136.7900 mm): Track [/BROTHER-CONNECTORS/SOL_0] on F.Cu, length 5.4164 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1813 mm)
    Local override; error
    @(218.1800 mm, 142.3500 mm): Track [/BROTHER-CONNECTORS/SOL_6] on F.Cu, length 2.1637 mm
    @(219.9200 mm, 141.2200 mm): Track [/BROTHER-CONNECTORS/SOL_7] on F.Cu, length 43.3200 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1884 mm)
    Local override; error
    @(218.2200 mm, 139.8500 mm): Track [/BROTHER-CONNECTORS/SOL_2] on F.Cu, length 0.9334 mm
    @(218.2250 mm, 139.2250 mm): Track [/BROTHER-CONNECTORS/SOL_1] on F.Cu, length 0.5869 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(218.0550 mm, 143.5800 mm): Track [/BROTHER-CONNECTORS/SOL_8] on F.Cu, length 2.7577 mm
    @(210.7056 mm, 142.9600 mm): Track [/BROTHER-CONNECTORS/SOL_7] on F.Cu, length 7.4744 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1300 mm)
    Local override; error
    @(218.8800 mm, 139.1900 mm): Track [/BROTHER-CONNECTORS/SOL_2] on F.Cu, length 43.5300 mm
    @(262.1900 mm, 138.8100 mm): Track [/BROTHER-CONNECTORS/SOL_1] on F.Cu, length 2.2910 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1600 mm)
    Local override; error
    @(302.7200 mm, 139.1500 mm): Track [/BROTHER-CONNECTORS/SOL_6] on F.Cu, length 5.7134 mm
    @(306.5500 mm, 143.6000 mm): Track [/BROTHER-CONNECTORS/SOL_7] on F.Cu, length 19.5900 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1900 mm)
    Local override; error
    @(313.6300 mm, 141.1100 mm): Track [/BROTHER-CONNECTORS/SOL_1] on F.Cu, length 3.2244 mm
    @(307.5800 mm, 141.5500 mm): Track [/BROTHER-CONNECTORS/SOL_2] on F.Cu, length 8.1100 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(210.7006 mm, 142.9550 mm): Via [/BROTHER-CONNECTORS/SOL_7] on F.Cu - B.Cu
    @(209.2700 mm, 143.5800 mm): Track [/BROTHER-CONNECTORS/SOL_8] on F.Cu, length 8.7850 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1672 mm)
    Local override; error
    @(263.8100 mm, 137.1900 mm): Track [/BROTHER-CONNECTORS/SOL_1] on F.Cu, length 40.0600 mm
    @(304.0600 mm, 136.7900 mm): Track [/BROTHER-CONNECTORS/SOL_0] on F.Cu, length 5.4164 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1900 mm)
    Local override; error
    @(307.7900 mm, 141.1100 mm): Track [/BROTHER-CONNECTORS/SOL_1] on F.Cu, length 5.8400 mm
    @(307.5800 mm, 141.5500 mm): Track [/BROTHER-CONNECTORS/SOL_2] on F.Cu, length 8.1100 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1884 mm)
    Local override; error
    @(302.7200 mm, 139.1500 mm): Track [/BROTHER-CONNECTORS/SOL_6] on F.Cu, length 5.7134 mm
    @(264.9200 mm, 139.5400 mm): Track [/BROTHER-CONNECTORS/SOL_7] on F.Cu, length 37.5700 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(215.6230 mm, 139.2250 mm): Track [/BROTHER-CONNECTORS/SOL_1] on F.Cu, length 2.6020 mm
    @(216.3700 mm, 138.6000 mm): Via [/BROTHER-CONNECTORS/SOL_0] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1400 mm)
    Local override; error
    @(264.7700 mm, 139.1500 mm): Track [/BROTHER-CONNECTORS/SOL_6] on F.Cu, length 37.9500 mm
    @(264.9200 mm, 139.5400 mm): Track [/BROTHER-CONNECTORS/SOL_7] on F.Cu, length 37.5700 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1300 mm)
    Local override; error
    @(218.2200 mm, 139.8500 mm): Track [/BROTHER-CONNECTORS/SOL_2] on F.Cu, length 0.9334 mm
    @(218.6400 mm, 138.8100 mm): Track [/BROTHER-CONNECTORS/SOL_1] on F.Cu, length 43.5500 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1500 mm)
    Local override; error
    @(218.1800 mm, 142.9600 mm): Track [/BROTHER-CONNECTORS/SOL_7] on F.Cu, length 2.4607 mm
    @(219.7100 mm, 140.8200 mm): Track [/BROTHER-CONNECTORS/SOL_6] on F.Cu, length 43.3900 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1740 mm)
    Local override; error
    @(215.6230 mm, 139.2250 mm): Via [/BROTHER-CONNECTORS/SOL_1] on F.Cu - B.Cu
    @(216.3700 mm, 138.6000 mm): Via [/BROTHER-CONNECTORS/SOL_0] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(216.3700 mm, 138.6000 mm): Track [/BROTHER-CONNECTORS/SOL_0] on B.Cu, length 13.6300 mm
    @(215.6230 mm, 139.2250 mm): Via [/BROTHER-CONNECTORS/SOL_1] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1200 mm)
    Local override; error
    @(216.5300 mm, 138.4400 mm): Track [/BROTHER-CONNECTORS/SOL_0] on F.Cu, length 7.3932 mm
    @(218.2250 mm, 139.2250 mm): Track [/BROTHER-CONNECTORS/SOL_1] on F.Cu, length 0.5869 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1615 mm)
    Local override; error
    @(223.9232 mm, 138.4400 mm): Track [/BROTHER-CONNECTORS/SOL_0] on F.Cu, length 0.0071 mm
    @(224.1250 mm, 137.9700 mm): Via [/ESP32/USB_M] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1250 mm)
    Local override; error
    @(223.9282 mm, 138.4450 mm): Track [/BROTHER-CONNECTORS/SOL_0] on F.Cu, length 38.0368 mm
    @(224.1250 mm, 137.9700 mm): Via [/ESP32/USB_M] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1150 mm)
    Local override; error
    @(261.9650 mm, 138.4450 mm): Track [/BROTHER-CONNECTORS/SOL_0] on F.Cu, length 2.3405 mm
    @(218.6400 mm, 138.8100 mm): Track [/BROTHER-CONNECTORS/SOL_1] on F.Cu, length 43.5500 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1500 mm)
    Local override; error
    @(303.8700 mm, 137.1900 mm): Track [/BROTHER-CONNECTORS/SOL_1] on F.Cu, length 5.5437 mm
    @(263.6200 mm, 136.7900 mm): Track [/BROTHER-CONNECTORS/SOL_0] on F.Cu, length 40.4400 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1672 mm)
    Local override; error
    @(303.8700 mm, 137.1900 mm): Track [/BROTHER-CONNECTORS/SOL_1] on F.Cu, length 5.5437 mm
    @(307.8900 mm, 140.6200 mm): Track [/BROTHER-CONNECTORS/SOL_0] on F.Cu, length 3.7300 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1900 mm)
    Local override; error
    @(307.8400 mm, 149.8600 mm): Track [/BROTHER-CONNECTORS/SOL_F] on F.Cu, length 18.5500 mm
    @(300.9500 mm, 142.4000 mm): Track [/BROTHER-CONNECTORS/SOL_E] on F.Cu, length 9.9278 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1700 mm)
    Local override; error
    @(266.4746 mm, 142.8200 mm): Track [/BROTHER-CONNECTORS/SOL_F] on F.Cu, length 34.3254 mm
    @(266.3200 mm, 142.4000 mm): Track [/BROTHER-CONNECTORS/SOL_E] on F.Cu, length 34.6300 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1743 mm)
    Local override; error
    @(218.9100 mm, 147.3300 mm): Track [/BROTHER-CONNECTORS/SOL_F] on F.Cu, length 4.1790 mm
    @(218.9350 mm, 146.7050 mm): Track [/BROTHER-CONNECTORS/SOL_E] on F.Cu, length 3.8537 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1700 mm)
    Local override; error
    @(266.3200 mm, 142.4000 mm): Track [/BROTHER-CONNECTORS/SOL_E] on F.Cu, length 34.6300 mm
    @(300.8000 mm, 142.8200 mm): Track [/BROTHER-CONNECTORS/SOL_F] on F.Cu, length 9.9561 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1743 mm)
    Local override; error
    @(218.9350 mm, 146.7050 mm): Track [/BROTHER-CONNECTORS/SOL_E] on F.Cu, length 3.8537 mm
    @(221.8650 mm, 144.3750 mm): Track [/BROTHER-CONNECTORS/SOL_F] on F.Cu, length 43.0546 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1700 mm)
    Local override; error
    @(266.3200 mm, 142.4000 mm): Track [/BROTHER-CONNECTORS/SOL_E] on F.Cu, length 34.6300 mm
    @(264.9196 mm, 144.3750 mm): Track [/BROTHER-CONNECTORS/SOL_F] on F.Cu, length 2.1991 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(213.4750 mm, 146.7050 mm): Track [/BROTHER-CONNECTORS/SOL_E] on F.Cu, length 5.4600 mm
    @(213.8500 mm, 147.3300 mm): Via [/BROTHER-CONNECTORS/SOL_F] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1900 mm)
    Local override; error
    @(212.8600 mm, 147.3200 mm): Via [/BROTHER-CONNECTORS/SOL_E] on F.Cu - B.Cu
    @(213.8500 mm, 147.3300 mm): Via [/BROTHER-CONNECTORS/SOL_F] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1750 mm)
    Local override; error
    @(212.8600 mm, 147.3200 mm): Via [/BROTHER-CONNECTORS/SOL_E] on F.Cu - B.Cu
    @(213.8400 mm, 147.3300 mm): Track [/BROTHER-CONNECTORS/SOL_F] on B.Cu, length 4.0871 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1900 mm)
    Local override; error
    @(187.9600 mm, 150.3300 mm): Track [/BROTHER-CONNECTORS/SOL_E] on B.Cu, length 78.9348 mm
    @(110.5852 mm, 150.7700 mm): Track [/BROTHER-CONNECTORS/SOL_F] on B.Cu, length 4.2641 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1900 mm)
    Local override; error
    @(187.9600 mm, 150.3300 mm): Track [/BROTHER-CONNECTORS/SOL_E] on B.Cu, length 78.9348 mm
    @(187.5900 mm, 150.7700 mm): Track [/BROTHER-CONNECTORS/SOL_F] on B.Cu, length 77.0048 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1900 mm)
    Local override; error
    @(187.9600 mm, 150.3300 mm): Track [/BROTHER-CONNECTORS/SOL_E] on B.Cu, length 78.9348 mm
    @(190.1900 mm, 153.3700 mm): Track [/BROTHER-CONNECTORS/SOL_F] on B.Cu, length 3.6770 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1743 mm)
    Local override; error
    @(213.4750 mm, 146.7050 mm): Track [/BROTHER-CONNECTORS/SOL_E] on F.Cu, length 5.4600 mm
    @(218.9100 mm, 147.3300 mm): Track [/BROTHER-CONNECTORS/SOL_F] on F.Cu, length 4.1790 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1700 mm)
    Local override; error
    @(300.9500 mm, 142.4000 mm): Track [/BROTHER-CONNECTORS/SOL_E] on F.Cu, length 9.9278 mm
    @(266.0800 mm, 141.9800 mm): Track [/BROTHER-CONNECTORS/SOL_D] on F.Cu, length 35.0800 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1700 mm)
    Local override; error
    @(266.0800 mm, 141.9800 mm): Track [/BROTHER-CONNECTORS/SOL_D] on F.Cu, length 35.0800 mm
    @(266.3200 mm, 142.4000 mm): Track [/BROTHER-CONNECTORS/SOL_E] on F.Cu, length 34.6300 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1700 mm)
    Local override; error
    @(266.0800 mm, 141.9800 mm): Track [/BROTHER-CONNECTORS/SOL_D] on F.Cu, length 35.0800 mm
    @(264.7400 mm, 143.9800 mm): Track [/BROTHER-CONNECTORS/SOL_E] on F.Cu, length 2.2345 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1500 mm)
    Local override; error
    @(218.9350 mm, 146.7050 mm): Track [/BROTHER-CONNECTORS/SOL_E] on F.Cu, length 3.8537 mm
    @(221.4200 mm, 143.5800 mm): Track [/BROTHER-CONNECTORS/SOL_D] on F.Cu, length 43.0600 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1821 mm)
    Local override; error
    @(212.8600 mm, 147.3200 mm): Track [/BROTHER-CONNECTORS/SOL_E] on F.Cu, length 0.8697 mm
    @(213.8500 mm, 147.3300 mm): Via [/BROTHER-CONNECTORS/SOL_F] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1530 mm)
    Local override; error
    @(300.8000 mm, 142.8200 mm): Track [/BROTHER-CONNECTORS/SOL_F] on F.Cu, length 9.9561 mm
    @(307.9700 mm, 149.4200 mm): Track [/BROTHER-CONNECTORS/SOL_E] on F.Cu, length 16.3600 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1450 mm)
    Local override; error
    @(218.9100 mm, 147.3300 mm): Track [/BROTHER-CONNECTORS/SOL_F] on F.Cu, length 4.1790 mm
    @(221.6600 mm, 143.9800 mm): Track [/BROTHER-CONNECTORS/SOL_E] on F.Cu, length 43.0800 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1900 mm)
    Local override; error
    @(307.8400 mm, 149.8600 mm): Track [/BROTHER-CONNECTORS/SOL_F] on F.Cu, length 18.5500 mm
    @(324.3300 mm, 149.4200 mm): Track [/BROTHER-CONNECTORS/SOL_E] on F.Cu, length 5.8266 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1538 mm)
    Local override; error
    @(212.8600 mm, 147.3200 mm): Via [/BROTHER-CONNECTORS/SOL_E] on F.Cu - B.Cu
    @(211.8900 mm, 147.3300 mm): Track [/BROTHER-CONNECTORS/SOL_D] on F.Cu, length 1.7536 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1701 mm)
    Local override; error
    @(212.8600 mm, 147.3200 mm): Via [/BROTHER-CONNECTORS/SOL_E] on F.Cu - B.Cu
    @(211.8900 mm, 147.3300 mm): Via [/BROTHER-CONNECTORS/SOL_D] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1255 mm)
    Local override; error
    @(212.8200 mm, 147.3200 mm): Track [/BROTHER-CONNECTORS/SOL_E] on B.Cu, length 3.4083 mm
    @(211.8900 mm, 147.3300 mm): Via [/BROTHER-CONNECTORS/SOL_D] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1900 mm)
    Local override; error
    @(109.0252 mm, 150.3300 mm): Track [/BROTHER-CONNECTORS/SOL_E] on B.Cu, length 4.8864 mm
    @(188.3600 mm, 149.8900 mm): Track [/BROTHER-CONNECTORS/SOL_D] on B.Cu, length 80.8948 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1900 mm)
    Local override; error
    @(187.9600 mm, 150.3300 mm): Track [/BROTHER-CONNECTORS/SOL_E] on B.Cu, length 78.9348 mm
    @(188.3600 mm, 149.8900 mm): Track [/BROTHER-CONNECTORS/SOL_D] on B.Cu, length 80.8948 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1900 mm)
    Local override; error
    @(190.5300 mm, 152.9000 mm): Track [/BROTHER-CONNECTORS/SOL_E] on B.Cu, length 3.6345 mm
    @(188.3600 mm, 149.8900 mm): Track [/BROTHER-CONNECTORS/SOL_D] on B.Cu, length 80.8948 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1900 mm)
    Local override; error
    @(266.0800 mm, 141.9800 mm): Track [/BROTHER-CONNECTORS/SOL_D] on F.Cu, length 35.0800 mm
    @(265.9100 mm, 141.5400 mm): Track [/BROTHER-CONNECTORS/SOL_C] on F.Cu, length 35.4300 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1700 mm)
    Local override; error
    @(218.9100 mm, 146.0900 mm): Track [/BROTHER-CONNECTORS/SOL_D] on F.Cu, length 3.5497 mm
    @(221.2000 mm, 143.1600 mm): Track [/BROTHER-CONNECTORS/SOL_C] on F.Cu, length 43.0900 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1955 mm)
    Local override; error
    @(301.1600 mm, 141.9800 mm): Track [/BROTHER-CONNECTORS/SOL_D] on F.Cu, length 9.8854 mm
    @(266.3200 mm, 142.4000 mm): Track [/BROTHER-CONNECTORS/SOL_E] on F.Cu, length 34.6300 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1900 mm)
    Local override; error
    @(264.4800 mm, 143.5800 mm): Track [/BROTHER-CONNECTORS/SOL_D] on F.Cu, length 2.2627 mm
    @(265.9100 mm, 141.5400 mm): Track [/BROTHER-CONNECTORS/SOL_C] on F.Cu, length 35.4300 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1500 mm)
    Local override; error
    @(221.4200 mm, 143.5800 mm): Track [/BROTHER-CONNECTORS/SOL_D] on F.Cu, length 43.0600 mm
    @(221.6600 mm, 143.9800 mm): Track [/BROTHER-CONNECTORS/SOL_E] on F.Cu, length 43.0800 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1955 mm)
    Local override; error
    @(300.9500 mm, 142.4000 mm): Track [/BROTHER-CONNECTORS/SOL_E] on F.Cu, length 9.9278 mm
    @(308.1500 mm, 148.9700 mm): Track [/BROTHER-CONNECTORS/SOL_D] on F.Cu, length 14.1300 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1892 mm)
    Local override; error
    @(211.8700 mm, 147.3300 mm): Track [/BROTHER-CONNECTORS/SOL_D] on B.Cu, length 2.7011 mm
    @(210.8500 mm, 147.3400 mm): Via [/BROTHER-CONNECTORS/SOL_C] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1530 mm)
    Local override; error
    @(218.7800 mm, 145.5800 mm): Track [/BROTHER-CONNECTORS/SOL_C] on F.Cu, length 3.4224 mm
    @(212.1300 mm, 145.0800 mm): Track [/BROTHER-CONNECTORS/SOL_B] on F.Cu, length 6.5800 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1400 mm)
    Local override; error
    @(301.3400 mm, 141.5400 mm): Track [/BROTHER-CONNECTORS/SOL_C] on F.Cu, length 9.9136 mm
    @(265.7200 mm, 141.1500 mm): Track [/BROTHER-CONNECTORS/SOL_B] on F.Cu, length 35.8800 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1400 mm)
    Local override; error
    @(264.2900 mm, 143.1600 mm): Track [/BROTHER-CONNECTORS/SOL_C] on F.Cu, length 2.2910 mm
    @(265.7200 mm, 141.1500 mm): Track [/BROTHER-CONNECTORS/SOL_B] on F.Cu, length 35.8800 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1400 mm)
    Local override; error
    @(265.7200 mm, 141.1500 mm): Track [/BROTHER-CONNECTORS/SOL_B] on F.Cu, length 35.8800 mm
    @(265.9100 mm, 141.5400 mm): Track [/BROTHER-CONNECTORS/SOL_C] on F.Cu, length 35.4300 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1530 mm)
    Local override; error
    @(218.7100 mm, 145.0800 mm): Track [/BROTHER-CONNECTORS/SOL_B] on F.Cu, length 3.2527 mm
    @(221.2000 mm, 143.1600 mm): Track [/BROTHER-CONNECTORS/SOL_C] on F.Cu, length 43.0900 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1884 mm)
    Local override; error
    @(301.1600 mm, 141.9800 mm): Track [/BROTHER-CONNECTORS/SOL_D] on F.Cu, length 9.8854 mm
    @(308.3500 mm, 148.5500 mm): Track [/BROTHER-CONNECTORS/SOL_C] on F.Cu, length 11.8500 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1700 mm)
    Local override; error
    @(308.1500 mm, 148.9700 mm): Track [/BROTHER-CONNECTORS/SOL_D] on F.Cu, length 14.1300 mm
    @(320.2000 mm, 148.5500 mm): Track [/BROTHER-CONNECTORS/SOL_C] on F.Cu, length 4.5962 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1680 mm)
    Local override; error
    @(209.8700 mm, 147.3400 mm): Track [/BROTHER-CONNECTORS/SOL_B] on F.Cu, length 3.1961 mm
    @(210.8500 mm, 147.3400 mm): Via [/BROTHER-CONNECTORS/SOL_C] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1800 mm)
    Local override; error
    @(210.8500 mm, 147.3400 mm): Via [/BROTHER-CONNECTORS/SOL_C] on F.Cu - B.Cu
    @(209.8700 mm, 147.3400 mm): Via [/BROTHER-CONNECTORS/SOL_B] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1680 mm)
    Local override; error
    @(210.8500 mm, 147.3400 mm): Track [/BROTHER-CONNECTORS/SOL_C] on B.Cu, length 1.9940 mm
    @(209.8700 mm, 147.3400 mm): Via [/BROTHER-CONNECTORS/SOL_B] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1600 mm)
    Local override; error
    @(264.0900 mm, 142.7800 mm): Track [/BROTHER-CONNECTORS/SOL_B] on F.Cu, length 2.3052 mm
    @(265.4900 mm, 140.7400 mm): Track [/BROTHER-CONNECTORS/SOL_A] on F.Cu, length 36.3200 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1955 mm)
    Local override; error
    @(218.7100 mm, 145.0800 mm): Track [/BROTHER-CONNECTORS/SOL_B] on F.Cu, length 3.2527 mm
    @(211.3450 mm, 144.5900 mm): Track [/BROTHER-CONNECTORS/SOL_A] on F.Cu, length 7.2250 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1600 mm)
    Local override; error
    @(265.7200 mm, 141.1500 mm): Track [/BROTHER-CONNECTORS/SOL_B] on F.Cu, length 35.8800 mm
    @(265.4900 mm, 140.7400 mm): Track [/BROTHER-CONNECTORS/SOL_A] on F.Cu, length 36.3200 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1600 mm)
    Local override; error
    @(301.6000 mm, 141.1500 mm): Track [/BROTHER-CONNECTORS/SOL_B] on F.Cu, length 9.8288 mm
    @(265.4900 mm, 140.7400 mm): Track [/BROTHER-CONNECTORS/SOL_A] on F.Cu, length 36.3200 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1955 mm)
    Local override; error
    @(218.5700 mm, 144.5900 mm): Track [/BROTHER-CONNECTORS/SOL_A] on F.Cu, length 3.1254 mm
    @(221.0100 mm, 142.7800 mm): Track [/BROTHER-CONNECTORS/SOL_B] on F.Cu, length 43.0800 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1955 mm)
    Local override; error
    @(218.5700 mm, 144.5900 mm): Track [/BROTHER-CONNECTORS/SOL_A] on F.Cu, length 3.1254 mm
    @(218.7100 mm, 145.0800 mm): Track [/BROTHER-CONNECTORS/SOL_B] on F.Cu, length 3.2527 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1700 mm)
    Local override; error
    @(263.8500 mm, 142.3800 mm): Track [/BROTHER-CONNECTORS/SOL_A] on F.Cu, length 2.3193 mm
    @(265.3200 mm, 140.3200 mm): Track [/BROTHER-CONNECTORS/SOL_9] on F.Cu, length 36.7200 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1884 mm)
    Local override; error
    @(308.7000 mm, 147.6300 mm): Track [/BROTHER-CONNECTORS/SOL_A] on F.Cu, length 7.4200 mm
    @(301.6000 mm, 141.1500 mm): Track [/BROTHER-CONNECTORS/SOL_B] on F.Cu, length 9.8288 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1700 mm)
    Local override; error
    @(265.3200 mm, 140.3200 mm): Track [/BROTHER-CONNECTORS/SOL_9] on F.Cu, length 36.7200 mm
    @(265.4900 mm, 140.7400 mm): Track [/BROTHER-CONNECTORS/SOL_A] on F.Cu, length 36.3200 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1500 mm)
    Local override; error
    @(218.7100 mm, 145.0800 mm): Track [/BROTHER-CONNECTORS/SOL_B] on F.Cu, length 3.2527 mm
    @(220.7800 mm, 142.3800 mm): Track [/BROTHER-CONNECTORS/SOL_A] on F.Cu, length 43.0700 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1884 mm)
    Local override; error
    @(265.7200 mm, 141.1500 mm): Track [/BROTHER-CONNECTORS/SOL_B] on F.Cu, length 35.8800 mm
    @(301.8100 mm, 140.7400 mm): Track [/BROTHER-CONNECTORS/SOL_A] on F.Cu, length 9.7439 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(208.3900 mm, 147.7700 mm): Track [/BROTHER-CONNECTORS/SOL_A] on B.Cu, length 10.0200 mm
    @(207.8300 mm, 147.1450 mm): Via [/BROTHER-CONNECTORS/SOL_9] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1900 mm)
    Local override; error
    @(102.9552 mm, 148.4000 mm): Track [/BROTHER-CONNECTORS/SOL_A] on B.Cu, length 7.6158 mm
    @(189.9600 mm, 147.9600 mm): Track [/BROTHER-CONNECTORS/SOL_9] on B.Cu, length 88.5648 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1900 mm)
    Local override; error
    @(189.9600 mm, 147.9600 mm): Track [/BROTHER-CONNECTORS/SOL_9] on B.Cu, length 88.5648 mm
    @(189.3800 mm, 148.4000 mm): Track [/BROTHER-CONNECTORS/SOL_A] on B.Cu, length 86.4248 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1900 mm)
    Local override; error
    @(189.9600 mm, 147.9600 mm): Track [/BROTHER-CONNECTORS/SOL_9] on B.Cu, length 88.5648 mm
    @(191.6200 mm, 150.6400 mm): Track [/BROTHER-CONNECTORS/SOL_A] on B.Cu, length 3.1678 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(218.4100 mm, 144.1000 mm): Track [/BROTHER-CONNECTORS/SOL_9] on F.Cu, length 2.9981 mm
    @(220.0050 mm, 141.6300 mm): Track [/BROTHER-CONNECTORS/SOL_8] on F.Cu, length 43.3200 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(302.0400 mm, 140.3200 mm): Track [/BROTHER-CONNECTORS/SOL_9] on F.Cu, length 9.6732 mm
    @(264.9850 mm, 139.9700 mm): Track [/BROTHER-CONNECTORS/SOL_8] on F.Cu, length 37.2000 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1672 mm)
    Local override; error
    @(263.6600 mm, 141.9800 mm): Track [/BROTHER-CONNECTORS/SOL_9] on F.Cu, length 2.3476 mm
    @(265.4900 mm, 140.7400 mm): Track [/BROTHER-CONNECTORS/SOL_A] on F.Cu, length 36.3200 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1500 mm)
    Local override; error
    @(218.5700 mm, 144.5900 mm): Track [/BROTHER-CONNECTORS/SOL_A] on F.Cu, length 3.1254 mm
    @(220.5300 mm, 141.9800 mm): Track [/BROTHER-CONNECTORS/SOL_9] on F.Cu, length 43.1300 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(265.3200 mm, 140.3200 mm): Track [/BROTHER-CONNECTORS/SOL_9] on F.Cu, length 36.7200 mm
    @(264.9850 mm, 139.9700 mm): Track [/BROTHER-CONNECTORS/SOL_8] on F.Cu, length 37.2000 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(206.9200 mm, 146.5650 mm): Via [/BROTHER-CONNECTORS/SOL_8] on F.Cu - B.Cu
    @(207.7850 mm, 147.1900 mm): Track [/BROTHER-CONNECTORS/SOL_9] on B.Cu, length 9.5650 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(218.1800 mm, 142.9600 mm): Track [/BROTHER-CONNECTORS/SOL_7] on F.Cu, length 2.4607 mm
    @(218.0550 mm, 143.5800 mm): Track [/BROTHER-CONNECTORS/SOL_8] on F.Cu, length 2.7577 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(302.0400 mm, 140.3200 mm): Track [/BROTHER-CONNECTORS/SOL_9] on F.Cu, length 9.6732 mm
    @(308.5150 mm, 146.3000 mm): Track [/BROTHER-CONNECTORS/SOL_8] on F.Cu, length 3.9350 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1800 mm)
    Local override; error
    @(264.9200 mm, 139.5400 mm): Track [/BROTHER-CONNECTORS/SOL_7] on F.Cu, length 37.5700 mm
    @(263.3250 mm, 141.6300 mm): Track [/BROTHER-CONNECTORS/SOL_8] on F.Cu, length 2.3476 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(218.1800 mm, 142.9600 mm): Track [/BROTHER-CONNECTORS/SOL_7] on F.Cu, length 2.4607 mm
    @(220.0050 mm, 141.6300 mm): Track [/BROTHER-CONNECTORS/SOL_8] on F.Cu, length 43.3200 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1800 mm)
    Local override; error
    @(264.9200 mm, 139.5400 mm): Track [/BROTHER-CONNECTORS/SOL_7] on F.Cu, length 37.5700 mm
    @(302.1850 mm, 139.9700 mm): Track [/BROTHER-CONNECTORS/SOL_8] on F.Cu, length 8.9520 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(263.6600 mm, 141.9800 mm): Track [/BROTHER-CONNECTORS/SOL_9] on F.Cu, length 2.3476 mm
    @(264.9850 mm, 139.9700 mm): Track [/BROTHER-CONNECTORS/SOL_8] on F.Cu, length 37.2000 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(265.1164 mm, 144.8500 mm): Track [/BROTHER-CONNECTORS/ENC_V2] on F.Cu, length 2.1779 mm
    @(266.5735 mm, 143.1100 mm): Track [/BROTHER-CONNECTORS/ENC_V1] on F.Cu, length 14.7965 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(279.0700 mm, 143.3100 mm): Track [/BROTHER-CONNECTORS/ENC_V2] on F.Cu, length 2.6304 mm
    @(266.5735 mm, 143.1100 mm): Track [/BROTHER-CONNECTORS/ENC_V1] on F.Cu, length 14.7965 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(237.5200 mm, 144.8500 mm): Track [/BROTHER-CONNECTORS/ENC_V2] on F.Cu, length 27.5964 mm
    @(237.6600 mm, 145.6500 mm): Track [/BROTHER-CONNECTORS/ENC_BELTPHASE] on F.Cu, length 0.8485 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(236.8600 mm, 144.6500 mm): Track [/BROTHER-CONNECTORS/ENC_V1] on F.Cu, length 28.1735 mm
    @(236.7300 mm, 145.6400 mm): Track [/BROTHER-CONNECTORS/ENC_V2] on F.Cu, length 1.1172 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(266.5735 mm, 143.1100 mm): Track [/BROTHER-CONNECTORS/ENC_V1] on F.Cu, length 14.7965 mm
    @(266.6564 mm, 143.3100 mm): Track [/BROTHER-CONNECTORS/ENC_V2] on F.Cu, length 12.4136 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1750 mm)
    Local override; error
    @(237.2200 mm, 149.3800 mm): Track [/BROTHER-CONNECTORS/ENC_BELTPHASE] on F.Cu, length 40.4800 mm
    @(236.7200 mm, 148.9300 mm): Via [/BROTHER-CONNECTORS/ENC_V2] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(265.0335 mm, 144.6500 mm): Track [/BROTHER-CONNECTORS/ENC_V1] on F.Cu, length 2.1779 mm
    @(266.6564 mm, 143.3100 mm): Track [/BROTHER-CONNECTORS/ENC_V2] on F.Cu, length 12.4136 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(236.8600 mm, 144.6500 mm): Track [/BROTHER-CONNECTORS/ENC_V1] on F.Cu, length 28.1735 mm
    @(221.8650 mm, 144.3750 mm): Track [/BROTHER-CONNECTORS/SOL_F] on F.Cu, length 43.0546 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1150 mm)
    Local override; error
    @(266.4746 mm, 142.8200 mm): Track [/BROTHER-CONNECTORS/SOL_F] on F.Cu, length 34.3254 mm
    @(281.3700 mm, 143.1100 mm): Track [/BROTHER-CONNECTORS/ENC_V1] on F.Cu, length 2.9133 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(235.8700 mm, 145.6400 mm): Track [/BROTHER-CONNECTORS/ENC_V1] on F.Cu, length 1.4001 mm
    @(221.8650 mm, 144.3750 mm): Track [/BROTHER-CONNECTORS/SOL_F] on F.Cu, length 43.0546 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1150 mm)
    Local override; error
    @(266.4746 mm, 142.8200 mm): Track [/BROTHER-CONNECTORS/SOL_F] on F.Cu, length 34.3254 mm
    @(266.5735 mm, 143.1100 mm): Track [/BROTHER-CONNECTORS/ENC_V1] on F.Cu, length 14.7965 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(186.7758 mm, 154.0300 mm): Track [/BROTHER-CONNECTORS/ENC_BELTPHASE] on F.Cu, length 1.1478 mm
    @(187.1900 mm, 155.0300 mm): PTH pad 4 [/IO CONDITIONING/EOL_L_K] of J702
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(276.7700 mm, 143.5100 mm): Track [/BROTHER-CONNECTORS/ENC_BELTPHASE] on F.Cu, length 2.3476 mm
    @(266.6564 mm, 143.3100 mm): Track [/BROTHER-CONNECTORS/ENC_V2] on F.Cu, length 12.4136 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(266.7392 mm, 143.5100 mm): Track [/BROTHER-CONNECTORS/ENC_BELTPHASE] on F.Cu, length 10.0308 mm
    @(266.6564 mm, 143.3100 mm): Track [/BROTHER-CONNECTORS/ENC_V2] on F.Cu, length 12.4136 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(265.1992 mm, 145.0500 mm): Track [/BROTHER-CONNECTORS/ENC_BELTPHASE] on F.Cu, length 2.1779 mm
    @(266.6564 mm, 143.3100 mm): Track [/BROTHER-CONNECTORS/ENC_V2] on F.Cu, length 12.4136 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(170.5493 mm, 155.3007 mm): Track [/BROTHER-CONNECTORS/ENC_BELTPHASE] on F.Cu, length 7.4882 mm
    @(177.0125 mm, 154.6757 mm): Pad 2 [GND] of R705 on F.Cu
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(238.4500 mm, 145.6300 mm): Track [/BROTHER-CONNECTORS/EOL_R_S] on F.Cu, length 0.5374 mm
    @(238.2600 mm, 145.0500 mm): Track [/BROTHER-CONNECTORS/ENC_BELTPHASE] on F.Cu, length 26.9392 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(187.1900 mm, 155.0300 mm): PTH pad 4 [/IO CONDITIONING/EOL_L_K] of J702
    @(185.7758 mm, 155.0300 mm): Track [/BROTHER-CONNECTORS/ENC_BELTPHASE] on F.Cu, length 1.4142 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(272.1700 mm, 143.9100 mm): Track [/BROTHER-CONNECTORS/EOL_R_N] on F.Cu, length 1.7819 mm
    @(266.8220 mm, 143.7100 mm): Track [/BROTHER-CONNECTORS/EOL_R_S] on F.Cu, length 7.6480 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(265.2820 mm, 145.2500 mm): Track [/BROTHER-CONNECTORS/EOL_R_S] on F.Cu, length 2.1779 mm
    @(266.9049 mm, 143.9100 mm): Track [/BROTHER-CONNECTORS/EOL_R_N] on F.Cu, length 5.2651 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(265.2820 mm, 145.2500 mm): Track [/BROTHER-CONNECTORS/EOL_R_S] on F.Cu, length 2.1779 mm
    @(265.1649 mm, 145.6500 mm): Track [/BROTHER-CONNECTORS/EOL_R_N] on F.Cu, length 2.4607 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1250 mm)
    Local override; error
    @(239.2200 mm, 145.6500 mm): Via [/BROTHER-CONNECTORS/EOL_R_N] on F.Cu - B.Cu
    @(238.8300 mm, 145.2500 mm): Track [/BROTHER-CONNECTORS/EOL_R_S] on F.Cu, length 26.4520 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(218.2400 mm, 130.7100 mm): Track [/BROTHER-CONNECTORS/EOL_R_S] on B.Cu, length 75.5350 mm
    @(217.7300 mm, 130.9100 mm): Track [/BROTHER-CONNECTORS/EOL_R_N] on B.Cu, length 4.5821 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1550 mm)
    Local override; error
    @(240.5300 mm, 131.4400 mm): Track [/ESP32/BUZZER] on B.Cu, length 14.1600 mm
    @(240.2000 mm, 144.4000 mm): Track [/BROTHER-CONNECTORS/EOL_R_N] on B.Cu, length 1.5884 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(217.2400 mm, 131.1100 mm): Track [/ESP32/ESP14] on B.Cu, length 79.2150 mm
    @(140.3650 mm, 130.9100 mm): Track [/BROTHER-CONNECTORS/EOL_R_N] on B.Cu, length 77.3650 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(274.4700 mm, 143.7100 mm): Track [/BROTHER-CONNECTORS/EOL_R_S] on F.Cu, length 2.0648 mm
    @(266.7392 mm, 143.5100 mm): Track [/BROTHER-CONNECTORS/ENC_BELTPHASE] on F.Cu, length 10.0308 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(238.8300 mm, 145.2500 mm): Track [/BROTHER-CONNECTORS/EOL_R_S] on F.Cu, length 26.4520 mm
    @(265.1992 mm, 145.0500 mm): Track [/BROTHER-CONNECTORS/ENC_BELTPHASE] on F.Cu, length 2.1779 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(265.1992 mm, 145.0500 mm): Track [/BROTHER-CONNECTORS/ENC_BELTPHASE] on F.Cu, length 2.1779 mm
    @(265.2820 mm, 145.2500 mm): Track [/BROTHER-CONNECTORS/EOL_R_S] on F.Cu, length 2.1779 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(265.1992 mm, 145.0500 mm): Track [/BROTHER-CONNECTORS/ENC_BELTPHASE] on F.Cu, length 2.1779 mm
    @(266.8220 mm, 143.7100 mm): Track [/BROTHER-CONNECTORS/EOL_R_S] on F.Cu, length 7.6480 mm
[clearance]: Clearance violation ( clearance 0.2000 mm; actual 0.1000 mm)
    Local override; error
    @(218.2400 mm, 130.7100 mm): Track [/BROTHER-CONNECTORS/EOL_R_S] on B.Cu, length 75.5350 mm
    @(140.3650 mm, 130.9100 mm): Track [/BROTHER-CONNECTORS/EOL_R_N] on B.Cu, length 77.3650 mm
[silk_overlap]: Silkscreen overlap
    Rule: board setup constraints silk; warning
    @(144.5500 mm, 121.5700 mm): Segment of J201 on F.Silkscreen
    @(143.7450 mm, 124.6000 mm): PCB text '39' on F.Silkscreen
[silk_overlap]: Silkscreen overlap
    Rule: board setup constraints silk; warning
    @(114.2900 mm, 149.3500 mm): Segment of J406 on F.Silkscreen
    @(143.0832 mm, 146.0258 mm): Polygon of kibuzzard-65BFD905 on F.Silkscreen
[silk_overlap]: Silkscreen overlap
    Rule: board setup constraints silk; warning
    @(141.6900 mm, 149.3500 mm): Segment of J406 on F.Silkscreen
    @(143.0832 mm, 146.0258 mm): Polygon of kibuzzard-65BFD905 on F.Silkscreen
[silk_overlap]: Silkscreen overlap
    Rule: board setup constraints silk; warning
    @(136.5925 mm, 153.3256 mm): Polygon of kibuzzard-65BFD8F7 on F.Silkscreen
    @(135.4000 mm, 156.1552 mm): Segment of J401 on F.Silkscreen
[silk_overlap]: Silkscreen overlap
    Rule: board setup constraints silk; warning
    @(116.2610 mm, 158.9302 mm): Polygon of kibuzzard-65BFE062 on F.Silkscreen
    @(124.7627 mm, 159.7225 mm): Segment of R821 on F.Silkscreen
[silk_overlap]: Silkscreen overlap
    Rule: board setup constraints silk; warning
    @(136.5925 mm, 153.3256 mm): Polygon of kibuzzard-65BFD8F7 on F.Silkscreen
    @(135.4000 mm, 152.1352 mm): Segment of J401 on F.Silkscreen
[silk_overlap]: Silkscreen overlap
    Rule: board setup constraints silk; warning
    @(252.0500 mm, 121.5200 mm): Segment of J801 on F.Silkscreen
    @(251.4000 mm, 123.2100 mm): PCB text 't r + -' on F.Silkscreen
[silk_overlap]: Silkscreen overlap
    Rule: board setup constraints silk; warning
    @(259.7627 mm, 125.4775 mm): Segment of R214 on F.Silkscreen
    @(252.3865 mm, 124.1692 mm): Polygon of kibuzzard-65A2E6F1 on F.Silkscreen
[silk_overlap]: Silkscreen overlap
    Rule: board setup constraints silk; warning
    @(252.3865 mm, 124.1692 mm): Polygon of kibuzzard-65A2E6F1 on F.Silkscreen
    @(259.7627 mm, 126.5225 mm): Segment of R214 on F.Silkscreen
[silk_overlap]: Silkscreen overlap
    Rule: board setup constraints silk; warning
    @(259.7627 mm, 124.5225 mm): Segment of R213 on F.Silkscreen
    @(252.3865 mm, 124.1692 mm): Polygon of kibuzzard-65A2E6F1 on F.Silkscreen
[silk_overlap]: Silkscreen overlap
    Rule: board setup constraints silk; warning
    @(204.3350 mm, 140.4650 mm): Segment of J805 on F.Silkscreen
    @(206.4684 mm, 140.4088 mm): Polygon of kibuzzard-65A1DFCB on F.Silkscreen
[silk_overlap]: Silkscreen overlap
    Rule: board setup constraints silk; warning
    @(150.1484 mm, 159.4294 mm): Polygon of kibuzzard-65BFD8D6 on F.Silkscreen
    @(154.4000 mm, 162.4500 mm): Segment of J413 on F.Silkscreen
[silk_overlap]: Silkscreen overlap
    Rule: board setup constraints silk; warning
    @(149.9003 mm, 153.6915 mm): Polygon of kibuzzard-65BFD8DF on F.Silkscreen
    @(154.3600 mm, 156.8600 mm): Segment of J410 on F.Silkscreen
[silk_overlap]: Silkscreen overlap
    Rule: board setup constraints silk; warning
    @(154.3600 mm, 156.8600 mm): Segment of J410 on F.Silkscreen
    @(149.9003 mm, 153.6915 mm): Polygon of kibuzzard-65BFD8DF on F.Silkscreen
[silk_overlap]: Silkscreen overlap
    Rule: board setup constraints silk; warning
    @(150.1484 mm, 159.4294 mm): Polygon of kibuzzard-65BFD8D6 on F.Silkscreen
    @(154.4000 mm, 158.1000 mm): Segment of J413 on F.Silkscreen
[silk_overlap]: Silkscreen overlap
    Rule: board setup constraints silk; warning
    @(205.7885 mm, 156.0594 mm): Polygon of kibuzzard-658236C5 on F.Silkscreen
    @(205.9204 mm, 153.5677 mm): Polygon of kibuzzard-658236BF on F.Silkscreen
[silk_overlap]: Silkscreen overlap
    Rule: board setup constraints silk; warning
    @(217.5882 mm, 151.1288 mm): Polygon of kibuzzard-658236FD on F.Silkscreen
    @(217.5812 mm, 153.6427 mm): Polygon of kibuzzard-658236F2 on F.Silkscreen
[silk_overlap]: Silkscreen overlap
    Rule: board setup constraints silk; warning
    @(217.5853 mm, 156.1427 mm): Polygon of kibuzzard-658236E5 on F.Silkscreen
    @(217.5700 mm, 158.6344 mm): Polygon of kibuzzard-65823743 on F.Silkscreen
[silk_overlap]: Silkscreen overlap
    Rule: board setup constraints silk; warning
    @(124.7627 mm, 158.6775 mm): Segment of R821 on F.Silkscreen
    @(116.2610 mm, 158.9302 mm): Polygon of kibuzzard-65BFE062 on F.Silkscreen
[silk_overlap]: Silkscreen overlap
    Rule: board setup constraints silk; warning
    @(78.0052 mm, 146.3744 mm): Polygon of kibuzzard-65BFD887 on F.Silkscreen
    @(68.7600 mm, 149.3300 mm): Segment of J411 on F.Silkscreen
[silk_overlap]: Silkscreen overlap
    Rule: board setup constraints silk; warning
    @(76.7600 mm, 149.3300 mm): Segment of J411 on F.Silkscreen
    @(78.0052 mm, 146.3744 mm): Polygon of kibuzzard-65BFD887 on F.Silkscreen
[silk_overlap]: Silkscreen overlap
    Rule: board setup constraints silk; warning
    @(85.2267 mm, 146.2515 mm): Polygon of kibuzzard-65BFD8A4 on F.Silkscreen
    @(89.9550 mm, 149.4200 mm): Segment of J407 on F.Silkscreen
[silk_overlap]: Silkscreen overlap
    Rule: board setup constraints silk; warning
    @(85.2267 mm, 146.2515 mm): Polygon of kibuzzard-65BFD8A4 on F.Silkscreen
    @(112.7050 mm, 149.4560 mm): Segment of J407 on F.Silkscreen
[silk_overlap]: Silkscreen overlap
    Rule: board setup constraints silk; warning
    @(79.6743 mm, 134.0808 mm): Polygon of kibuzzard-65A1AC88 on F.Silkscreen
    @(145.0000 mm, 159.0000 mm): Circle of TP703 on F.Silkscreen
[silk_overlap]: Silkscreen overlap
    Rule: board setup constraints silk; warning
    @(87.1270 mm, 153.1194 mm): Polygon of kibuzzard-65BFD8C0 on F.Silkscreen
    @(91.5700 mm, 156.1552 mm): Segment of J402 on F.Silkscreen
[silk_overlap]: Silkscreen overlap
    Rule: board setup constraints silk; warning
    @(87.1270 mm, 153.1194 mm): Polygon of kibuzzard-65BFD8C0 on F.Silkscreen
    @(110.1300 mm, 156.1552 mm): Segment of J402 on F.Silkscreen
[silk_overlap]: Silkscreen overlap
    Rule: board setup constraints silk; warning
    @(68.7600 mm, 142.5250 mm): Segment of J414 on F.Silkscreen
    @(80.0345 mm, 139.3967 mm): Polygon of kibuzzard-65BFD893 on F.Silkscreen
[silk_overlap]: Silkscreen overlap
    Rule: board setup constraints silk; warning
    @(78.0800 mm, 140.1050 mm): Segment of J414 on F.Silkscreen
    @(80.0345 mm, 139.3967 mm): Polygon of kibuzzard-65BFD893 on F.Silkscreen
[silk_overlap]: Silkscreen overlap
    Rule: board setup constraints silk; warning
    @(78.7600 mm, 142.5250 mm): Segment of J414 on F.Silkscreen
    @(80.0345 mm, 139.3967 mm): Polygon of kibuzzard-65BFD893 on F.Silkscreen
[silk_overlap]: Silkscreen overlap
    Rule: board setup constraints silk; warning
    @(273.1404 mm, 158.5500 mm): Segment of J803 on F.Silkscreen
    @(268.5841 mm, 157.5119 mm): Polygon of kibuzzard-659F41CB on F.Silkscreen
[silk_overlap]: Silkscreen overlap
    Rule: board setup constraints silk; warning
    @(268.5841 mm, 157.5119 mm): Polygon of kibuzzard-659F41CB on F.Silkscreen
    @(273.1404 mm, 161.0500 mm): Segment of J803 on F.Silkscreen
[silk_overlap]: Silkscreen overlap
    Rule: board setup constraints silk; warning
    @(274.1904 mm, 158.5500 mm): Segment of J803 on F.Silkscreen
    @(268.5841 mm, 157.5119 mm): Polygon of kibuzzard-659F41CB on F.Silkscreen
[silk_overlap]: Silkscreen overlap
    Rule: board setup constraints silk; warning
    @(269.6819 mm, 133.5614 mm): Polygon of kibuzzard-659F49F4 on F.Silkscreen
    @(273.8374 mm, 134.5184 mm): Circle of TP603 on F.Silkscreen
[silk_overlap]: Silkscreen overlap
    Rule: board setup constraints silk; warning
    @(333.3450 mm, 158.4025 mm): Segment of J409 on F.Silkscreen
    @(328.5454 mm, 157.6607 mm): Polygon of kibuzzard-65BFD865 on F.Silkscreen
[silk_overlap]: Silkscreen overlap
    Rule: board setup constraints silk; warning
    @(328.5454 mm, 157.6607 mm): Polygon of kibuzzard-65BFD865 on F.Silkscreen
    @(333.3450 mm, 160.7825 mm): Segment of J409 on F.Silkscreen
[silk_overlap]: Silkscreen overlap
    Rule: board setup constraints silk; warning
    @(328.5454 mm, 157.6607 mm): Polygon of kibuzzard-65BFD865 on F.Silkscreen
    @(333.3450 mm, 160.7825 mm): Segment of J409 on F.Silkscreen
[silk_overlap]: Silkscreen overlap
    Rule: board setup constraints silk; warning
    @(321.6600 mm, 160.1600 mm): Circle of TP702 on F.Silkscreen
    @(315.2007 mm, 159.2308 mm): Polygon of kibuzzard-65A1ADEE on F.Silkscreen
[silk_overlap]: Silkscreen overlap
    Rule: board setup constraints silk; warning
    @(306.6372 mm, 149.0571 mm): Polygon of kibuzzard-65C3D944 on F.Silkscreen
    @(305.3200 mm, 149.9800 mm): Circle of TP601 on F.Silkscreen
[silk_overlap]: Silkscreen overlap
    Rule: board setup constraints silk; warning
    @(306.8630 mm, 134.5184 mm): Circle of TP602 on F.Silkscreen
    @(302.8609 mm, 133.5900 mm): Polygon of kibuzzard-659F49E4 on F.Silkscreen
[silk_over_copper]: Silkscreen clipped by solder mask
    Local override; warning
    @(120.0863 mm, 160.1957 mm): Polygon of kibuzzard-65BFE062 on F.Silkscreen
[silk_over_copper]: Silkscreen clipped by solder mask
    Local override; warning
    @(121.2445 mm, 160.1957 mm): Polygon of kibuzzard-65BFE062 on F.Silkscreen
[silk_over_copper]: Silkscreen clipped by solder mask
    Local override; warning
    @(116.2610 mm, 158.9302 mm): Polygon of kibuzzard-65BFE062 on F.Silkscreen
[silk_over_copper]: Silkscreen clipped by solder mask
    Local override; warning
    @(190.3100 mm, 116.7800 mm): Segment of SW203 on F.Silkscreen
[silk_over_copper]: Silkscreen clipped by solder mask
    Local override; warning
    @(190.3100 mm, 120.4200 mm): Segment of SW203 on F.Silkscreen
[silk_over_copper]: Silkscreen clipped by solder mask
    Local override; warning
    @(302.8609 mm, 133.5900 mm): Polygon of kibuzzard-659F49E4 on F.Silkscreen
[silk_over_copper]: Silkscreen clipped by solder mask
    Local override; warning
    @(252.3865 mm, 124.1692 mm): Polygon of kibuzzard-65A2E6F1 on F.Silkscreen
[silk_over_copper]: Silkscreen clipped by solder mask
    Local override; warning
    @(117.0000 mm, 158.6900 mm): Segment of Q805 on F.Silkscreen
[silk_over_copper]: Silkscreen clipped by solder mask
    Local override; warning
    @(117.0000 mm, 161.8100 mm): Segment of Q805 on F.Silkscreen
[silk_over_copper]: Silkscreen clipped by solder mask
    Local override; warning
    @(306.6372 mm, 149.0571 mm): Polygon of kibuzzard-65C3D944 on F.Silkscreen
[silk_over_copper]: Silkscreen clipped by solder mask
    Local override; warning
    @(79.6743 mm, 134.0808 mm): Polygon of kibuzzard-65A1AC88 on F.Silkscreen
[silk_over_copper]: Silkscreen clipped by solder mask
    Local override; warning
    @(167.0300 mm, 116.7800 mm): Segment of SW201 on F.Silkscreen
[silk_over_copper]: Silkscreen clipped by solder mask
    Local override; warning
    @(167.0300 mm, 120.4200 mm): Segment of SW201 on F.Silkscreen
[silk_over_copper]: Silkscreen clipped by solder mask
    Local override; warning
    @(178.6700 mm, 116.7800 mm): Segment of SW202 on F.Silkscreen
[silk_over_copper]: Silkscreen clipped by solder mask
    Local override; warning
    @(178.6700 mm, 120.4200 mm): Segment of SW202 on F.Silkscreen
[silk_over_copper]: Silkscreen clipped by solder mask
    Local override; warning
    @(268.5841 mm, 157.5119 mm): Polygon of kibuzzard-659F41CB on F.Silkscreen
[silk_over_copper]: Silkscreen clipped by solder mask
    Local override; warning
    @(269.6819 mm, 133.5614 mm): Polygon of kibuzzard-659F49F4 on F.Silkscreen
[silk_over_copper]: Silkscreen clipped by solder mask
    Local override; warning
    @(206.4684 mm, 140.4088 mm): Polygon of kibuzzard-65A1DFCB on F.Silkscreen
[silk_over_copper]: Silkscreen clipped by solder mask
    Local override; warning
    @(315.2007 mm, 159.2308 mm): Polygon of kibuzzard-65A1ADEE on F.Silkscreen
[lib_footprint_issues]: The current configuration does not include the footprint library 'Capacitor_THT'.
    Local override; warning
    @(268.2900 mm, 121.7100 mm): Footprint C609
[lib_footprint_issues]: The current configuration does not include the footprint library 'Capacitor_SMD'.
    Local override; warning
    @(247.5000 mm, 152.3600 mm): Footprint C501
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(125.0000 mm, 159.2000 mm): Footprint R821
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(125.0000 mm, 159.2000 mm): Footprint R821
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(125.0000 mm, 159.2000 mm): Footprint R821
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(125.0000 mm, 159.2000 mm): Footprint R821
[lib_footprint_issues]: The current configuration does not include the footprint library 'matei'.
    Local override; warning
    @(71.8500 mm, 158.9200 mm): Footprint G***
[lib_footprint_issues]: The current configuration does not include the footprint library 'Fiducial'.
    Local override; warning
    @(124.8600 mm, 129.0800 mm): Footprint FID104
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(212.7500 mm, 136.9750 mm): Footprint R813
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(273.0646 mm, 155.4750 mm): Footprint R807
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(235.3250 mm, 126.7750 mm): Footprint R207
[lib_footprint_issues]: The current configuration does not include the footprint library 'Library'.
    Local override; warning
    @(280.9300 mm, 145.1700 mm): Footprint J405
[lib_footprint_issues]: The current configuration does not include the footprint library 'easyeda2kicad'.
    Local override; warning
    @(193.9600 mm, 120.4800 mm): Footprint SW203
[lib_footprint_issues]: The current configuration does not include the footprint library 'Library'.
    Local override; warning
    @(322.2000 mm, 145.3000 mm): Footprint J404
[lib_footprint_issues]: The current configuration does not include the footprint library 'TestPoint'.
    Local override; warning
    @(145.0000 mm, 159.0000 mm): Footprint TP703
[lib_footprint_issues]: The current configuration does not include the footprint library 'TestPoint'.
    Local override; warning
    @(145.0000 mm, 159.0000 mm): Footprint TP703
[lib_footprint_issues]: The current configuration does not include the footprint library 'TestPoint'.
    Local override; warning
    @(253.4800 mm, 148.9900 mm): Footprint TP503
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(242.2050 mm, 134.6750 mm): Footprint R203
[lib_footprint_issues]: The current configuration does not include the footprint library 'Capacitor_SMD'.
    Local override; warning
    @(305.9044 mm, 125.3500 mm): Footprint C610
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(180.8875 mm, 154.6757 mm): Footprint R706
[lib_footprint_issues]: The current configuration does not include the footprint library 'Capacitor_SMD'.
    Local override; warning
    @(276.4600 mm, 130.8500 mm): Footprint C621
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(310.1200 mm, 133.3500 mm): Footprint R604
[lib_footprint_issues]: The current configuration does not include the footprint library 'TestPoint'.
    Local override; warning
    @(270.9300 mm, 149.1500 mm): Footprint TP401
[lib_footprint_issues]: The current configuration does not include the footprint library 'Capacitor_SMD'.
    Local override; warning
    @(273.0300 mm, 121.8300 mm): Footprint C602
[lib_footprint_issues]: The current configuration does not include the footprint library 'Library'.
    Local override; warning
    @(339.3591 mm, 152.0338 mm): Footprint J412
[lib_footprint_issues]: The current configuration does not include the footprint library 'Library'.
    Local override; warning
    @(163.8400 mm, 159.7500 mm): Footprint J413
[lib_footprint_issues]: The current configuration does not include the footprint library 'Capacitor_SMD'.
    Local override; warning
    @(255.1750 mm, 150.8850 mm): Footprint C502
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(260.0000 mm, 126.0000 mm): Footprint R214
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(235.3150 mm, 131.4600 mm): Footprint R819
[lib_footprint_issues]: The current configuration does not include the footprint library 'Capacitor_SMD'.
    Local override; warning
    @(122.1750 mm, 141.3250 mm): Footprint C303
[lib_footprint_issues]: The current configuration does not include the footprint library 'Package_SO'.
    Local override; warning
    @(103.3500 mm, 139.3250 mm): Footprint U304
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(98.7100 mm, 130.8100 mm): Footprint R810
[lib_footprint_issues]: The current configuration does not include the footprint library 'Diode_SMD'.
    Local override; warning
    @(279.9900 mm, 133.3400 mm): Footprint D604
[lib_footprint_issues]: The current configuration does not include the footprint library 'Connector_JST'.
    Local override; warning
    @(202.5500 mm, 143.5250 mm): Footprint J805
[lib_footprint_issues]: The current configuration does not include the footprint library 'TestPoint'.
    Local override; warning
    @(268.4200 mm, 149.1400 mm): Footprint TP402
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(313.1200 mm, 157.2500 mm): Footprint R738
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(180.8875 mm, 157.9174 mm): Footprint R710
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(209.2500 mm, 135.7500 mm): Footprint R216
[lib_footprint_issues]: The current configuration does not include the footprint library 'Capacitor_SMD'.
    Local override; warning
    @(305.8700 mm, 121.8500 mm): Footprint C601
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(177.8375 mm, 156.2966 mm): Footprint R707
[lib_footprint_issues]: The current configuration does not include the footprint library 'Package_SO'.
    Local override; warning
    @(115.9000 mm, 139.3250 mm): Footprint U303
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(212.7500 mm, 133.6750 mm): Footprint R209
[lib_footprint_issues]: The current configuration does not include the footprint library 'easyeda2kicad'.
    Local override; warning
    @(292.1050 mm, 156.0848 mm): Footprint J601
[lib_footprint_issues]: The current configuration does not include the footprint library 'Connector_PinHeader_2.54mm'.
    Local override; warning
    @(212.5875 mm, 152.5174 mm): Footprint J701
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(180.8875 mm, 153.0549 mm): Footprint R704
[lib_footprint_issues]: The current configuration does not include the footprint library 'MountingHole'.
    Local override; warning
    @(332.1841 mm, 152.5588 mm): Footprint H106
[lib_footprint_issues]: The current configuration does not include the footprint library 'Connector_PinHeader_2.54mm'.
    Local override; warning
    @(252.0500 mm, 120.2500 mm): Footprint J801
[lib_footprint_issues]: The current configuration does not include the footprint library 'Library'.
    Local override; warning
    @(62.9000 mm, 120.6200 mm): Footprint J602
[lib_footprint_issues]: The current configuration does not include the footprint library 'easyeda2kicad'.
    Local override; warning
    @(161.8600 mm, 153.8100 mm): Footprint J410
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(242.2050 mm, 136.8900 mm): Footprint R204
[lib_footprint_issues]: The current configuration does not include the footprint library 'Package_TO_SOT_SMD'.
    Local override; warning
    @(117.0000 mm, 160.2500 mm): Footprint Q805
[lib_footprint_issues]: The current configuration does not include the footprint library 'Package_TO_SOT_SMD'.
    Local override; warning
    @(117.0000 mm, 160.2500 mm): Footprint Q805
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(304.8300 mm, 130.6200 mm): Footprint R606
[lib_footprint_issues]: The current configuration does not include the footprint library 'Fiducial'.
    Local override; warning
    @(240.9900 mm, 126.5800 mm): Footprint FID102
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(177.8375 mm, 153.0549 mm): Footprint R703
[lib_footprint_issues]: The current configuration does not include the footprint library 'Fiducial'.
    Local override; warning
    @(266.5400 mm, 153.0400 mm): Footprint FID106
[lib_footprint_issues]: The current configuration does not include the footprint library 'Library'.
    Local override; warning
    @(72.7600 mm, 146.4500 mm): Footprint J411
[lib_footprint_issues]: The current configuration does not include the footprint library 'Capacitor_SMD'.
    Local override; warning
    @(280.5600 mm, 130.8400 mm): Footprint C617
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(276.9600 mm, 133.3400 mm): Footprint R605
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(273.0646 mm, 152.4250 mm): Footprint R801
[lib_footprint_issues]: The current configuration does not include the footprint library 'Capacitor_SMD'.
    Local override; warning
    @(274.6600 mm, 130.6300 mm): Footprint C615
[lib_footprint_issues]: The current configuration does not include the footprint library 'Capacitor_SMD'.
    Local override; warning
    @(235.3250 mm, 125.2000 mm): Footprint C202
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(180.8875 mm, 156.2966 mm): Footprint R708
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(238.0100 mm, 152.1500 mm): Footprint R211
[lib_footprint_issues]: The current configuration does not include the footprint library 'Diode_SMD'.
    Local override; warning
    @(238.6925 mm, 132.4900 mm): Footprint D201
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(235.3250 mm, 129.9100 mm): Footprint R818
[lib_footprint_issues]: The current configuration does not include the footprint library 'TestPoint'.
    Local override; warning
    @(249.1600 mm, 148.9800 mm): Footprint TP502
[lib_footprint_issues]: The current configuration does not include the footprint library 'Capacitor_SMD'.
    Local override; warning
    @(235.3000 mm, 133.3700 mm): Footprint C201
[lib_footprint_issues]: The current configuration does not include the footprint library 'MountingHole'.
    Local override; warning
    @(332.1841 mm, 133.7628 mm): Footprint H104
[lib_footprint_issues]: The current configuration does not include the footprint library 'Connector_PinHeader_2.54mm'.
    Local override; warning
    @(184.6500 mm, 152.4900 mm): Footprint J702
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(257.4750 mm, 160.3725 mm): Footprint R503
[lib_footprint_issues]: The current configuration does not include the footprint library 'Capacitor_THT'.
    Local override; warning
    @(268.2600 mm, 128.9300 mm): Footprint C613
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(275.3746 mm, 152.2800 mm): Footprint R804
[lib_footprint_issues]: The current configuration does not include the footprint library 'Capacitor_SMD'.
    Local override; warning
    @(109.6250 mm, 141.3250 mm): Footprint C302
[lib_footprint_issues]: The current configuration does not include the footprint library 'Fiducial'.
    Local override; warning
    @(331.7500 mm, 121.5400 mm): Footprint FID103
[lib_footprint_issues]: The current configuration does not include the footprint library 'Library'.
    Local override; warning
    @(76.8200 mm, 127.9400 mm): Footprint J408
[lib_footprint_issues]: The current configuration does not include the footprint library 'Capacitor_SMD'.
    Local override; warning
    @(212.7500 mm, 124.8750 mm): Footprint C204
[lib_footprint_issues]: The current configuration does not include the footprint library 'Capacitor_SMD'.
    Local override; warning
    @(313.7400 mm, 130.8300 mm): Footprint C616
[lib_footprint_issues]: The current configuration does not include the footprint library 'Capacitor_SMD'.
    Local override; warning
    @(97.0576 mm, 137.3124 mm): Footprint C603
[lib_footprint_issues]: The current configuration does not include the footprint library 'Diode_SMD'.
    Local override; warning
    @(238.6925 mm, 134.6800 mm): Footprint D202
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(247.5000 mm, 150.8350 mm): Footprint R501
[lib_footprint_issues]: The current configuration does not include the footprint library 'Capacitor_SMD'.
    Local override; warning
    @(191.9600 mm, 152.5400 mm): Footprint C702
[lib_footprint_issues]: The current configuration does not include the footprint library 'TestPoint'.
    Local override; warning
    @(99.2400 mm, 133.6800 mm): Footprint TP301
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(212.7500 mm, 135.3250 mm): Footprint R814
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(280.3900 mm, 152.3100 mm): Footprint R803
[lib_footprint_issues]: The current configuration does not include the footprint library 'Diode_SMD'.
    Local override; warning
    @(303.9862 mm, 163.1200 mm): Footprint D602
[lib_footprint_issues]: The current configuration does not include the footprint library 'Library'.
    Local override; warning
    @(107.5700 mm, 153.7852 mm): Footprint J402
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(212.7500 mm, 132.0250 mm): Footprint R210
[lib_footprint_issues]: The current configuration does not include the footprint library 'Package_TO_SOT_SMD'.
    Local override; warning
    @(280.6150 mm, 155.0475 mm): Footprint Q802
[lib_footprint_issues]: The current configuration does not include the footprint library 'Library'.
    Local override; warning
    @(341.9500 mm, 145.1600 mm): Footprint J604
[lib_footprint_issues]: The current configuration does not include the footprint library 'MountingHole'.
    Local override; warning
    @(202.0091 mm, 133.7628 mm): Footprint H102
[lib_footprint_issues]: The current configuration does not include the footprint library 'Capacitor_SMD'.
    Local override; warning
    @(122.2500 mm, 125.6750 mm): Footprint C305
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(177.8375 mm, 159.5382 mm): Footprint R711
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(177.8375 mm, 154.6757 mm): Footprint R705
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(241.2050 mm, 155.0100 mm): Footprint R212
[lib_footprint_issues]: The current configuration does not include the footprint library 'easyeda2kicad'.
    Local override; warning
    @(170.6800 mm, 120.4800 mm): Footprint SW201
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(273.1100 mm, 130.6300 mm): Footprint R609
[lib_footprint_issues]: The current configuration does not include the footprint library 'Connector_USB'.
    Local override; warning
    @(251.3500 mm, 160.0850 mm): Footprint J501
[lib_footprint_issues]: The current configuration does not include the footprint library 'Package_TO_SOT_SMD'.
    Local override; warning
    @(275.5746 mm, 155.0175 mm): Footprint Q801
[lib_footprint_issues]: The current configuration does not include the footprint library 'Jumper'.
    Local override; warning
    @(101.8800 mm, 126.6675 mm): Footprint J804
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(93.2700 mm, 130.8000 mm): Footprint R812
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(235.3000 mm, 134.9200 mm): Footprint R201
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(259.2250 mm, 160.3725 mm): Footprint R502
[lib_footprint_issues]: The current configuration does not include the footprint library 'easyeda2kicad'.
    Local override; warning
    @(182.3200 mm, 120.4800 mm): Footprint SW202
[lib_footprint_issues]: The current configuration does not include the footprint library 'Inductor_SMD'.
    Local override; warning
    @(288.2844 mm, 126.3250 mm): Footprint L602
[lib_footprint_issues]: The current configuration does not include the footprint library 'Connector_PinHeader_2.54mm'.
    Local override; warning
    @(126.6200 mm, 120.3000 mm): Footprint J202
[lib_footprint_issues]: The current configuration does not include the footprint library 'Capacitor_SMD'.
    Local override; warning
    @(109.6250 mm, 137.3250 mm): Footprint C604
[lib_footprint_issues]: The current configuration does not include the footprint library 'Capacitor_SMD'.
    Local override; warning
    @(311.7200 mm, 130.8300 mm): Footprint C618
[lib_footprint_issues]: The current configuration does not include the footprint library 'easyeda2kicad'.
    Local override; warning
    @(302.1300 mm, 156.1500 mm): Footprint D601
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(235.3250 mm, 128.3500 mm): Footprint R208
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(235.3200 mm, 123.6500 mm): Footprint R205
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(271.5700 mm, 130.6300 mm): Footprint R607
[lib_footprint_issues]: The current configuration does not include the footprint library 'Diode_SMD'.
    Local override; warning
    @(313.1600 mm, 133.3600 mm): Footprint D603
[lib_footprint_issues]: The current configuration does not include the footprint library 'Inductor_SMD'.
    Local override; warning
    @(321.3800 mm, 126.3200 mm): Footprint L601
[lib_footprint_issues]: The current configuration does not include the footprint library 'Connector_PinHeader_2.54mm'.
    Local override; warning
    @(144.5500 mm, 120.3000 mm): Footprint J201
[lib_footprint_issues]: The current configuration does not include the footprint library 'easyeda2kicad'.
    Local override; warning
    @(233.6600 mm, 158.7200 mm): Footprint BUZZER201
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(276.9500 mm, 134.8700 mm): Footprint R610
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(242.2050 mm, 132.4900 mm): Footprint R202
[lib_footprint_issues]: The current configuration does not include the footprint library 'Capacitor_SMD'.
    Local override; warning
    @(212.7500 mm, 126.4000 mm): Footprint C203
[lib_footprint_issues]: The current configuration does not include the footprint library 'Library'.
    Local override; warning
    @(132.8400 mm, 153.7852 mm): Footprint J401
[lib_footprint_issues]: The current configuration does not include the footprint library 'Jumper'.
    Local override; warning
    @(281.5004 mm, 159.3600 mm): Footprint J802
[lib_footprint_issues]: The current configuration does not include the footprint library 'Capacitor_THT'.
    Local override; warning
    @(333.7200 mm, 126.7400 mm): Footprint C607
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(177.8375 mm, 157.9174 mm): Footprint R709
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(278.0900 mm, 155.4850 mm): Footprint R808
[lib_footprint_issues]: The current configuration does not include the footprint library 'Library'.
    Local override; warning
    @(116.7400 mm, 146.2800 mm): Footprint J406
[lib_footprint_issues]: The current configuration does not include the footprint library 'MountingHole'.
    Local override; warning
    @(202.0091 mm, 152.5588 mm): Footprint H103
[lib_footprint_issues]: The current configuration does not include the footprint library 'Capacitor_SMD'.
    Local override; warning
    @(309.6900 mm, 130.8400 mm): Footprint C620
[lib_footprint_issues]: The current configuration does not include the footprint library 'Package_TO_SOT_SMD'.
    Local override; warning
    @(300.0000 mm, 155.0000 mm): Footprint U403
[lib_footprint_issues]: The current configuration does not include the footprint library 'Capacitor_SMD'.
    Local override; warning
    @(110.9500 mm, 123.6700 mm): Footprint C301
[lib_footprint_issues]: The current configuration does not include the footprint library 'Capacitor_SMD'.
    Local override; warning
    @(307.9200 mm, 130.6200 mm): Footprint C614
[lib_footprint_issues]: The current configuration does not include the footprint library 'Package_TO_SOT_SMD'.
    Local override; warning
    @(94.2300 mm, 127.3200 mm): Footprint Q803
[lib_footprint_issues]: The current configuration does not include the footprint library 'Package_TO_SOT_SMD'.
    Local override; warning
    @(251.3500 mm, 152.5850 mm): Footprint U501
[lib_footprint_issues]: The current configuration does not include the footprint library 'Library'.
    Local override; warning
    @(320.9100 mm, 138.8300 mm): Footprint J403
[lib_footprint_issues]: The current configuration does not include the footprint library 'Package_SO'.
    Local override; warning
    @(310.7294 mm, 126.3500 mm): Footprint U601
[lib_footprint_issues]: The current configuration does not include the footprint library 'easyeda2kicad'.
    Local override; warning
    @(338.3450 mm, 157.7325 mm): Footprint J409
[lib_footprint_issues]: The current configuration does not include the footprint library 'TestPoint'.
    Local override; warning
    @(273.8374 mm, 134.5184 mm): Footprint TP603
[lib_footprint_issues]: The current configuration does not include the footprint library 'Package_SO'.
    Local override; warning
    @(128.4500 mm, 139.3250 mm): Footprint U302
[lib_footprint_issues]: The current configuration does not include the footprint library 'TestPoint'.
    Local override; warning
    @(97.0500 mm, 133.6900 mm): Footprint TP302
[lib_footprint_issues]: The current configuration does not include the footprint library 'Capacitor_SMD'.
    Local override; warning
    @(212.5250 mm, 123.0750 mm): Footprint C205
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(177.8375 mm, 161.1591 mm): Footprint R713
[lib_footprint_issues]: The current configuration does not include the footprint library 'easyeda2kicad'.
    Local override; warning
    @(73.7600 mm, 139.4750 mm): Footprint J414
[lib_footprint_issues]: The current configuration does not include the footprint library 'Fiducial'.
    Local override; warning
    @(82.5100 mm, 151.9600 mm): Footprint FID101
[lib_footprint_issues]: The current configuration does not include the footprint library 'TestPoint'.
    Local override; warning
    @(321.6600 mm, 160.1600 mm): Footprint TP702
[lib_footprint_issues]: The current configuration does not include the footprint library 'Capacitor_THT'.
    Local override; warning
    @(301.4274 mm, 121.7422 mm): Footprint C606
[lib_footprint_issues]: The current configuration does not include the footprint library 'Diode_SMD'.
    Local override; warning
    @(311.0544 mm, 121.8000 mm): Footprint D605
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(314.6700 mm, 157.2500 mm): Footprint R737
[lib_footprint_issues]: The current configuration does not include the footprint library 'Capacitor_SMD'.
    Local override; warning
    @(273.0344 mm, 125.3250 mm): Footprint C611
[lib_footprint_issues]: The current configuration does not include the footprint library 'Package_SO'.
    Local override; warning
    @(277.8594 mm, 126.3300 mm): Footprint U602
[lib_footprint_issues]: The current configuration does not include the footprint library 'Package_SO'.
    Local override; warning
    @(116.6250 mm, 126.9750 mm): Footprint U301
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(260.0000 mm, 124.0000 mm): Footprint R213
[lib_footprint_issues]: The current configuration does not include the footprint library 'MountingHole'.
    Local override; warning
    @(71.8341 mm, 152.5588 mm): Footprint H101
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(177.8375 mm, 151.4341 mm): Footprint R701
[lib_footprint_issues]: The current configuration does not include the footprint library 'Diode_SMD'.
    Local override; warning
    @(240.9300 mm, 159.4350 mm): Footprint D204
[lib_footprint_issues]: The current configuration does not include the footprint library 'Package_SO'.
    Local override; warning
    @(194.3400 mm, 157.5300 mm): Footprint U701
[lib_footprint_issues]: The current configuration does not include the footprint library 'Connector_JST'.
    Local override; warning
    @(276.2504 mm, 160.3350 mm): Footprint J803
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(90.9628 mm, 140.6530 mm): Footprint R736
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(90.9628 mm, 139.1030 mm): Footprint R735
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(96.7700 mm, 130.8125 mm): Footprint R811
[lib_footprint_issues]: The current configuration does not include the footprint library 'Package_TO_SOT_SMD'.
    Local override; warning
    @(121.0000 mm, 160.2500 mm): Footprint Q806
[lib_footprint_issues]: The current configuration does not include the footprint library 'Package_TO_SOT_SMD'.
    Local override; warning
    @(121.0000 mm, 160.2500 mm): Footprint Q806
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(212.7500 mm, 138.6000 mm): Footprint R815
[lib_footprint_issues]: The current configuration does not include the footprint library 'TestPoint'.
    Local override; warning
    @(305.3200 mm, 149.9800 mm): Footprint TP601
[lib_footprint_issues]: The current configuration does not include the footprint library 'TestPoint'.
    Local override; warning
    @(306.8630 mm, 134.5184 mm): Footprint TP602
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(255.1750 mm, 152.4350 mm): Footprint R102
[lib_footprint_issues]: The current configuration does not include the footprint library 'Diode_SMD'.
    Local override; warning
    @(278.0594 mm, 121.8000 mm): Footprint D606
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(306.3800 mm, 130.6200 mm): Footprint R608
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(255.1750 mm, 153.9850 mm): Footprint R504
[lib_footprint_issues]: The current configuration does not include the footprint library 'Capacitor_SMD'.
    Local override; warning
    @(122.1750 mm, 137.3250 mm): Footprint C605
[lib_footprint_issues]: The current configuration does not include the footprint library 'TestPoint'.
    Local override; warning
    @(251.3300 mm, 148.9600 mm): Footprint TP501
[lib_footprint_issues]: The current configuration does not include the footprint library 'Package_TO_SOT_SMD'.
    Local override; warning
    @(97.7500 mm, 127.3300 mm): Footprint Q804
[lib_footprint_issues]: The current configuration does not include the footprint library 'Connector_PinHeader_2.54mm'.
    Local override; warning
    @(93.9400 mm, 120.3600 mm): Footprint J806
[lib_footprint_issues]: The current configuration does not include the footprint library 'Capacitor_SMD'.
    Local override; warning
    @(97.0500 mm, 141.3250 mm): Footprint C304
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(180.8875 mm, 161.1591 mm): Footprint R714
[lib_footprint_issues]: The current configuration does not include the footprint library 'Capacitor_THT'.
    Local override; warning
    @(301.5036 mm, 129.1336 mm): Footprint C612
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(247.5000 mm, 153.8850 mm): Footprint R101
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(180.8875 mm, 159.5382 mm): Footprint R712
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(180.8875 mm, 151.4341 mm): Footprint R702
[lib_footprint_issues]: The current configuration does not include the footprint library 'Capacitor_SMD'.
    Local override; warning
    @(196.7000 mm, 152.5300 mm): Footprint C701
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(93.9900 mm, 124.5575 mm): Footprint R816
[lib_footprint_issues]: The current configuration does not include the footprint library 'Library'.
    Local override; warning
    @(110.0800 mm, 146.2200 mm): Footprint J407
[lib_footprint_issues]: The current configuration does not include the footprint library 'Espressif'.
    Local override; warning
    @(224.1250 mm, 129.6750 mm): Footprint U201
[lib_footprint_issues]: The current configuration does not include the footprint library 'Fiducial'.
    Local override; warning
    @(197.9400 mm, 143.5900 mm): Footprint FID105
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(97.0450 mm, 124.5675 mm): Footprint R817
[lib_footprint_issues]: The current configuration does not include the footprint library 'Capacitor_SMD'.
    Local override; warning
    @(278.5100 mm, 130.8400 mm): Footprint C619
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(278.0900 mm, 152.4350 mm): Footprint R802
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(303.9663 mm, 161.5500 mm): Footprint R603
[lib_footprint_issues]: The current configuration does not include the footprint library 'Diode_SMD'.
    Local override; warning
    @(238.6925 mm, 136.8900 mm): Footprint D203
[lib_footprint_issues]: The current configuration does not include the footprint library 'MountingHole'.
    Local override; warning
    @(71.8341 mm, 133.7628 mm): Footprint H108
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(209.2500 mm, 135.7500 mm): Footprint R216
[lib_footprint_issues]: The current configuration does not include the footprint library 'Resistor_SMD'.
    Local override; warning
    @(209.2500 mm, 135.7500 mm): Footprint R216
[lib_footprint_issues]: The current configuration does not include the footprint library 'Package_TO_SOT_SMD'.
    Local override; warning
    @(300.0000 mm, 155.0000 mm): Footprint U403
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(62.2241 mm, 116.1117 mm): Segment on Edge.Cuts
    @(192.4100 mm, 116.3800 mm): Segment of SW203 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(62.2241 mm, 116.1117 mm): Segment on Edge.Cuts
    @(195.4900 mm, 108.9300 mm): Segment of SW203 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(343.3493 mm, 164.2140 mm): Segment on Edge.Cuts
    @(287.0250 mm, 160.9048 mm): Segment of J601 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(343.3493 mm, 164.2140 mm): Segment on Edge.Cuts
    @(287.0250 mm, 164.2048 mm): Segment of J601 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(343.3493 mm, 164.2140 mm): Segment on Edge.Cuts
    @(297.1850 mm, 164.2048 mm): Segment of J601 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(249.7100 mm, 116.1609 mm): Segment on Edge.Cuts
    @(250.7200 mm, 116.1500 mm): Segment of J801 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(249.7100 mm, 116.1609 mm): Segment on Edge.Cuts
    @(251.6700 mm, 116.1500 mm): Segment of J801 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(249.7100 mm, 116.1609 mm): Segment on Edge.Cuts
    @(251.7300 mm, 116.1500 mm): Segment of J801 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(249.7100 mm, 116.1609 mm): Segment on Edge.Cuts
    @(251.8500 mm, 116.1500 mm): Segment of J801 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(249.7100 mm, 116.1609 mm): Segment on Edge.Cuts
    @(251.9700 mm, 116.1500 mm): Segment of J801 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(249.7100 mm, 116.1609 mm): Segment on Edge.Cuts
    @(252.0900 mm, 116.1500 mm): Segment of J801 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(249.7100 mm, 116.1609 mm): Segment on Edge.Cuts
    @(252.2100 mm, 116.1500 mm): Segment of J801 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(249.7100 mm, 116.1609 mm): Segment on Edge.Cuts
    @(252.3300 mm, 116.1500 mm): Segment of J801 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(249.7100 mm, 116.1609 mm): Segment on Edge.Cuts
    @(252.4300 mm, 110.1500 mm): Segment of J801 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(249.7100 mm, 116.1609 mm): Segment on Edge.Cuts
    @(253.3200 mm, 118.8100 mm): Segment of J801 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(249.7100 mm, 116.1609 mm): Segment on Edge.Cuts
    @(254.2100 mm, 116.1500 mm): Segment of J801 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(249.7100 mm, 116.1609 mm): Segment on Edge.Cuts
    @(254.9700 mm, 110.1500 mm): Segment of J801 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(249.7100 mm, 116.1609 mm): Segment on Edge.Cuts
    @(255.8600 mm, 118.8100 mm): Segment of J801 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(249.7100 mm, 116.1609 mm): Segment on Edge.Cuts
    @(256.7500 mm, 116.1500 mm): Segment of J801 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(249.7100 mm, 116.1609 mm): Segment on Edge.Cuts
    @(257.5100 mm, 110.1500 mm): Segment of J801 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(249.7100 mm, 116.1609 mm): Segment on Edge.Cuts
    @(258.4000 mm, 118.8100 mm): Segment of J801 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(249.7100 mm, 116.1609 mm): Segment on Edge.Cuts
    @(259.2900 mm, 116.1500 mm): Segment of J801 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(249.7100 mm, 116.1609 mm): Segment on Edge.Cuts
    @(260.0500 mm, 110.1500 mm): Segment of J801 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(249.7100 mm, 116.1609 mm): Segment on Edge.Cuts
    @(261.0000 mm, 116.1500 mm): Segment of J801 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(249.7100 mm, 116.1609 mm): Segment on Edge.Cuts
    @(261.0000 mm, 118.8100 mm): Segment of J801 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(62.2241 mm, 116.1117 mm): Segment on Edge.Cuts
    @(169.1300 mm, 116.3800 mm): Segment of SW201 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(62.2241 mm, 116.1117 mm): Segment on Edge.Cuts
    @(172.2100 mm, 108.9300 mm): Segment of SW201 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(62.2241 mm, 116.1117 mm): Segment on Edge.Cuts
    @(180.7700 mm, 116.3800 mm): Segment of SW202 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(62.2241 mm, 116.1117 mm): Segment on Edge.Cuts
    @(183.8500 mm, 108.9300 mm): Segment of SW202 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(62.2241 mm, 116.1117 mm): Segment on Edge.Cuts
    @(126.2400 mm, 116.2000 mm): Segment of J202 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(62.2241 mm, 116.1117 mm): Segment on Edge.Cuts
    @(126.3000 mm, 116.2000 mm): Segment of J202 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(62.2241 mm, 116.1117 mm): Segment on Edge.Cuts
    @(126.4200 mm, 116.2000 mm): Segment of J202 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(62.2241 mm, 116.1117 mm): Segment on Edge.Cuts
    @(126.5400 mm, 116.2000 mm): Segment of J202 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(62.2241 mm, 116.1117 mm): Segment on Edge.Cuts
    @(126.6600 mm, 116.2000 mm): Segment of J202 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(62.2241 mm, 116.1117 mm): Segment on Edge.Cuts
    @(126.7800 mm, 116.2000 mm): Segment of J202 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(62.2241 mm, 116.1117 mm): Segment on Edge.Cuts
    @(126.9000 mm, 116.2000 mm): Segment of J202 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(62.2241 mm, 116.1117 mm): Segment on Edge.Cuts
    @(127.0000 mm, 110.2000 mm): Segment of J202 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(62.2241 mm, 116.1117 mm): Segment on Edge.Cuts
    @(128.7800 mm, 116.2000 mm): Segment of J202 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(62.2241 mm, 116.1117 mm): Segment on Edge.Cuts
    @(129.5400 mm, 110.2000 mm): Segment of J202 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(62.2241 mm, 116.1117 mm): Segment on Edge.Cuts
    @(131.3200 mm, 116.2000 mm): Segment of J202 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(62.2241 mm, 116.1117 mm): Segment on Edge.Cuts
    @(132.0800 mm, 110.2000 mm): Segment of J202 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(62.2241 mm, 116.1117 mm): Segment on Edge.Cuts
    @(133.8600 mm, 116.2000 mm): Segment of J202 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(62.2241 mm, 116.1117 mm): Segment on Edge.Cuts
    @(134.6200 mm, 110.2000 mm): Segment of J202 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(62.2241 mm, 116.1117 mm): Segment on Edge.Cuts
    @(144.1700 mm, 116.2000 mm): Segment of J201 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(62.2241 mm, 116.1117 mm): Segment on Edge.Cuts
    @(144.2300 mm, 116.2000 mm): Segment of J201 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(62.2241 mm, 116.1117 mm): Segment on Edge.Cuts
    @(144.3500 mm, 116.2000 mm): Segment of J201 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(62.2241 mm, 116.1117 mm): Segment on Edge.Cuts
    @(144.4700 mm, 116.2000 mm): Segment of J201 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(62.2241 mm, 116.1117 mm): Segment on Edge.Cuts
    @(144.5900 mm, 116.2000 mm): Segment of J201 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(62.2241 mm, 116.1117 mm): Segment on Edge.Cuts
    @(144.7100 mm, 116.2000 mm): Segment of J201 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(62.2241 mm, 116.1117 mm): Segment on Edge.Cuts
    @(144.8300 mm, 116.2000 mm): Segment of J201 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(62.2241 mm, 116.1117 mm): Segment on Edge.Cuts
    @(144.9300 mm, 110.2000 mm): Segment of J201 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(62.2241 mm, 116.1117 mm): Segment on Edge.Cuts
    @(146.7100 mm, 116.2000 mm): Segment of J201 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(62.2241 mm, 116.1117 mm): Segment on Edge.Cuts
    @(147.4700 mm, 110.2000 mm): Segment of J201 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(62.2241 mm, 116.1117 mm): Segment on Edge.Cuts
    @(149.2500 mm, 116.2000 mm): Segment of J201 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(62.2241 mm, 116.1117 mm): Segment on Edge.Cuts
    @(150.0100 mm, 110.2000 mm): Segment of J201 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(62.2241 mm, 116.1117 mm): Segment on Edge.Cuts
    @(151.7900 mm, 116.2000 mm): Segment of J201 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(62.2241 mm, 116.1117 mm): Segment on Edge.Cuts
    @(152.5500 mm, 110.2000 mm): Segment of J201 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(62.2241 mm, 116.1117 mm): Segment on Edge.Cuts
    @(93.5600 mm, 116.2600 mm): Segment of J806 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(62.2241 mm, 116.1117 mm): Segment on Edge.Cuts
    @(93.6200 mm, 116.2600 mm): Segment of J806 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(62.2241 mm, 116.1117 mm): Segment on Edge.Cuts
    @(93.7400 mm, 116.2600 mm): Segment of J806 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(62.2241 mm, 116.1117 mm): Segment on Edge.Cuts
    @(93.8600 mm, 116.2600 mm): Segment of J806 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(62.2241 mm, 116.1117 mm): Segment on Edge.Cuts
    @(93.9800 mm, 116.2600 mm): Segment of J806 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(62.2241 mm, 116.1117 mm): Segment on Edge.Cuts
    @(94.1000 mm, 116.2600 mm): Segment of J806 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(62.2241 mm, 116.1117 mm): Segment on Edge.Cuts
    @(94.2200 mm, 116.2600 mm): Segment of J806 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(62.2241 mm, 116.1117 mm): Segment on Edge.Cuts
    @(94.3200 mm, 110.2600 mm): Segment of J806 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(62.2241 mm, 116.1117 mm): Segment on Edge.Cuts
    @(96.1000 mm, 116.2600 mm): Segment of J806 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(62.2241 mm, 116.1117 mm): Segment on Edge.Cuts
    @(96.8600 mm, 110.2600 mm): Segment of J806 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(62.2241 mm, 116.1117 mm): Segment on Edge.Cuts
    @(98.6400 mm, 116.2600 mm): Segment of J806 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(62.2241 mm, 116.1117 mm): Segment on Edge.Cuts
    @(99.4000 mm, 110.2600 mm): Segment of J806 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(62.2241 mm, 116.1117 mm): Segment on Edge.Cuts
    @(101.1800 mm, 116.2600 mm): Segment of J806 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(62.2241 mm, 116.1117 mm): Segment on Edge.Cuts
    @(101.9400 mm, 110.2600 mm): Segment of J806 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(201.5727 mm, 121.6791 mm): Segment on Edge.Cuts
    @(216.4250 mm, 116.8750 mm): Segment of U201 on F.Silkscreen
[silk_edge_clearance]: Silkscreen clipped by board edge
    Rule: board setup constraints silk; warning
    @(201.5727 mm, 121.6791 mm): Segment on Edge.Cuts
    @(231.8250 mm, 116.8750 mm): Segment of U201 on F.Silkscreen
[via_dangling]: Via is not connected or connected on only one layer
    Local override; warning
    @(207.0000 mm, 163.1000 mm): Via [+12V] on F.Cu - B.Cu
[track_dangling]: Track has unconnected end
    Local override; warning
    @(217.6700 mm, 136.0557 mm): Track [/ESP32/EOL_R_N] on B.Cu, length 3.7557 mm
[via_dangling]: Via is not connected or connected on only one layer
    Local override; warning
    @(206.0750 mm, 135.7500 mm): Via [/ESP32/MACHINE_PWR_SENSE] on F.Cu - B.Cu
[via_dangling]: Via is not connected or connected on only one layer
    Local override; warning
    @(205.4250 mm, 135.7500 mm): Via [/ESP32/MACHINE_PWR_SENSE] on F.Cu - B.Cu
[track_dangling]: Track has unconnected end
    Local override; warning
    @(213.2500 mm, 138.5000 mm): Track [/ESP32/MACHINE_PWR_SENSE] on In2.Cu, length 0.3400 mm

** Found 2 unconnected pads **
[unconnected_items]: Missing connection between items
    Local override; error
    @(210.0750 mm, 135.7500 mm): Pad 1 [/ESP32/MACHINE_PWR_SENSE] of R216 on B.Cu
    @(207.0000 mm, 163.1000 mm): Via [+12V] on F.Cu - B.Cu
[unconnected_items]: Missing connection between items
    Local override; error
    @(217.1250 mm, 129.6750 mm): Pad 8 [/ESP32/MACHINE_PWR_SENSE] of U201 on F.Cu
    @(206.0000 mm, 134.7500 mm): Track [/ESP32/MACHINE_PWR_SENSE] on B.Cu, length 3.5000 mm

** Found 0 Footprint errors **

** End of Report **
```
