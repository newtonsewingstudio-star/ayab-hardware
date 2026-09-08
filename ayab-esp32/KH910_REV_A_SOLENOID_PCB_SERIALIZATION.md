# KH910 Rev A — Solenoid PCB Serialization Isolation

Each staged board is temporary. No staged PCB is committed by this workflow.

## Structural metadata
```text
00_original.kicad_pcb: bytes=4147073 depth=0 min_depth=0 in_string=False
10_netdefs_rename.kicad_pcb: bytes=4147166 depth=0 min_depth=0 in_string=False
20_migration_only.kicad_pcb: bytes=4146265 depth=0 min_depth=0 in_string=False
30_with_footprints.kicad_pcb: bytes=4166803 depth=0 min_depth=0 in_string=False
40_full.kicad_pcb: bytes=4173384 depth=0 min_depth=0 in_string=False

root tokens full:
version
generator
general
paper
layers
setup
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
net
```

## KiCad load probes

### 00_original.kicad_pcb
- exit: 0
- parser: **LOADED**
```text
Found 731 violations
Found 0 unconnected items
Saved DRC Report to /tmp/00_original.kicad_pcb.rpt

--- report excerpt ---
** Drc report for 00_original.kicad_pcb **
** Created on 2026-09-08T23:56:09+0000 **
** Report includes: Errors, Warnings **

** Found 731 DRC violations **
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
    @(219.5500 mm, 134.1300 mm): Via [/ESP32/EOL_L_P] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(218.8000 mm, 134.1300 mm): Via [/ESP32/EOL_L_N] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(206.3600 mm, 131.9300 mm): Via [/ESP32/EOL_R_P] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(207.4900 mm, 131.9700 mm): Via [/ESP32/EOL_R_N] on F.Cu - B.Cu
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
    @(239.2200 mm, 149.8600 mm): Via [/BROTHER-CONNECTORS/EOL_R_N] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(239.2200 mm, 145.6500 mm): Via [/BROTHER-CONNECTORS/EOL_R_N] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(238.4500 mm, 145.6300 mm): Via [/BROTHER-CONNECTORS/EOL_R_S] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(238.4300 mm, 150.4200 mm): Via [/BROTHER-CONNECTORS/EOL_R_S] on F.Cu - B.Cu
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
    @(220.9700 mm, 134.1500 mm): Via [/ESP32/ESP17] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(221.6700 mm, 134.1400 mm): Via [/ESP32/ESP18] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(222.3000 mm, 134.1200 mm): Via [/ESP32/ESP21] on F.Cu - B.Cu
[starved_thermal]: Thermal relief connection to zone incomplete (layer F.Cu; zone min spoke count 2; actual 1)
    Local override; error
    @(312.6794 mm, 124.0250 mm): Zone [GND] on F.Cu, priority 5
    @(309.6900 mm, 129.8900 mm): Pad 2 [GND] of C620 on F.Cu
[starved_thermal]: Thermal relief connection to zone incomplete (layer F.Cu; zone min spoke count 2; actual 1)
    Local override; error
    @(307.5294 mm, 130.6000 mm): Zone [/PSU/5V_SW] on F.Cu, priority 5
    @(306.3800 mm, 131.4450 mm): Pad 2 [/PSU/5V_SW] of R608 on F.Cu
[starved_thermal]: Thermal relief connection to zone incomplete (layer B.Cu; 1 spokes connected to isolated island)
    Local override; error
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
    @(76.8200 mm, 127.9400 mm): PTH pad 2 [GND] of J408
[starved_thermal]: Thermal relief connection to zone incomplete (layer F.Cu; zone min spoke count 2; actual 1)
    Local override; error
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
    @(280.7775 mm, 133.3400 mm): Pad 1 [GND] of D604 on F.Cu
[starved_thermal]: Thermal relief connection to zone incomplete (layer F.Cu; zone min spoke count 2; actual 1)
    Local override; error
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
    @(177.0125 mm, 156.2966 mm): Pad 2 [GND] of R707 on F.Cu
[starved_thermal]: Thermal relief connection to zone incomplete (layer F.Cu; zone min spoke count 2; actual 1)
    Local override; error
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
    @(91.7878 mm, 128.4780 mm): Pad 2 [GND] of R724 on F.Cu
[starved_thermal]: Thermal relief connection to zone incomplete (layer F.Cu; zone min spoke count 2; actual 1)
    Local override; error
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
    @(211.5750 mm, 123.0750 mm): Pad 2 [GND] of C205 on F.Cu
[starved_thermal]: Thermal relief connection to zone incomplete (layer F.Cu; zone min spoke count 2; actual 1)
    Local override; error
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
    @(314.6700 mm, 158.0750 mm): Pad 2 [GND] of R732 on F.Cu
```

