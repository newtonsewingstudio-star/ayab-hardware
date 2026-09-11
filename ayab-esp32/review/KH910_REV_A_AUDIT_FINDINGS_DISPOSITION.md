# KH910 Rev A — Independent Audit Findings Disposition

Audit input: external static review of commit `e3dd936`.

Status: the first two audit rounds were closed, and the later independent KiCad 9/10 audit of commit `647998e` produced repair order F1–F12. Those items are closed in the corrected commit containing `KH910_REV_A_EXTERNAL_AUDIT_REPAIR_CLOSURE.md`. The final claim remains conditional on the corrected branch CI run being green; physical first-article and energized tests remain separate post-assembly gates.

| Finding | Disposition | Closure evidence required |
|---|---|---|
| P1: GPIO4 exposed if R216 opens | Closed in design. D205 upper clamp, D206 lower clamp, and C206 filter are integrated while R215 remains the independent current limiter. | Schematic/PCB pin parity, 0/0/0 KiCad DRC, zero ERC errors, and visual review passed. |
| P1: divider transient margin thin | Closed for one-prototype design release. The clamps bound ordinary positive/negative excursions and C206 filters fast noise; this is not claimed as surge certification. | Part identity/polarity audit and clamp-current calculation passed. Measured rail/ADC/transient data remains a first-bring-up requirement. |
| P2: solenoid gate fault tree incomplete | Closed in review. The component open/short cases and unsafe residuals are explicit in the fail-safe review. | Topology validation passed; supervised no-coil reset/brownout tests remain required after assembly. |
| P2: I/O map called itself a draft/authority | Closed. The map is a human-readable interface contract; native KiCad is the electrical authority and the generated pin audit is the reconciliation. | Current pin audit and topology checks passed. |
| P3: iterative script churn/self-audit provenance | Mitigated, not erased. Staging scripts are not release evidence by themselves. | CI rederived KiCad/ERC/DRC and topology evidence from frozen source; the external auditor is still asked to reproduce it independently. |
| P3: internal PASS language could be misread | Closed editorially. PASS is expressly limited to manufacture and supervised bring-up of one prototype. | Final wording retains the non-certification and unperformed physical-test limits. |

## Round 2 external review

The auditor independently verified every hash in the 222-file `09fa402` handoff package and accepted the two protected-sense findings, the solenoid-gate fault-tree finding, and the I/O-map authority finding as closed. The auditor also accepted the revised PASS wording and agreed that the iterative-tooling provenance issue is mitigated but cannot be erased by more author-generated evidence.

The auditor could not independently access the GitHub repository or run KiCad in the available review environment. The package's CI links, stored DRC/ERC reports, and generated topology reports therefore remain independently unreproduced. A KiCad-equipped reviewer must run the native-source checks before the first PCB order.

The physical measurements listed in the fail-safe review require an assembled board. They are a post-assembly, pre-solenoid-operation gate—not a pre-fabrication gate.

The Round 2 reviewer also identified an audit-trail wording error in the handoff: the preliminary-notes file was a faithful structured summary, not a verbatim transcript. Future packages use that accurate description.

No fabrication files are part of this correction or its evidence package.

## Independent KiCad audit repair order

The full F1–F12 disposition, including corrected ordering metadata, GPIO3 isolation, capacitor-rail parity, DNP flags, native instance paths, local-library pinning, fault-tree expansion, manufacturing limits, current derating, and visual/silkscreen cleanup, is recorded in `KH910_REV_A_EXTERNAL_AUDIT_REPAIR_CLOSURE.md`.

The authoritative CI workflow now runs full KiCad 9 schematic parity plus all frozen Rev A audits. Its former jobset step was removed because that jobset includes fabrication-output jobs and therefore does not belong in design-only validation.
