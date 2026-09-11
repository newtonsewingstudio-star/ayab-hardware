# KH910 Rev A — External Audit Repair Closure

Audit basis: independent KiCad 9/10 report for commit `647998e`.

Corrected revision: the commit containing this document. All statements below are pre-fabrication CAD conclusions; post-assembly electrical and thermal tests remain unperformed.

| ID | Closure in the corrected source |
|---|---|
| F1 | R820/R821/R822 values, manufacturer parts, and LCSC identifiers agree between schematic and PCB. |
| F2 | R735–R738 are consistently 10 kΩ with the intended 10 kΩ ordering metadata. |
| F3 | GPIO3 is reserved/no-connect at U201; the unrelated J701/U701 local channel remains intact and is no longer tied to the ESP32 strap pin. |
| F4 | C603/C604/C605 are consistently on `SOLENOID_12V_SW`; their switched capacitance is included in the power-gate review. |
| F5 | R501, R701–R707, R709, R711, and R713 have matching schematic and PCB DNP intent. |
| F6 | D205/D206/C206 carry valid native instance paths; KiCad 9 full schematic parity reports zero footprint errors. |
| F7 | R209/R210 are represented in the schematic as the intended 5.1 kΩ I²C pull-ups. |
| F8 | The fail-safe fault tree distinguishes software lockup, hard stuck pins, open terminals, shorts, overcurrent, startup charge, and unsafe residual faults. |
| F9 | All used custom symbol and footprint libraries are project-pinned. D601 has a custom bridge identity. Board-house limits and the remaining first-article mechanical checks are explicit. |
| F10 | Obsolete comparator remnants and aliases were removed, GPIO/pin documentation was reconciled, Hall test-point names were corrected, the gate-area C legend was removed, the obsolete revision badge was replaced, and gate/test/clamp polarity cues were added. |
| F11 | The permitted bridge/solenoid/current/duty envelope is documented; the 1.37 A MOSFET stress case is explicitly prohibited as an operating point. |
| F12 | Critical package/ordering metadata and the reported D204/D605/D606 associations were normalized. KiCad 10 ERC is clean in the configured local-library environment. |

## Required release evidence

- KiCad 9 DRC with full schematic parity: 0 violations, 0 unconnected pads, 0 footprint errors, 0 parity issues.
- KiCad ERC: 0 errors. A properly configured KiCad 10 installation also reports 0 warnings.
- All eight frozen Rev A source/topology/parity audits pass.
- Manufacturing metadata validator passes all ordering, DNP, and pinned-footprint checks.
- Updated top and bottom native renders receive visual review.
- The branch CI run for this corrected commit is green.

The design-check workflow no longer executes the repository jobset because that jobset contains manufacturing-output jobs. CI performs only read-only ERC, DRC/parity, topology, pin-map, library, and metadata validation.

No fabrication files are produced by this closure.
