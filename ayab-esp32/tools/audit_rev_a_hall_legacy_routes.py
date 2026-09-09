#!/usr/bin/env python3
from __future__ import annotations
import re
from pathlib import Path

PCB = Path(__file__).resolve().parents[1] / "ayab-esp32.kicad_pcb"
OUT = Path(__file__).resolve().parents[1] / "KH910_REV_A_HALL_LEGACY_ROUTES.md"
TARGET_IDS = {26: "/ESP32/EOL_L_P", 27: "/ESP32/EOL_L_N"}


def balanced(text: str, start: int) -> tuple[str,int]:
    depth=0; ins=False; esc=False
    for i in range(start,len(text)):
        c=text[i]
        if ins:
            if esc: esc=False
            elif c=='\\': esc=True
            elif c=='"': ins=False
            continue
        if c=='"': ins=True
        elif c=='(': depth+=1
        elif c==')':
            depth-=1
            if depth==0: return text[start:i+1],i+1
    raise RuntimeError("unterminated")


def blocks(text: str, token: str):
    pos=0
    while True:
        pos=text.find(token,pos)
        if pos<0: return
        b,end=balanced(text,pos)
        yield b
        pos=end


def xy(block: str, kind: str):
    m=re.search(rf'\({kind}\s+([-+0-9.eE]+)\s+([-+0-9.eE]+)',block)
    return (float(m.group(1)),float(m.group(2))) if m else None


def main():
    t=PCB.read_text(errors='replace')
    rows=[]
    for kind,token in (("segment","(segment "),("via","(via "),("arc","(arc ")):
        for b in blocks(t,token):
            n=re.search(r'\(net\s+(\d+)\)',b)
            if not n or int(n.group(1)) not in TARGET_IDS: continue
            nid=int(n.group(1)); layer=re.search(r'\(layer\s+"([^"]+)"\)',b)
            s=xy(b,'start'); e=xy(b,'end'); at=xy(b,'at')
            rows.append((nid,kind,layer.group(1) if layer else 'F.Cu-B.Cu',s,e,at,b))
    lines=["# KH910 Rev A — Legacy Hall Route Audit","",f"Total items: **{len(rows)}**","", "The baseline PCB is DRC-clean. These are the exact legacy EOL_L_P/EOL_L_N copper items before Hall migration.",""]
    for nid in (26,27):
        items=[r for r in rows if r[0]==nid]
        lines += [f"## {TARGET_IDS[nid]} — {len(items)} items",""]
        for i,r in enumerate(items,1):
            _,kind,layer,s,e,at,_=r
            if kind=='via': desc=f"via at {at}"
            else: desc=f"{kind} {s} -> {e}"
            lines.append(f"{i}. `{layer}` {desc}")
        lines.append("")
        lines += ["### MCU-near subset (x >= 205 or y <= 145)",""]
        mcu=[]
        for i,r in enumerate(items,1):
            pts=[p for p in (r[3],r[4],r[5]) if p]
            if any(p[0]>=205 or p[1]<=145 for p in pts): mcu.append((i,r))
        for i,r in mcu:
            _,kind,layer,s,e,at,_=r
            desc=f"via at {at}" if kind=='via' else f"{kind} {s} -> {e}"
            lines.append(f"- item {i}: `{layer}` {desc}")
        lines.append("")
    OUT.write_text('\n'.join(lines)+'\n')
    print(OUT)

if __name__=='__main__': main()
