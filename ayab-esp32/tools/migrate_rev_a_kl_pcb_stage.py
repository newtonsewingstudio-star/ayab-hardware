#!/usr/bin/env python3
"""Stage the Rev A KH-910 K/L PCB parity migration.

The validated schematic keeps the physical machine K/L nets under KiCad's
compiled names /BROTHER-CONNECTORS/EOL_R_N and EOL_R_S, while J702.6/.7 and
U701.8/.9 become isolated local level-shifter channels.  This transformer:

- splits the J702/U701/R711-R714 local branches away from the machine nets;
- retags the already DRC-clean ESP17/ESP18 GPIO corridors to machine K/L;
- retags U201 GPIO17/GPIO18 and J202.2/.3 to machine K/L;
- adds R213/R214 10k 3.3 V pull-ups near the existing MCU pull-up bank;
- adds only the short endpoint vias/stubs needed by the separate A* router.

It is intentionally staged.  The repository PCB must not be replaced unless the
follow-up router, zone refill, topology validator and project-aware DRC all pass.
"""
from __future__ import annotations

import argparse
import re
import uuid
from pathlib import Path

import migrate_rev_a_hall_pcb_serialized_compat as compat

k = compat.migration
reference = compat.reference
value = compat.value
replace_property = compat.replace_property

MACH_K = "/BROTHER-CONNECTORS/EOL_R_N"
MACH_L = "/BROTHER-CONNECTORS/EOL_R_S"
ESP17 = "/ESP32/ESP17"
ESP18 = "/ESP32/ESP18"
P3V3 = "+3V3"
LOCAL_K = "Net-(J702-Pin_6)"
LOCAL_L = "Net-(J702-Pin_7)"

BRIDGE_K = {(194.71, 151.86), (194.71, 157.31)}
BRIDGE_L = {(194.98, 151.99), (194.98, 157.69)}

R213_POS = (209.5, 132.025)
R214_POS = (209.5, 135.325)
R213_P1 = (210.325, 132.025)
R213_P2 = (208.675, 132.025)
R214_P1 = (210.325, 135.325)
R214_P2 = (208.675, 135.325)
R210_P1 = (211.925, 132.025)
R814_P1 = (211.925, 135.325)

ROUTE_ENDPOINTS = {
    MACH_K: [((194.71, 151.86), (194.71, 130.91)), ((207.5, 132.025), (207.5, 130.91))],
    MACH_L: [((194.98, 151.99), (194.98, 130.71)), ((207.5, 135.325), (205.5, 130.71))],
}


def near(a, b, tol=0.003):
    return abs(a[0] - b[0]) <= tol and abs(a[1] - b[1]) <= tol


def same_pair(points, pair):
    if len(points) < 2:
        return False
    return (near(points[0], tuple(pair)[0]) and near(points[-1], tuple(pair)[1])) or (
        near(points[0], tuple(pair)[1]) and near(points[-1], tuple(pair)[0])
    )


def root_end(text: str) -> int:
    rs = k.root_start(text)
    depth = 0
    ins = False
    esc = False
    for i in range(rs, len(text)):
        c = text[i]
        if ins:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                ins = False
            continue
        if c == '"':
            ins = True
        elif c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                return i
    raise RuntimeError("board root end not found")


def clone_pullup(src: str, ref: str, pos: tuple[float, float], machine_net_id: int, machine_name: str, p3v3_id: int) -> str:
    out = replace_property(src, "Reference", ref)
    out = replace_property(out, "Value", "10k")
    # Copy R210's assembly-friendly 0603 geometry but replace the BOM metadata
    # with the exact fields from compiled R213/R214 schematic netlist.
    out, n = re.subn(r'(property "LCSC ID" ")([^"]+)(")', r'\1C25804\3', out, count=1)
    if n != 1:
        raise RuntimeError("R210 clone missing LCSC ID property")
    out, n = re.subn(r'(property "OEM PN" ")([^"]+)(")', r'\10603WAF1002T5E\3', out, count=1)
    if n != 1:
        raise RuntimeError("R210 clone missing OEM PN property")
    out, n = re.subn(r'\(at 212\.75 132\.025\)', f'(at {pos[0]} {pos[1]} 180)', out, count=1)
    if n != 1:
        raise RuntimeError("R210 clone top-level position not found exactly once")
    # Deterministic unique UUIDs make reruns reproducible and avoid collisions.
    idx = 0
    def repl(_m):
        nonlocal idx
        idx += 1
        return f'(uuid "{uuid.uuid5(uuid.NAMESPACE_URL, f"kh910-rev-a-{ref}-{idx}")}")'
    out = re.sub(r'\(uuid "[0-9a-f-]+"\)', repl, out)
    out = k.replace_pad_net_in_footprint(out, "1", p3v3_id, P3V3)
    out = k.replace_pad_net_in_footprint(out, "2", machine_net_id, machine_name)
    return out