### 10_netdefs_rename.kicad_pcb
- exit: 0
- parser: **LOADED**
```text
Found 731 violations
Found 0 unconnected items
Saved DRC Report to /tmp/10_netdefs_rename.kicad_pcb.rpt

--- report excerpt ---
** Drc report for 10_netdefs_rename.kicad_pcb **
** Created on 2026-09-08T23:56:10+0000 **
** Report includes: Errors, Warnings **

** Found 731 DRC violations **
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
    @(219.5500 mm, 134.1300 mm): Via [/ESP32/EOL_L_P] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(218.8000 mm, 134.1300 mm): Via [/ESP32/EOL_L_N] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(206.3600 mm, 131.9300 mm): Via [/ESP32/EOL_R_P] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(207.4900 mm, 131.9700 mm): Via [/ESP32/EOL_R_N] on F.Cu - B.Cu
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
    @(239.2200 mm, 149.8600 mm): Via [/BROTHER-CONNECTORS/EOL_R_N] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(239.2200 mm, 145.6500 mm): Via [/BROTHER-CONNECTORS/EOL_R_N] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(238.4500 mm, 145.6300 mm): Via [/BROTHER-CONNECTORS/EOL_R_S] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(238.4300 mm, 150.4200 mm): Via [/BROTHER-CONNECTORS/EOL_R_S] on F.Cu - B.Cu
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
    @(220.9700 mm, 134.1500 mm): Via [/ESP32/ESP17] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(221.6700 mm, 134.1400 mm): Via [/ESP32/ESP18] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(222.3000 mm, 134.1200 mm): Via [SOLENOID_PWR_EN] on F.Cu - B.Cu
[starved_thermal]: Thermal relief connection to zone incomplete (layer F.Cu; zone min spoke count 2; actual 1)
    Local override; error
    @(312.6794 mm, 124.0250 mm): Zone [GND] on F.Cu, priority 5
    @(309.6900 mm, 129.8900 mm): Pad 2 [GND] of C620 on F.Cu
[starved_thermal]: Thermal relief connection to zone incomplete (layer F.Cu; zone min spoke count 2; actual 1)
    Local override; error
    @(307.5294 mm, 130.6000 mm): Zone [/PSU/5V_SW] on F.Cu, priority 5
    @(306.3800 mm, 131.4450 mm): Pad 2 [/PSU/5V_SW] of R608 on F.Cu
[starved_thermal]: Thermal relief connection to zone incomplete (layer B.Cu; 1 spokes connected to isolated island)
    Local override; error
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
    @(76.8200 mm, 127.9400 mm): PTH pad 2 [GND] of J408
[starved_thermal]: Thermal relief connection to zone incomplete (layer F.Cu; zone min spoke count 2; actual 1)
    Local override; error
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
    @(280.7775 mm, 133.3400 mm): Pad 1 [GND] of D604 on F.Cu
[starved_thermal]: Thermal relief connection to zone incomplete (layer F.Cu; zone min spoke count 2; actual 1)
    Local override; error
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
    @(177.0125 mm, 156.2966 mm): Pad 2 [GND] of R707 on F.Cu
[starved_thermal]: Thermal relief connection to zone incomplete (layer F.Cu; zone min spoke count 2; actual 1)
    Local override; error
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
    @(91.7878 mm, 128.4780 mm): Pad 2 [GND] of R724 on F.Cu
[starved_thermal]: Thermal relief connection to zone incomplete (layer F.Cu; zone min spoke count 2; actual 1)
    Local override; error
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
    @(211.5750 mm, 123.0750 mm): Pad 2 [GND] of C205 on F.Cu
[starved_thermal]: Thermal relief connection to zone incomplete (layer F.Cu; zone min spoke count 2; actual 1)
    Local override; error
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
    @(314.6700 mm, 158.0750 mm): Pad 2 [GND] of R732 on F.Cu
```

