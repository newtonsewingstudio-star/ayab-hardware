# KH910 Rev A — Hall / Comparator PCB Parity Audit

Generated read-only from the current repository PCB using KiCad `pcbnew`.

- Board footprints: **236**
- Board nets: **153**
- Obsolete comparator footprints still present: **0/24**
- New Hall-divider footprints present: **4/4**

## Required parity summary

- C703: absent
- C704: absent
- R715: absent
- R716: absent
- R717: absent
- R718: absent
- R719: absent
- R720: absent
- R721: absent
- R722: absent
- R723: absent
- R724: absent
- R725: absent
- R726: absent
- R727: absent
- R728: absent
- R729: absent
- R730: absent
- R731: absent
- R732: absent
- R733: absent
- R734: absent
- U702: absent
- U703: absent
- R735: PRESENT
- R736: PRESENT
- R737: PRESENT
- R738: PRESENT

## Interesting footprints and pads

### J408 — 910.950 EOL L
- footprint at: (76.820, 127.940) rot 180.0
- pad 1: (79.320, 127.940) net `+5V` (#5)
- pad 2: (76.820, 127.940) net `GND` (#2)
- pad 3: (74.320, 127.940) net `/BROTHER-CONNECTORS/EOL_L` (#63)

### J409 — 930.940 EOL R
- footprint at: (338.345, 157.732) rot 0.0
- pad 1: (340.885, 157.732) net `+5V` (#5)
- pad 2: (338.345, 157.732) net `GND` (#2)
- pad 3: (335.805, 157.732) net `/BROTHER-CONNECTORS/EOL_R` (#64)

### J411 — 900.965 EOL L
- footprint at: (72.760, 146.450) rot 0.0
- pad 1: (74.760, 146.450) net `+5V` (#5)
- pad 2: (72.760, 146.450) net `GND` (#2)
- pad 3: (70.760, 146.450) net `/BROTHER-CONNECTORS/EOL_L` (#63)

### J412 — 900.965 EOL R
- footprint at: (339.359, 152.034) rot 0.0
- pad 1: (341.359, 152.034) net `+5V` (#5)
- pad 2: (339.359, 152.034) net `GND` (#2)
- pad 3: (337.359, 152.034) net `/BROTHER-CONNECTORS/EOL_R` (#64)

### J414 — 930.940 EOL L
- footprint at: (73.760, 139.475) rot 0.0
- pad 1: (76.300, 139.475) net `+5V` (#5)
- pad 2: (73.760, 139.475) net `GND` (#2)
- pad 3: (71.220, 139.475) net `/BROTHER-CONNECTORS/EOL_L` (#63)

### R735 — 10k
- footprint at: (90.963, 139.103) rot 0.0
- pad 1: (90.138, 139.103) net `/BROTHER-CONNECTORS/EOL_L` (#63)
- pad 2: (91.788, 139.103) net `/ESP32/HALL_L_ADC` (#143)

### R736 — 10k
- footprint at: (90.963, 140.653) rot 180.0
- pad 1: (91.788, 140.653) net `/ESP32/HALL_L_ADC` (#143)
- pad 2: (90.138, 140.653) net `GND` (#2)

### R737 — 10k
- footprint at: (314.670, 157.250) rot -90.0
- pad 1: (314.670, 156.425) net `/BROTHER-CONNECTORS/EOL_R` (#64)
- pad 2: (314.670, 158.075) net `/ESP32/HALL_R_ADC` (#144)

### R738 — 10k
- footprint at: (313.120, 157.250) rot 90.0
- pad 1: (313.120, 158.075) net `/ESP32/HALL_R_ADC` (#144)
- pad 2: (313.120, 156.425) net `GND` (#2)

### TP701 — HALL-L-RAW
- footprint at: (85.390, 135.000) rot 0.0
- pad 1: (85.390, 135.000) net `/BROTHER-CONNECTORS/EOL_L` (#63)

### TP702 — HALL-R-RAW
- footprint at: (321.660, 160.160) rot 0.0
- pad 1: (321.660, 160.160) net `/BROTHER-CONNECTORS/EOL_R` (#64)

### U201 — ESP32-S3-MINI-1
- footprint at: (224.125, 129.675) rot 0.0
- pad 5: (217.125, 127.125) net `/ESP32/HALL_L_ADC` (#143)
- pad 6: (217.125, 127.975) net `/ESP32/HALL_R_ADC` (#144)
- pad 17: (219.025, 136.675) net `/AUX-CONNECTORS/AYAB_SCK` (#80)
- pad 18: (219.875, 136.675) net `/ESP32/FRONT_PANEL_AUX` (#109)

### U701 — SN74LVC4245
- footprint at: (194.340, 157.530) rot 0.0
- pad 1: (191.477, 153.955) net `+5V` (#5)
- pad 2: (191.477, 154.605) net `+5V` (#5)
- pad 3: (191.477, 155.255) net `/BROTHER-CONNECTORS/ENC_V1` (#66)
- pad 4: (191.477, 155.905) net `/BROTHER-CONNECTORS/ENC_V2` (#65)
- pad 5: (191.477, 156.555) net `/BROTHER-CONNECTORS/ENC_BELTPHASE` (#67)
- pad 6: (191.477, 157.205) net `Net-(J702-Pin_4)` (#37)
- pad 7: (191.477, 157.855) net `Net-(J702-Pin_5)` (#38)
- pad 8: (191.477, 158.505) net `Net-(J702-Pin_6)` (#145)
- pad 9: (191.477, 159.155) net `Net-(J702-Pin_7)` (#146)
- pad 10: (191.477, 159.805) net `Net-(J702-Pin_8)` (#71)
- pad 11: (191.477, 160.455) net `GND` (#2)
- pad 12: (191.477, 161.105) net `GND` (#2)
- pad 13: (197.202, 161.105) net `GND` (#2)
- pad 14: (197.202, 160.455) net `Net-(J701-Pin_8)` (#68)
- pad 15: (197.202, 159.805) net `Net-(J701-Pin_7)` (#30)
- pad 16: (197.202, 159.155) net `Net-(J701-Pin_6)` (#29)
- pad 17: (197.202, 158.505) net `Net-(J701-Pin_5)` (#27)
- pad 18: (197.202, 157.855) net `Net-(J701-Pin_4)` (#26)
- pad 19: (197.202, 157.205) net `/ESP32/ENC_BP` (#33)
- pad 20: (197.202, 156.555) net `/ESP32/ENC_B` (#32)
- pad 21: (197.202, 155.905) net `/ESP32/ENC_A` (#31)
- pad 22: (197.202, 155.255) net `GND` (#2)
- pad 23: (197.202, 154.605) net `+3V3` (#6)
- pad 24: (197.202, 153.955) net `+3V3` (#6)

## Hall-related board nets

- net 63: `/BROTHER-CONNECTORS/EOL_L`
- net 64: `/BROTHER-CONNECTORS/EOL_R`
- net 69: `/BROTHER-CONNECTORS/EOL_R_N`
- net 70: `/BROTHER-CONNECTORS/EOL_R_S`
- net 143: `/ESP32/HALL_L_ADC`
- net 144: `/ESP32/HALL_R_ADC`

## Raw Hall test points

- TP701: (85.390, 135.000) net `/BROTHER-CONNECTORS/EOL_L`
- TP702: (321.660, 160.160) net `/BROTHER-CONNECTORS/EOL_R`

## Copper ending exactly on obsolete pads

- No routed track/via endpoints land exactly on obsolete pads.

## Nearby footprint inventory around comparator clusters

## Migration implications

The PCB migration must remove the obsolete comparator footprint set and add R735-R738 before final parity validation. Net assignment for the new footprints must be derived from the validated schematic netlist, not guessed from legacy PCB net names.
