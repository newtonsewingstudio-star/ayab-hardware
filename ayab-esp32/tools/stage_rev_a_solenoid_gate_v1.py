#!/usr/bin/env python3
"""Stage only the KH910 Rev A solenoid high-side fail-safe gate.

Requires the already-promoted SOLENOID_12V_SW partition. Adds the current
schematic gate components Q805/Q806/R820/R821/R822/TP703 and local routing.
The caller must refill zones and pass KiCad DRC before promotion.
"""
from __future__ import annotations

from pathlib import Path
import sys
import re
import pcbnew

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import patch_rev_a_solenoid_pcb as u

P = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE.parent / "ayab-esp32.kicad_pcb"
SCH = HERE.parent / "solenoids.kicad_sch"
RAW = "+12V"
GND = "GND"
SW = "SOLENOID_12V_SW"
EN_OLD = "/ESP32/ESP21"
EN = "SOLENOID_PWR_EN"
PG = "Net-(Q805-G)"
NG = "Net-(Q806-G)"


def netnum_by_name(defs: dict[int, str], name: str) -> int:
    hits = [n for n, v in defs.items() if v == name]
    if len(hits) != 1:
        raise RuntimeError(f"expected exactly one PCB net {name!r}, got {hits}")
    return hits[0]


def assert_promoted_baseline() -> tuple[int, int, int, int]:
    b = pcbnew.LoadBoard(str(P))
    if b is None:
        raise RuntimeError("could not load staged PCB")
    j401 = next((f for f in b.GetFootprints() if f.GetReference() == "J401"), None)
    if j401 is None:
        raise RuntimeError("J401 missing")
    p9 = next((p for p in j401.Pads() if p.GetNumber() == "9"), None)
    if p9 is None or p9.GetNetname() != SW:
        raise RuntimeError(f"promoted partition missing: J401.9={None if p9 is None else p9.GetNetname()!r}")

    raw_bus = False
    for t in b.GetTracks():
        if isinstance(t, pcbnew.PCB_VIA) or t.GetNetname() != RAW or t.GetLayer() != pcbnew.B_Cu:
            continue
        a, z = t.GetStart(), t.GetEnd()
        x1, y1, x2, y2 = map(pcbnew.ToMM, (a.x, a.y, z.x, z.y))
        if abs(y1 - 163.1) < 0.08 and abs(y2 - 163.1) < 0.08 and min(x1, x2) <= 174.5 <= max(x1, x2):
            raw_bus = True
            break
    if not raw_bus:
        raise RuntimeError("raw +12V B.Cu backbone no longer spans x=174.5 at y=163.1")

    en_anchor = False
    for t in b.GetTracks():
        if not isinstance(t, pcbnew.PCB_VIA) or t.GetNetname() not in (EN_OLD, EN):
            continue
        p = t.GetPosition(); x, y = pcbnew.ToMM(p.x), pcbnew.ToMM(p.y)
        if abs(x - 222.3) < 0.08 and abs(y - 134.12) < 0.08:
            en_anchor = True
            break
    if not en_anchor:
        raise RuntimeError("GPIO21 enable anchor via near (222.3,134.12) missing")

    txt = P.read_text(encoding="utf-8")
    defs = u.net_defs(txt)
    raw = netnum_by_name(defs, RAW)
    gnd = netnum_by_name(defs, GND)
    sw = netnum_by_name(defs, SW)
    en_name = EN if EN in defs.values() else EN_OLD
    en = netnum_by_name(defs, en_name)
    return raw, gnd, sw, en