### 20_migration_only.kicad_pcb
- exit: 0
- parser: **LOADED**
```text
Found 753 violations
Found 13 unconnected items
Saved DRC Report to /tmp/20_migration_only.kicad_pcb.rpt

--- report excerpt ---
** Drc report for 20_migration_only.kicad_pcb **
** Created on 2026-09-08T23:56:12+0000 **
** Report includes: Errors, Warnings **

** Found 753 DRC violations **
[solder_mask_bridge]: Front solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(97.0500 mm, 140.3750 mm): Track [+12V] on F.Cu, length 1.4474 mm
    @(97.0500 mm, 140.3750 mm): Pad 1 [SOLENOID_12V_SW] of C304 on F.Cu
[solder_mask_bridge]: Front solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(122.1750 mm, 140.3750 mm): Track [+12V] on F.Cu, length 1.0400 mm
    @(122.1750 mm, 140.3750 mm): Pad 1 [SOLENOID_12V_SW] of C303 on F.Cu
[solder_mask_bridge]: Front solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(109.6250 mm, 140.3750 mm): Track [+12V] on F.Cu, length 0.8900 mm
    @(109.6250 mm, 140.3750 mm): Pad 1 [SOLENOID_12V_SW] of C302 on F.Cu
[solder_mask_bridge]: Front solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(124.0050 mm, 141.8000 mm): Track [+12V] on F.Cu, length 2.3450 mm
    @(124.0050 mm, 141.8000 mm): Pad 9 [SOLENOID_12V_SW] of U302 on F.Cu
[solder_mask_bridge]: Front solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(98.9050 mm, 141.8000 mm): Track [+12V] on F.Cu, length 2.2650 mm
    @(98.9050 mm, 141.8000 mm): Pad 9 [SOLENOID_12V_SW] of U304 on F.Cu
[solder_mask_bridge]: Front solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(111.4550 mm, 141.8000 mm): Track [+12V] on F.Cu, length 2.4250 mm
    @(111.4550 mm, 141.8000 mm): Pad 9 [SOLENOID_12V_SW] of U303 on F.Cu
[solder_mask_bridge]: Rear solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(312.4500 mm, 141.8500 mm): Track [+12V] on B.Cu, length 2.1779 mm
    @(310.9100 mm, 138.8300 mm): PTH pad 9 [SOLENOID_12V_SW] of J403
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
    @(219.5500 mm, 134.1300 mm): Via [/ESP32/EOL_L_P] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(218.8000 mm, 134.1300 mm): Via [/ESP32/EOL_L_N] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(206.3600 mm, 131.9300 mm): Via [/ESP32/EOL_R_P] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(207.4900 mm, 131.9700 mm): Via [/ESP32/EOL_R_N] on F.Cu - B.Cu
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
    @(239.2200 mm, 149.8600 mm): Via [/BROTHER-CONNECTORS/EOL_R_N] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(239.2200 mm, 145.6500 mm): Via [/BROTHER-CONNECTORS/EOL_R_N] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(238.4500 mm, 145.6300 mm): Via [/BROTHER-CONNECTORS/EOL_R_S] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(238.4300 mm, 150.4200 mm): Via [/BROTHER-CONNECTORS/EOL_R_S] on F.Cu - B.Cu
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
    @(220.9700 mm, 134.1500 mm): Via [/ESP32/ESP17] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(221.6700 mm, 134.1400 mm): Via [/ESP32/ESP18] on F.Cu - B.Cu
[via_diameter]: Via diameter (board setup constraints min diameter 0.5000 mm; actual 0.4500 mm)
    Rule: netclass 'Default'; error
    @(222.3000 mm, 134.1200 mm): Via [SOLENOID_PWR_EN] on F.Cu - B.Cu
[starved_thermal]: Thermal relief connection to zone incomplete (layer F.Cu; zone min spoke count 2; actual 1)
    Local override; error
    @(307.5294 mm, 130.6000 mm): Zone [/PSU/5V_SW] on F.Cu, priority 5
    @(306.3800 mm, 131.4450 mm): Pad 2 [/PSU/5V_SW] of R608 on F.Cu
```

