#!/usr/bin/env python3
"""Extract exact PCB geometry needed to route the Rev A solenoid fail-safe."""
from __future__ import annotations
import math, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PCB=ROOT/'ayab-esp32.kicad_pcb'
SOL=ROOT/'solenoids.kicad_sch'
OUT=ROOT/'KH910_REV_A_SOLENOID_ROUTING_AUDIT.md'

def block(text,start):
    d=0; ins=False; esc=False
    for i in range(start,len(text)):
        c=text[i]
        if ins:
            if esc: esc=False
            elif c=='\\': esc=True
            elif c=='"': ins=False
            continue
        if c=='"': ins=True
        elif c=='(': d+=1
        elif c==')':
            d-=1
            if d==0:return text[start:i+1],i+1
    raise RuntimeError('unbalanced')

def blocks(text,token):
    p=0
    while 1:
        p=text.find(token,p)
        if p<0:return
        b,e=block(text,p);yield b;p=e

def ref(b):
    for pat in (r'\(property "Reference" "([^"]+)"',r'\(fp_text reference "([^"]+)"'):
        m=re.search(pat,b)
        if m:return m.group(1)
    return ''

def val(b):
    for pat in (r'\(property "Value" "([^"]+)"',r'\(fp_text value "([^"]+)"'):
        m=re.search(pat,b)
        if m:return m.group(1)
    return ''

def fpat(b):
    m=re.match(r'\(footprint\s+"([^"]+)"',b);return m.group(1) if m else ''

def fpos(b):
    m=re.search(r'^\(footprint.*?\(at\s+([-\d.]+)\s+([-\d.]+)(?:\s+([-\d.]+))?\)',b,re.S)
    return tuple(float(m.group(i) or 0) for i in (1,2,3)) if m else (0,0,0)

def pads(b):
    out=[]
    x0,y0,a=fpos(b); th=math.radians(a); ca=math.cos(th); sa=math.sin(th)
    for pb in blocks(b,'(pad '):
        mn=re.match(r'\(pad\s+"?([^"\s)]*)"?',pb); num=mn.group(1) if mn else '?'
        ma=re.search(r'\(at\s+([-\d.]+)\s+([-\d.]+)',pb); lx=float(ma.group(1)) if ma else 0; ly=float(ma.group(2)) if ma else 0
        # KiCad footprint local coordinates rotate with the footprint.
        gx=x0+lx*ca-ly*sa; gy=y0+lx*sa+ly*ca
        net=re.search(r'\(net\s+(\d+)\s+"([^"]+)"\)',pb)
        out.append((num,gx,gy,int(net.group(1)) if net else 0,net.group(2) if net else ''))
    return out

def sch_path_for(project_ref):
    s=SOL.read_text()
    for sb in blocks(s,'(symbol (lib_id '):
        if f'(reference "{project_ref}")' not in sb: continue
        # pick project ayab-esp32 path ending at symbol uuid
        m=re.search(r'\(project "ayab-esp32".*?\(path "([^"]+)"\s*\n\s*\(reference "'+re.escape(project_ref)+r'"\)',sb,re.S)
        if m:return m.group(1)
    return ''

def segs_for_net(pcb,n):
    out=[]
    for sb in blocks(pcb,'(segment '):
        mn=re.search(r'\(net\s+(\d+)\)',sb)
        if not mn or int(mn.group(1))!=n: continue
        ms=re.search(r'\(start\s+([-\d.]+)\s+([-\d.]+)\)',sb); me=re.search(r'\(end\s+([-\d.]+)\s+([-\d.]+)\)',sb)
        mw=re.search(r'\(width\s+([-\d.]+)\)',sb); ml=re.search(r'\(layer\s+"([^"]+)"\)',sb)
        if ms and me:out.append((float(ms.group(1)),float(ms.group(2)),float(me.group(1)),float(me.group(2)),float(mw.group(1)) if mw else 0,ml.group(1) if ml else ''))
    return out

def vias_for_net(pcb,n):
    out=[]
    for vb in blocks(pcb,'(via '):
        mn=re.search(r'\(net\s+(\d+)\)',vb)
        if not mn or int(mn.group(1))!=n:continue
        ma=re.search(r'\(at\s+([-\d.]+)\s+([-\d.]+)\)',vb); ms=re.search(r'\(size\s+([-\d.]+)\)',vb); md=re.search(r'\(drill\s+([-\d.]+)\)',vb)
        if ma:out.append((float(ma.group(1)),float(ma.group(2)),float(ms.group(1)) if ms else 0,float(md.group(1)) if md else 0))
    return out

