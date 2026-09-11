# Independent audit of 9bde764

The preserved [audit report](AYAB_KH910_Final_Preorder_Audit_9bde764.md) concludes PASS for one controlled, bare prototype PCB, subject to its documented physical-test gates before machine or solenoid use. The [evidence archive](AYAB_KH910_Final_Preorder_Audit_9bde764_Evidence.zip) contains the separate KiCad 9.0.9 and KiCad 10.0.6 checks, native renders, independent comparisons, CI records and repair verification. `SHA256SUMS.txt` verifies these exact archived artifacts.

The report describes an audit of commit `9bde764c6e157920af34ccd1063949ac5dcc5109` and subsequent isolated repairs. Its statements that the original repository was unchanged and repairs were uncommitted are historical statements about completion of that audit. This repository update now incorporates those repairs:

- Include artwork footprints in revision-label clearance checks.
- Correct the current KiCad 10 Package-field diagnostic reference to TP703 in two closure notes.
- Add regression tests for the real label position, artwork overlap and the previous pad overlap.

PCB, schematic, project settings and libraries were not changed by these repairs. No fabrication outputs are included or were generated for this update. Physical assembly, fit, power sequencing, current and thermal testing remain unperformed.
