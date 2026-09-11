# AYAB KH910 Rev A — Final independent audit and repairs

**Verdict: PASS — suitable for ordering one controlled, unassembled prototype PCB in the documented four-layer/M2 configuration. No unresolved pre-order CAD condition was found after this audit's two small repairs. Physical qualification is still required before machine installation or solenoid operation.**

Reviewed repository: [newtonsewingstudio-star/ayab-hardware](https://github.com/newtonsewingstudio-star/ayab-hardware). Branch: `ayab-esp32-kh910-rev-a`. Packaged/current remote head: **9bde764c6e157920af34ccd1063949ac5dcc5109**. Underlying CAD repair commit: **231ab3c9c348c4bb3880c5ed453855c066cb82e0**. Baseline: **00b397811cd4ecf61d68ad1d0c13dd36463a22ea**. Audit date: 11 September 2026.

The two previous P2 conditions are closed: the revision marking is clear, and all footprint-tree object identities are unique. Fresh KiCad 9.0.9 checks show **0 DRC violations, 0 unconnected pads, 0 footprint errors and 0 schematic-parity issues**. ERC has **0 errors**, with 78 classified standard-power-library warnings. All nine repository validators pass. Independent comparisons verify 670 numbered PCB pins, 193 native schematic associations, all 11 required DNP decisions and all 23 custom-footprint instances.

Two additional P3 issues were found and repaired in the delivered isolated source: the clearance validator omitted artwork footprints, and two current compatibility documents named the wrong test point. Three regression tests pass. **No PCB, schematic, library, project setting, component value, routing or purchasing field required alteration.** The delivered source is the reviewed commit's selected source content plus these local script/document/test repairs; it is not a newly committed or CI-tested Git revision.

## 1. Authorization, scope and source integrity

The user's latest instruction authorizes auditing and repairing remaining issues. The package's handoff and stored reports were treated as evidence, not instructions or proof. Source inspection, native checks, independent comparisons and repair verification were carried out locally. No commit, push, order or workflow was initiated. No fabrication files were generated.

The original ZIP contains 318 files, and all **317 entries in its manifest pass**. Its SHA-256 is:

```text
b2d87d5c008ee1a2fa3f6d835ec32999c834e26781ea21fe2cb31b41c8e650c3
```

All **310 packaged Git-tracked paths match a fresh Git archive byte for byte**. A further comparison directly against raw Git objects avoids confusing archive conversion with Git storage: **18 files are byte-identical to their raw Git objects; all 310 match after CRLF/LF normalization**. The difference in the other 292 files is solely newline representation, including the native KiCad text files. Thus the package matches the committed source content, but this report does not falsely call every package byte identical to its raw Git blob. The eight additional package files contain handoff, manifest, prior-audit, diff and CI evidence.

Local HEAD and the live remote agree on the full 9bde764 hash. The tracked original working tree remains clean. These three pre-existing untracked entries were left in place, and all 18 underlying file hashes remain unchanged:

```text
?? ayab-esp32/tools/__pycache__/
?? render-34512445704/
?? work-pcbnew-api.log
```

Separate disposable copies held KiCad 9 and KiCad 10 input. All 318 original files in each copy remain byte-unchanged. KiCad 10 added only its local `.kicad_prl` preference file. It did not save a migrated PCB or schematic. The original supplied ZIP is unchanged.

There is one AYAB-ESP32 PCB and eight schematic sheets including the root; no daughterboard. A recursive scan of the handoff, including its nested prior-audit archive, found no Gerber/drill/placement output. The full historical repository still contains ten unrelated AYAB-interface Gerbers, listed in the evidence; those are excluded from both delivered ZIPs.

## 2. Environment and fresh native checks

Primary: **KiCad 9.0.9**, official Windows runtime, Python 3.11.5, x64. Supplemental: **KiCad 10.0.6**, Windows installation, Python 3.11.5, x64. Host: Windows 10 Home 10.0.19045 x64. Auxiliary evidence processing used Python 3.12.14 and Node/Sharp.

Each version used separate configuration and temporary directories, configured standard symbol/footprint tables and its own native source copy. The project uses repository-pinned custom libraries. U701's standard 3D model was supplied through an external legacy-variable override using the same hash-verified official model as the previous audit; every 3D render in this audit includes that dependency. Exact paths, commands, environment settings, exit codes and full console outputs are preserved in the appendix and evidence.

The primary run reproduces the KiCad 9 release commands and acceptance criteria on Windows. It is not a byte-for-byte recreation of the Ubuntu CI runner. CI's dependency script selects the KiCad 9 release series; its exact installed patch version was not independently established from an installation log. KiCad 10 results remain supplemental.

| Native check | KiCad 9.0.9 — primary | KiCad 10.0.6 — supplemental |
|---|---|---|
| PCB DRC with violation-sensitive exit | Exit 0; 0 violations, 0 unconnected, 0 footprint errors | Exit 0; 0 violations, 0 unconnected, 0 footprint errors |
| Full schematic parity | Exit 0; console explicitly reports 0 parity issues | Exit 5; 187 field-mismatch warnings, classified below |
| ERC with violation-sensitive exit | Exit 5; 0 errors, 78 library warnings | Exit 0; 0 errors, 0 warnings |
| Fresh electrical netlist | Exit 0; no annotation warning | Exit 0; no annotation warning; identical net memberships |
| Front/back 2D and 3D exports | Exit 0 | Exit 0 |

KiCad 9's 78 ERC warnings are exclusively `lib_symbol_mismatch`: **43 GND, 19 +3V3, 10 +5V and 6 +12V**. Independent comparison of cached and standard symbols found the same pin numbers, types, positions and lengths; power pin-name metadata differs. These are not missing custom symbols or established electrical faults. They explain the warning-sensitive ERC exit 5. Some KiCad 9 exports emit a nonfatal Fontconfig message; the exports complete.

KiCad 10's 187 parity diagnostics are **164 Description differences, 22 Datasheet differences and one missing Package field on TP703 at (145,159)**. The previous duplicated-ID source reported TP701; the current fresh report identifies TP703. These are local metadata diagnostics, not disconnected copper or wrong component values. Broader independent comparison finds 183 Description and 22 Datasheet value differences; its scope differs from KiCad's report. No value, manufacturer, order-code, DNP or electrical-net mismatch was found. The inherited noncritical metadata was retained, with accurate compatibility documentation.

KiCad 10 uses tighter SVG page framing and a greener default 3D material appearance than KiCad 9. Both render the same component geometry and clear revision marking. No pixel-equivalence or actual manufactured solder-mask-color claim is made.

## 3. Closure of the previous findings

| Finding | Result | Independent evidence |
|---|---|---|
| N1 wrong diode purchasing identities | PASS, maintained | D204/D605/D606 remain SS54, C22452, MDD, SMA in active schematic and PCB. |
| N2 six stale schematic paths | PASS, maintained | R213/R214/R735–R738 match active instances; all 193 associations match. |
| N3 copper assumptions | PASS, maintained | 35 µm outer / 17.5 µm inner; modeled 1.6062 mm board. |
| N4 revision marking overlap | **CLOSED** | Label at (180,142), with clear pads, mask openings, outlines and artwork; independent geometry plus fresh populated render. |
| N5 conditional clamp-current wording | PASS, maintained | Conditional 3.6 V-node values remain separate from loose current bounds and GPIO safety claims. |
| N6 local model paths | PASS, maintained | All 165 local references match exact archive filename case; one standard model configured externally. |
| N7 critical metadata | PASS, maintained | Critical rectifier/bridge/clamp/isolation parts retain the corrected identities and purchasing fields. |
| N8 fabrication-free wording | PASS, maintained | Release package distinguished from historical unrelated Git Gerbers. |
| N9 annotation | PASS, maintained | No annotation warning in either fresh ERC/netlist export. |
| N10 mounting hardware | PASS, maintained | Six M2 values match 2.2 mm drills; physical chassis fit remains unmeasured. |
| N11 duplicated object IDs | **CLOSED** | 237 distinct footprint roots and 6,053 distinct footprint-tree UUIDs; no copied root or nested ID remains. |
| N12 supplemental metadata wording | **CLOSED in delivered repair** | Field types were described correctly, but the current affected reference is TP703. Two current source notes corrected. |
| N13 resistor-temperature assumption | **CLOSED** | Full -55 to +155 °C rated range used, maximum 130 °C departure; 45.919k minimum recalculated and manufacturer data checked. |

The complete revision text bounding box is **X=172.856428–187.143573, Y=141.303850–142.696150 mm** on front silk. An independent scan included actual mask expansion, 176 front courtyards derived from their graphic primitives, front body outlines, visible fields and artwork; 3,259 obstacle boxes were considered. No obstacle intersects the box plus a 0.20 mm margin. The nearest bounding-box obstacle is artwork, approximately **1.350677 mm** away. Expanded corners lie inside the native board outline; the actual location is visibly clear of the central slot and outer edge. Dimensions of vendor hardware still require physical confirmation.

The eight repaired footprint trees are R820/R821/R822/TP703/Q805/Q806/C206/D206. Four remaining repeated raw IDs each belong to a dimension and its own embedded dimension label. Their parent-child relationships are verified; they are not shared between distinct footprint objects. The native KiCad 9 loaded board also has 237 unique footprint root IDs.

After removing only object UUID fields and accounting for the declared label move, **the entire parsed PCB equals the previous audited board**. All 237 footprint geometries, placements, pads, layers, nets, schematic paths and DNP flags are preserved. All 1,734 straight track segments, 12 curved track segments, 252 vias, five zones, ten outline lines and ten outline arcs remain unchanged. Both fresh netlists retain the same 152 net memberships as 00b3978.

## 4. Original F1–F12 regression review

| Item | Fresh independent conclusion |
|---|---|
| F1 gate resistor identities | R820/R822 100k, C25803, 0603WAF1003T5E; R821 10k, C25804, 0603WAF1002T5E. Schematic/PCB agree. |
| F2 Hall dividers | R735–R738 remain 10k, C25804, 0603WAF1002T5E in both representations. |
| F3 GPIO3 isolation | U201.7 no-connect; J701.6/U701.16 and J701.7/U701.15 local channels retained. GPIO4 sense and GPIO17/18 end-stop paths intact. |
| F4 switched capacitors | C603/C604/C605 connect SOLENOID_12V_SW to GND. |
| F5 DNP | All eleven specified resistors agree: R501, R701–R707, R709, R711, R713. |
| F6 native parity | Direct KiCad 9 parity completes with zero issues; 193 associations and 670 numbered pins agree independently. |
| F7 I²C | R209/R210 remain 5k1 pull-ups from +3V3 to AYAB_SCL/AYAB_SDA. |
| F8 fault tree | Correct default-OFF topology with disclosed unsafe single faults; detailed review below. |
| F9 custom libraries/manufacturing | 18 custom footprint IDs / 23 instances match pinned full pad signatures; controlled rules and stackup unchanged. |
| F10 cleanup and labels | Active comparator remnants and R611 absent; Hall/K/L remain intact; old badges absent; required labels visible. Revision label now clear. |
| F11 current limits | 0.65 A total bridge average, ≤40 °C ambient, 0.25 A logic reserve, ≤four nominal 86 mA coils pending qualification. |
| F12 critical ordering metadata | D204/D601/D605/D606/U403/D205/D206 identities, descriptions, datasheets, packages and DNP reviewed; no material mismatch found. |

All 34 cached custom-symbol pin definitions agree with the pinned symbol library after normalizing equivalent hidden-pin syntax. The unused cached LM393 definition does not represent an active comparator. U702/U703, C703/C704, R715–R734 and R611 remain absent from active native components.

## 5. Machine-sense and power-isolation analysis

Independently traced topology:

| Component/pin | Native connection |
|---|---|
| R215, 47k | +12V to MACHINE_PWR_SENSE |
| R216, 10k | MACHINE_PWR_SENSE to GND |
| U201.8 / GPIO4 | MACHINE_PWR_SENSE |
| D205 | cathode/pad 1 = +3V3; anode/pad 2 = sense |
| D206 | cathode/pad 1 = sense; anode/pad 2 = GND |
| C206, 100n | sense to GND |

The divider ratio is 10/57 = 0.1754386. The nominal filter time constant is approximately 0.825 ms. R215 remains in series independently of R216 and limits current when R216 is open.

| Raw voltage | Unclamped divider voltage | R216-open current, nominal R215 and assumed 3.6 V node | Loose current with node ≥0 V and R215=45.919k |
|---:|---:|---:|---:|
| 12 V | 2.1053 V | 0.1787 mA | 0.2613 mA |
| 15 V | 2.6316 V | 0.2426 mA | 0.3267 mA |
| 40 V | 7.0175 V; clamps must conduct | 0.7745 mA | 0.8711 mA |

The updated arithmetic uses `47000 × (1 − 0.01 − 100e-6 × 130) = 45919 ohms`. The 0603, 47k part's -55 to +155 °C operating range, ±1% tolerance and ±100 ppm/°C TCR are supported by the [UNI-ROYAL manufacturer datasheet, ratings and TCR tables](https://datasheet.lcsc.com/datasheet/pdf/0a975aaa49b7c97f38a963127be4a823.pdf?productCode=C25819). Maximum departure from 25 °C is 130 °C. This removes the previous unsupported inference from ambient maximum to element temperature. The bounds still assume a nonnegative sense node and the resistor within its applicable specifications; they are not a guarantee after damage, aging, overload or improper assembly. Temperature-range coverage does not waive power derating or certify the clamp voltage.

Residual limitations remain: an R215 short removes the independent limiter; wrong/missing clamps defeat the intended polarity; lost or rising +3V3 can back-power the rail; diode forward voltage/leakage and transient duration matter. No ESP32 injection-current allowance, certified surge waveform performance or guaranteed maximum GPIO voltage is assumed. R216-open testing and realistic supply/transient measurement remain physical gates.

D205/D206 use Comchip CDBU0130-HF / C2886021 with consistent polarity and metadata. Their deliberately accepted 0603 land pattern is a controlled prototype choice, not a claim that it exactly equals the manufacturer's recommended land pattern. Inspect actual assembly wetting and orientation. The [Comchip datasheet](https://datasheet.lcsc.com/datasheet/pdf/5aaa32c8ca1bb3249827196c5b1a5057.pdf?productCode=C2886021) remains the component reference.

U403 remains TI LM66100DCKR / C2869734 / SC-70-6. VIN is `/PSU/5V_SW`, GND and unused ST are GND, CE and VOUT are +5V, and pin 4 is no-connect. The topology retains the intended machine/system 5 V isolation with R611 absent. See [TI LM66100 datasheet](https://www.ti.com/lit/ds/symlink/lm66100.pdf). Actual USB-only and combined-power back-feed behavior has not been measured.

## 6. Solenoid gate, faults and thermal limits

Q805 source/pad 2 is raw +12V; drain/pad 3 is SOLENOID_12V_SW; R820 pulls gate/pad 1 to source. Q806 source/pad 2 is GND, drain/pad 3 pulls the Q805 gate down, and its gate/pad 1 is driven from GPIO21/SOLENOID_PWR_EN through R821. R822 holds that gate low. Q805's body diode blocks ordinary raw-to-load feed in the off orientation. Intended common contacts, U302/U303/U304 COM pins, C603/C604/C605 and TP703 all use the switched rail.

At nominal 12 V, R820 gate current is approximately 120 µA. The 10k/100k Q806 input divider gives approximately 3.0 V gate drive from a 3.3 V command. Released GPIO, reset/boot, unpowered MCU and brownout therefore default to **static OFF under the no-fault assumptions**. USB-only supplies no machine 12 V. This is not proof of zero startup pulses or instantaneous discharge of load capacitors.

| Fault group | Independent result |
|---|---|
| R820 open or broken source connection | Q805 gate floats; unsafe residual. |
| R820 short / Q805 gate-source short | Q805 off initially, but Q806 enable can create raw-to-ground overcurrent. |
| R821 open / short | Open defaults Q806 off through R822; short loses drive-current isolation but does not itself command on. |
| R822 open / broken ground / short | Open or broken ground lets Q806 gate float; short holds off with limited GPIO load. |
| Q805 drain-source short | Rail permanently supplied; unsafe. |
| Q806 drain-source short | Q805 forced on; unsafe. |
| Q806 gate-source short | Off with about 0.33 mA GPIO load through R821. |
| Q805 or Q806 gate-drain short | Coupled gate/output networks can conduct or self-bias; not credited as safe OFF. |
| Missing MOSFET / open drain-source conduction path | Isolated forward/control path interrupted, static OFF. |
| Open internal gate lead | Internal gate can float despite the external resistor; unsafe/indeterminate. |
| Software-held GPIO21 high | Remains on until an effective watchdog/reset releases it. |
| Hard electrical GPIO21 stuck high | Reset cannot clear the fault; unsafe. |
| GPIO21 stuck low | Static OFF. |
| Raw-to-switched copper bridge | Bypasses Q805; unsafe. |
| Stored charge / startup coupling | No instantaneous-off assumption; scope power sequences. |
| Q805 beyond ±20 V VGS | Damage mode uncontrolled; unsafe. |

The updated fault tree correctly retains these limitations. It is neither redundant nor safety-rated, and no separate timed hardware watchdog is present. Firmware-held-high and physically stuck-high faults are correctly distinguished.

D601 is the KMB14F 1 A average-rated bridge and supplies logic as well as solenoids. Its custom pins are 1/2=AC inputs `/PSU/INP_1` and `/PSU/INP_2`, 3=+12V, 4=GND. Its name, custom symbol and footprint agree; do not substitute a differently numbered generic bridge. See the [FUXINSEMI KMB14F datasheet](https://datasheet.lcsc.com/datasheet/pdf/e72e2e5f3749444edb574593f092205f.pdf?productCode=C880909).

The 0.65 A total average bridge ceiling at ≤40 °C is an initial controlled test envelope, not a measured thermal rating. `0.25 + 4 × 0.086 = 0.594 A`, leaving 0.056 A margin. Five coils plus the logic reserve would be 0.680 A and exceed the ceiling. Measure logic current as the bridge-input contribution, and reduce the allowable coil count if needed. Sixteen-coil/all-coil operation and the 1.37 A stress example remain prohibited.

At 0.65 A and the assumed 70 mΩ Q805 resistance, dissipation is 0.0296 W and drop 45.5 mV. The actual solenoid branch excludes the logic contribution; this is a conservative nominal switch calculation, not a hot-device measurement. Shared routed trunks are 1.0/1.27 mm with 0.8/0.4 mm vias; narrow 0.25/0.35 mm branches are not credited with whole-bus capacity. No extra current capacity is credited to inner planes. Inrush, switching peaks, plating, thermal reliefs and actual temperatures require dummy-load qualification.

## 7. Visual, mechanical and manufacturing review

Fresh front/back copper/silk views, top/bottom populated 3D renders, body/courtyard views and inner layers were reviewed. The solenoid gate area, rear clamp cluster, connectors, high-current paths and revision marking show no newly established pre-order body/copper/connector obstruction. `SOLENOID GATE`, `TP703 SW`, `D205 K=3V3` and `D206 A=GND` are legible and correctly oriented. The revision date is clear of pads and populated bodies. Legacy silk over insulated copper is not itself an exposed-pad overlap.

The four-layer board remains nominal 1.6 mm, with modeled finished thickness 1.6062 mm, 35 µm outer copper, 17.5 µm inner copper and 1.0604 mm core. The approximate outline centerline extent is 285.122 × 48.102 mm; the rounded central slot is approximately 3.8 × 10.425 mm. Six grounded mounting holes remain 2.2 mm and require M2 hardware. No hole or connector was resized during this audit.

Project minima remain: 0.10 mm clearance, 0.10 mm track width, 0.25 mm copper-to-edge, 0.20 mm through-hole drill, 0.05 mm via annulus, 0.30 mm via diameter and 0.25 mm hole-to-hole clearance. DRC exclusions are empty. Some silk/courtyard/library diagnostic categories are ignored, so a clean DRC alone does not prove readable marking or physical clearance. Independent geometry and visual checks supplement it.

All custom placed pads were compared against the pinned files, preserving duplicate pad numbers and checking position, orientation, size, shape, layers, drill and explicit mask/paste/chamfer/round-rectangle parameters. All 23 instances match. All 165 local 3D paths resolve with exact case. U701's `${KICAD6_3DMODEL_DIR}/Package_SO.3dshapes/TSSOP-24_4.4x7.8mm_P0.65mm.wrl` uses an externally configured, hash-verified [official KiCad model](https://gitlab.com/kicad/libraries/kicad-packages3D/-/tree/3a3cad1c1a74b408e66a1ce8333eef16a6d7f3c4/Package_SO.3dshapes). No source path was changed to suit this computer.

Rendered models cannot establish actual connector mating force, harness access, vendor body tolerances, clamp solderability, standoff insulation or chassis fit. Those remain physical gates.

## 8. Issues found and repaired during this audit

No unresolved P0/P1/P2 finding was established. These two P3 issues are closed in the delivered isolated repair:

| Finding | Evidence and location | Repair and verification |
|---|---|---|
| N12 follow-up: wrong reference in compatibility notes | Current KiCad 10 report names **TP703**, front at **(145,159)**, net **SOLENOID_12V_SW**, for the missing Package field. Two current documents still named TP701. | Corrected the two current closure documents to TP703. The earlier immutable audit and supplied handoff remain original evidence. No purchasing field or footprint changed. |
| N14: label validator skips artwork | `validate_rev_a_manufacturing_metadata.py` filtered `G***` artwork out of its silk-obstacle loop. A disposable fixture moving the revision text to **(150,133)** over AYAB artwork incorrectly returned `REVISION_LABEL_CLEARANCE_OK`. This is a checker gap, not a defect at the actual (180,142) label location. | Changed the silk/courtyard loop to inspect all footprint objects, retaining the deliberate duplicate-reference exception for artwork elsewhere. Added three regression cases: actual release label passes, AYAB artwork overlap is rejected, old R713/R714 pad overlap is rejected. All three pass. |

The repaired source contains **three modified tracked files and one added test file**. The PCB, all eight schematics, project and pinned libraries remain byte-identical to the audited package. The native KiCad results therefore apply to the repaired source's identical CAD input; only the changed validator and its regression tests required a new execution. Both pass. Repeated native board loads in the tests emit harmless duplicate image-handler notices; assertions still complete successfully.

The supplied patch is checked against the original checkout without applying it there. The source ZIP contains the 310 selected tracked source files with these repairs, plus the new test. The repair manifest identifies the modified files and base commit; no new Git hash is invented. Local repairs have not been pushed or run in remote CI.

## 9. Repository validators and limits

All nine source validators returned exit 0 on the frozen package. The modified manufacturing validator also returns exit 0 on the repaired source.

| Validator | Fresh evidence | Limit |
|---|---|---|
| audit_esp32_pinmap.py | 39 GPIOs; zero target-function mismatches | Does not establish actual firmware behavior. |
| audit_rev_a_hall_pcb_parity.py | 0/24 obsolete parts; 4/4 replacement dividers | Inventory alone is not full electrical proof. |
| audit_rev_a_kl_pcb_parity.py | K/L pad/net inventory completed | Supplemented by independent complete pin comparison. |
| audit_rev_a_power_pcb_parity.py | Fresh report PASS | Targets selected power circuits. |
| audit_rev_a_prototype_pcb_parity.py | `PROTOTYPE_PCB_PARITY_OK` | Presence/value checks are not a physical test. |
| audit_rev_a_solenoid_gate_source.py | `SOLENOID_GATE_SOURCE_AUDIT_OK` | Static topology/metadata, not timing/thermal qualification. |
| validate_rev_a_machine_sense_protection.py | `MACHINE_SENSE_PROTECTION_TOPOLOGY_OK` | Checks selected topology and conditional bounds, not surge immunity. |
| validate_rev_a_solenoid_failsafe_pcb.py | `SOLENOID_FAILSAFE_TOPOLOGY_OK` | No energized fault-injection evidence. |
| validate_rev_a_manufacturing_metadata.py | `MANUFACTURING_METADATA_OK`, ORDERING_REFS 9, DNP_REFS 11, PINNED_FOOTPRINT_IDS 18, PINNED_FOOTPRINT_INSTANCES 23, CONTROLLED_BOARD_RULES 5, CONTROLLED_ASSEMBLY_LABELS 5, FOOTPRINT_TREE_UUIDS_UNIQUE 6053, `REVISION_LABEL_CLEARANCE_OK` | Artwork gap repaired. Its pad dictionary and approximate clearances remain narrower than an independent full pad/visual review. |

Three validators normally write review files inside the project; an external wrapper redirected only their report destinations. Validator logic was inspected and executed without treating its output as sole proof. No repair/generation script from the handoff was blindly executed.

## 10. Independent CI verification

Public GitHub API responses independently confirm all six supplied runs succeeded at repair commit **231ab3c9c348c4bb3880c5ed453855c066cb82e0**, on the correct repository and branch:

- [Hardware Check — 34640744875](https://github.com/newtonsewingstudio-star/ayab-hardware/actions/runs/34640744875)
- [Hall PCB Parity — 34640744863](https://github.com/newtonsewingstudio-star/ayab-hardware/actions/runs/34640744863)
- [Machine Sense Protection — 34640744798](https://github.com/newtonsewingstudio-star/ayab-hardware/actions/runs/34640744798)
- [Rev A Patch — 34640744834](https://github.com/newtonsewingstudio-star/ayab-hardware/actions/runs/34640744834)
- [Prototype Power PCB Parity — 34640744862](https://github.com/newtonsewingstudio-star/ayab-hardware/actions/runs/34640744862)
- [Solenoid Gate Validation — 34640744812](https://github.com/newtonsewingstudio-star/ayab-hardware/actions/runs/34640744812)

The Hardware Check job confirms successful KiCad installation, DRC/unconnected/footprint/full-parity gate, ERC error gate, and frozen audits including manufacturing metadata. Installation ran 19:47:45–19:48:47 UTC; DRC 19:48:47–19:48:50; ERC 19:48:50–19:48:51. The subsequent head 9bde764 changes only six stored image/SVG/DRC evidence files relative to that repair commit. Native sources, libraries and validators are unchanged between the two commits.

The independently retrieved sequence contains **69 branch runs for 11 September through query time, with no fabrication-named workflow run**. No workflow was triggered by this audit. The six remote successes cover the supplied source lineage; the small additional repairs in this deliverable are verified locally and are not claimed to have remote CI approval.

## 11. Post-assembly gates — NEEDS PHYSICAL TEST

These tests remain unperformed. They do not block ordering the first bare PCB, but they block machine installation or operational solenoid use:

1. Inspect actual part numbers, polarity, bridge custom mapping, clamp wetting, MOSFET orientation and all eleven DNP positions. Check pull-resistor continuity and absence of a raw-to-switched short before power.
2. Dry-fit M2 mounting hardware, slot, connectors, harnesses, antenna recess, underside components and insulated standoffs. Stop if the real chassis requires incompatible hardware.
3. With a current-limited supply and no solenoids, scope USB-only, machine-only, combined-power insertion sequences, reset, boot, watchdog reset and brownout. Check rail pulses, capacitor discharge and USB/machine back-feed.
4. Measure GPIO4 divider voltage, real supply peaks, ADC calibration and clamp/reference behavior. The 40 V arithmetic is not a certified surge test.
5. Use dummy loads within 0.65 A total bridge average and ≤40 °C ambient; reserve 0.25 A for logic until measured and allow no more than four measured ~86 mA coils' equivalent load. Measure bridge, regulator, MOSFET, trace and via temperatures, inrush/PWM peaks and voltage drops.
6. Confirm actual firmware mapping, default-low/released GPIO21, watchdog behavior, fresh machine-sense reading after reset and coil/current limits. Hardware stuck-high faults remain outside software recovery.

No physical test is represented as passed. No redundancy, safety rating, surge certification or energized operational readiness is inferred from a clean CAD audit.

## 12. Deliverables

The Markdown report, separate evidence ZIP, repaired-source ZIP and Git patch are stored outside the original repository. Both ZIPs have internal SHA-256 manifests; an external checksum file covers all delivered artifacts. The evidence archive excludes native source and negative-test fixture PCBs. The source archive excludes prior-audit ZIPs, handoff claims and unrelated legacy fabrication files.

**No Gerbers, drill files, placement files, BOMs, fabrication archives or other manufacturing outputs were generated. The original repository and supplied ZIP remain unchanged; the documented repairs exist only in the delivered isolated source.**


## Appendix A. Identity, timestamps and exact native input hashes

Initial check: 2026-09-11T20:07:12.351729+00:00. Final integrity check: 2026-09-11T20:25:15.404725+00:00.

Hashes below identify the exact packaged native inputs, also preserved unchanged in repaired source. Raw Git blob comparisons with newline distinctions are separately recorded in `raw-git-blob-comparison.json`.

| Native input | SHA-256 |
|---|---|
| `ayab-esp32/aux-connectors.kicad_sch` | `8953ec6a5c7ba926bc05c7e164976838bfb856d60bdc0458fab7a0771deeb04c` |
| `ayab-esp32/ayab-esp32.kicad_pcb` | `536f5525a8f04bf00aeadd02659ede1529dee4bd18bf136bd198e38f73603f75` |
| `ayab-esp32/ayab-esp32.kicad_pro` | `47683b6e97a6068971e41c5b29e63c9acfe43a70209b5c2ef44fe0a5465e1094` |
| `ayab-esp32/ayab-esp32.kicad_sch` | `f16c154c027d713d92f88358626448ca086ffba4ac9a2d45e80553fa586847b0` |
| `ayab-esp32/brother-connectors.kicad_sch` | `666c9733fba2a378c8555c70a48d9c9775152211c656be7c58b8579405c2c0e1` |
| `ayab-esp32/ioconditioning.kicad_sch` | `b1e3824be118cbeda0715c93dac2c9a822c0449abad61833cfbbae263e1af4ef` |
| `ayab-esp32/mcu.kicad_sch` | `ab9816dff4e3c11c4127943c920975d966a8eb21dc820e211391a475628756cb` |
| `ayab-esp32/psu.kicad_sch` | `9809415ea13f67e546f3f4940ca3bc18e1c6f21b0f716613506352693dcb8272` |
| `ayab-esp32/solenoids.kicad_sch` | `1a694d931cbdbfe4df79e345a77c5873b221ccb5fa2572464b54342b2e4467fc` |
| `ayab-esp32/usb.kicad_sch` | `2297790fd359a3a7e72cc9fdbe5c85345b89951eddf4cdef2a00814e4b66fef6` |

Historical fabrication files in the full repository, excluded from both deliverables:

- `ayab-interface/layout/gerber/ayab_rs.bottom.gbr`
- `ayab-interface/layout/gerber/ayab_rs.bottommask.gbr`
- `ayab-interface/layout/gerber/ayab_rs.bottompaste.gbr`
- `ayab-interface/layout/gerber/ayab_rs.bottomsilk.gbr`
- `ayab-interface/layout/gerber/ayab_rs.fab.gbr`
- `ayab-interface/layout/gerber/ayab_rs.outline.gbr`
- `ayab-interface/layout/gerber/ayab_rs.top.gbr`
- `ayab-interface/layout/gerber/ayab_rs.topmask.gbr`
- `ayab-interface/layout/gerber/ayab_rs.toppaste.gbr`
- `ayab-interface/layout/gerber/ayab_rs.topsilk.gbr`

## Appendix B. Object identity repairs and native associations

All 193 active schematic associations match their PCB paths. All 237 loaded footprint roots and 6,053 serialized footprint-tree IDs are unique. The upstream repair changed these eight footprint trees, preserving every non-UUID field:

| Reference | Current root UUID | Changed IDs |
|---|---|---:|
| R822 | `9d3e9778-6678-5e2c-9089-36c9a8f8bb8b` | 23 |
| R821 | `26399990-30a1-5272-ab9b-0b1ae2b67f9b` | 23 |
| R820 | `570df8d2-0f72-517f-ab6b-ad1a745cba1d` | 23 |
| TP703 | `ae6f39ee-baa6-5544-bb40-7d63c24a2fea` | 11 |
| Q805 | `c5836758-fc8c-5750-9dc9-b74e6e934dd4` | 27 |
| Q806 | `64f738e3-e685-5b2d-9056-fe1c76c8ffa4` | 27 |
| C206 | `6c1b14ac-cfef-5945-b19e-8d130d1c60ef` | 22 |
| D206 | `1080c6c5-39e7-5866-92b2-4ce09b252e77` | 23 |

The four remaining repeated raw IDs each connect a dimension to its own embedded label. Exact parent paths and full association records are in the evidence.


## Appendix C. Independent critical pad trace

All listed schematic nets match the native PCB. Hierarchical prefixes are retained. Coordinates are footprint origins; absolute pad positions are in `pcbnew9-geometry.json`.

| Reference.pin | Value | Side / origin (mm) | Schematic and PCB net |
|---|---|---|---|
| U201.5 | ESP32-S3-MINI-1 | F.Cu: 224.125, 129.675 | `/ESP32/HALL_L_ADC` |
| U201.6 | ESP32-S3-MINI-1 | F.Cu: 224.125, 129.675 | `/ESP32/HALL_R_ADC` |
| U201.7 | ESP32-S3-MINI-1 | F.Cu: 224.125, 129.675 | `unconnected-(U201-GPIO3{slash}TOUCH3{slash}ADC1_CH2-Pad7)` |
| U201.8 | ESP32-S3-MINI-1 | F.Cu: 224.125, 129.675 | `/ESP32/MACHINE_PWR_SENSE` |
| U201.21 | ESP32-S3-MINI-1 | F.Cu: 224.125, 129.675 | `/BROTHER-CONNECTORS/EOL_R_N` |
| U201.22 | ESP32-S3-MINI-1 | F.Cu: 224.125, 129.675 | `/BROTHER-CONNECTORS/EOL_R_S` |
| U201.25 | ESP32-S3-MINI-1 | F.Cu: 224.125, 129.675 | `SOLENOID_PWR_EN` |
| J701.6 | CTRL_3v3 | F.Cu: 212.587498, 152.5174 | `Net-(J701-Pin_6)` |
| J701.7 | CTRL_3v3 | F.Cu: 212.587498, 152.5174 | `Net-(J701-Pin_7)` |
| U701.15 | SN74LVC4245 | F.Cu: 194.34, 157.53 | `Net-(J701-Pin_7)` |
| U701.16 | SN74LVC4245 | F.Cu: 194.34, 157.53 | `Net-(J701-Pin_6)` |
| U302.9 | ULN2003A | F.Cu: 128.45, 139.325 | `SOLENOID_12V_SW` |
| U303.9 | ULN2003A | F.Cu: 115.9, 139.325 | `SOLENOID_12V_SW` |
| U304.9 | ULN2003A | F.Cu: 103.35, 139.325 | `SOLENOID_12V_SW` |
| J401.9 | 900.965.CK35 SOLENOIDS A | F.Cu: 132.84, 153.7852 | `SOLENOID_12V_SW` |
| J401.10 | 900.965.CK35 SOLENOIDS A | F.Cu: 132.84, 153.7852 | `SOLENOID_12V_SW` |
| J403.9 | 910.950 SOLENOIDS A | F.Cu: 320.91, 138.83 | `SOLENOID_12V_SW` |
| J403.10 | 910.950 SOLENOIDS A | F.Cu: 320.91, 138.83 | `SOLENOID_12V_SW` |
| J406.9 | 930.940 SOLENOIDS A | F.Cu: 116.74, 146.28 | `SOLENOID_12V_SW` |
| J406.10 | 930.940 SOLENOIDS A | F.Cu: 116.74, 146.28 | `SOLENOID_12V_SW` |
| R215.1 | 47k | B.Cu: 225, 159 | `+12V` |
| R215.2 | 47k | B.Cu: 225, 159 | `/ESP32/MACHINE_PWR_SENSE` |
| R216.1 | 10k | B.Cu: 228.5, 159 | `/ESP32/MACHINE_PWR_SENSE` |
| R216.2 | 10k | B.Cu: 228.5, 159 | `GND` |
| D205.1 | CDBU0130-HF | B.Cu: 234, 157 | `+3V3` |
| D205.2 | CDBU0130-HF | B.Cu: 234, 157 | `/ESP32/MACHINE_PWR_SENSE` |
| D206.1 | CDBU0130-HF | B.Cu: 234, 160.5 | `/ESP32/MACHINE_PWR_SENSE` |
| D206.2 | CDBU0130-HF | B.Cu: 234, 160.5 | `GND` |
| C206.1 | 100n | B.Cu: 237.25, 160.5 | `/ESP32/MACHINE_PWR_SENSE` |
| C206.2 | 100n | B.Cu: 237.25, 160.5 | `GND` |
| Q805.1 | LP9435LT1G | F.Cu: 117, 160.25 | `Net-(Q805-G)` |
| Q805.2 | LP9435LT1G | F.Cu: 117, 160.25 | `+12V` |
| Q805.3 | LP9435LT1G | F.Cu: 117, 160.25 | `SOLENOID_12V_SW` |
| Q806.1 | AO3400A | F.Cu: 121, 160.25 | `Net-(Q806-G)` |
| Q806.2 | AO3400A | F.Cu: 121, 160.25 | `GND` |
| Q806.3 | AO3400A | F.Cu: 121, 160.25 | `Net-(Q805-G)` |
| R820.1 | 100k | F.Cu: 113, 161.9 | `+12V` |
| R820.2 | 100k | F.Cu: 113, 161.9 | `Net-(Q805-G)` |
| R821.1 | 10k | F.Cu: 125, 159.2 | `SOLENOID_PWR_EN` |
| R821.2 | 10k | F.Cu: 125, 159.2 | `Net-(Q806-G)` |
| R822.1 | 100k | F.Cu: 128, 161.5 | `GND` |
| R822.2 | 100k | F.Cu: 128, 161.5 | `Net-(Q806-G)` |
| R209.1 | 5k1 | F.Cu: 212.75, 133.675 | `+3V3` |
| R209.2 | 5k1 | F.Cu: 212.75, 133.675 | `/AUX-CONNECTORS/AYAB_SCL` |
| R210.1 | 5k1 | F.Cu: 212.75, 132.025 | `+3V3` |
| R210.2 | 5k1 | F.Cu: 212.75, 132.025 | `/AUX-CONNECTORS/AYAB_SDA` |
| C603.1 | 10u | F.Cu: 97.0576, 137.3124 | `SOLENOID_12V_SW` |
| C603.2 | 10u | F.Cu: 97.0576, 137.3124 | `GND` |
| C604.1 | 10u | F.Cu: 109.625, 137.325 | `SOLENOID_12V_SW` |
| C604.2 | 10u | F.Cu: 109.625, 137.325 | `GND` |
| C605.1 | 10u | F.Cu: 122.175, 137.325 | `SOLENOID_12V_SW` |
| C605.2 | 10u | F.Cu: 122.175, 137.325 | `GND` |
| R735.1 | 10k | F.Cu: 90.9628, 139.103 | `/BROTHER-CONNECTORS/EOL_L` |
| R735.2 | 10k | F.Cu: 90.9628, 139.103 | `/ESP32/HALL_L_ADC` |
| R736.1 | 10k | F.Cu: 90.9628, 140.653 | `/ESP32/HALL_L_ADC` |
| R736.2 | 10k | F.Cu: 90.9628, 140.653 | `GND` |
| R737.1 | 10k | F.Cu: 314.67, 157.25 | `/BROTHER-CONNECTORS/EOL_R` |
| R737.2 | 10k | F.Cu: 314.67, 157.25 | `/ESP32/HALL_R_ADC` |
| R738.1 | 10k | F.Cu: 313.12, 157.25 | `/ESP32/HALL_R_ADC` |
| R738.2 | 10k | F.Cu: 313.12, 157.25 | `GND` |
| D601.1 | KMB14F | F.Cu: 302.13, 156.15 | `/PSU/INP_1` |
| D601.2 | KMB14F | F.Cu: 302.13, 156.15 | `/PSU/INP_2` |
| D601.3 | KMB14F | F.Cu: 302.13, 156.15 | `+12V` |
| D601.4 | KMB14F | F.Cu: 302.13, 156.15 | `GND` |
| U403.1 | LM66100DCKR | B.Cu: 300, 155 | `/PSU/5V_SW` |
| U403.2 | LM66100DCKR | B.Cu: 300, 155 | `GND` |
| U403.3 | LM66100DCKR | B.Cu: 300, 155 | `+5V` |
| U403.4 | LM66100DCKR | B.Cu: 300, 155 | `unconnected-(U403-N{slash}C-Pad4)` |
| U403.5 | LM66100DCKR | B.Cu: 300, 155 | `GND` |
| U403.6 | LM66100DCKR | B.Cu: 300, 155 | `+5V` |
| TP701.1 | HALL-L-RAW | F.Cu: 85.39, 135 | `/BROTHER-CONNECTORS/EOL_L` |
| TP702.1 | HALL-R-RAW | F.Cu: 321.66, 160.16 | `/BROTHER-CONNECTORS/EOL_R` |
| TP703.1 | SOL12_SW | F.Cu: 145, 159 | `SOLENOID_12V_SW` |
| R213.1 | 10k | F.Cu: 260, 124 | `+3V3` |
| R213.2 | 10k | F.Cu: 260, 124 | `/BROTHER-CONNECTORS/EOL_R_N` |
| R214.1 | 10k | F.Cu: 260, 126 | `+3V3` |
| R214.2 | 10k | F.Cu: 260, 126 | `/BROTHER-CONNECTORS/EOL_R_S` |

## Appendix D. Critical purchasing metadata

These read-only extracts are evidence, not a BOM. Active references come from the fresh schematic netlist.

### D204

| Field | Schematic | PCB |
|---|---|---|
| Value | SS54 | SS54 |
| Description | SS54 5 A 40 V SMA Schottky rectifier | SS54 5 A 40 V SMA Schottky rectifier |
| Datasheet | https://datasheet.lcsc.com/datasheet/pdf/8a09f89034087b5d1623ed150a6cce5b.pdf?productCode=C22452 | https://datasheet.lcsc.com/datasheet/pdf/8a09f89034087b5d1623ed150a6cce5b.pdf?productCode=C22452 |
| Package | SMA | SMA |
| OEM | MDD (Microdiode Semiconductor) | MDD (Microdiode Semiconductor) |
| OEM PN | SS54 | SS54 |
| LCSC ID | C22452 | C22452 |
| DNP | False | False |

### D601

| Field | Schematic | PCB |
|---|---|---|
| Value | KMB14F | KMB14F |
| Description | KMB14F 1 A bridge rectifier; PCB pins 1/2=AC, 3=+12V, 4=GND | KMB14F 1 A bridge rectifier; PCB pins 1/2=AC, 3=+12V, 4=GND |
| Datasheet | https://datasheet.lcsc.com/datasheet/pdf/e72e2e5f3749444edb574593f092205f.pdf?productCode=C880909 | https://datasheet.lcsc.com/datasheet/pdf/e72e2e5f3749444edb574593f092205f.pdf?productCode=C880909 |
| Package | MBF | MBF |
| OEM | FUXINSEMI | FUXINSEMI |
| OEM PN | KMB14F | KMB14F |
| LCSC ID | C880909 | C880909 |
| DNP | False | False |

### D605

| Field | Schematic | PCB |
|---|---|---|
| Value | SS54 | SS54 |
| Description | SS54 5 A 40 V SMA Schottky rectifier | SS54 5 A 40 V SMA Schottky rectifier |
| Datasheet | https://datasheet.lcsc.com/datasheet/pdf/8a09f89034087b5d1623ed150a6cce5b.pdf?productCode=C22452 | https://datasheet.lcsc.com/datasheet/pdf/8a09f89034087b5d1623ed150a6cce5b.pdf?productCode=C22452 |
| Package | SMA | SMA |
| OEM | MDD (Microdiode Semiconductor) | MDD (Microdiode Semiconductor) |
| OEM PN | SS54 | SS54 |
| LCSC ID | C22452 | C22452 |
| DNP | False | False |

### D606

| Field | Schematic | PCB |
|---|---|---|
| Value | SS54 | SS54 |
| Description | SS54 5 A 40 V SMA Schottky rectifier | SS54 5 A 40 V SMA Schottky rectifier |
| Datasheet | https://datasheet.lcsc.com/datasheet/pdf/8a09f89034087b5d1623ed150a6cce5b.pdf?productCode=C22452 | https://datasheet.lcsc.com/datasheet/pdf/8a09f89034087b5d1623ed150a6cce5b.pdf?productCode=C22452 |
| Package | SMA | SMA |
| OEM | MDD (Microdiode Semiconductor) | MDD (Microdiode Semiconductor) |
| OEM PN | SS54 | SS54 |
| LCSC ID | C22452 | C22452 |
| DNP | False | False |

### U403

| Field | Schematic | PCB |
|---|---|---|
| Value | LM66100DCKR | LM66100DCKR |
| Description | (blank) | LM66100 5.5-V 1.5-A ideal diode with reverse-current blocking |
| Datasheet | https://www.ti.com/lit/ds/symlink/lm66100.pdf | https://www.ti.com/lit/ds/symlink/lm66100.pdf |
| Package | SC-70-6 | SC-70-6 |
| OEM | Texas Instruments | Texas Instruments |
| OEM PN | LM66100DCKR | LM66100DCKR |
| LCSC ID | C2869734 | C2869734 |
| DNP | False | False |

### D205

| Field | Schematic | PCB |
|---|---|---|
| Value | CDBU0130-HF | CDBU0130-HF |
| Description | CDBU0130-HF 30 V low-leakage Schottky diode | CDBU0130-HF 30 V low-leakage Schottky diode |
| Datasheet | https://datasheet.lcsc.com/lcsc/2205091530_Comchip-Technology-CDBU0130-HF_C2886021.pdf | https://datasheet.lcsc.com/lcsc/2205091530_Comchip-Technology-CDBU0130-HF_C2886021.pdf |
| Package | 0603/SOD-523F | 0603/SOD-523F |
| OEM | Comchip Technology | Comchip Technology |
| OEM PN | CDBU0130-HF | CDBU0130-HF |
| LCSC ID | C2886021 | C2886021 |
| DNP | False | False |

### D206

| Field | Schematic | PCB |
|---|---|---|
| Value | CDBU0130-HF | CDBU0130-HF |
| Description | CDBU0130-HF 30 V low-leakage Schottky diode | CDBU0130-HF 30 V low-leakage Schottky diode |
| Datasheet | https://datasheet.lcsc.com/lcsc/2205091530_Comchip-Technology-CDBU0130-HF_C2886021.pdf | https://datasheet.lcsc.com/lcsc/2205091530_Comchip-Technology-CDBU0130-HF_C2886021.pdf |
| Package | 0603/SOD-523F | 0603/SOD-523F |
| OEM | Comchip Technology | Comchip Technology |
| OEM PN | CDBU0130-HF | CDBU0130-HF |
| LCSC ID | C2886021 | C2886021 |
| DNP | False | False |


## Appendix E. Reproducible commands and complete console output

The commands below preserve actual paths, working directory, exit codes and stdout/stderr. Use PowerShell’s call operator `&` before a quoted executable when replaying interactively. Version-specific configuration and model overrides are in `kicad9/environment.json`, `kicad10/environment.json` and each `model-environment.json`. Native runs used separate original input copies; changed validator/tests ran from the isolated repaired source.

### initial status

Working directory: `C:\Users\bjrem\Documents\Codex\2026-09-10\referenced-chatgpt-conversation-this-is-an\work\ayab-hardware-current`

Exit: **0**

```text
git status --short
```

stdout:

```text
?? ayab-esp32/tools/__pycache__/
?? render-34512445704/
?? work-pcbnew-api.log
```

stderr:

```text
(empty)
```

### initial branch

Working directory: `C:\Users\bjrem\Documents\Codex\2026-09-10\referenced-chatgpt-conversation-this-is-an\work\ayab-hardware-current`

Exit: **0**

```text
git branch --show-current
```

stdout:

```text
ayab-esp32-kh910-rev-a
```

stderr:

```text
(empty)
```

### initial head

Working directory: `C:\Users\bjrem\Documents\Codex\2026-09-10\referenced-chatgpt-conversation-this-is-an\work\ayab-hardware-current`

Exit: **0**

```text
git rev-parse HEAD
```

stdout:

```text
9bde764c6e157920af34ccd1063949ac5dcc5109
```

stderr:

```text
(empty)
```

### initial remote

Working directory: `C:\Users\bjrem\Documents\Codex\2026-09-10\referenced-chatgpt-conversation-this-is-an\work\ayab-hardware-current`

Exit: **0**

```text
git remote -v
```

stdout:

```text
origin	https://github.com/newtonsewingstudio-star/ayab-hardware.git (fetch)
origin	https://github.com/newtonsewingstudio-star/ayab-hardware.git (push)
```

stderr:

```text
(empty)
```

### initial remote_head

Working directory: `C:\Users\bjrem\Documents\Codex\2026-09-10\referenced-chatgpt-conversation-this-is-an\work\ayab-hardware-current`

Exit: **0**

```text
git ls-remote origin refs/heads/ayab-esp32-kh910-rev-a
```

stdout:

```text
9bde764c6e157920af34ccd1063949ac5dcc5109	refs/heads/ayab-esp32-kh910-rev-a
```

stderr:

```text
(empty)
```

### Git archive source comparison

Working directory: `C:\Users\bjrem\Documents\Codex\2026-09-10\referenced-chatgpt-conversation-this-is-an\work\ayab-hardware-current`

Exit: **0**

```text
git archive --format=zip --output C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\git-source.zip 9bde764c6e157920af34ccd1063949ac5dcc5109
```

stdout:

```text
(empty)
```

stderr:

```text
(empty)
```

### KiCad 9: audit_esp32_pinmap.py

Working directory: `C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\source`

Exit: **0**

```text
C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\independent-audit-647998e\kicad9-runtime\bin\python.exe C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\redirect_report.py ayab-esp32\tools\audit_esp32_pinmap.py C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\audit-results\kicad9\audit_esp32_pinmap.py.md
```

stdout:

```text
AUDITOR_REPORT_REDIRECT C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\source\ayab-esp32\KH910_REV_A_CURRENT_PIN_AUDIT.md -> C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\audit-results\kicad9\audit_esp32_pinmap.py.md
Wrote C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\source\ayab-esp32\KH910_REV_A_CURRENT_PIN_AUDIT.md
```

stderr:

```text
(empty)
```

### KiCad 9: audit_rev_a_hall_pcb_parity.py

Working directory: `C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\source`

Exit: **0**

```text
C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\independent-audit-647998e\kicad9-runtime\bin\python.exe C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\redirect_report.py ayab-esp32\tools\audit_rev_a_hall_pcb_parity.py C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\audit-results\kicad9\audit_rev_a_hall_pcb_parity.py.md
```

stdout:

```text
AUDITOR_REPORT_REDIRECT C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\source\ayab-esp32\KH910_REV_A_HALL_PCB_PARITY.md -> C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\audit-results\kicad9\audit_rev_a_hall_pcb_parity.py.md
C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\source\ayab-esp32\KH910_REV_A_HALL_PCB_PARITY.md
```

stderr:

```text
(empty)
```

### KiCad 9: audit_rev_a_kl_pcb_parity.py

Working directory: `C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\source`

Exit: **0**

```text
C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\independent-audit-647998e\kicad9-runtime\bin\python.exe C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\redirect_report.py ayab-esp32\tools\audit_rev_a_kl_pcb_parity.py C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\audit-results\kicad9\audit_rev_a_kl_pcb_parity.py.md
```

stdout:

```text
AUDITOR_REPORT_REDIRECT C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\source\ayab-esp32\KH910_REV_A_KL_PCB_PARITY.md -> C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\audit-results\kicad9\audit_rev_a_kl_pcb_parity.py.md
C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\source\ayab-esp32\KH910_REV_A_KL_PCB_PARITY.md
```

stderr:

```text
(empty)
```

### KiCad 9: audit_rev_a_power_pcb_parity.py

Working directory: `C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\source`

Exit: **0**

```text
C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\independent-audit-647998e\kicad9-runtime\bin\python.exe ayab-esp32\tools\audit_rev_a_power_pcb_parity.py --output C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\audit-results\kicad9\power-parity.md
```

stdout:

```text
C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\audit-results\kicad9\power-parity.md
```

stderr:

```text
(empty)
```

### KiCad 9: audit_rev_a_prototype_pcb_parity.py

Working directory: `C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\source`

Exit: **0**

```text
C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\independent-audit-647998e\kicad9-runtime\bin\python.exe ayab-esp32\tools\audit_rev_a_prototype_pcb_parity.py
```

stdout:

```text
PROTOTYPE_PCB_PARITY_AUDIT
PRESENT C206, D205, D206, Q805, Q806, R215, R216, R820, R821, R822, TP603, TP703, U403, U601, U602
PROTOTYPE_PCB_PARITY_OK
```

stderr:

```text
(empty)
```

### KiCad 9: audit_rev_a_solenoid_gate_source.py

Working directory: `C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\source`

Exit: **0**

```text
C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\independent-audit-647998e\kicad9-runtime\bin\python.exe ayab-esp32\tools\audit_rev_a_solenoid_gate_source.py
```

stdout:

```text
SOLENOID_GATE_SOURCE_AUDIT_OK
SOURCE_REVIEW: no physical prototype evidence and no AYAB-ESP32 release fabrication output generated
PARTS: Q805 LP9435LT1G, Q806 AO3400A, 100k/10k default-off network, TP703
```

stderr:

```text
(empty)
```

### KiCad 9: back-outlines

Working directory: `C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\source`

Exit: **0**

```text
C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\independent-audit-647998e\kicad9-runtime\bin\kicad-cli.exe pcb export svg --mode-single --page-size-mode 2 --layers B.Fab,B.CrtYd,Edge.Cuts -o C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\audit-results\kicad9\back-outlines.svg ayab-esp32/ayab-esp32.kicad_pcb
```

stdout:

```text
Plotted to 'C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\audit-results\kicad9\back-outlines.svg'.
Done.
```

stderr:

```text
(empty)
```

### KiCad 9: back

Working directory: `C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\source`

Exit: **0**

```text
C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\independent-audit-647998e\kicad9-runtime\bin\kicad-cli.exe pcb export svg --mode-single --page-size-mode 2 --layers B.Cu,B.SilkS,Edge.Cuts -o C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\audit-results\kicad9\back.svg ayab-esp32/ayab-esp32.kicad_pcb
```

stdout:

```text
Plotted to 'C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\audit-results\kicad9\back.svg'.
Done.
```

stderr:

```text
(empty)
```

### KiCad 9: drc-parity

Working directory: `C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\source`

Exit: **0**

```text
C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\independent-audit-647998e\kicad9-runtime\bin\kicad-cli.exe pcb drc --schematic-parity --exit-code-violations -o C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\audit-results\kicad9\drc-parity.rpt ayab-esp32/ayab-esp32.kicad_pcb
```

stdout:

```text
Found 0 violations
Found 0 unconnected items
Found 0 schematic parity issues
Saved DRC Report to C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\audit-results\kicad9\drc-parity.rpt
```

stderr:

```text
Fontconfig error: Cannot load default config file: No such file: (null)
```

### KiCad 9: drc

Working directory: `C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\source`

Exit: **0**

```text
C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\independent-audit-647998e\kicad9-runtime\bin\kicad-cli.exe pcb drc --exit-code-violations -o C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\audit-results\kicad9\drc.rpt ayab-esp32/ayab-esp32.kicad_pcb
```

stdout:

```text
Found 0 violations
Found 0 unconnected items
Saved DRC Report to C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\audit-results\kicad9\drc.rpt
```

stderr:

```text
(empty)
```

### KiCad 9: erc

Working directory: `C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\source`

Exit: **5**

```text
C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\independent-audit-647998e\kicad9-runtime\bin\kicad-cli.exe sch erc --exit-code-violations -o C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\audit-results\kicad9\erc.rpt ayab-esp32/ayab-esp32.kicad_sch
```

stdout:

```text
Found 78 violations
Saved ERC Report to C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\audit-results\kicad9\erc.rpt
```

stderr:

```text
Fontconfig error: Cannot load default config file: No such file: (null)
```

### KiCad 9: front-outlines

Working directory: `C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\source`

Exit: **0**

```text
C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\independent-audit-647998e\kicad9-runtime\bin\kicad-cli.exe pcb export svg --mode-single --page-size-mode 2 --layers F.Fab,F.CrtYd,Edge.Cuts -o C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\audit-results\kicad9\front-outlines.svg ayab-esp32/ayab-esp32.kicad_pcb
```

stdout:

```text
Plotted to 'C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\audit-results\kicad9\front-outlines.svg'.
Done.
```

stderr:

```text
(empty)
```

### KiCad 9: front

Working directory: `C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\source`

Exit: **0**

```text
C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\independent-audit-647998e\kicad9-runtime\bin\kicad-cli.exe pcb export svg --mode-single --page-size-mode 2 --layers F.Cu,F.SilkS,Edge.Cuts -o C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\audit-results\kicad9\front.svg ayab-esp32/ayab-esp32.kicad_pcb
```

stdout:

```text
Plotted to 'C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\audit-results\kicad9\front.svg'.
Done.
```

stderr:

```text
(empty)
```

### KiCad 9: inner1

Working directory: `C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\source`

Exit: **0**

```text
C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\independent-audit-647998e\kicad9-runtime\bin\kicad-cli.exe pcb export svg --mode-single --page-size-mode 2 --layers In1.Cu,Edge.Cuts -o C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\audit-results\kicad9\inner1.svg ayab-esp32/ayab-esp32.kicad_pcb
```

stdout:

```text
Plotted to 'C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\audit-results\kicad9\inner1.svg'.
Done.
```

stderr:

```text
(empty)
```

### KiCad 9: inner2

Working directory: `C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\source`

Exit: **0**

```text
C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\independent-audit-647998e\kicad9-runtime\bin\kicad-cli.exe pcb export svg --mode-single --page-size-mode 2 --layers In2.Cu,Edge.Cuts -o C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\audit-results\kicad9\inner2.svg ayab-esp32/ayab-esp32.kicad_pcb
```

stdout:

```text
Plotted to 'C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\audit-results\kicad9\inner2.svg'.
Done.
```

stderr:

```text
(empty)
```

### KiCad 9: netlist

Working directory: `C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\source`

Exit: **0**

```text
C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\independent-audit-647998e\kicad9-runtime\bin\kicad-cli.exe sch export netlist --format kicadxml -o C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\audit-results\kicad9\live-netlist.xml ayab-esp32/ayab-esp32.kicad_sch
```

stdout:

```text
(empty)
```

stderr:

```text
Fontconfig error: Cannot load default config file: No such file: (null)
```

### KiCad 9: python-version

Working directory: `C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\source`

Exit: **0**

```text
C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\independent-audit-647998e\kicad9-runtime\bin\python.exe -c "import sys,pcbnew;print(sys.version);print(pcbnew.Version())"
```

stdout:

```text
3.11.5 (main, Jan 18 2026, 05:50:19) [MSC v.1944 64 bit (AMD64)]
9.0.9
```

stderr:

```text
(empty)
```

### KiCad 9: render-bottom

Working directory: `C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\source`

Exit: **0**

```text
C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\independent-audit-647998e\kicad9-runtime\bin\kicad-cli.exe pcb render --side bottom --width 3600 --height 1000 --zoom 3 -o C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\audit-results\kicad9\render-bottom.png ayab-esp32/ayab-esp32.kicad_pcb
```

stdout:

```text
Loading…
Build board outline

Create layers
Create tracks and vias
Create zones
Build Tech layers
Build Tech layer 11
Build Tech layer 9
Build Tech layer 15
Build Tech layer 13
Build Tech layer 7
Build Tech layer 5
Build Tech layer 3
Build Tech layer 1
Build Tech layer 17
Build Tech layer 19
Build Tech layer 21
Build Tech layer 23
Build Tech layer 39
Build Tech layer 41
Build Tech layer 43
Build Tech layer 45
Build Tech layer 47
Build Tech layer 49
Build Tech layer 51
Build Tech layer 53
Build Tech layer 55
Build Tech layer 57
Build Tech layer 59
Build Tech layer 61
Build Tech layer 63
Build Tech layer 65
Build Tech layer 67
Build Tech layer 69
Build Tech layer 71
Build Tech layer 73
Build Tech layer 75
Build Tech layer 77
Build Tech layer 79
Build Tech layer 81
Build Tech layer 83
Build Tech layer 85
Build Tech layer 87
Build Tech layer 89
Build Tech layer 91
Build Tech layer 93
Build Tech layer 95
Build Tech layer 97
Build Tech layer 99
Build Tech layer 101
Build Tech layer 103
Build Tech layer 105
Build Tech layer 107
Build Tech layer 109
Build Tech layer 111
Build Tech layer 113
Build Tech layer 115
Build Tech layer 117
Build Tech layer 119
Build Tech layer 121
Build Tech layer 123
Build Tech layer 125
Build Tech layer 127
Simplifying copper layer polygons
Calculating plated copper
Simplify holes contours
Build BVH for holes and vias
Load Raytracing: board
Load Raytracing: layers
Loading 3D models...
Reload time 2.767 s
Rendering: 14 %
Rendering: 25 %
Rendering: 40 %
Rendering: 44 %
Rendering: 53 %
Rendering: 62 %
Rendering: 70 %
Rendering: 79 %
Rendering: 98 %
Rendering: 100 %
Rendering time 6.834 s
Successfully created 3D render image
```

stderr:

```text
(empty)
```

### KiCad 9: render-top

Working directory: `C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\source`

Exit: **0**

```text
C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\independent-audit-647998e\kicad9-runtime\bin\kicad-cli.exe pcb render --side top --width 3600 --height 1000 --zoom 3 -o C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\audit-results\kicad9\render-top.png ayab-esp32/ayab-esp32.kicad_pcb
```

stdout:

```text
Loading…
Build board outline

Create layers
Create tracks and vias
Create zones
Build Tech layers
Build Tech layer 11
Build Tech layer 9
Build Tech layer 15
Build Tech layer 13
Build Tech layer 7
Build Tech layer 5
Build Tech layer 3
Build Tech layer 1
Build Tech layer 17
Build Tech layer 19
Build Tech layer 21
Build Tech layer 23
Build Tech layer 39
Build Tech layer 41
Build Tech layer 43
Build Tech layer 45
Build Tech layer 47
Build Tech layer 49
Build Tech layer 51
Build Tech layer 53
Build Tech layer 55
Build Tech layer 57
Build Tech layer 59
Build Tech layer 61
Build Tech layer 63
Build Tech layer 65
Build Tech layer 67
Build Tech layer 69
Build Tech layer 71
Build Tech layer 73
Build Tech layer 75
Build Tech layer 77
Build Tech layer 79
Build Tech layer 81
Build Tech layer 83
Build Tech layer 85
Build Tech layer 87
Build Tech layer 89
Build Tech layer 91
Build Tech layer 93
Build Tech layer 95
Build Tech layer 97
Build Tech layer 99
Build Tech layer 101
Build Tech layer 103
Build Tech layer 105
Build Tech layer 107
Build Tech layer 109
Build Tech layer 111
Build Tech layer 113
Build Tech layer 115
Build Tech layer 117
Build Tech layer 119
Build Tech layer 121
Build Tech layer 123
Build Tech layer 125
Build Tech layer 127
Simplifying copper layer polygons
Calculating plated copper
Simplify holes contours
Build BVH for holes and vias
Load Raytracing: board
Load Raytracing: layers
Loading 3D models...
Reload time 3.386 s
Rendering: 15 %
Rendering: 31 %
Rendering: 42 %
Rendering: 52 %
Rendering: 61 %
Rendering: 70 %
Rendering: 80 %
Rendering: 100 %
Rendering time 5.960 s
Successfully created 3D render image
```

stderr:

```text
(empty)
```

### KiCad 9: schematics

Working directory: `C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\source`

Exit: **0**

```text
C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\independent-audit-647998e\kicad9-runtime\bin\kicad-cli.exe sch export svg -o C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\audit-results\kicad9\schematics\ ayab-esp32/ayab-esp32.kicad_sch
```

stdout:

```text
Plotted to 'C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\audit-results\kicad9\schematics\ayab-esp32.svg'.
Plotted to 'C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\audit-results\kicad9\schematics\ayab-esp32-ESP32.svg'.
Plotted to 'C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\audit-results\kicad9\schematics\ayab-esp32-SOLENOID DRIVERS.svg'.
Plotted to 'C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\audit-results\kicad9\schematics\ayab-esp32-BROTHER-CONNECTORS.svg'.
Plotted to 'C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\audit-results\kicad9\schematics\ayab-esp32-USB.svg'.
Plotted to 'C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\audit-results\kicad9\schematics\ayab-esp32-PSU.svg'.
Plotted to 'C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\audit-results\kicad9\schematics\ayab-esp32-IO CONDITIONING.svg'.
Plotted to 'C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\audit-results\kicad9\schematics\ayab-esp32-AUX-CONNECTORS.svg'.
Done.
```

stderr:

```text
Fontconfig error: Cannot load default config file: No such file: (null)
```

### KiCad 9: validate_rev_a_machine_sense_protection.py

Working directory: `C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\source`

Exit: **0**

```text
C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\independent-audit-647998e\kicad9-runtime\bin\python.exe ayab-esp32\tools\validate_rev_a_machine_sense_protection.py ayab-esp32/ayab-esp32.kicad_pcb
```

stdout:

```text
MACHINE_SENSE_PROTECTION_TOPOLOGY_OK
POSITIVE_CLAMP D205: MACHINE_PWR_SENSE anode, +3V3 cathode
NEGATIVE_CLAMP D206: GND anode, MACHINE_PWR_SENSE cathode
ADC_FILTER C206: 100n MACHINE_PWR_SENSE to GND
R216_OPEN_CURRENT VRAW=12.0V CONDITIONAL_0.179mA_AT_3V6_NOMINAL_R215 LOOSE_UPPER_0.261mA_NODE_GE_0V_R215_MIN_FULL_RATED_ELEMENT_TEMP
R216_OPEN_CURRENT VRAW=15.0V CONDITIONAL_0.243mA_AT_3V6_NOMINAL_R215 LOOSE_UPPER_0.327mA_NODE_GE_0V_R215_MIN_FULL_RATED_ELEMENT_TEMP
R216_OPEN_CURRENT VRAW=40.0V CONDITIONAL_0.774mA_AT_3V6_NOMINAL_R215 LOOSE_UPPER_0.871mA_NODE_GE_0V_R215_MIN_FULL_RATED_ELEMENT_TEMP
CURRENT_BOUNDS_DO_NOT_GUARANTEE_GPIO_VOLTAGE_OR_SURGE_COMPLIANCE
```

stderr:

```text
(empty)
```

### KiCad 9: validate_rev_a_manufacturing_metadata.py

Working directory: `C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\source`

Exit: **0**

```text
C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\independent-audit-647998e\kicad9-runtime\bin\python.exe ayab-esp32\tools\validate_rev_a_manufacturing_metadata.py
```

stdout:

```text
MANUFACTURING_METADATA_OK
ORDERING_REFS 9
DNP_REFS 11
PINNED_FOOTPRINT_IDS 18
PINNED_FOOTPRINT_INSTANCES 23
CONTROLLED_BOARD_RULES 5
CONTROLLED_ASSEMBLY_LABELS 5
FOOTPRINT_TREE_UUIDS_UNIQUE 6053
REVISION_LABEL_CLEARANCE_OK
```

stderr:

```text
(empty)
```

### KiCad 9: validate_rev_a_solenoid_failsafe_pcb.py

Working directory: `C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\source`

Exit: **0**

```text
C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\independent-audit-647998e\kicad9-runtime\bin\python.exe ayab-esp32\tools\validate_rev_a_solenoid_failsafe_pcb.py ayab-esp32/ayab-esp32.kicad_pcb
```

stdout:

```text
SOLENOID_FAILSAFE_TOPOLOGY_OK
DEFAULT_OFF Q805 gate pulled to +12V by R820; Q806 gate pulled to GND by R822
ENABLE SOLENOID_PWR_EN through R821
SWITCHED_RAIL SOLENOID_12V_SW validated on left and right machine power branches
```

stderr:

```text
(empty)
```

### KiCad 9: version

Working directory: `C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\source`

Exit: **0**

```text
C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\independent-audit-647998e\kicad9-runtime\bin\kicad-cli.exe version
```

stdout:

```text
9.0.9
```

stderr:

```text
(empty)
```

### KiCad 10: back

Working directory: `C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\source-kicad10`

Exit: **0**

```text
"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe" pcb export svg --mode-single --page-size-mode 2 --layers B.Cu,B.SilkS,Edge.Cuts -o C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\audit-results\kicad10\back.svg ayab-esp32/ayab-esp32.kicad_pcb
```

stdout:

```text
Plotted to 'C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\audit-results\kicad10\back.svg'.
Done.
```

stderr:

```text
(empty)
```

### KiCad 10: drc-parity

Working directory: `C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\source-kicad10`

Exit: **5**

```text
"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe" pcb drc --schematic-parity --exit-code-violations -o C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\audit-results\kicad10\drc-parity.rpt ayab-esp32/ayab-esp32.kicad_pcb
```

stdout:

```text
Found 0 violations
Found 0 unconnected items
Found 187 schematic parity issues
Saved DRC Report to C:/Users/bjrem/Documents/Codex/2026-09-11/files-pasted-by-the-user-perform/work/preorder-audit-9bde764/audit-results/kicad10/drc-parity.rpt
```

stderr:

```text
(empty)
```

### KiCad 10: drc

Working directory: `C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\source-kicad10`

Exit: **0**

```text
"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe" pcb drc --exit-code-violations -o C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\audit-results\kicad10\drc.rpt ayab-esp32/ayab-esp32.kicad_pcb
```

stdout:

```text
Found 0 violations
Found 0 unconnected items
Saved DRC Report to C:/Users/bjrem/Documents/Codex/2026-09-11/files-pasted-by-the-user-perform/work/preorder-audit-9bde764/audit-results/kicad10/drc.rpt
```

stderr:

```text
(empty)
```

### KiCad 10: erc

Working directory: `C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\source-kicad10`

Exit: **0**

```text
"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe" sch erc --exit-code-violations -o C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\audit-results\kicad10\erc.rpt ayab-esp32/ayab-esp32.kicad_sch
```

stdout:

```text
Found 0 violations
Saved ERC Report to C:/Users/bjrem/Documents/Codex/2026-09-11/files-pasted-by-the-user-perform/work/preorder-audit-9bde764/audit-results/kicad10/erc.rpt
```

stderr:

```text
(empty)
```

### KiCad 10: front

Working directory: `C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\source-kicad10`

Exit: **0**

```text
"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe" pcb export svg --mode-single --page-size-mode 2 --layers F.Cu,F.SilkS,Edge.Cuts -o C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\audit-results\kicad10\front.svg ayab-esp32/ayab-esp32.kicad_pcb
```

stdout:

```text
Plotted to 'C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\audit-results\kicad10\front.svg'.
Done.
```

stderr:

```text
(empty)
```

### KiCad 10: netlist

Working directory: `C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\source-kicad10`

Exit: **0**

```text
"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe" sch export netlist --format kicadxml -o C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\audit-results\kicad10\live-netlist.xml ayab-esp32/ayab-esp32.kicad_sch
```

stdout:

```text
(empty)
```

stderr:

```text
(empty)
```

### KiCad 10: python-version

Working directory: `C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\source-kicad10`

Exit: **0**

```text
"C:\Program Files\KiCad\10.0\bin\python.exe" -c "import sys,pcbnew;print(sys.version);print(pcbnew.Version())"
```

stdout:

```text
3.11.5 (main, Jan 23 2026, 07:39:48) [MSC v.1944 64 bit (AMD64)]
10.0.6
```

stderr:

```text
(empty)
```

### KiCad 10: render-bottom

Working directory: `C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\source-kicad10`

Exit: **0**

```text
"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe" pcb render --side bottom --width 3600 --height 1000 --zoom 3 -o C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\audit-results\kicad10\render-bottom.png ayab-esp32/ayab-esp32.kicad_pcb
```

stdout:

```text
Loading…
Build board outline

Create layers
Create tracks and vias
Create zones
Build Tech layers
Build Tech layer 11
Build Tech layer 9
Build Tech layer 15
Build Tech layer 13
Build Tech layer 7
Build Tech layer 5
Build Tech layer 3
Build Tech layer 1
Build Tech layer 17
Build Tech layer 19
Build Tech layer 21
Build Tech layer 23
Build Tech layer 39
Build Tech layer 41
Build Tech layer 43
Build Tech layer 45
Build Tech layer 47
Build Tech layer 49
Build Tech layer 51
Build Tech layer 53
Build Tech layer 55
Build Tech layer 57
Build Tech layer 59
Build Tech layer 61
Build Tech layer 63
Build Tech layer 65
Build Tech layer 67
Build Tech layer 69
Build Tech layer 71
Build Tech layer 73
Build Tech layer 75
Build Tech layer 77
Build Tech layer 79
Build Tech layer 81
Build Tech layer 83
Build Tech layer 85
Build Tech layer 87
Build Tech layer 89
Build Tech layer 91
Build Tech layer 93
Build Tech layer 95
Build Tech layer 97
Build Tech layer 99
Build Tech layer 101
Build Tech layer 103
Build Tech layer 105
Build Tech layer 107
Build Tech layer 109
Build Tech layer 111
Build Tech layer 113
Build Tech layer 115
Build Tech layer 117
Build Tech layer 119
Build Tech layer 121
Build Tech layer 123
Build Tech layer 125
Build Tech layer 127
Simplifying copper layer polygons
Calculating plated copper
Simplify holes contours
Build BVH for holes and vias
Load Raytracing: board
Load Raytracing: layers
Loading 3D models...
Reload time 2.285 s
Rendering: 16 
Rendering: 33 
Rendering: 44 
Rendering: 54 
Rendering: 63 
Rendering: 64 
Rendering: 73 
Rendering: 82 
Rendering: 100 
Rendering time 6.467 s
Successfully created 3D render image
```

stderr:

```text
(empty)
```

### KiCad 10: render-top

Working directory: `C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\source-kicad10`

Exit: **0**

```text
"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe" pcb render --side top --width 3600 --height 1000 --zoom 3 -o C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\audit-results\kicad10\render-top.png ayab-esp32/ayab-esp32.kicad_pcb
```

stdout:

```text
Loading…
Build board outline

Create layers
Create tracks and vias
Create zones
Build Tech layers
Build Tech layer 11
Build Tech layer 9
Build Tech layer 15
Build Tech layer 13
Build Tech layer 7
Build Tech layer 5
Build Tech layer 3
Build Tech layer 1
Build Tech layer 17
Build Tech layer 19
Build Tech layer 21
Build Tech layer 23
Build Tech layer 39
Build Tech layer 41
Build Tech layer 43
Build Tech layer 45
Build Tech layer 47
Build Tech layer 49
Build Tech layer 51
Build Tech layer 53
Build Tech layer 55
Build Tech layer 57
Build Tech layer 59
Build Tech layer 61
Build Tech layer 63
Build Tech layer 65
Build Tech layer 67
Build Tech layer 69
Build Tech layer 71
Build Tech layer 73
Build Tech layer 75
Build Tech layer 77
Build Tech layer 79
Build Tech layer 81
Build Tech layer 83
Build Tech layer 85
Build Tech layer 87
Build Tech layer 89
Build Tech layer 91
Build Tech layer 93
Build Tech layer 95
Build Tech layer 97
Build Tech layer 99
Build Tech layer 101
Build Tech layer 103
Build Tech layer 105
Build Tech layer 107
Build Tech layer 109
Build Tech layer 111
Build Tech layer 113
Build Tech layer 115
Build Tech layer 117
Build Tech layer 119
Build Tech layer 121
Build Tech layer 123
Build Tech layer 125
Build Tech layer 127
Simplifying copper layer polygons
Calculating plated copper
Simplify holes contours
Build BVH for holes and vias
Load Raytracing: board
Load Raytracing: layers
Loading 3D models...
Reload time 3.682 s
Rendering: 15 
Rendering: 32 
Rendering: 43 
Rendering: 53 
Rendering: 63 
Rendering: 71 
Rendering: 80 
Rendering: 100 
Rendering time 5.860 s
Successfully created 3D render image
```

stderr:

```text
(empty)
```

### KiCad 10: version

Working directory: `C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\source-kicad10`

Exit: **0**

```text
"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe" version
```

stdout:

```text
10.0.6
```

stderr:

```text
(empty)
```

### validator-artwork-before-repair

Working directory: `C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764`

Exit: **0**

```text
C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\independent-audit-647998e\kicad9-runtime\bin\python.exe -c "import importlib.util;from pathlib import Path;s=importlib.util.spec_from_file_location(\"validator\",'C:\\Users\\bjrem\\Documents\\Codex\\2026-09-11\\files-pasted-by-the-user-perform\\work\\preorder-audit-9bde764\\source\\ayab-esp32\\tools\\validate_rev_a_manufacturing_metadata.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.PCB=Path('C:\\Users\\bjrem\\Documents\\Codex\\2026-09-11\\files-pasted-by-the-user-perform\\work\\preorder-audit-9bde764\\test-fixtures\\artwork-overlap.kicad_pcb');m.main()"
```

stdout:

```text
MANUFACTURING_METADATA_OK
ORDERING_REFS 9
DNP_REFS 11
PINNED_FOOTPRINT_IDS 18
PINNED_FOOTPRINT_INSTANCES 23
CONTROLLED_BOARD_RULES 5
CONTROLLED_ASSEMBLY_LABELS 5
FOOTPRINT_TREE_UUIDS_UNIQUE 6053
REVISION_LABEL_CLEARANCE_OK
```

stderr:

```text
(empty)
```

### repaired-manufacturing-validator

Working directory: `C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\repaired-source`

Exit: **0**

```text
C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\independent-audit-647998e\kicad9-runtime\bin\python.exe ayab-esp32/tools/validate_rev_a_manufacturing_metadata.py
```

stdout:

```text
MANUFACTURING_METADATA_OK
ORDERING_REFS 9
DNP_REFS 11
PINNED_FOOTPRINT_IDS 18
PINNED_FOOTPRINT_INSTANCES 23
CONTROLLED_BOARD_RULES 5
CONTROLLED_ASSEMBLY_LABELS 5
FOOTPRINT_TREE_UUIDS_UNIQUE 6053
REVISION_LABEL_CLEARANCE_OK
```

stderr:

```text
(empty)
```

### repair-regression-tests

Working directory: `C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\repaired-source`

Exit: **0**

```text
C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\independent-audit-647998e\kicad9-runtime\bin\python.exe ayab-esp32/tools/test_rev_a_manufacturing_metadata.py -v
```

stdout:

```text
(empty)
```

stderr:

```text
test_artwork_overlap_is_rejected (__main__.RevisionLabelClearanceTests.test_artwork_overlap_is_rejected) ... ok
test_previous_pad_overlap_is_rejected (__main__.RevisionLabelClearanceTests.test_previous_pad_overlap_is_rejected) ... Adding duplicate image handler for 'PNG file'
Adding duplicate image handler for 'JPEG file'
Adding duplicate image handler for 'TIFF file'
Adding duplicate image handler for 'GIF file'
Adding duplicate image handler for 'PNM file'
Adding duplicate image handler for 'PCX file'
Adding duplicate image handler for 'IFF file'
Adding duplicate image handler for 'Windows icon file'
Adding duplicate image handler for 'Windows cursor file'
Adding duplicate image handler for 'Windows animated cursor file'
Adding duplicate image handler for 'TGA file'
Adding duplicate image handler for 'XPM file'
ok
test_release_label_passes (__main__.RevisionLabelClearanceTests.test_release_label_passes) ... Adding duplicate image handler for 'PNG file'
Adding duplicate image handler for 'JPEG file'
Adding duplicate image handler for 'TIFF file'
Adding duplicate image handler for 'GIF file'
Adding duplicate image handler for 'PNM file'
Adding duplicate image handler for 'PCX file'
Adding duplicate image handler for 'IFF file'
Adding duplicate image handler for 'Windows icon file'
Adding duplicate image handler for 'Windows cursor file'
Adding duplicate image handler for 'Windows animated cursor file'
Adding duplicate image handler for 'TGA file'
Adding duplicate image handler for 'XPM file'
ok

----------------------------------------------------------------------
Ran 3 tests in 3.425s

OK
```

### repair-patch-check

Working directory: `C:\Users\bjrem\Documents\Codex\2026-09-10\referenced-chatgpt-conversation-this-is-an\work\ayab-hardware-current`

Exit: **0**

```text
git apply --check C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\audit-results\remaining-repairs.patch
```

stdout:

```text
(empty)
```

stderr:

```text
(empty)
```

### repair-patch-application-test

Working directory: `C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\patch-apply-check`

Exit: **0**

```text
git apply C:\Users\bjrem\Documents\Codex\2026-09-11\files-pasted-by-the-user-perform\work\preorder-audit-9bde764\audit-results\remaining-repairs.patch
```

stdout:

```text
(empty)
```

stderr:

```text
(empty)
```

### final status

Working directory: `C:\Users\bjrem\Documents\Codex\2026-09-10\referenced-chatgpt-conversation-this-is-an\work\ayab-hardware-current`

Exit: **0**

```text
git status --short
```

stdout:

```text
?? ayab-esp32/tools/__pycache__/
?? render-34512445704/
?? work-pcbnew-api.log
```

stderr:

```text
(empty)
```

### final branch

Working directory: `C:\Users\bjrem\Documents\Codex\2026-09-10\referenced-chatgpt-conversation-this-is-an\work\ayab-hardware-current`

Exit: **0**

```text
git branch --show-current
```

stdout:

```text
ayab-esp32-kh910-rev-a
```

stderr:

```text
(empty)
```

### final head

Working directory: `C:\Users\bjrem\Documents\Codex\2026-09-10\referenced-chatgpt-conversation-this-is-an\work\ayab-hardware-current`

Exit: **0**

```text
git rev-parse HEAD
```

stdout:

```text
9bde764c6e157920af34ccd1063949ac5dcc5109
```

stderr:

```text
(empty)
```

### final remote

Working directory: `C:\Users\bjrem\Documents\Codex\2026-09-10\referenced-chatgpt-conversation-this-is-an\work\ayab-hardware-current`

Exit: **0**

```text
git ls-remote origin refs/heads/ayab-esp32-kh910-rev-a
```

stdout:

```text
9bde764c6e157920af34ccd1063949ac5dcc5109	refs/heads/ayab-esp32-kh910-rev-a
```

stderr:

```text
(empty)
```


## Appendix F. Evidence and repair index

- `kicad9/` and `kicad10/`: separated native reports, console records, electrical netlists, config and renders.
- `independent-*.json`, `critical-*.json`, `native-associations.json`: independent geometry, connectivity, metadata, uniqueness and clearance checks.
- `ci-*.json`: fresh API records for all six runs, jobs and branch sequence.
- `source-*.json`, `raw-git-blob-comparison.json`, `final-source-integrity.json`: source content, newline handling and preservation evidence.
- `repair-summary.json`, `repair-regression-tests.json`, `repair-patch-*.json`, `remaining-repairs.patch`: concrete repairs and regression/patch verification.
- `audit-helpers/`: external audit orchestration. Helpers retain machine-specific paths; adapt paths and supply source/runtime dependencies when reproducing elsewhere.

Negative-test fixture boards are not release inputs and are excluded from delivery. The source ZIP and patch identify the additional local repairs separately from the upstream commit.