def inventory(text: str):
    children = k.root_children(text)
    nets = {}
    fps = {}
    for s in children:
        b = text[s.start:s.end]
        if s.head == "net":
            n = k.parse_net_definition(b)
            if n:
                nets[n[1]] = n[0]
        elif s.head == "footprint":
            r = reference(b)
            if r:
                fps[r] = b
    return children, nets, fps


def migrate(src: Path, dst: Path) -> None:
    text = src.read_text(encoding="utf-8")
    children, nets, fps = inventory(text)
    for name in (MACH_K, MACH_L, ESP17, ESP18, P3V3):
        if name not in nets:
            raise RuntimeError(f"missing audited net {name}")
    if LOCAL_K in nets or LOCAL_L in nets:
        raise RuntimeError("local K/L split nets already exist")
    if "R213" in fps or "R214" in fps:
        raise RuntimeError("R213/R214 unexpectedly already on PCB")
    for r in ("J405", "J702", "R711", "R712", "R713", "R714", "R210", "R814", "J202", "U201", "U701"):
        if r not in fps:
            raise RuntimeError(f"missing audited footprint {r}")

    # Audit the exact pre-migration pad ownership before changing anything.
    expected = {
        ("J405", "8"): MACH_K, ("J405", "7"): MACH_L,
        ("J702", "6"): MACH_K, ("J702", "7"): MACH_L,
        ("R711", "1"): MACH_K, ("R712", "2"): MACH_K,
        ("R713", "1"): MACH_L, ("R714", "2"): MACH_L,
        ("U701", "8"): MACH_K, ("U701", "9"): MACH_L,
        ("J202", "2"): ESP17, ("J202", "3"): ESP18,
        ("U201", "21"): ESP17, ("U201", "22"): ESP18,
    }
    for (ref, pn), want in expected.items():
        got = k.pad_net(k.direct_pad_blocks(fps[ref])[pn])
        if not got or got[1] != want:
            raise RuntimeError(f"precondition {ref}.{pn}: {got} != {want}")

    local_ids = {LOCAL_K: max(nets.values()) + 1, LOCAL_L: max(nets.values()) + 2}
    edits = []
    last_net_end = None
    bridge_removed = {MACH_K: 0, MACH_L: 0}
    local_retagged = {MACH_K: 0, MACH_L: 0}
    gpio_copper = {ESP17: 0, ESP18: 0}

    pad_retags = {
        "J702": {"6": (local_ids[LOCAL_K], LOCAL_K), "7": (local_ids[LOCAL_L], LOCAL_L)},
        "R711": {"1": (local_ids[LOCAL_K], LOCAL_K)},
        "R712": {"2": (local_ids[LOCAL_K], LOCAL_K)},
        "R713": {"1": (local_ids[LOCAL_L], LOCAL_L)},
        "R714": {"2": (local_ids[LOCAL_L], LOCAL_L)},
        "U701": {"8": (local_ids[LOCAL_K], LOCAL_K), "9": (local_ids[LOCAL_L], LOCAL_L)},
        "J202": {"2": (nets[MACH_K], MACH_K), "3": (nets[MACH_L], MACH_L)},
        "U201": {"21": (nets[MACH_K], MACH_K), "22": (nets[MACH_L], MACH_L)},
    }

    for s in children:
        b = text[s.start:s.end]
        if s.head == "net":
            last_net_end = s.end
            continue
        if s.head == "footprint":
            ref = reference(b)
            if ref in pad_retags:
                nb = b
                for pn, (nid, nn) in pad_retags[ref].items():
                    nb = k.replace_pad_net_in_footprint(nb, pn, nid, nn)
                edits.append((s.start, s.end, nb))
            continue
        if s.head not in {"segment", "via", "arc"}:
            continue
        nid = k.item_net_id(b)
        pts = k.item_points(b)
        if nid == nets[ESP17]:
            edits.append((s.start, s.end, k.replace_item_net(b, nets[MACH_K])))
            gpio_copper[ESP17] += 1
            continue
        if nid == nets[ESP18]:
            edits.append((s.start, s.end, k.replace_item_net(b, nets[MACH_L])))
            gpio_copper[ESP18] += 1
            continue
        if nid == nets[MACH_K]:
            if same_pair(pts, BRIDGE_K):
                edits.append((s.start, s.end, ""))
                bridge_removed[MACH_K] += 1
            elif pts and all(x < 195.1 and y >= 157.0 for x, y in pts):
                edits.append((s.start, s.end, k.replace_item_net(b, local_ids[LOCAL_K])))
                local_retagged[MACH_K] += 1
            continue
        if nid == nets[MACH_L]:
            if same_pair(pts, BRIDGE_L):
                edits.append((s.start, s.end, ""))
                bridge_removed[MACH_L] += 1
            elif pts and all(x < 195.2 and y >= 157.0 for x, y in pts):
                edits.append((s.start, s.end, k.replace_item_net(b, local_ids[LOCAL_L])))
                local_retagged[MACH_L] += 1
            continue

    if last_net_end is None:
        raise RuntimeError("net table not found")
    if bridge_removed != {MACH_K: 1, MACH_L: 1}:
        raise RuntimeError(f"bridge removal mismatch {bridge_removed}")
    if gpio_copper != {ESP17: 7, ESP18: 7}:
        raise RuntimeError(f"audited GPIO corridor copper mismatch {gpio_copper}")
    if min(local_retagged.values()) < 8:
        raise RuntimeError(f"too little local branch copper retagged {local_retagged}")

    edits.append((last_net_end, last_net_end,
                  f'\n\t(net {local_ids[LOCAL_K]} "{LOCAL_K}")\n\t(net {local_ids[LOCAL_L]} "{LOCAL_L}")'))

    # Clone the existing 0603 footprint only after all source assertions pass.
    r213 = clone_pullup(fps["R210"], "R213", R213_POS, nets[MACH_K], MACH_K, nets[P3V3])
    r214 = clone_pullup(fps["R210"], "R214", R214_POS, nets[MACH_L], MACH_L, nets[P3V3])
    rend = root_end(text)
    extra = [r213, r214]
    # Short 3.3 V links into the existing pull-up bank.
    extra += [
        k.segment(R213_P1, R210_P1, "F.Cu", nets[P3V3], "kl-r213-3v3"),
        k.segment(R214_P1, R814_P1, "F.Cu", nets[P3V3], "kl-r214-3v3"),
        k.segment(R213_P2, (207.5, 132.025), "F.Cu", nets[MACH_K], "kl-r213-machine"),
        k.segment(R214_P2, (207.5, 135.325), "F.Cu", nets[MACH_L], "kl-r214-machine"),
    ]
    for name, pairs in ROUTE_ENDPOINTS.items():
        for idx, (a, b) in enumerate(pairs):
            extra.append(k.via(a, nets[name], f"kl-{name}-{idx}-start"))
            extra.append(k.via(b, nets[name], f"kl-{name}-{idx}-goal"))
    edits.append((rend, rend, "\n\t" + "\n\t".join(extra) + "\n"))

    for a, b, repl in sorted(edits, key=lambda e: (e[0], e[1]), reverse=True):
        text = text[:a] + repl + text[b:]
    dst.write_text(text, encoding="utf-8")
    print("KL_ELECTRICAL_STAGE_OK", dst)
    print("LOCAL_NET_IDS", local_ids)
    print("LOCAL_COPPER_RETAGGED", local_retagged)
    print("GPIO_CORRIDORS_RETAGGED", gpio_copper)


