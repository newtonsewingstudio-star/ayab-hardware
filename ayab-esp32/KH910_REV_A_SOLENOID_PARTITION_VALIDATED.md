# KH910 Rev A — Validated Solenoid Power Partition

Status: **PCB partition and high-side fail-safe gate integrated and validated.**

Validated with KiCad **9.0.9** on 2026-09-09.

## Promoted PCB baseline

Validated PCB commit:

- `f6939be62d4003606674687d116c649aa0e4e390`
- commit message: `Apply validated KH910 solenoid power partition`

Both the staged board and the installed repository-path board passed:

- **0 DRC violations**
- **0 unconnected pads**
- **0 footprint errors**

Workflow evidence:

- workflow: `KH910 Rev A Solenoid Partition Stage`
- successful staged-validation run: `34401711442`
- promotion run: `34401865506`

## Electrical partition now implemented on PCB

### Raw +12 V remains raw

The existing global raw +12 V backbone remains the machine/controller input rail. The left solenoid cluster is disconnected from that backbone at the former J401 feed. The old right-side J403 raw-feed branch is also removed from the solenoid connector common.

### Left solenoid-local rail is switched

The complete existing heavy local +12 V distribution around the three ULN2003A solenoid drivers is reused as `SOLENOID_12V_SW` rather than replaced with individual lift traces.

The following are now on `SOLENOID_12V_SW` on the PCB:

- J401 pads 9/10
- J406 pads 9/10
- J403 pads 9/10
- U302/U303/U304 COM pad 9
- C302/C303/C304 pad 1
- C603/C604/C605 pad 1

The six local 10 uF capacitors therefore remain physically with the solenoid load domain behind the future high-side switch. This avoids the impossible clearance geometry produced by trying to leave C603/C604/C605 on the interleaved raw bus.

The migration retagged:

- 32 existing left-local F.Cu +12 V track objects
- 4 existing local layer-transition vias
- existing heavy J401/J406 connector/common copper
- the J403 pad-9/pad-10 common bridge

### Switched interconnect

A new **1.0 mm** internal-layer route connects the left switched solenoid rail to the right J403 common. The validated route selected **In1.Cu** and lands directly on the J403 through-hole common, avoiding the dense J403 signal fan-out and avoiding the extra right-side via used by the rejected layout.

## Why the earlier partition was rejected

The first clean staged partition attempted to keep the interleaved local horizontal bus raw and lift six solenoid branches away from it. KiCad DRC showed that architecture was physically invalid:

- vertical lift traces crossed adjacent capacitor GND pads/vias;
- switched pads were only about 0.055 mm from the old raw bus;
- an added right-side via collided with J403 solenoid signal fan-out.

That attempt reached 46 DRC violations / 3 unconnected. The architecture above eliminates those conflicts and validates at 0/0.

## High-side gate integration

The high-side gate was integrated into the PCB in commit `350f7d0` and is
checked directly by the `KH910 Rev A Solenoid Gate Validation` workflow. The
integrated board has 0 DRC violations, 0 unconnected pads, 0 footprint errors,
and the required default-OFF topology.

The implemented gate is:

- Q805 — LP9435LT1G P-channel high-side MOSFET
- Q806 — AO3400A N-channel gate pull-down MOSFET
- R820 — 100 kOhm P-MOS gate-to-source pull-up (default OFF)
- R821 — 10 kOhm GPIO21 to Q806 gate
- R822 — 100 kOhm Q806 gate pulldown
- GPIO21 / `SOLENOID_PWR_EN`

This closes the solenoid-gate PCB implementation item. It does not replace
prototype power-state testing or the separate final manufacturing review.

## Release status

- Hall input PCB parity: complete / clean
- K/L PCB parity: complete / clean
- Solenoid raw/switched partition: **complete / clean**
- Solenoid high-side fail-safe gate physical PCB: **complete / clean**
- KH-910 connector/power mapping: **open**
- final release/BOM/manufacturing audit: **open**

Do not fabricate Rev A until the remaining gates above are closed.
