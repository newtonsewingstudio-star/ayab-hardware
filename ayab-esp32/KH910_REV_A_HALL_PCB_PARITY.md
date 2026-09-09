# KH910 Rev A — Hall / Comparator PCB Parity Audit

Generated read-only from the current repository PCB using KiCad `pcbnew`.

- Board footprints: **245**
- Board nets: **153**
- Obsolete comparator footprints still present: **24/24**
- New Hall-divider footprints present: **0/4**

## Required parity summary

- C703: PRESENT (remove)
- C704: PRESENT (remove)
- R715: PRESENT (remove)
- R716: PRESENT (remove)
- R717: PRESENT (remove)
- R718: PRESENT (remove)
- R719: PRESENT (remove)
- R720: PRESENT (remove)
- R721: PRESENT (remove)
- R722: PRESENT (remove)
- R723: PRESENT (remove)
- R724: PRESENT (remove)
- R725: PRESENT (remove)
- R726: PRESENT (remove)
- R727: PRESENT (remove)
- R728: PRESENT (remove)
- R729: PRESENT (remove)
- R730: PRESENT (remove)
- R731: PRESENT (remove)
- R732: PRESENT (remove)
- R733: PRESENT (remove)
- R734: PRESENT (remove)
- U702: PRESENT (remove)
- U703: PRESENT (remove)
- R735: **MISSING (add)**
- R736: **MISSING (add)**
- R737: **MISSING (add)**
- R738: **MISSING (add)**

## Interesting footprints and pads

