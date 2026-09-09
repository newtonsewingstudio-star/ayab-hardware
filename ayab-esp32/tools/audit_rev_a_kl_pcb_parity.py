#!/usr/bin/env python3
"""Read-only PCB parity audit for Rev A KH910 right-side K/L signals."""
from __future__ import annotations
from pathlib import Path
import pcbnew

ROOT=Path(__file__).resolve().parents[1]
PCB=ROOT/'ayab-esp32.kicad_pcb'
OUT=ROOT/'KH910_REV_A_KL_PCB_PARITY.md'
REFS={'U201','R213','R214','J202','J405','J702','U701','R711','R712','R713','R714'}
TOKENS=('EOL_R_N','EOL_R_S','KH910_R_K','KH910_R_L','J702-Pin_6','J702-Pin_7')

def mm(v): return pcbnew.ToMM(v)
def pt(p): return f'({mm(p.x):.4f}, {mm(p.y):.4f})'

def main():
    b=pcbnew.LoadBoard(str(PCB)); fps={f.GetReference():f for f in b.GetFootprints()}
    lines=['# KH910 Rev A — K/L PCB Parity Audit','',
           'Read-only inventory of the current repository PCB. The validated schematic separates the KH910 machine K/L inputs from the retained U701/J702 level-shifter channels.','',
           '## Footprints and pad nets','']
    for ref in sorted(REFS):
        f=fps.get(ref)
        if not f:
            lines += [f'### {ref}','- **MISSING**','']; continue
        lines += [f'### {ref} — {f.GetValue()}',f'- footprint: {pt(f.GetPosition())} rot {f.GetOrientationDegrees():.1f}']
        for p in f.Pads():
            lines.append(f'- pad {p.GetNumber()}: {pt(p.GetPosition())} net `{p.GetNetname()}` (#{p.GetNetCode()})')
        lines.append('')
    lines += ['## Matching board nets and connected pads','']
    for code,ni in sorted(b.GetNetInfo().NetsByNetcode().items()):
        name=ni.GetNetname()
        if not any(t in name for t in TOKENS): continue
        lines += [f'### net {code}: `{name}`','']
        members=[]
        for f in b.GetFootprints():
            for p in f.Pads():
                if p.GetNetCode()==code: members.append((f.GetReference(),p.GetNumber(),pt(p.GetPosition())))
        for ref,pn,xy in sorted(members): lines.append(f'- {ref}.{pn} at {xy}')
        lines.append('')
    lines += ['## Copper on matching nets','']
    for item in b.GetTracks():
        name=item.GetNetname()
        if not any(t in name for t in TOKENS): continue
        if isinstance(item,pcbnew.PCB_VIA):
            lines.append(f'- `{name}` via at {pt(item.GetPosition())}')
        else:
            lines.append(f'- `{name}` {b.GetLayerName(item.GetLayer())}: {pt(item.GetStart())} -> {pt(item.GetEnd())}')
    lines += ['','## Parity interpretation','',
              '- J405 machine K/L pads must ultimately remain on the dedicated machine-signal nets that reach the ESP32 through the new pull-up stage.',
              '- U701/J702 channels 6/7 must remain connected locally but must not remain electrically tied to J405 K/L after the Rev A PCB split.',
              '- Do not fabricate until this split and the analog Hall migration both pass project-aware DRC.','']
    OUT.write_text('\n'.join(lines)); print(OUT)
if __name__=='__main__': main()
