# KH910 Rev A — Solenoid PCB DRC Failure

Generated from the rejected staged PCB. The invalid PCB itself was not committed.

## KiCad validation output
```text
Found 251 violations
Found 9 unconnected items
Saved DRC Report to /tmp/solenoid-pcb-drc.rpt

--- direct DRC report ---
** Drc report for ayab-esp32.kicad_pcb **
** Created on 2026-09-09T11:14:11+0000 **
** Report includes: Errors, Warnings **

** Found 251 DRC violations **
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
    @(296.5620 mm, 151.9500 mm): Track [GND] on F.Cu, length 2.0500 mm
    @(297.6050 mm, 153.0348 mm): Pad 3 [/PSU/INP_2] of J601 on F.Cu
[solder_mask_bridge]: Front solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(296.5620 mm, 154.0000 mm): Track [GND] on F.Cu, length 5.3870 mm
    @(297.6050 mm, 153.0348 mm): Pad 3 [/PSU/INP_2] of J601 on F.Cu
[solder_mask_bridge]: Front solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(132.8950 mm, 136.8500 mm): Track [SOLENOID_12V_SW] on F.Cu, length 1.4000 mm
    @(132.8950 mm, 136.8500 mm): Pad 1 [/SOLENOID DRIVERS/MCU_SOL_7] of U302 on F.Cu
[solder_mask_bridge]: Front solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(120.3450 mm, 136.8500 mm): Track [SOLENOID_12V_SW] on F.Cu, length 1.4000 mm
    @(120.3450 mm, 136.8500 mm): Pad 1 [/SOLENOID DRIVERS/MCU_SOL_0] of U303 on F.Cu
[solder_mask_bridge]: Front solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(120.3450 mm, 136.8500 mm): Track [SOLENOID_12V_SW] on F.Cu, length 1.4000 mm
    @(122.1750 mm, 136.3750 mm): Pad 2 [GND] of C605 on F.Cu
[solder_mask_bridge]: Front solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(121.7450 mm, 136.8500 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(122.1750 mm, 136.3750 mm): Pad 2 [GND] of C605 on F.Cu
[solder_mask_bridge]: Front solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(107.7950 mm, 136.8500 mm): Track [SOLENOID_12V_SW] on F.Cu, length 1.4000 mm
    @(107.7950 mm, 136.8500 mm): Pad 1 [/SOLENOID DRIVERS/MCU_SOL_E] of U304 on F.Cu
[solder_mask_bridge]: Front solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(107.7950 mm, 136.8500 mm): Track [SOLENOID_12V_SW] on F.Cu, length 1.4000 mm
    @(109.6250 mm, 136.3750 mm): Pad 2 [GND] of C604 on F.Cu
[solder_mask_bridge]: Front solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(109.1950 mm, 136.8500 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(109.6250 mm, 136.3750 mm): Pad 2 [GND] of C604 on F.Cu
[solder_mask_bridge]: Front solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(109.6250 mm, 142.2750 mm): Track [SOLENOID_12V_SW] on F.Cu, length 1.4000 mm
    @(109.6250 mm, 142.2750 mm): Pad 2 [GND] of C302 on F.Cu
[solder_mask_bridge]: Front solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(122.1750 mm, 142.2750 mm): Track [SOLENOID_12V_SW] on F.Cu, length 1.4000 mm
    @(122.1750 mm, 142.2750 mm): Pad 2 [GND] of C303 on F.Cu
[solder_mask_bridge]: Front solder mask aperture bridges items with different nets
    Rule: board setup solder mask min width; error
    @(97.0500 mm, 142.2750 mm): Track [SOLENOID_12V_SW] on F.Cu, length 1.4000 mm
    @(97.0500 mm, 142.2750 mm): Pad 2 [GND] of C304 on F.Cu
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
[hole_to_hole]: Drilled hole too close to other hole (board setup constraints min 0.2495 mm; actual 0.0000 mm)
    Rule: board setup constraints; error
    @(95.6500 mm, 142.2750 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(95.5400 mm, 142.2700 mm): Via [GND] on F.Cu - B.Cu
[hole_to_hole]: Drilled hole too close to other hole (board setup constraints min 0.2495 mm; actual 0.1119 mm)
    Rule: board setup constraints; error
    @(292.1050 mm, 154.6348 mm): NPTH pad of J601
    @(290.8000 mm, 154.5000 mm): Via [GND] on F.Cu - B.Cu
[hole_to_hole]: Drilled hole too close to other hole (board setup constraints min 0.2495 mm; actual 0.1119 mm)
    Rule: board setup constraints; error
    @(292.1050 mm, 154.6348 mm): NPTH pad of J601
    @(290.8000 mm, 154.5000 mm): Via [GND] on F.Cu - B.Cu
[courtyards_overlap]: Courtyards overlap
    Rule: board setup constraints courtyard; error
    @(297.5000 mm, 151.0000 mm): Footprint Q806
    @(294.6000 mm, 150.0500 mm): Footprint R821
[courtyards_overlap]: Courtyards overlap
    Rule: board setup constraints courtyard; error
    @(297.5000 mm, 151.0000 mm): Footprint Q806
    @(301.0000 mm, 150.0000 mm): Footprint Q805
[courtyards_overlap]: Courtyards overlap
    Rule: board setup constraints courtyard; error
    @(301.0000 mm, 150.9380 mm): Footprint R820
    @(301.0000 mm, 150.0000 mm): Footprint Q805
[shorting_items]: Items shorting two nets (nets GND and SOLENOID_12V_SW)
    Local override; error
    @(95.5450 mm, 142.2750 mm): Track [GND] on F.Cu, length 0.0071 mm
    @(95.6500 mm, 142.2750 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
[shorting_items]: Items shorting two nets (nets GND and +12V)
    Local override; error
    @(300.8600 mm, 153.3300 mm): Track [GND] on F.Cu, length 2.2500 mm
    @(301.9500 mm, 150.9380 mm): Track [+12V] on F.Cu, length 2.0945 mm
[shorting_items]: Items shorting two nets (nets GND and +12V)
    Local override; error
    @(300.8600 mm, 151.0800 mm): Track [GND] on F.Cu, length 0.8202 mm
    @(301.9500 mm, 150.9380 mm): Track [+12V] on F.Cu, length 2.0945 mm
[shorting_items]: Items shorting two nets (nets SOLENOID_12V_SW and GND)
    Local override; error
    @(95.6500 mm, 142.2750 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(97.0500 mm, 142.2750 mm): Track [GND] on F.Cu, length 1.5050 mm
[tracks_crossing]: Tracks crossing
    Local override; error
    @(109.6250 mm, 142.2750 mm): Track [GND] on F.Cu, length 1.2600 mm
    @(109.6250 mm, 142.2750 mm): Track [SOLENOID_12V_SW] on F.Cu, length 1.4000 mm
[tracks_crossing]: Tracks crossing
    Local override; error
    @(122.1750 mm, 142.2750 mm): Track [SOLENOID_12V_SW] on F.Cu, length 1.4000 mm
    @(122.1750 mm, 142.2750 mm): Track [GND] on F.Cu, length 1.2400 mm
[shorting_items]: Items shorting two nets (nets GND and +12V)
    Local override; error
    @(299.7100 mm, 149.4200 mm): Via [GND] on F.Cu - B.Cu
    @(300.0500 mm, 149.0625 mm): Pad 2 [+12V] of Q805 on F.Cu
[shorting_items]: Items shorting two nets (nets GND and SOLENOID_12V_SW)
    Local override; error
    @(109.6300 mm, 143.5400 mm): Via [GND] on F.Cu - B.Cu
    @(109.1950 mm, 136.8500 mm): Track [SOLENOID_12V_SW] on In1.Cu, length 25.6500 mm
[shorting_items]: Items shorting two nets (nets SOLENOID_12V_SW and GND)
    Local override; error
    @(95.6500 mm, 162.5000 mm): Track [SOLENOID_12V_SW] on In1.Cu, length 215.2600 mm
    @(306.4000 mm, 163.1200 mm): Via [GND] on F.Cu - B.Cu
[shorting_items]: Items shorting two nets (nets SOLENOID_12V_SW and GND)
    Local override; error
    @(114.8400 mm, 153.7850 mm): Track [SOLENOID_12V_SW] on In1.Cu, length 8.7150 mm
    @(114.5900 mm, 159.9900 mm): Via [GND] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.1000 mm; actual 0.0500 mm)
    Local override; error
    @(304.3500 mm, 147.4000 mm): Track [/BROTHER-CONNECTORS/EOL_R_N] on F.Cu, length 28.6900 mm
    @(299.2000 mm, 146.8000 mm): Pad 1 [SOLENOID_12V_SW] of TP703 on F.Cu
[shorting_items]: Items shorting two nets (nets SOLENOID_12V_SW and +5V)
    Local override; error
    @(301.0000 mm, 146.8000 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(301.0900 mm, 147.9900 mm): Track [+5V] on B.Cu, length 1.9233 mm
[clearance]: Clearance violation ( clearance 0.1000 mm; actual 0.0200 mm)
    Local override; error
    @(300.2800 mm, 150.5000 mm): Via [GND] on F.Cu - B.Cu
    @(301.0000 mm, 150.9375 mm): Pad 3 [SOLENOID_12V_SW] of Q805 on F.Cu
[shorting_items]: Items shorting two nets (nets SOLENOID_12V_SW and GND)
    Local override; error
    @(301.0000 mm, 146.8000 mm): Track [SOLENOID_12V_SW] on In1.Cu, length 15.7000 mm
    @(300.2800 mm, 150.5000 mm): Via [GND] on F.Cu - B.Cu
[shorting_items]: Items shorting two nets (nets SOLENOID_12V_SW and GND)
    Local override; error
    @(111.0250 mm, 142.2750 mm): Track [SOLENOID_12V_SW] on In1.Cu, length 20.2250 mm
    @(111.4800 mm, 153.8700 mm): Via [GND] on F.Cu - B.Cu
[shorting_items]: Items shorting two nets (nets Net-(Q805-G) and GND)
    Local override; error
    @(301.9500 mm, 149.0625 mm): Pad 1 [Net-(Q805-G)] of Q805 on F.Cu
    @(302.4300 mm, 149.4200 mm): Via [GND] on F.Cu - B.Cu
[shorting_items]: Items shorting two nets (nets SOLENOID_12V_SW and GND)
    Local override; error
    @(301.0000 mm, 149.0620 mm): Track [SOLENOID_12V_SW] on F.Cu, length 2.2620 mm
    @(301.0700 mm, 149.4200 mm): Via [GND] on F.Cu - B.Cu
[shorting_items]: Items shorting two nets (nets SOLENOID_12V_SW and GND)
    Local override; error
    @(301.0000 mm, 146.8000 mm): Track [SOLENOID_12V_SW] on In1.Cu, length 15.7000 mm
    @(301.0700 mm, 149.4200 mm): Via [GND] on F.Cu - B.Cu
[shorting_items]: Items shorting two nets (nets SOLENOID_12V_SW and GND)
    Local override; error
    @(310.9100 mm, 138.8300 mm): Track [SOLENOID_12V_SW] on In1.Cu, length 23.6700 mm
    @(310.4300 mm, 145.1600 mm): Via [GND] on F.Cu - B.Cu
[shorting_items]: Items shorting two nets (nets GND and +12V)
    Local override; error
    @(301.6400 mm, 150.5000 mm): Via [GND] on F.Cu - B.Cu
    @(301.9500 mm, 150.9380 mm): Track [+12V] on F.Cu, length 2.0945 mm
[shorting_items]: Items shorting two nets (nets SOLENOID_12V_SW and GND)
    Local override; error
    @(301.0000 mm, 146.8000 mm): Track [SOLENOID_12V_SW] on In1.Cu, length 15.7000 mm
    @(301.6400 mm, 150.5000 mm): Via [GND] on F.Cu - B.Cu
[shorting_items]: Items shorting two nets (nets Net-(Q805-G) and GND)
    Local override; error
    @(300.0500 mm, 150.9380 mm): Track [Net-(Q805-G)] on F.Cu, length 1.6132 mm
    @(298.9200 mm, 150.5000 mm): Via [GND] on F.Cu - B.Cu
[shorting_items]: Items shorting two nets (nets SOLENOID_12V_SW and /BROTHER-CONNECTORS/EOL_R_S)
    Local override; error
    @(299.2000 mm, 146.8000 mm): Track [SOLENOID_12V_SW] on F.Cu, length 1.8000 mm
    @(304.4500 mm, 147.0200 mm): Track [/BROTHER-CONNECTORS/EOL_R_S] on F.Cu, length 26.6700 mm
[shorting_items]: Items shorting two nets (nets SOLENOID_12V_SW and GND)
    Local override; error
    @(121.7450 mm, 136.8500 mm): Track [SOLENOID_12V_SW] on In1.Cu, length 25.6500 mm
    @(122.1500 mm, 143.5400 mm): Via [GND] on F.Cu - B.Cu
[shorting_items]: Items shorting two nets (nets SOLENOID_12V_SW and GND)
    Local override; error
    @(95.6500 mm, 142.2750 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(95.5400 mm, 142.2700 mm): Via [GND] on F.Cu - B.Cu
[shorting_items]: Items shorting two nets (nets SOLENOID_12V_SW and GND)
    Local override; error
    @(95.6500 mm, 142.2750 mm): Track [SOLENOID_12V_SW] on In1.Cu, length 20.2250 mm
    @(95.5400 mm, 142.2700 mm): Via [GND] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.1000 mm; actual 0.0550 mm)
    Local override; error
    @(109.7900 mm, 139.3200 mm): Track [+12V] on F.Cu, length 10.6700 mm
    @(109.6250 mm, 140.3750 mm): Pad 1 [SOLENOID_12V_SW] of C302 on F.Cu
[clearance]: Clearance violation ( clearance 0.1000 mm; actual 0.0950 mm)
    Local override; error
    @(225.8250 mm, 136.6750 mm): Track [SOLENOID_PWR_EN] on F.Cu, length 1.9802 mm
    @(223.9282 mm, 138.4450 mm): Track [/BROTHER-CONNECTORS/SOL_0] on F.Cu, length 38.0368 mm
[shorting_items]: Items shorting two nets (nets SOLENOID_12V_SW and +12V)
    Local override; error
    @(97.0500 mm, 140.3750 mm): Pad 1 [SOLENOID_12V_SW] of C304 on F.Cu
    @(97.0500 mm, 140.3750 mm): Track [+12V] on F.Cu, length 1.4474 mm
[clearance]: Clearance violation ( clearance 0.1000 mm; actual 0.0550 mm)
    Local override; error
    @(97.0500 mm, 140.3750 mm): Pad 1 [SOLENOID_12V_SW] of C304 on F.Cu
    @(99.1200 mm, 139.3200 mm): Track [+12V] on F.Cu, length 2.3300 mm
[clearance]: Clearance violation ( clearance 0.1000 mm; actual 0.0550 mm)
    Local override; error
    @(122.1600 mm, 139.3200 mm): Track [+12V] on F.Cu, length 4.2100 mm
    @(122.1750 mm, 140.3750 mm): Pad 1 [SOLENOID_12V_SW] of C303 on F.Cu
[shorting_items]: Items shorting two nets (nets +12V and SOLENOID_12V_SW)
    Local override; error
    @(122.1750 mm, 140.3750 mm): Track [+12V] on F.Cu, length 1.0400 mm
    @(122.1750 mm, 140.3750 mm): Pad 1 [SOLENOID_12V_SW] of C303 on F.Cu
[clearance]: Clearance violation ( clearance 0.1000 mm; actual 0.0550 mm)
    Local override; error
    @(123.8700 mm, 139.3200 mm): Track [+12V] on F.Cu, length 1.7100 mm
    @(122.1750 mm, 140.3750 mm): Pad 1 [SOLENOID_12V_SW] of C303 on F.Cu
[shorting_items]: Items shorting two nets (nets SOLENOID_12V_SW and +12V)
    Local override; error
    @(109.6250 mm, 140.3750 mm): Pad 1 [SOLENOID_12V_SW] of C302 on F.Cu
    @(109.6250 mm, 140.3750 mm): Track [+12V] on F.Cu, length 0.8900 mm
[tracks_crossing]: Tracks crossing
    Local override; error
    @(120.3450 mm, 136.8500 mm): Track [SOLENOID_12V_SW] on F.Cu, length 1.4000 mm
    @(120.3450 mm, 135.2450 mm): Track [/SOLENOID DRIVERS/MCU_SOL_0] on F.Cu, length 1.6050 mm
[clearance]: Clearance violation ( clearance 0.1000 mm; actual 0.0550 mm)
    Local override; error
    @(109.6250 mm, 140.3750 mm): Pad 1 [SOLENOID_12V_SW] of C302 on F.Cu
    @(111.5100 mm, 139.3200 mm): Track [+12V] on F.Cu, length 1.7200 mm
[shorting_items]: Items shorting two nets (nets /SOLENOID DRIVERS/MCU_SOL_7 and SOLENOID_12V_SW)
    Local override; error
    @(132.8700 mm, 135.1200 mm): Track [/SOLENOID DRIVERS/MCU_SOL_7] on F.Cu, length 1.7050 mm
    @(132.8950 mm, 136.8500 mm): Track [SOLENOID_12V_SW] on F.Cu, length 1.4000 mm
[tracks_crossing]: Tracks crossing
    Local override; error
    @(132.8700 mm, 136.8250 mm): Track [/SOLENOID DRIVERS/MCU_SOL_7] on F.Cu, length 0.0354 mm
    @(132.8950 mm, 136.8500 mm): Track [SOLENOID_12V_SW] on F.Cu, length 1.4000 mm
[shorting_items]: Items shorting two nets (nets SOLENOID_12V_SW and +12V)
    Local override; error
    @(124.0050 mm, 141.8000 mm): Pad 9 [SOLENOID_12V_SW] of U302 on F.Cu
    @(124.0050 mm, 141.8000 mm): Track [+12V] on F.Cu, length 2.3450 mm
[shorting_items]: Items shorting two nets (nets SOLENOID_12V_SW and +12V)
    Local override; error
    @(98.9050 mm, 141.8000 mm): Pad 9 [SOLENOID_12V_SW] of U304 on F.Cu
    @(98.9050 mm, 141.8000 mm): Track [+12V] on F.Cu, length 2.2650 mm
[shorting_items]: Items shorting two nets (nets SOLENOID_12V_SW and +12V)
    Local override; error
    @(111.4550 mm, 141.8000 mm): Pad 9 [SOLENOID_12V_SW] of U303 on F.Cu
    @(111.4550 mm, 141.8000 mm): Track [+12V] on F.Cu, length 2.4250 mm
[tracks_crossing]: Tracks crossing
    Local override; error
    @(107.7950 mm, 134.7800 mm): Track [/SOLENOID DRIVERS/MCU_SOL_E] on F.Cu, length 2.0700 mm
    @(107.7950 mm, 136.8500 mm): Track [SOLENOID_12V_SW] on F.Cu, length 1.4000 mm
[shorting_items]: Items shorting two nets (nets SOLENOID_12V_SW and +12V)
    Local override; error
    @(310.9100 mm, 138.8300 mm): PTH pad 9 [SOLENOID_12V_SW] of J403
    @(312.4500 mm, 141.8500 mm): Track [+12V] on B.Cu, length 2.1779 mm
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(301.9500 mm, 150.9380 mm): Track [+12V] on F.Cu, length 2.0945 mm
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.4290 mm)
    Local override; error
    @(303.4300 mm, 152.4200 mm): Track [+12V] on F.Cu, length 0.9400 mm
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[clearance]: Clearance violation ( clearance 0.1000 mm; actual 0.0904 mm)
    Local override; error
    @(300.8600 mm, 153.3300 mm): Track [GND] on F.Cu, length 2.2500 mm
    @(301.9500 mm, 150.9380 mm): Track [+12V] on F.Cu, length 0.1250 mm
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(301.9500 mm, 150.9380 mm): Track [+12V] on F.Cu, length 0.1250 mm
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[shorting_items]: Items shorting two nets (nets GND and Net-(Q805-G))
    Local override; error
    @(300.8600 mm, 153.3300 mm): Track [GND] on F.Cu, length 2.2500 mm
    @(300.0500 mm, 150.9380 mm): Track [Net-(Q805-G)] on F.Cu, length 0.1250 mm
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(300.0500 mm, 150.9380 mm): Track [Net-(Q805-G)] on F.Cu, length 0.1250 mm
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[clearance]: Clearance violation ( clearance 0.1000 mm; actual 0.0624 mm)
    Local override; error
    @(300.8600 mm, 153.3300 mm): Track [GND] on F.Cu, length 2.2500 mm
    @(300.0500 mm, 150.9380 mm): Track [Net-(Q805-G)] on F.Cu, length 1.6132 mm
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(300.0500 mm, 150.9380 mm): Track [Net-(Q805-G)] on F.Cu, length 1.6132 mm
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(295.4250 mm, 150.0500 mm): Track [Net-(Q806-G)] on F.Cu, length 1.1370 mm
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(295.4250 mm, 150.0500 mm): Track [Net-(Q806-G)] on F.Cu, length 1.6088 mm
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(294.3000 mm, 151.2000 mm): Track [Net-(Q806-G)] on F.Cu, length 1.8000 mm
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(294.3000 mm, 153.0000 mm): Track [Net-(Q806-G)] on F.Cu, length 1.4750 mm
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[shorting_items]: Items shorting two nets (nets /PSU/INP_2 and GND)
    Local override; error
    @(297.6050 mm, 153.0348 mm): Pad 3 [/PSU/INP_2] of J601 on F.Cu
    @(296.5620 mm, 151.9500 mm): Track [GND] on F.Cu, length 2.0500 mm
[shorting_items]: Items shorting two nets (nets GND and /PSU/INP_2)
    Local override; error
    @(296.5620 mm, 154.0000 mm): Track [GND] on F.Cu, length 5.3870 mm
    @(297.6050 mm, 153.0348 mm): Pad 3 [/PSU/INP_2] of J601 on F.Cu
[hole_clearance]: Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0000 mm)
    Rule: board setup constraints hole; error
    @(291.1750 mm, 153.0000 mm): Track [GND] on F.Cu, length 1.0000 mm
    @(292.1050 mm, 154.6348 mm): NPTH pad of J601
[hole_clearance]: Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0000 mm)
    Rule: board setup constraints hole; error
    @(291.1750 mm, 154.0000 mm): Track [GND] on F.Cu, length 0.6250 mm
    @(292.1050 mm, 154.6348 mm): NPTH pad of J601
[hole_clearance]: Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.1119 mm)
    Rule: board setup constraints hole; error
    @(292.1050 mm, 154.6348 mm): NPTH pad of J601
    @(290.8000 mm, 154.5000 mm): Via [GND] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.1000 mm; actual 0.0650 mm)
    Local override; error
    @(225.8250 mm, 136.6750 mm): Track [SOLENOID_PWR_EN] on F.Cu, length 1.9802 mm
    @(226.6750 mm, 136.6750 mm): Pad 26 [unconnected-(U201-GPIO26-Pad26)] of U201 on F.Cu
[shorting_items]: Items shorting two nets (nets SOLENOID_PWR_EN and /BROTHER-CONNECTORS/SOL_0)
    Local override; error
    @(227.2000 mm, 138.1000 mm): Via [SOLENOID_PWR_EN] on F.Cu - B.Cu
    @(223.9282 mm, 138.4450 mm): Track [/BROTHER-CONNECTORS/SOL_0] on F.Cu, length 38.0368 mm
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(227.2000 mm, 138.1000 mm): Via [SOLENOID_PWR_EN] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[hole_clearance]: Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0000 mm)
    Rule: board setup constraints hole; error
    @(227.2000 mm, 138.1000 mm): Via [SOLENOID_PWR_EN] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(227.2000 mm, 138.1000 mm): Via [SOLENOID_PWR_EN] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[hole_clearance]: Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0000 mm)
    Rule: board setup constraints hole; error
    @(227.2000 mm, 138.1000 mm): Via [SOLENOID_PWR_EN] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(227.2000 mm, 138.1000 mm): Via [SOLENOID_PWR_EN] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[hole_clearance]: Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0000 mm)
    Rule: board setup constraints hole; error
    @(227.2000 mm, 138.1000 mm): Via [SOLENOID_PWR_EN] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(227.2000 mm, 138.1000 mm): Track [SOLENOID_PWR_EN] on In1.Cu, length 57.8000 mm
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[shorting_items]: Items shorting two nets (nets +5V and SOLENOID_PWR_EN)
    Local override; error
    @(290.9300 mm, 145.1700 mm): PTH pad 1 [+5V] of J405
    @(285.0000 mm, 138.1000 mm): Track [SOLENOID_PWR_EN] on In1.Cu, length 9.8995 mm
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(285.0000 mm, 138.1000 mm): Track [SOLENOID_PWR_EN] on In1.Cu, length 9.8995 mm
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[shorting_items]: Items shorting two nets (nets +5V and SOLENOID_PWR_EN)
    Local override; error
    @(290.9300 mm, 145.1700 mm): PTH pad 1 [+5V] of J405
    @(292.0000 mm, 145.1000 mm): Track [SOLENOID_PWR_EN] on In1.Cu, length 2.4000 mm
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(292.0000 mm, 145.1000 mm): Track [SOLENOID_PWR_EN] on In1.Cu, length 2.4000 mm
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[shorting_items]: Items shorting two nets (nets SOLENOID_PWR_EN and /BROTHER-CONNECTORS/EOL_R_N)
    Local override; error
    @(292.0000 mm, 147.5000 mm): Via [SOLENOID_PWR_EN] on F.Cu - B.Cu
    @(304.3500 mm, 147.4000 mm): Track [/BROTHER-CONNECTORS/EOL_R_N] on F.Cu, length 28.6900 mm
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.1505 mm)
    Local override; error
    @(292.0000 mm, 147.5000 mm): Via [SOLENOID_PWR_EN] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(292.0000 mm, 147.5000 mm): Via [SOLENOID_PWR_EN] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[hole_clearance]: Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0000 mm)
    Rule: board setup constraints hole; error
    @(292.0000 mm, 147.5000 mm): Via [SOLENOID_PWR_EN] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(292.0000 mm, 147.5000 mm): Via [SOLENOID_PWR_EN] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[hole_clearance]: Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0000 mm)
    Rule: board setup constraints hole; error
    @(292.0000 mm, 147.5000 mm): Via [SOLENOID_PWR_EN] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(292.0000 mm, 147.5000 mm): Via [SOLENOID_PWR_EN] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[hole_clearance]: Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0000 mm)
    Rule: board setup constraints hole; error
    @(292.0000 mm, 147.5000 mm): Via [SOLENOID_PWR_EN] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[shorting_items]: Items shorting two nets (nets /BROTHER-CONNECTORS/EOL_R_N and SOLENOID_PWR_EN)
    Local override; error
    @(304.3500 mm, 147.4000 mm): Track [/BROTHER-CONNECTORS/EOL_R_N] on F.Cu, length 28.6900 mm
    @(292.0000 mm, 147.5000 mm): Track [SOLENOID_PWR_EN] on F.Cu, length 3.1069 mm
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(292.0000 mm, 147.5000 mm): Track [SOLENOID_PWR_EN] on F.Cu, length 3.1069 mm
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[tracks_crossing]: Tracks crossing
    Local override; error
    @(301.0000 mm, 149.0620 mm): Track [SOLENOID_12V_SW] on F.Cu, length 2.2620 mm
    @(304.3500 mm, 147.4000 mm): Track [/BROTHER-CONNECTORS/EOL_R_N] on F.Cu, length 28.6900 mm
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(301.0000 mm, 149.0620 mm): Track [SOLENOID_12V_SW] on F.Cu, length 2.2620 mm
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[clearance]: Clearance violation ( clearance 0.1000 mm; actual 0.0500 mm)
    Local override; error
    @(301.0000 mm, 146.8000 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(304.3500 mm, 147.4000 mm): Track [/BROTHER-CONNECTORS/EOL_R_N] on F.Cu, length 28.6900 mm
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(301.0000 mm, 146.8000 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[hole_clearance]: Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0805 mm)
    Rule: board setup constraints hole; error
    @(301.0000 mm, 146.8000 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(301.0000 mm, 146.8000 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[hole_clearance]: Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0000 mm)
    Rule: board setup constraints hole; error
    @(301.0000 mm, 146.8000 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(301.0000 mm, 146.8000 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[hole_clearance]: Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0000 mm)
    Rule: board setup constraints hole; error
    @(301.0000 mm, 146.8000 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(301.0000 mm, 146.8000 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[hole_clearance]: Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0000 mm)
    Rule: board setup constraints hole; error
    @(301.0000 mm, 146.8000 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0805 mm)
    Local override; error
    @(299.2000 mm, 146.8000 mm): Track [SOLENOID_12V_SW] on F.Cu, length 1.8000 mm
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(301.0000 mm, 146.8000 mm): Track [SOLENOID_12V_SW] on In1.Cu, length 15.7000 mm
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[shorting_items]: Items shorting two nets (nets SOLENOID_12V_SW and GND)
    Local override; error
    @(95.6500 mm, 162.5000 mm): Track [SOLENOID_12V_SW] on In1.Cu, length 215.2600 mm
    @(247.0300 mm, 161.1350 mm): PTH pad S1 [GND] of J501
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(95.6500 mm, 162.5000 mm): Track [SOLENOID_12V_SW] on In1.Cu, length 215.2600 mm
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(116.8400 mm, 153.7850 mm): Track [SOLENOID_12V_SW] on In1.Cu, length 8.7150 mm
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(114.8400 mm, 153.7850 mm): Track [SOLENOID_12V_SW] on In1.Cu, length 8.7150 mm
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[shorting_items]: Items shorting two nets (nets /BROTHER-CONNECTORS/SOL_0 and SOLENOID_12V_SW)
    Local override; error
    @(118.8400 mm, 153.7852 mm): PTH pad 8 [/BROTHER-CONNECTORS/SOL_0] of J401
    @(119.2400 mm, 146.2800 mm): Track [SOLENOID_12V_SW] on In1.Cu, length 16.2200 mm
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(119.2400 mm, 146.2800 mm): Track [SOLENOID_12V_SW] on In1.Cu, length 16.2200 mm
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(116.7400 mm, 146.2800 mm): Track [SOLENOID_12V_SW] on In1.Cu, length 16.2200 mm
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(310.9100 mm, 138.8300 mm): Track [SOLENOID_12V_SW] on In1.Cu, length 23.6700 mm
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(308.4100 mm, 138.8300 mm): Track [SOLENOID_12V_SW] on In1.Cu, length 23.6700 mm
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[shorting_items]: Items shorting two nets (nets /SOLENOID DRIVERS/MCU_SOL_7 and SOLENOID_12V_SW)
    Local override; error
    @(132.8950 mm, 136.8500 mm): Pad 1 [/SOLENOID DRIVERS/MCU_SOL_7] of U302 on F.Cu
    @(132.8950 mm, 136.8500 mm): Track [SOLENOID_12V_SW] on F.Cu, length 1.4000 mm
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(132.8950 mm, 136.8500 mm): Track [SOLENOID_12V_SW] on F.Cu, length 1.4000 mm
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(134.2950 mm, 136.8500 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[hole_clearance]: Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0000 mm)
    Rule: board setup constraints hole; error
    @(134.2950 mm, 136.8500 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(134.2950 mm, 136.8500 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[hole_clearance]: Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0000 mm)
    Rule: board setup constraints hole; error
    @(134.2950 mm, 136.8500 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(134.2950 mm, 136.8500 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[hole_clearance]: Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0000 mm)
    Rule: board setup constraints hole; error
    @(134.2950 mm, 136.8500 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[shorting_items]: Items shorting two nets (nets SOLENOID_12V_SW and /BROTHER-CONNECTORS/SOL_5)
    Local override; error
    @(134.2950 mm, 136.8500 mm): Track [SOLENOID_12V_SW] on In1.Cu, length 25.6500 mm
    @(134.2400 mm, 146.2800 mm): PTH pad 3 [/BROTHER-CONNECTORS/SOL_5] of J406
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(134.2950 mm, 136.8500 mm): Track [SOLENOID_12V_SW] on In1.Cu, length 25.6500 mm
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[shorting_items]: Items shorting two nets (nets GND and SOLENOID_12V_SW)
    Local override; error
    @(122.1750 mm, 136.3750 mm): Pad 2 [GND] of C605 on F.Cu
    @(120.3450 mm, 136.8500 mm): Track [SOLENOID_12V_SW] on F.Cu, length 1.4000 mm
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0906 mm)
    Local override; error
    @(120.3450 mm, 136.8500 mm): Track [SOLENOID_12V_SW] on F.Cu, length 1.4000 mm
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[shorting_items]: Items shorting two nets (nets GND and SOLENOID_12V_SW)
    Local override; error
    @(122.1750 mm, 136.3750 mm): Pad 2 [GND] of C605 on F.Cu
    @(121.7450 mm, 136.8500 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(121.7450 mm, 136.8500 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[hole_clearance]: Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.1406 mm)
    Rule: board setup constraints hole; error
    @(121.7450 mm, 136.8500 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(121.7450 mm, 136.8500 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[hole_clearance]: Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0000 mm)
    Rule: board setup constraints hole; error
    @(121.7450 mm, 136.8500 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(121.7450 mm, 136.8500 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[hole_clearance]: Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0000 mm)
    Rule: board setup constraints hole; error
    @(121.7450 mm, 136.8500 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(121.7450 mm, 136.8500 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[hole_clearance]: Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0000 mm)
    Rule: board setup constraints hole; error
    @(121.7450 mm, 136.8500 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[shorting_items]: Items shorting two nets (nets /BROTHER-CONNECTORS/SOL_0 and SOLENOID_12V_SW)
    Local override; error
    @(121.7400 mm, 146.2800 mm): PTH pad 8 [/BROTHER-CONNECTORS/SOL_0] of J406
    @(121.7450 mm, 136.8500 mm): Track [SOLENOID_12V_SW] on In1.Cu, length 25.6500 mm
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(121.7450 mm, 136.8500 mm): Track [SOLENOID_12V_SW] on In1.Cu, length 25.6500 mm
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[shorting_items]: Items shorting two nets (nets GND and SOLENOID_12V_SW)
    Local override; error
    @(109.6250 mm, 136.3750 mm): Pad 2 [GND] of C604 on F.Cu
    @(107.7950 mm, 136.8500 mm): Track [SOLENOID_12V_SW] on F.Cu, length 1.4000 mm
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0906 mm)
    Local override; error
    @(107.7950 mm, 136.8500 mm): Track [SOLENOID_12V_SW] on F.Cu, length 1.4000 mm
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[shorting_items]: Items shorting two nets (nets GND and SOLENOID_12V_SW)
    Local override; error
    @(109.6250 mm, 136.3750 mm): Pad 2 [GND] of C604 on F.Cu
    @(109.1950 mm, 136.8500 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(109.1950 mm, 136.8500 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[hole_clearance]: Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.1406 mm)
    Rule: board setup constraints hole; error
    @(109.1950 mm, 136.8500 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(109.1950 mm, 136.8500 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[hole_clearance]: Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0000 mm)
    Rule: board setup constraints hole; error
    @(109.1950 mm, 136.8500 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(109.1950 mm, 136.8500 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[hole_clearance]: Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0000 mm)
    Rule: board setup constraints hole; error
    @(109.1950 mm, 136.8500 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(109.1950 mm, 136.8500 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[hole_clearance]: Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0000 mm)
    Rule: board setup constraints hole; error
    @(109.1950 mm, 136.8500 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[shorting_items]: Items shorting two nets (nets /BROTHER-CONNECTORS/SOL_F and SOLENOID_12V_SW)
    Local override; error
    @(110.0800 mm, 146.2200 mm): PTH pad 1 [/BROTHER-CONNECTORS/SOL_F] of J407
    @(109.1950 mm, 136.8500 mm): Track [SOLENOID_12V_SW] on In1.Cu, length 25.6500 mm
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(109.1950 mm, 136.8500 mm): Track [SOLENOID_12V_SW] on In1.Cu, length 25.6500 mm
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[shorting_items]: Items shorting two nets (nets GND and SOLENOID_12V_SW)
    Local override; error
    @(109.6250 mm, 142.2750 mm): Pad 2 [GND] of C302 on F.Cu
    @(109.6250 mm, 142.2750 mm): Track [SOLENOID_12V_SW] on F.Cu, length 1.4000 mm
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(109.6250 mm, 142.2750 mm): Track [SOLENOID_12V_SW] on F.Cu, length 1.4000 mm
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.3905 mm)
    Local override; error
    @(111.0250 mm, 142.2750 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(111.0250 mm, 142.2750 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[hole_clearance]: Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0000 mm)
    Rule: board setup constraints hole; error
    @(111.0250 mm, 142.2750 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(111.0250 mm, 142.2750 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[hole_clearance]: Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0000 mm)
    Rule: board setup constraints hole; error
    @(111.0250 mm, 142.2750 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(111.0250 mm, 142.2750 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[hole_clearance]: Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0000 mm)
    Rule: board setup constraints hole; error
    @(111.0250 mm, 142.2750 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[shorting_items]: Items shorting two nets (nets SOLENOID_12V_SW and /BROTHER-CONNECTORS/SOL_F)
    Local override; error
    @(111.0250 mm, 142.2750 mm): Track [SOLENOID_12V_SW] on In1.Cu, length 20.2250 mm
    @(110.0800 mm, 146.2200 mm): PTH pad 1 [/BROTHER-CONNECTORS/SOL_F] of J407
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(111.0250 mm, 142.2750 mm): Track [SOLENOID_12V_SW] on In1.Cu, length 20.2250 mm
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[shorting_items]: Items shorting two nets (nets SOLENOID_12V_SW and GND)
    Local override; error
    @(122.1750 mm, 142.2750 mm): Track [SOLENOID_12V_SW] on F.Cu, length 1.4000 mm
    @(122.1750 mm, 142.2750 mm): Pad 2 [GND] of C303 on F.Cu
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(122.1750 mm, 142.2750 mm): Track [SOLENOID_12V_SW] on F.Cu, length 1.4000 mm
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.3905 mm)
    Local override; error
    @(123.5750 mm, 142.2750 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(123.5750 mm, 142.2750 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[hole_clearance]: Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0000 mm)
    Rule: board setup constraints hole; error
    @(123.5750 mm, 142.2750 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(123.5750 mm, 142.2750 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[hole_clearance]: Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0000 mm)
    Rule: board setup constraints hole; error
    @(123.5750 mm, 142.2750 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(123.5750 mm, 142.2750 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[hole_clearance]: Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0000 mm)
    Rule: board setup constraints hole; error
    @(123.5750 mm, 142.2750 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[shorting_items]: Items shorting two nets (nets SOLENOID_12V_SW and /BROTHER-CONNECTORS/SOL_2)
    Local override; error
    @(123.5750 mm, 142.2750 mm): Track [SOLENOID_12V_SW] on In1.Cu, length 20.2250 mm
    @(122.8400 mm, 153.7852 mm): PTH pad 6 [/BROTHER-CONNECTORS/SOL_2] of J401
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(123.5750 mm, 142.2750 mm): Track [SOLENOID_12V_SW] on In1.Cu, length 20.2250 mm
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[shorting_items]: Items shorting two nets (nets GND and SOLENOID_12V_SW)
    Local override; error
    @(97.0500 mm, 142.2750 mm): Pad 2 [GND] of C304 on F.Cu
    @(97.0500 mm, 142.2750 mm): Track [SOLENOID_12V_SW] on F.Cu, length 1.4000 mm
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(97.0500 mm, 142.2750 mm): Track [SOLENOID_12V_SW] on F.Cu, length 1.4000 mm
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(95.6500 mm, 142.2750 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[hole_clearance]: Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0000 mm)
    Rule: board setup constraints hole; error
    @(95.6500 mm, 142.2750 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(95.6500 mm, 142.2750 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[hole_clearance]: Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0000 mm)
    Rule: board setup constraints hole; error
    @(95.6500 mm, 142.2750 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(95.6500 mm, 142.2750 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[hole_clearance]: Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0000 mm)
    Rule: board setup constraints hole; error
    @(95.6500 mm, 142.2750 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(95.6500 mm, 142.2750 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[hole_clearance]: Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0000 mm)
    Rule: board setup constraints hole; error
    @(95.6500 mm, 142.2750 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[shorting_items]: Items shorting two nets (nets SOLENOID_12V_SW and /BROTHER-CONNECTORS/SOL_9)
    Local override; error
    @(95.6500 mm, 142.2750 mm): Track [SOLENOID_12V_SW] on In1.Cu, length 20.2250 mm
    @(95.5700 mm, 153.7852 mm): PTH pad 7 [/BROTHER-CONNECTORS/SOL_9] of J402
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(95.6500 mm, 142.2750 mm): Track [SOLENOID_12V_SW] on In1.Cu, length 20.2250 mm
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[hole_clearance]: Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.1119 mm)
    Rule: board setup constraints hole; error
    @(292.1050 mm, 154.6348 mm): NPTH pad of J601
    @(290.8000 mm, 154.5000 mm): Via [GND] on F.Cu - B.Cu
[shorting_items]: Items shorting two nets (nets /PSU/INP_2 and GND)
    Local override; error
    @(297.6050 mm, 153.0348 mm): Pad 3 [/PSU/INP_2] of J601 on F.Cu
    @(296.5625 mm, 151.9500 mm): Pad 2 [GND] of Q806 on F.Cu
[hole_clearance]: Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0000 mm)
    Rule: board setup constraints hole; error
    @(109.6250 mm, 136.3750 mm): Pad 2 [GND] of C604 on F.Cu
    @(109.1950 mm, 136.8500 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
[hole_clearance]: Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0000 mm)
    Rule: board setup constraints hole; error
    @(122.1750 mm, 136.3750 mm): Pad 2 [GND] of C605 on F.Cu
    @(121.7450 mm, 136.8500 mm): Via [SOLENOID_12V_SW] on F.Cu - B.Cu
[hole_clearance]: Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0000 mm)
    Rule: board setup constraints hole; error
    @(301.9500 mm, 149.0625 mm): Pad 1 [Net-(Q805-G)] of Q805 on F.Cu
    @(302.4300 mm, 149.4200 mm): Via [GND] on F.Cu - B.Cu
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(301.9500 mm, 149.0625 mm): Pad 1 [Net-(Q805-G)] of Q805 on F.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[hole_clearance]: Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0000 mm)
    Rule: board setup constraints hole; error
    @(300.0500 mm, 149.0625 mm): Pad 2 [+12V] of Q805 on F.Cu
    @(299.7100 mm, 149.4200 mm): Via [GND] on F.Cu - B.Cu
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(300.0500 mm, 149.0625 mm): Pad 2 [+12V] of Q805 on F.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[clearance]: Clearance violation ( clearance 0.1000 mm; actual 0.0500 mm)
    Local override; error
    @(301.0000 mm, 150.9375 mm): Pad 3 [SOLENOID_12V_SW] of Q805 on F.Cu
    @(301.8250 mm, 150.9380 mm): Pad 1 [+12V] of R820 on F.Cu
[hole_clearance]: Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.2200 mm)
    Rule: board setup constraints hole; error
    @(301.0000 mm, 150.9375 mm): Pad 3 [SOLENOID_12V_SW] of Q805 on F.Cu
    @(300.2800 mm, 150.5000 mm): Via [GND] on F.Cu - B.Cu
[clearance]: Clearance violation ( clearance 0.1000 mm; actual 0.0500 mm)
    Local override; error
    @(301.0000 mm, 150.9375 mm): Pad 3 [SOLENOID_12V_SW] of Q805 on F.Cu
    @(300.1750 mm, 150.9380 mm): Pad 2 [Net-(Q805-G)] of R820 on F.Cu
[hole_clearance]: Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.1400 mm)
    Rule: board setup constraints hole; error
    @(301.0000 mm, 150.9375 mm): Pad 3 [SOLENOID_12V_SW] of Q805 on F.Cu
    @(301.6400 mm, 150.5000 mm): Via [GND] on F.Cu - B.Cu
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(301.0000 mm, 150.9375 mm): Pad 3 [SOLENOID_12V_SW] of Q805 on F.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(296.5625 mm, 150.0500 mm): Pad 1 [Net-(Q806-G)] of Q806 on F.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[hole_clearance]: Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0000 mm)
    Rule: board setup constraints hole; error
    @(298.4375 mm, 151.0000 mm): Pad 3 [Net-(Q805-G)] of Q806 on F.Cu
    @(298.9200 mm, 150.5000 mm): Via [GND] on F.Cu - B.Cu
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(298.4375 mm, 151.0000 mm): Pad 3 [Net-(Q805-G)] of Q806 on F.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[hole_clearance]: Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0000 mm)
    Rule: board setup constraints hole; error
    @(301.8250 mm, 150.9380 mm): Pad 1 [+12V] of R820 on F.Cu
    @(301.6400 mm, 150.5000 mm): Via [GND] on F.Cu - B.Cu
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(301.8250 mm, 150.9380 mm): Pad 1 [+12V] of R820 on F.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[hole_clearance]: Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0000 mm)
    Rule: board setup constraints hole; error
    @(300.1750 mm, 150.9380 mm): Pad 2 [Net-(Q805-G)] of R820 on F.Cu
    @(300.2800 mm, 150.5000 mm): Via [GND] on F.Cu - B.Cu
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(300.1750 mm, 150.9380 mm): Pad 2 [Net-(Q805-G)] of R820 on F.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(293.7750 mm, 150.0500 mm): Pad 1 [SOLENOID_PWR_EN] of R821 on F.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(295.4250 mm, 150.0500 mm): Pad 2 [Net-(Q806-G)] of R821 on F.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(292.8250 mm, 153.0000 mm): Pad 2 [Net-(Q806-G)] of R822 on F.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[clearance]: Clearance violation (zone clearance 0.5000 mm; actual 0.0000 mm)
    Local override; error
    @(299.2000 mm, 146.8000 mm): Pad 1 [SOLENOID_12V_SW] of TP703 on F.Cu
    @(34.5500 mm, 85.9000 mm): Zone [GND] on F.Cu, B.Cu and 2 more, priority 0
[track_dangling]: Track has unconnected end
    Local override; warning
    @(116.8400 mm, 151.6100 mm): Track [+12V] on F.Cu, length 3.3941 mm
[track_dangling]: Track has unconnected end
    Local override; warning
    @(119.2426 mm, 140.1026 mm): Track [+12V] on B.Cu, length 1.0926 mm

** Found 9 unconnected pads **
[unconnected_items]: Missing connection between items
    Local override; error
    @(68.3200 mm, 143.7400 mm): Track [+12V] on B.Cu, length 17.1800 mm
    @(99.1200 mm, 139.3200 mm): Track [+12V] on F.Cu, length 2.3300 mm
[unconnected_items]: Missing connection between items
    Local override; error
    @(116.8400 mm, 151.6100 mm): Track [+12V] on F.Cu, length 3.3941 mm
    @(124.0050 mm, 141.8000 mm): Track [+12V] on F.Cu, length 2.3450 mm
[unconnected_items]: Missing connection between items
    Local override; error
    @(301.9500 mm, 150.9380 mm): Track [+12V] on F.Cu, length 0.1250 mm
    @(300.0500 mm, 149.0625 mm): Pad 2 [+12V] of Q805 on F.Cu
[unconnected_items]: Missing connection between items
    Local override; error
    @(97.0500 mm, 142.2750 mm): Track [SOLENOID_12V_SW] on F.Cu, length 1.4000 mm
    @(97.0500 mm, 140.3750 mm): Pad 1 [SOLENOID_12V_SW] of C304 on F.Cu
[unconnected_items]: Missing connection between items
    Local override; error
    @(98.9050 mm, 141.8000 mm): Pad 9 [SOLENOID_12V_SW] of U304 on F.Cu
    @(97.0500 mm, 142.2750 mm): Track [SOLENOID_12V_SW] on F.Cu, length 1.4000 mm
[unconnected_items]: Missing connection between items
    Local override; error
    @(109.6250 mm, 142.2750 mm): Track [SOLENOID_12V_SW] on F.Cu, length 1.4000 mm
    @(109.6250 mm, 140.3750 mm): Pad 1 [SOLENOID_12V_SW] of C302 on F.Cu
[unconnected_items]: Missing connection between items
    Local override; error
    @(122.1750 mm, 140.3750 mm): Pad 1 [SOLENOID_12V_SW] of C303 on F.Cu
    @(122.1750 mm, 142.2750 mm): Track [SOLENOID_12V_SW] on F.Cu, length 1.4000 mm
[unconnected_items]: Missing connection between items
    Local override; error
    @(301.0000 mm, 150.9375 mm): Pad 3 [SOLENOID_12V_SW] of Q805 on F.Cu
    @(301.0000 mm, 149.0620 mm): Track [SOLENOID_12V_SW] on F.Cu, length 2.2620 mm
[unconnected_items]: Missing connection between items
    Local override; error
    @(300.0500 mm, 150.9380 mm): Track [Net-(Q805-G)] on F.Cu, length 0.1250 mm
    @(301.9500 mm, 149.0625 mm): Pad 1 [Net-(Q805-G)] of Q805 on F.Cu

** Found 0 Footprint errors **

** End of Report **
```

## DesignChecks files