### C703 — 100n
- footprint at: (87.913, 128.478) rot 180.0
- pad 1: (88.688, 128.478) net `GND` (#2)
- pad 2: (87.138, 128.478) net `+5V` (#5)

### C704 — 100n
- footprint at: (325.270, 154.200) rot 90.0
- pad 1: (325.270, 154.975) net `GND` (#2)
- pad 2: (325.270, 153.425) net `+5V` (#5)

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

### R715 — 100k
- footprint at: (87.913, 139.103) rot 0.0
- pad 1: (87.088, 139.103) net `/IO CONDITIONING/EOL_L_K` (#37)
- pad 2: (88.738, 139.103) net `Net-(U702A--)` (#90)

### R716 — 100k
- footprint at: (87.913, 130.028) rot 180.0
- pad 1: (88.738, 130.028) net `Net-(U702B-+)` (#91)
- pad 2: (87.088, 130.028) net `/IO CONDITIONING/EOL_L_L` (#38)

### R717 — 100k
- footprint at: (314.670, 154.200) rot -90.0
- pad 1: (314.670, 153.375) net `/BROTHER-CONNECTORS/EOL_R_N` (#69)
- pad 2: (314.670, 155.025) net `Net-(U703A--)` (#92)

### R718 — 100k
- footprint at: (323.720, 154.200) rot 90.0
- pad 1: (323.720, 155.025) net `Net-(U703B-+)` (#93)
- pad 2: (323.720, 153.375) net `/BROTHER-CONNECTORS/EOL_R_S` (#70)

### R719 — 10k
- footprint at: (87.913, 140.653) rot 180.0
- pad 1: (88.738, 140.653) net `Net-(U702A--)` (#90)
- pad 2: (87.088, 140.653) net `Net-(R719-Pad2)` (#94)

### R720 — 10k
- footprint at: (90.963, 130.028) rot 180.0
- pad 1: (91.788, 130.028) net `Net-(R720-Pad1)` (#95)
- pad 2: (90.138, 130.028) net `Net-(U702B-+)` (#91)

### R721 — 10k
- footprint at: (313.120, 154.200) rot 90.0
- pad 1: (313.120, 155.025) net `Net-(U703A--)` (#92)
- pad 2: (313.120, 153.375) net `Net-(R721-Pad2)` (#96)

### R722 — 10k
- footprint at: (323.720, 157.250) rot 90.0
- pad 1: (323.720, 158.075) net `Net-(R722-Pad1)` (#97)
- pad 2: (323.720, 156.425) net `Net-(U703B-+)` (#93)

### R723 — 4k7
- footprint at: (87.913, 126.928) rot 0.0
- pad 1: (87.088, 126.928) net `+5V` (#5)
- pad 2: (88.738, 126.928) net `Net-(R720-Pad1)` (#95)

### R724 — 1k
- footprint at: (90.963, 128.478) rot 0.0
- pad 1: (90.138, 128.478) net `Net-(R720-Pad1)` (#95)
- pad 2: (91.788, 128.478) net `GND` (#2)

### R725 — 4k7
- footprint at: (326.820, 154.200) rot -90.0
- pad 1: (326.820, 153.375) net `+5V` (#5)
- pad 2: (326.820, 155.025) net `Net-(R722-Pad1)` (#97)

### R726 — 1k
- footprint at: (325.270, 157.250) rot -90.0
- pad 1: (325.270, 156.425) net `Net-(R722-Pad1)` (#97)
- pad 2: (325.270, 158.075) net `GND` (#2)

### R727 — 3k3
- footprint at: (87.913, 142.203) rot 0.0
- pad 1: (87.088, 142.203) net `+5V` (#5)
- pad 2: (88.738, 142.203) net `Net-(R719-Pad2)` (#94)

### R728 — 4k7
- footprint at: (90.963, 142.203) rot 0.0
- pad 1: (90.138, 142.203) net `Net-(R719-Pad2)` (#94)
- pad 2: (91.788, 142.203) net `GND` (#2)

### R729 — 3k3
- footprint at: (311.570, 154.200) rot -90.0
- pad 1: (311.570, 153.375) net `+5V` (#5)
- pad 2: (311.570, 155.025) net `Net-(R721-Pad2)` (#96)

### R730 — 4k7
- footprint at: (311.570, 157.250) rot -90.0
- pad 1: (311.570, 156.425) net `Net-(R721-Pad2)` (#96)
- pad 2: (311.570, 158.075) net `GND` (#2)

### R731 — 22k
- footprint at: (90.963, 139.103) rot 0.0
- pad 1: (90.138, 139.103) net `/BROTHER-CONNECTORS/EOL_L` (#63)
- pad 2: (91.788, 139.103) net `GND` (#2)

### R732 — 22k
- footprint at: (314.670, 157.250) rot -90.0
- pad 1: (314.670, 156.425) net `/BROTHER-CONNECTORS/EOL_R` (#64)
- pad 2: (314.670, 158.075) net `GND` (#2)

### R733 — 47k
- footprint at: (90.963, 140.653) rot 180.0
- pad 1: (91.788, 140.653) net `+5V` (#5)
- pad 2: (90.138, 140.653) net `/BROTHER-CONNECTORS/EOL_L` (#63)

### R734 — 47k
- footprint at: (313.120, 157.250) rot 90.0
- pad 1: (313.120, 158.075) net `+5V` (#5)
- pad 2: (313.120, 156.425) net `/BROTHER-CONNECTORS/EOL_R` (#64)

### TP701 — CMP-L
- footprint at: (85.390, 135.000) rot 0.0
- pad 1: (85.390, 135.000) net `/BROTHER-CONNECTORS/EOL_L` (#63)

### TP702 — CMP-R
- footprint at: (321.660, 160.160) rot 0.0
- pad 1: (321.660, 160.160) net `/BROTHER-CONNECTORS/EOL_R` (#64)

### U201 — ESP32-S3-MINI-1
- footprint at: (224.125, 129.675) rot 0.0
- pad 5: (217.125, 127.125) net `/ESP32/EOL_L_P` (#26)
- pad 6: (217.125, 127.975) net `/ESP32/EOL_L_N` (#27)
- pad 17: (219.025, 136.675) net `/AUX-CONNECTORS/AYAB_SCK` (#80)
- pad 18: (219.875, 136.675) net `/ESP32/ESP14` (#117)

### U701 — SN74LVC4245
- footprint at: (194.340, 157.530) rot 0.0
- pad 1: (191.477, 153.955) net `+5V` (#5)
- pad 2: (191.477, 154.605) net `+5V` (#5)
- pad 3: (191.477, 155.255) net `/BROTHER-CONNECTORS/ENC_V1` (#66)
- pad 4: (191.477, 155.905) net `/BROTHER-CONNECTORS/ENC_V2` (#65)
- pad 5: (191.477, 156.555) net `/BROTHER-CONNECTORS/ENC_BELTPHASE` (#67)
- pad 6: (191.477, 157.205) net `/IO CONDITIONING/EOL_L_K` (#37)
- pad 7: (191.477, 157.855) net `/IO CONDITIONING/EOL_L_L` (#38)
- pad 8: (191.477, 158.505) net `/BROTHER-CONNECTORS/EOL_R_N` (#69)
- pad 9: (191.477, 159.155) net `/BROTHER-CONNECTORS/EOL_R_S` (#70)
- pad 10: (191.477, 159.805) net `Net-(J702-Pin_8)` (#71)
- pad 11: (191.477, 160.455) net `GND` (#2)
- pad 12: (191.477, 161.105) net `GND` (#2)
- pad 13: (197.202, 161.105) net `GND` (#2)
- pad 14: (197.202, 160.455) net `Net-(J701-Pin_8)` (#68)
- pad 15: (197.202, 159.805) net `/ESP32/EOL_R_N` (#30)
- pad 16: (197.202, 159.155) net `/ESP32/EOL_R_P` (#29)
- pad 17: (197.202, 158.505) net `/ESP32/EOL_L_N` (#27)
- pad 18: (197.202, 157.855) net `/ESP32/EOL_L_P` (#26)
- pad 19: (197.202, 157.205) net `/ESP32/ENC_BP` (#33)
- pad 20: (197.202, 156.555) net `/ESP32/ENC_B` (#32)
- pad 21: (197.202, 155.905) net `/ESP32/ENC_A` (#31)
- pad 22: (197.202, 155.255) net `GND` (#2)
- pad 23: (197.202, 154.605) net `+3V3` (#6)
- pad 24: (197.202, 153.955) net `+3V3` (#6)

### U702 — LM393
- footprint at: (89.133, 134.553) rot 90.0
- pad 1: (87.228, 137.028) net `/IO CONDITIONING/EOL_L_K` (#37)
- pad 2: (88.498, 137.028) net `Net-(U702A--)` (#90)
- pad 3: (89.768, 137.028) net `/BROTHER-CONNECTORS/EOL_L` (#63)
- pad 4: (91.038, 137.028) net `GND` (#2)
- pad 5: (91.038, 132.078) net `Net-(U702B-+)` (#91)
- pad 6: (89.768, 132.078) net `/BROTHER-CONNECTORS/EOL_L` (#63)
- pad 7: (88.498, 132.078) net `/IO CONDITIONING/EOL_L_L` (#38)
- pad 8: (87.228, 132.078) net `+5V` (#5)

### U703 — LM393
- footprint at: (319.195, 155.400) rot 0.0
- pad 1: (316.720, 153.495) net `/BROTHER-CONNECTORS/EOL_R_N` (#69)
- pad 2: (316.720, 154.765) net `Net-(U703A--)` (#92)
- pad 3: (316.720, 156.035) net `/BROTHER-CONNECTORS/EOL_R` (#64)
- pad 4: (316.720, 157.305) net `GND` (#2)
- pad 5: (321.670, 157.305) net `Net-(U703B-+)` (#93)
- pad 6: (321.670, 156.035) net `/BROTHER-CONNECTORS/EOL_R` (#64)
- pad 7: (321.670, 154.765) net `/BROTHER-CONNECTORS/EOL_R_S` (#70)
- pad 8: (321.670, 153.495) net `+5V` (#5)

## Hall-related board nets

- net 63: `/BROTHER-CONNECTORS/EOL_L`
- net 64: `/BROTHER-CONNECTORS/EOL_R`
- net 69: `/BROTHER-CONNECTORS/EOL_R_N`
- net 70: `/BROTHER-CONNECTORS/EOL_R_S`
- net 27: `/ESP32/EOL_L_N`
- net 26: `/ESP32/EOL_L_P`
- net 30: `/ESP32/EOL_R_N`
- net 29: `/ESP32/EOL_R_P`
- net 37: `/IO CONDITIONING/EOL_L_K`
- net 38: `/IO CONDITIONING/EOL_L_L`

## Raw Hall test points

- TP701: (85.390, 135.000) net `/BROTHER-CONNECTORS/EOL_L`
- TP702: (321.660, 160.160) net `/BROTHER-CONNECTORS/EOL_R`

## Copper ending exactly on obsolete pads

- C703 pad 1 (88.688, 128.478) net `GND`: track `GND` F.Cu (88.688,128.478)->(88.113,127.903)
- C703 pad 2 (87.138, 128.478) net `+5V`: track `+5V` F.Cu (87.088,128.428)->(87.138,128.478) | track `+5V` F.Cu (86.363,129.253)->(87.138,128.478)
- C704 pad 1 (325.270, 154.975) net `GND`: track `GND` F.Cu (325.270,154.975)->(326.075,154.170)
- C704 pad 2 (325.270, 153.425) net `+5V`: track `+5V` F.Cu (324.495,152.650)->(325.270,153.425) | track `+5V` F.Cu (325.270,153.425)->(326.770,153.425)
- R715 pad 1 (87.088, 139.103) net `/IO CONDITIONING/EOL_L_K`: track `/IO CONDITIONING/EOL_L_K` F.Cu (87.088,139.103)->(86.557,139.103) | track `/IO CONDITIONING/EOL_L_K` F.Cu (87.228,138.963)->(87.088,139.103)
- R715 pad 2 (88.738, 139.103) net `Net-(U702A--)`: track `Net-(U702A--)` F.Cu (88.498,138.863)->(88.738,139.103) | track `Net-(U702A--)` F.Cu (88.738,140.653)->(88.738,139.103)
- R716 pad 1 (88.738, 130.028) net `Net-(U702B-+)`: track `Net-(U702B-+)` F.Cu (88.738,130.028)->(90.138,130.028)
- R716 pad 2 (87.088, 130.028) net `/IO CONDITIONING/EOL_L_L`: track `/IO CONDITIONING/EOL_L_L` F.Cu (87.088,130.028)->(88.498,131.438)
- R717 pad 1 (314.670, 153.375) net `/BROTHER-CONNECTORS/EOL_R_N`: track `/BROTHER-CONNECTORS/EOL_R_N` F.Cu (314.670,153.375)->(313.935,152.640) | track `/BROTHER-CONNECTORS/EOL_R_N` F.Cu (314.670,153.375)->(316.600,153.375)
- R717 pad 2 (314.670, 155.025) net `Net-(U703A--)`: track `Net-(U703A--)` F.Cu (313.120,155.025)->(314.670,155.025) | track `Net-(U703A--)` F.Cu (314.930,154.765)->(314.670,155.025)
- R718 pad 1 (323.720, 155.025) net `Net-(U703B-+)`: track `Net-(U703B-+)` F.Cu (323.720,156.425)->(323.720,155.025)
- R718 pad 2 (323.720, 153.375) net `/BROTHER-CONNECTORS/EOL_R_S`: track `/BROTHER-CONNECTORS/EOL_R_S` F.Cu (322.330,154.765)->(323.720,153.375)
- R719 pad 1 (88.738, 140.653) net `Net-(U702A--)`: track `Net-(U702A--)` F.Cu (88.738,140.653)->(88.738,139.103)
- R719 pad 2 (87.088, 140.653) net `Net-(R719-Pad2)`: track `Net-(R719-Pad2)` F.Cu (88.638,142.203)->(87.088,140.653)
- R720 pad 1 (91.788, 130.028) net `Net-(R720-Pad1)`: track `Net-(R720-Pad1)` F.Cu (91.788,130.028)->(91.688,130.028)
- R720 pad 2 (90.138, 130.028) net `Net-(U702B-+)`: track `Net-(U702B-+)` F.Cu (90.138,130.028)->(91.038,130.928) | track `Net-(U702B-+)` F.Cu (88.738,130.028)->(90.138,130.028)
- R721 pad 1 (313.120, 155.025) net `Net-(U703A--)`: track `Net-(U703A--)` F.Cu (313.120,155.025)->(314.670,155.025)
- R721 pad 2 (313.120, 153.375) net `Net-(R721-Pad2)`: track `Net-(R721-Pad2)` F.Cu (311.570,154.925)->(313.120,153.375)
- R722 pad 1 (323.720, 158.075) net `Net-(R722-Pad1)`: track `Net-(R722-Pad1)` F.Cu (323.720,158.075)->(323.720,157.975)
- R722 pad 2 (323.720, 156.425) net `Net-(U703B-+)`: track `Net-(U703B-+)` F.Cu (323.720,156.425)->(323.720,155.025) | track `Net-(U703B-+)` F.Cu (322.840,157.305)->(323.720,156.425)
- R723 pad 1 (87.088, 126.928) net `+5V`: track `+5V` F.Cu (87.088,126.928)->(87.088,128.428) | track `+5V` F.Cu (87.088,126.928)->(87.088,125.728)
- R723 pad 2 (88.738, 126.928) net `Net-(R720-Pad1)`: track `Net-(R720-Pad1)` F.Cu (90.138,128.328)->(88.738,126.928)
- R724 pad 1 (90.138, 128.478) net `Net-(R720-Pad1)`: track `Net-(R720-Pad1)` F.Cu (90.138,128.478)->(90.138,128.328) | track `Net-(R720-Pad1)` F.Cu (91.688,130.028)->(90.138,128.478)
- R725 pad 1 (326.820, 153.375) net `+5V`: track `+5V` F.Cu (326.770,153.425)->(326.820,153.375)
- R725 pad 2 (326.820, 155.025) net `Net-(R722-Pad1)`: track `Net-(R722-Pad1)` F.Cu (325.420,156.425)->(326.820,155.025)
- R726 pad 1 (325.270, 156.425) net `Net-(R722-Pad1)`: track `Net-(R722-Pad1)` F.Cu (323.720,157.975)->(325.270,156.425) | track `Net-(R722-Pad1)` F.Cu (325.270,156.425)->(325.420,156.425)
- R727 pad 1 (87.088, 142.203) net `+5V`: track `+5V` F.Cu (87.088,142.203)->(87.088,143.552)
- R727 pad 2 (88.738, 142.203) net `Net-(R719-Pad2)`: track `Net-(R719-Pad2)` F.Cu (88.738,142.203)->(88.638,142.203) | track `Net-(R719-Pad2)` F.Cu (90.138,142.203)->(88.738,142.203)
- R728 pad 1 (90.138, 142.203) net `Net-(R719-Pad2)`: track `Net-(R719-Pad2)` F.Cu (90.138,142.203)->(88.738,142.203)
- R728 pad 2 (91.788, 142.203) net `GND`: track `GND` F.Cu (91.788,142.203)->(93.053,142.203) | track `GND` F.Cu (91.788,142.203)->(91.063,141.478)
- R729 pad 1 (311.570, 153.375) net `+5V`: track `+5V` F.Cu (311.565,153.370)->(311.570,153.375) | track `+5V` F.Cu (310.370,154.575)->(311.570,153.375)
- R729 pad 2 (311.570, 155.025) net `Net-(R721-Pad2)`: track `Net-(R721-Pad2)` F.Cu (311.570,155.025)->(311.570,154.925) | track `Net-(R721-Pad2)` F.Cu (311.570,156.425)->(311.570,155.025)
- R730 pad 1 (311.570, 156.425) net `Net-(R721-Pad2)`: track `Net-(R721-Pad2)` F.Cu (311.570,156.425)->(311.570,155.025)
- R731 pad 1 (90.138, 139.103) net `/BROTHER-CONNECTORS/EOL_L`: track `/BROTHER-CONNECTORS/EOL_L` F.Cu (90.138,139.103)->(90.138,140.653) | track `/BROTHER-CONNECTORS/EOL_L` F.Cu (89.768,138.733)->(90.138,139.103)
- R731 pad 2 (91.788, 139.103) net `GND`: track `GND` F.Cu (91.063,139.828)->(91.788,139.103) | track `GND` F.Cu (91.038,138.353)->(91.788,139.103) | track `GND` F.Cu (91.788,139.103)->(93.063,139.103)
- R732 pad 1 (314.670, 156.425) net `/BROTHER-CONNECTORS/EOL_R`: track `/BROTHER-CONNECTORS/EOL_R` F.Cu (314.925,156.170)->(314.670,156.425) | track `/BROTHER-CONNECTORS/EOL_R` F.Cu (313.120,156.425)->(314.670,156.425)
- R733 pad 1 (91.788, 140.653) net `+5V`: track `+5V` F.Cu (93.083,140.653)->(91.788,140.653)
- R733 pad 2 (90.138, 140.653) net `/BROTHER-CONNECTORS/EOL_L`: track `/BROTHER-CONNECTORS/EOL_L` F.Cu (90.138,139.103)->(90.138,140.653)
- R734 pad 1 (313.120, 158.075) net `+5V`: track `+5V` F.Cu (313.120,158.075)->(312.325,157.280)
- R734 pad 2 (313.120, 156.425) net `/BROTHER-CONNECTORS/EOL_R`: track `/BROTHER-CONNECTORS/EOL_R` F.Cu (313.120,156.425)->(314.670,156.425)
- U702 pad 1 (87.228, 137.028) net `/IO CONDITIONING/EOL_L_K`: track `/IO CONDITIONING/EOL_L_K` F.Cu (87.228,137.028)->(87.228,138.963)
- U702 pad 2 (88.498, 137.028) net `Net-(U702A--)`: track `Net-(U702A--)` F.Cu (88.498,137.028)->(88.498,138.863)
- U702 pad 3 (89.768, 137.028) net `/BROTHER-CONNECTORS/EOL_L`: track `/BROTHER-CONNECTORS/EOL_L` F.Cu (89.768,132.078)->(89.768,137.028) | track `/BROTHER-CONNECTORS/EOL_L` F.Cu (89.768,137.028)->(89.768,138.733)
- U702 pad 4 (91.038, 137.028) net `GND`: track `GND` F.Cu (91.038,137.028)->(91.038,138.353)
- U702 pad 5 (91.038, 132.078) net `Net-(U702B-+)`: track `Net-(U702B-+)` F.Cu (91.038,130.928)->(91.038,132.078)
- U702 pad 6 (89.768, 132.078) net `/BROTHER-CONNECTORS/EOL_L`: track `/BROTHER-CONNECTORS/EOL_L` F.Cu (89.768,132.078)->(89.768,137.028) | via `/BROTHER-CONNECTORS/EOL_L` F.Cu | track `/BROTHER-CONNECTORS/EOL_L` B.Cu (89.512,132.078)->(89.768,132.078)
- U702 pad 7 (88.498, 132.078) net `/IO CONDITIONING/EOL_L_L`: track `/IO CONDITIONING/EOL_L_L` F.Cu (88.498,132.078)->(88.498,134.107) | track `/IO CONDITIONING/EOL_L_L` F.Cu (88.498,131.438)->(88.498,132.078)
- U702 pad 8 (87.228, 132.078) net `+5V`: track `+5V` F.Cu (87.228,132.078)->(87.228,131.393) | track `+5V` F.Cu (87.228,132.078)->(86.012,132.078)
- U703 pad 1 (316.720, 153.495) net `/BROTHER-CONNECTORS/EOL_R_N`: track `/BROTHER-CONNECTORS/EOL_R_N` F.Cu (316.600,153.375)->(316.720,153.495)
- U703 pad 2 (316.720, 154.765) net `Net-(U703A--)`: track `Net-(U703A--)` F.Cu (316.720,154.765)->(314.930,154.765)
- U703 pad 3 (316.720, 156.035) net `/BROTHER-CONNECTORS/EOL_R`: track `/BROTHER-CONNECTORS/EOL_R` F.Cu (317.245,156.035)->(316.720,156.035) | track `/BROTHER-CONNECTORS/EOL_R` F.Cu (316.720,156.035)->(316.585,156.170) | track `/BROTHER-CONNECTORS/EOL_R` F.Cu (321.670,156.035)->(316.720,156.035)
- U703 pad 5 (321.670, 157.305) net `Net-(U703B-+)`: track `Net-(U703B-+)` F.Cu (321.670,157.305)->(322.840,157.305)
- U703 pad 6 (321.670, 156.035) net `/BROTHER-CONNECTORS/EOL_R`: track `/BROTHER-CONNECTORS/EOL_R` F.Cu (321.670,156.035)->(316.720,156.035)
- U703 pad 7 (321.670, 154.765) net `/BROTHER-CONNECTORS/EOL_R_S`: track `/BROTHER-CONNECTORS/EOL_R_S` F.Cu (321.670,154.765)->(322.330,154.765) | track `/BROTHER-CONNECTORS/EOL_R_S` F.Cu (321.670,154.765)->(320.995,154.765)
- U703 pad 8 (321.670, 153.495) net `+5V`: track `+5V` F.Cu (321.670,153.495)->(322.515,152.650) | track `+5V` F.Cu (320.595,153.495)->(321.670,153.495)

## Nearby footprint inventory around comparator clusters

### Around U702 at (89.133, 134.553) rot 90.0

- 3.77 mm: TP701 `CMP-L` at (85.390, 135.000) rot 0.0
- 4.69 mm: R716 `100k` at (87.913, 130.028) rot 180.0
- 4.71 mm: R715 `100k` at (87.913, 139.103) rot 0.0
- 4.88 mm: R720 `10k` at (90.963, 130.028) rot 180.0
- 4.90 mm: R731 `22k` at (90.963, 139.103) rot 0.0
- 5.59 mm: R812 `5k1` at (93.270, 130.800) rot -90.0
- 6.20 mm: C703 `100n` at (87.913, 128.478) rot 180.0
- 6.22 mm: R719 `10k` at (87.913, 140.653) rot 180.0
- 6.34 mm: R724 `1k` at (90.963, 128.478) rot 0.0
- 6.37 mm: R733 `47k` at (90.963, 140.653) rot 180.0
- 6.81 mm: kibuzzard-65A1AC88 `G***` at (82.340, 135.010) rot 0.0
- 7.12 mm: R809 `47R` at (95.190, 130.803) rot 90.0
- 7.72 mm: R723 `4k7` at (87.913, 126.928) rot 0.0
- 7.75 mm: R727 `3k3` at (87.913, 142.203) rot 0.0
- 7.87 mm: R728 `4k7` at (90.963, 142.203) rot 0.0
- 7.96 mm: TP302 `MCP_INTB` at (97.050, 133.690) rot 0.0
- 8.39 mm: C603 `10u` at (97.058, 137.312) rot 90.0
- 8.50 mm: R811 `5k1` at (96.770, 130.812) rot -90.0
- 8.85 mm: Q803 `AO3400A` at (94.230, 127.320) rot 90.0
- 9.78 mm: kibuzzard-65BFD893 `G***` at (81.790, 141.020) rot 0.0
- 10.14 mm: TP301 `MCP_INTA` at (99.240, 133.680) rot -90.0
- 10.28 mm: R810 `47R` at (98.710, 130.810) rot 90.0
- 10.42 mm: C304 `10u` at (97.050, 141.325) rot -90.0
- 11.11 mm: R816 `5k1` at (93.990, 124.558) rot 0.0
- 11.24 mm: Q804 `AO3400A` at (97.750, 127.330) rot 90.0
- 12.74 mm: R817 `5k1` at (97.045, 124.567) rot 180.0
- 13.54 mm: kibuzzard-65BFD8A4 `G***` at (86.760, 147.880) rot 0.0
- 13.98 mm: J408 `910.950 EOL L` at (76.820, 127.940) rot 180.0
- 14.99 mm: J806 `AYAB_I2C` at (93.940, 120.360) rot 90.0
- 14.99 mm: J804 `I2C_VBUS` at (101.880, 126.668) rot 180.0
- 15.00 mm: U304 `ULN2003A` at (103.350, 139.325) rot -90.0

### Around U703 at (319.195, 155.400) rot 0.0

- 4.68 mm: R717 `100k` at (314.670, 154.200) rot -90.0
- 4.68 mm: R718 `100k` at (323.720, 154.200) rot 90.0
- 4.85 mm: kibuzzard-65A1ADEE `G***` at (318.240, 160.160) rot 0.0
- 4.89 mm: R722 `10k` at (323.720, 157.250) rot 90.0
- 4.89 mm: R732 `22k` at (314.670, 157.250) rot -90.0
- 5.36 mm: TP702 `CMP-R` at (321.660, 160.160) rot 0.0
- 6.19 mm: C704 `100n` at (325.270, 154.200) rot 90.0
- 6.19 mm: R721 `10k` at (313.120, 154.200) rot 90.0
- 6.35 mm: R726 `1k` at (325.270, 157.250) rot -90.0
- 6.35 mm: R734 `47k` at (313.120, 157.250) rot 90.0
- 6.42 mm: kibuzzard-65BFD82E `G***` at (320.920, 149.220) rot 0.0
- 7.72 mm: R725 `4k7` at (326.820, 154.200) rot -90.0
- 7.72 mm: R729 `3k3` at (311.570, 154.200) rot -90.0
- 7.85 mm: R730 `4k7` at (311.570, 157.250) rot -90.0
- 10.54 mm: J404 `910.950 SOLENOIDS B` at (322.200, 145.300) rot 180.0
- 11.55 mm: kibuzzard-65BFD865 `G***` at (330.070, 159.290) rot 0.0
- 13.00 mm: kibuzzard-65C3D944 `G***` at (307.380, 149.980) rot 0.0
- 13.30 mm: H106 `M3` at (332.184, 152.559) rot 0.0
- 14.90 mm: TP601 `12V` at (305.320, 149.980) rot -90.0

## Migration implications

The PCB migration must remove the obsolete comparator footprint set and add R735-R738 before final parity validation. Net assignment for the new footprints must be derived from the validated schematic netlist, not guessed from legacy PCB net names.