def main() -> None:
    raw, gnd, sw, en = assert_promoted_baseline()
    pcb = P.read_text(encoding="utf-8")
    sch = SCH.read_text(encoding="utf-8")
    refs = ("Q805", "Q806", "R820", "R821", "R822", "TP703")
    present = [r for r in refs if re.search(rf'\(fp_text reference "{r}"', pcb)]
    if present:
        raise RuntimeError("partial/already-present gate PCB state: " + ", ".join(present))

    defs = u.net_defs(pcb)
    if PG in defs.values() or NG in defs.values():
        raise RuntimeError("gate-only PCB nets already exist without gate footprints")
    pg, ng = max(defs) + 1, max(defs) + 2

    if EN_OLD in pcb:
        pcb = pcb.replace(EN_OLD, EN)
    elif EN not in pcb:
        raise RuntimeError("neither legacy nor current solenoid enable net name exists")
    pcb = u.insert_before_first(pcb, '  (footprint ', f'  (net {pg} "{PG}")\n  (net {ng} "{NG}")')

    _, _, q502 = u.find_fp(pcb, "Q502")
    _, _, q201 = u.find_fp(pcb, "Q201")
    _, _, r809 = u.find_fp(pcb, "R809")
    _, _, tp701 = u.find_fp(pcb, "TP701")
    prefix = u.sheet_prefix_from_existing(pcb)
    su = {r: u.symbol_uuid_by_ref(sch, r) for r in refs}
    path = lambda r: prefix + "/" + su[r]

    q805 = u.clone_fp(q502, "Q805", "LP9435LT1G", 172.0, 147.0, -90, path("Q805"), "C383257",
                      {"1": (pg, PG), "2": (raw, RAW), "3": (sw, SW)})
    q806 = u.clone_fp(q201, "Q806", "AO3400A", 172.0, 153.0, 0, path("Q806"), "C20917",
                      {"1": (ng, NG), "2": (gnd, GND), "3": (pg, PG)})
    r820 = u.clone_fp(r809, "R820", "100k", 175.0, 144.5, 0, path("R820"), "C25803",
                      {"1": (raw, RAW), "2": (pg, PG)})
    r821 = u.clone_fp(r809, "R821", "10k", 169.5, 159.0, 90, path("R821"), "C25804",
                      {"1": (en, EN), "2": (ng, NG)})
    r822 = u.clone_fp(r809, "R822", "100k", 172.0, 162.0, 0, path("R822"), "C25803",
                      {"1": (gnd, GND), "2": (ng, NG)})
    tp703 = u.clone_fp(tp701, "TP703", "SOL12_SW", 145.0, 159.0, 0, path("TP703"), "",
                       {"1": (sw, SW)})
    newfps = [q805, q806, r820, r821, r822, tp703]
    pcb = u.insert_before_first(pcb, '  (segment ', "\n".join(newfps))

    q805_g, q805_s, q805_d = (u.pad_global(q805, str(i)) for i in (1, 2, 3))
    q806_g, q806_s, q806_d = (u.pad_global(q806, str(i)) for i in (1, 2, 3))
    r820_raw, r820_pg = (u.pad_global(r820, str(i)) for i in (1, 2))
    r821_en, r821_ng = (u.pad_global(r821, str(i)) for i in (1, 2))
    r822_gnd, r822_ng = (u.pad_global(r822, str(i)) for i in (1, 2))
    tp = u.pad_global(tp703, "1")
    route: list[str] = []

    raw_top = (174.5, 147.0); raw_bus = (174.5, 163.1)
    route += [
        u.segment(*q805_s, *raw_top, 1.0, "F.Cu", raw),
        u.via(*raw_top, raw, 1.0, 0.5),
        u.segment(*raw_top, *raw_bus, 1.27, "In1.Cu", raw),
        u.via(*raw_bus, raw, 1.0, 0.5),
        u.segment(*r820_raw, *q805_s, 0.5, "F.Cu", raw),
    ]

    sw_top = (169.5, 147.0)
    route += [
        u.segment(*q805_d, *sw_top, 1.0, "F.Cu", sw),
        u.via(*sw_top, sw, 1.0, 0.5),
        u.segment(*sw_top, 155.0, 147.0, 1.27, "In1.Cu", sw),
        u.segment(155.0, 147.0, 140.0, 153.7852, 1.27, "In1.Cu", sw),
        u.segment(140.0, 153.7852, 116.84, 153.7852, 1.27, "In1.Cu", sw),
    ]

    route += [
        u.segment(*tp, 145.0, 157.5, 0.5, "F.Cu", sw),
        u.via(145.0, 157.5, sw, 0.8, 0.4),
        u.segment(145.0, 157.5, 140.0, 153.7852, 0.5, "In1.Cu", sw),
    ]

    route += [
        u.segment(*q805_g, *r820_pg, 0.25, "F.Cu", pg),
        u.segment(*q805_g, 172.0, 150.0, 0.25, "F.Cu", pg),
        u.segment(172.0, 150.0, *q806_d, 0.25, "F.Cu", pg),
        u.segment(*q806_g, *r821_ng, 0.25, "F.Cu", ng),
        u.segment(*r821_ng, 170.5, 160.5, 0.25, "F.Cu", ng),
        u.segment(170.5, 160.5, *r822_ng, 0.25, "F.Cu", ng),
    ]

    gv = (170.0, 160.5)
    route += [
        u.segment(*q806_s, *gv, 0.35, "F.Cu", gnd),
        u.segment(*r822_gnd, *gv, 0.35, "F.Cu", gnd),
        u.via(*gv, gnd, 0.8, 0.4),
    ]

    ev = (168.0, 157.5)
    route += [
        u.segment(222.3, 134.12, 205.0, 134.12, 0.25, "In1.Cu", en),
        u.segment(205.0, 134.12, 188.0, 142.0, 0.25, "In1.Cu", en),
        u.segment(188.0, 142.0, 176.0, 150.0, 0.25, "In1.Cu", en),
        u.segment(176.0, 150.0, *ev, 0.25, "In1.Cu", en),
        u.via(*ev, en, 0.6, 0.3),
        u.segment(*ev, *r821_en, 0.25, "F.Cu", en),
    ]

    pcb = u.insert_before_first(pcb, '  (zone ', "\n".join(route))
    for ref in refs:
        if not re.search(rf'\(fp_text reference "{ref}"', pcb):
            raise RuntimeError(f"serialized gate footprint missing: {ref}")
    for name in (SW, EN, PG, NG):
        if name not in pcb:
            raise RuntimeError(f"serialized gate net missing: {name}")
    if EN_OLD in pcb:
        raise RuntimeError("legacy ESP21 net name remains after gate staging")

    P.write_text(pcb, encoding="utf-8")
    print("SOLENOID_GATE_STAGED")
    print("nets", {"raw": raw, "gnd": gnd, "sw": sw, "en": en, "pg": pg, "ng": ng})
    for ref, block in zip(refs, newfps):
        print(ref, u.top_at(block))


if __name__ == "__main__":
    main()