def validate(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    children, nets, fps = inventory(text)
    for name in (MACH_K, MACH_L, LOCAL_K, LOCAL_L, P3V3):
        if name not in nets:
            raise RuntimeError(f"validated board missing net {name}")
    for ref in ("R213", "R214"):
        if ref not in fps or value(fps[ref]) != "10k":
            raise RuntimeError(f"bad/missing {ref}")
    expected = {
        ("J405", "8"): MACH_K, ("J405", "7"): MACH_L,
        ("J702", "6"): LOCAL_K, ("J702", "7"): LOCAL_L,
        ("R711", "1"): LOCAL_K, ("R712", "2"): LOCAL_K,
        ("R713", "1"): LOCAL_L, ("R714", "2"): LOCAL_L,
        ("U701", "8"): LOCAL_K, ("U701", "9"): LOCAL_L,
        ("J202", "2"): MACH_K, ("J202", "3"): MACH_L,
        ("U201", "21"): MACH_K, ("U201", "22"): MACH_L,
        ("R213", "1"): P3V3, ("R213", "2"): MACH_K,
        ("R214", "1"): P3V3, ("R214", "2"): MACH_L,
    }
    for (ref, pn), want in expected.items():
        got = k.pad_net(k.direct_pad_blocks(fps[ref])[pn])
        if not got or got[1] != want:
            raise RuntimeError(f"validation {ref}.{pn}: {got} != {want}")
    # The old logical ESP17/18 PCB nets may remain in the net table, but must no
    # longer own pads or copper.
    for s in children:
        b = text[s.start:s.end]
        if s.head == "footprint":
            for pb in k.direct_pad_blocks(b).values():
                got = k.pad_net(pb)
                if got and got[1] in {ESP17, ESP18}:
                    raise RuntimeError(f"stale GPIO pad net remains: {got}")
        elif s.head in {"segment", "via", "arc"}:
            nid = k.item_net_id(b)
            if nid in {nets.get(ESP17), nets.get(ESP18)}:
                raise RuntimeError("stale GPIO corridor copper remains")
    print("KL_TOPOLOGY_VALIDATION_OK", path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path)
    ap.add_argument("output", type=Path, nargs="?")
    ap.add_argument("--validate", action="store_true")
    args = ap.parse_args()
    if args.validate:
        validate(args.input)
    else:
        if args.output is None:
            ap.error("output is required")
        migrate(args.input, args.output)


if __name__ == "__main__":
    main()