def dist_point_seg(px,py,s):
    x1,y1,x2,y2,*_=s; dx=x2-x1;dy=y2-y1
    if dx==dy==0:return math.hypot(px-x1,py-y1)
    t=max(0,min(1,((px-x1)*dx+(py-y1)*dy)/(dx*dx+dy*dy)))
    return math.hypot(px-(x1+t*dx),py-(y1+t*dy))

def main():
    pcb=PCB.read_text(errors='replace'); fps=list(blocks(pcb,'(footprint ')); by={ref(b):b for b in fps if ref(b)}
    netdefs={int(n):name for n,name in re.findall(r'^\s*\(net\s+(\d+)\s+"([^"]+)"\)',pcb,re.M)}
    maxnet=max(netdefs) if netdefs else 0
    seg4=segs_for_net(pcb,4);via4=vias_for_net(pcb,4)
    targets=[]
    for r in ['J401','J403','J406','U302','U303','U304']:
        b=by[r]
        for p in pads(b):
            if p[3]==4: targets.append((r,)+p)
    lines=['# KH910 Rev A — Solenoid Routing Audit','',f'- max existing net number: **{maxnet}**',f'- +12V segments: **{len(seg4)}**',f'- +12V vias: **{len(via4)}**','','## Target +12 V pads that must move to SOLENOID_12V_SW','', '| Ref | Pad | Global X | Global Y | Current net | Nearest +12V copper |','|---|---:|---:|---:|---|---:|']
    for r,pn,x,y,n,name in targets:
        nearest=min((dist_point_seg(x,y,s) for s in seg4),default=999)
        lines.append(f'| {r} | {pn} | {x:.3f} | {y:.3f} | `{name}` | {nearest:.3f} mm |')
    lines+=['','## +12V copper segments within 12 mm of any target pad','']
    near=[]
    for s in seg4:
        if min((dist_point_seg(x,y,s) for _,_,x,y,_,_ in targets),default=999)<=12:near.append(s)
    for s in near:lines.append(f'- `{s[5]}` width {s[4]:.3f}: ({s[0]:.3f},{s[1]:.3f}) -> ({s[2]:.3f},{s[3]:.3f})')
    lines+=['','## Existing +12V vias near target pads','']
    for v in via4:
        if min((math.hypot(v[0]-x,v[1]-y) for _,_,x,y,_,_ in targets),default=999)<=12: lines.append(f'- via ({v[0]:.3f},{v[1]:.3f}) size {v[2]:.3f} drill {v[3]:.3f}')
    lines+=['','## Existing MOSFET footprint templates','']
    for r,b in sorted(by.items()):
        lc=re.search(r'\(property "LCSC ID" "([^"]+)"',b); l=lc.group(1) if lc else ''
        if l in ('C383257','C20917') or val(b) in ('LP9435LT1G','AO3400A'):
            lines.append(f'### {r} — {val(b)} / {l}')
            lines.append(f'- footprint `{fpat(b)}` at {fpos(b)}')
            for p in pads(b):lines.append(f'- pad {p[0]} global ({p[1]:.3f},{p[2]:.3f}) net `{p[4]}`')
            lines.append('')
    lines+=['## New schematic device paths','']
    for r in ['Q805','Q806','R820','R821','R822']:
        lines.append(f'- {r}: `{sch_path_for(r)}`')
    # Board extents from Edge.Cuts line/arc coordinates, coarse but enough for placement context.
    coords=[]
    for gb in blocks(pcb,'(gr_line '):
        if '"Edge.Cuts"' not in gb:continue
        for m in re.finditer(r'\((?:start|end)\s+([-\d.]+)\s+([-\d.]+)\)',gb):coords.append((float(m.group(1)),float(m.group(2))))
    if coords:
        xs=[p[0] for p in coords];ys=[p[1] for p in coords]
        lines+=['','## Coarse board edge bounds','',f'- X: {min(xs):.3f} .. {max(xs):.3f}',f'- Y: {min(ys):.3f} .. {max(ys):.3f}']
    OUT.write_text('\n'.join(lines)+'\n');print(OUT)
if __name__=='__main__':main()
