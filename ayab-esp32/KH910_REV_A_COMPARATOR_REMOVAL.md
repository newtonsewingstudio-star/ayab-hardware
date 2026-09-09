# KH910 Rev A — Legacy Comparator Removal Boundary

Status: approved implementation boundary for the next schematic/PCB cleanup stage.

## Decision

Remove the LM393 Hall/EOL comparator network that is electrically obsolete after the Rev A direct KH910 K/L and passive analog Hall changes.

### Remove

- U702 — LM393, left Hall/EOL comparator package
- U703 — LM393, right Hall/EOL comparator package
- C703, C704 — comparator-package 5 V decoupling
- R715–R718 — comparator output feedback / hysteresis paths
- R719–R722 — comparator input/reference coupling
- R723–R730 — comparator reference divider networks
- R731–R734 — legacy EOL/Hall raw-signal bias/load network

### Retain

- U701 — SN74LVC4245 encoder/control level shifter
- C701, C702 — U701 rail decoupling
- R701–R706 — retained encoder input conditioning
- R707–R714 — leave unchanged in this pass; these belong to the generic U701 A4–A7 / CTRL_5V channels and become electrically isolated from the Hall sensors once R715–R718 are removed
- R735/R736 — `EOL_L` to `HALL_L_ADC` passive 1:2 divider
- R737/R738 — `EOL_R` to `HALL_R_ADC` passive 1:2 divider
- TP701/TP702 — retain as raw Hall/EOL service test points; rename displayed values from `CMP-L` / `CMP-R` to `HALL-L-RAW` / `HALL-R-RAW`
- all Brother machine connectors
- direct KH910 K/L paths to GPIO17/GPIO18

## Electrical basis

The full hierarchical netlist audit establishes:

- `HALL_L_ADC`: R735 pin 2, R736 pin 1, ESP32 GPIO1
- `HALL_R_ADC`: R737 pin 2, R738 pin 1, ESP32 GPIO2
- raw `EOL_L`: machine connectors, R735 pin 1, TP701, plus obsolete U702/R731/R733 loading
- raw `EOL_R`: machine connectors, R737 pin 1, TP702, plus obsolete U703/R732/R734 loading

R731/R733 and R732/R734 must not remain as legacy bias networks on the new passive ADC inputs. The intended Rev A Hall path is the simple 10 kΩ / 10 kΩ passive divider only.

The K/L comparator outputs are no longer required for KH910: the top-level Rev A schematic already routes the native digital K and L signals independently to GPIO17 and GPIO18 with 3.3 V pull-ups.

## Why R707–R714 are not removed yet

R707–R714 are attached to U701 A4–A7 and the generic `CTRL_5V` header channels. They are not required for the Rev A Hall/K/L architecture, but removing them is a separate simplification decision. Keeping them temporarily avoids conflating comparator removal with possible repurposing or deletion of generic control-header channels.

## Validation gate

The schematic cleanup is acceptable only if a regenerated full hierarchical netlist proves:

1. U702 and U703 are absent.
2. C703/C704 and R715–R734 are absent.
3. R735–R738 remain.
4. `HALL_L_ADC` still connects R735/R736 to ESP32 GPIO1.
5. `HALL_R_ADC` still connects R737/R738 to ESP32 GPIO2.
6. encoder nets `ENC_A`, `ENC_B`, and `ENC_BP` still pass through U701.
7. direct `KH910_R_K` / `KH910_R_L` top-level paths remain unchanged.
8. KiCad can parse the complete schematic and export its netlist.

After schematic validation, remove the matching obsolete footprints and their now-orphaned copper from the PCB using the native `pcbnew` API, refill zones, and run DRC before placing the solenoid fail-safe gate.