### 30_with_footprints.kicad_pcb
- exit: 0
- parser: **LOADED**
```text
Found 813 violations
Found 22 unconnected items
Saved DRC Report to /tmp/30_with_footprints.kicad_pcb.rpt

--- report excerpt ---
** Drc report for 30_with_footprints.kicad_pcb **
** Created on 2026-09-08T23:56:14+0000 **
** Report includes: Errors, Warnings **

** Found 813 DRC violations **
[solder_mask_bridge]: Front solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(300.8600 mm, 153.3300 mm): Track [GND] on F.Cu, length 2.2500 mm
    @(301.8250 mm, 150.9380 mm): Pad 1 [+12V] of R820 on F.Cu
[solder_mask_bridge]: Front solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(300.8600 mm, 153.3300 mm): Track [GND] on F.Cu, length 2.2500 mm
    @(301.0000 mm, 150.9375 mm): Pad 3 [SOLENOID_12V_SW] of Q805 on F.Cu
[solder_mask_bridge]: Front solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(300.8600 mm, 153.3300 mm): Track [GND] on F.Cu, length 2.2500 mm
    @(300.1750 mm, 150.9380 mm): Pad 2 [Net-(Q805-G)] of R820 on F.Cu
[solder_mask_bridge]: Front solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(300.8600 mm, 151.0800 mm): Track [GND] on F.Cu, length 0.8202 mm
    @(301.8250 mm, 150.9380 mm): Pad 1 [+12V] of R820 on F.Cu
[solder_mask_bridge]: Front solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(300.8600 mm, 151.0800 mm): Track [GND] on F.Cu, length 0.8202 mm
    @(301.0000 mm, 150.9375 mm): Pad 3 [SOLENOID_12V_SW] of Q805 on F.Cu
[solder_mask_bridge]: Front solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(300.8600 mm, 151.0800 mm): Track [GND] on F.Cu, length 0.8202 mm
    @(300.1750 mm, 150.9380 mm): Pad 2 [Net-(Q805-G)] of R820 on F.Cu
[solder_mask_bridge]: Front solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(299.7100 mm, 149.4200 mm): Via [GND] on F.Cu - B.Cu
    @(300.0500 mm, 149.0625 mm): Pad 2 [+12V] of Q805 on F.Cu
[solder_mask_bridge]: Front solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(300.2800 mm, 150.5000 mm): Via [GND] on F.Cu - B.Cu
    @(300.1750 mm, 150.9380 mm): Pad 2 [Net-(Q805-G)] of R820 on F.Cu
[solder_mask_bridge]: Front solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(302.4300 mm, 149.4200 mm): Via [GND] on F.Cu - B.Cu
    @(301.9500 mm, 149.0625 mm): Pad 1 [Net-(Q805-G)] of Q805 on F.Cu
[solder_mask_bridge]: Front solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(301.6400 mm, 150.5000 mm): Via [GND] on F.Cu - B.Cu
    @(301.8250 mm, 150.9380 mm): Pad 1 [+12V] of R820 on F.Cu
[solder_mask_bridge]: Front solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(301.6400 mm, 150.5000 mm): Via [GND] on F.Cu - B.Cu
    @(301.0000 mm, 150.9375 mm): Pad 3 [SOLENOID_12V_SW] of Q805 on F.Cu
[solder_mask_bridge]: Front solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(298.9200 mm, 150.5000 mm): Via [GND] on F.Cu - B.Cu
    @(298.4375 mm, 151.0000 mm): Pad 3 [Net-(Q805-G)] of Q806 on F.Cu
[solder_mask_bridge]: Front solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(97.0500 mm, 140.3750 mm): Track [+12V] on F.Cu, length 1.4474 mm
    @(97.0500 mm, 140.3750 mm): Pad 1 [SOLENOID_12V_SW] of C304 on F.Cu
[solder_mask_bridge]: Front solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(122.1750 mm, 140.3750 mm): Track [+12V] on F.Cu, length 1.0400 mm
    @(122.1750 mm, 140.3750 mm): Pad 1 [SOLENOID_12V_SW] of C303 on F.Cu
[solder_mask_bridge]: Front solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(109.6250 mm, 140.3750 mm): Track [+12V] on F.Cu, length 0.8900 mm
    @(109.6250 mm, 140.3750 mm): Pad 1 [SOLENOID_12V_SW] of C302 on F.Cu
[solder_mask_bridge]: Front solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(124.0050 mm, 141.8000 mm): Track [+12V] on F.Cu, length 2.3450 mm
    @(124.0050 mm, 141.8000 mm): Pad 9 [SOLENOID_12V_SW] of U302 on F.Cu
[solder_mask_bridge]: Front solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(98.9050 mm, 141.8000 mm): Track [+12V] on F.Cu, length 2.2650 mm
    @(98.9050 mm, 141.8000 mm): Pad 9 [SOLENOID_12V_SW] of U304 on F.Cu
[solder_mask_bridge]: Front solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(111.4550 mm, 141.8000 mm): Track [+12V] on F.Cu, length 2.4250 mm
    @(111.4550 mm, 141.8000 mm): Pad 9 [SOLENOID_12V_SW] of U303 on F.Cu
[solder_mask_bridge]: Rear solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(312.4500 mm, 141.8500 mm): Track [+12V] on B.Cu, length 2.1779 mm
    @(310.9100 mm, 138.8300 mm): PTH pad 9 [SOLENOID_12V_SW] of J403
[solder_mask_bridge]: Front solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(304.4500 mm, 147.0200 mm): Track [/BROTHER-CONNECTORS/EOL_R_S] on F.Cu, length 26.6700 mm
    @(299.2000 mm, 146.8000 mm): Pad 1 [SOLENOID_12V_SW] of TP703 on F.Cu
[solder_mask_bridge]: Front solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(297.6050 mm, 153.0348 mm): Pad 3 [/PSU/INP_2] of J601 on F.Cu
    @(296.5625 mm, 151.9500 mm): Pad 2 [GND] of Q806 on F.Cu
[solder_mask_bridge]: Front solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(301.9500 mm, 149.0625 mm): Pad 1 [Net-(Q805-G)] of Q805 on F.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[solder_mask_bridge]: Front solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(300.0500 mm, 149.0625 mm): Pad 2 [+12V] of Q805 on F.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[solder_mask_bridge]: Front solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(301.0000 mm, 150.9375 mm): Pad 3 [SOLENOID_12V_SW] of Q805 on F.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[solder_mask_bridge]: Front solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(296.5625 mm, 150.0500 mm): Pad 1 [Net-(Q806-G)] of Q806 on F.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[solder_mask_bridge]: Front solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(298.4375 mm, 151.0000 mm): Pad 3 [Net-(Q805-G)] of Q806 on F.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[solder_mask_bridge]: Front solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(301.8250 mm, 150.9380 mm): Pad 1 [+12V] of R820 on F.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[solder_mask_bridge]: Front solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(300.1750 mm, 150.9380 mm): Pad 2 [Net-(Q805-G)] of R820 on F.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[solder_mask_bridge]: Front solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(293.7750 mm, 150.0500 mm): Pad 1 [SOLENOID_PWR_EN] of R821 on F.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[solder_mask_bridge]: Front solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(295.4250 mm, 150.0500 mm): Pad 2 [Net-(Q806-G)] of R821 on F.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[solder_mask_bridge]: Front solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(292.8250 mm, 153.0000 mm): Pad 2 [Net-(Q806-G)] of R822 on F.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[solder_mask_bridge]: Front solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(299.2000 mm, 146.8000 mm): Pad 1 [SOLENOID_12V_SW] of TP703 on F.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
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
    @(219.5500 mm, 134.1300 mm): Via [/ESP32/EOL_L_P] on F.Cu - B.Cu
```

### 40_full.kicad_pcb
- exit: 3
- parser: **FAILED TO LOAD**
```text
Failed to load board
```
