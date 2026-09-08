#!/usr/bin/env python3
"""Inventory every board object attached to the existing +12V net."""
from __future__ import annotations
import math,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; PCB=ROOT/'ayab-esp32.kicad_pcb'; OUT=ROOT/'KH910_REV_A_12V_BUS_AUDIT.md'

def block(t,s):
 d=0;ins=False;esc=False
 for i in range(s,len(t)):
  c=t[i]
  if ins:
   if esc:esc=False
   elif c=='\\':esc=True
   elif c=='"':ins=False
   continue
  if c=='"':ins=True
  elif c=='(':d+=1
  elif c==')':
   d-=1
   if d==0:return t[s:i+1],i+1
 raise RuntimeError('unbalanced')
def blocks(t,token):
 p=0
 while 1:
  p=t.find(token,p)
  if p<0:return
  b,e=block(t,p);yield b;p=e
def fp_ref(b):
 for p in (r'\(property "Reference" "([^"]+)"',r'\(fp_text reference "([^"]+)"'):
  m=re.search(p,b)
  if m:return m.group(1)
 return '?'
def fp_val(b):
 for p in (r'\(property "Value" "([^"]+)"',r'\(fp_text value "([^"]+)"'):
  m=re.search(p,b)
  if m:return m.group(1)
 return '?'
def fpos(b):
 m=re.search(r'^\(footprint.*?\(at\s+([-\d.]+)\s+([-\d.]+)(?:\s+([-\d.]+))?\)',b,re.S)
 return tuple(float(m.group(i) or 0) for i in (1,2,3)) if m else (0,0,0)
def global_pad(fp,pb):
 x0,y0,a=fpos(fp);m=re.search(r'\(at\s+([-\d.]+)\s+([-\d.]+)',pb);lx=float(m.group(1)) if m else 0;ly=float(m.group(2)) if m else 0
 th=math.radians(a);return x0+lx*math.cos(th)-ly*math.sin(th),y0+lx*math.sin(th)+ly*math.cos(th)
def main():
 t=PCB.read_text(errors='replace'); lines=['# KH910 Rev A — Existing +12 V Bus Audit','']
 rows=[]
 for fp in blocks(t,'(footprint '):
  for pb in blocks(fp,'(pad '):
   n=re.search(r'\(net\s+(\d+)\s+"([^"]+)"\)',pb)
   if not n or n.group(2)!='+12V':continue
   pm=re.match(r'\(pad\s+"?([^"\s)]*)"?',pb);pn=pm.group(1) if pm else '?';x,y=global_pad(fp,pb)
   typ='SMD' if ' smd ' in pb[:100] else ('TH' if ' thru_hole ' in pb[:120] else '?')
   rows.append((fp_ref(fp),fp_val(fp),pn,x,y,typ))
 lines+=['## All footprint pads currently on +12V','', '| Ref | Value | Pad | X | Y | Type |','|---|---|---:|---:|---:|---|']
 for r,v,p,x,y,typ in sorted(rows):lines.append(f'| {r} | {v} | {p} | {x:.3f} | {y:.3f} | {typ} |')
 lines+=['','## +12V zones','']
 z=0
 for zb in blocks(t,'(zone '):
  n=re.search(r'\(net\s+(\d+)\)',zb);name=re.search(r'\(net_name\s+"([^"]+)"\)',zb)
  if (n and n.group(1)=='4') or (name and name.group(1)=='+12V'):
   z+=1; layer=re.search(r'\(layer\s+"([^"]+)"\)',zb);layers=re.search(r'\(layers\s+([^\n]+)\)',zb)
   lines.append(f'- zone {z}: layer={layer.group(1) if layer else (layers.group(1).strip() if layers else "?")}')
   # coarse polygon bounds
   pts=[(float(a),float(b)) for a,b in re.findall(r'\(xy\s+([-\d.]+)\s+([-\d.]+)\)',zb)]
   if pts:
    lines.append(f'  - bounds X {min(x for x,_ in pts):.3f}..{max(x for x,_ in pts):.3f}, Y {min(y for _,y in pts):.3f}..{max(y for _,y in pts):.3f}')
 if not z:lines.append('- none')
 lines+=['','## +12V segment endpoints with degree 1 (possible branch/source ends)','']
 seg=[]
 for sb in blocks(t,'(segment '):
  n=re.search(r'\(net\s+(\d+)\)',sb)
  if not n or n.group(1)!='4':continue
  a=re.search(r'\(start\s+([-\d.]+)\s+([-\d.]+)\)',sb);b=re.search(r'\(end\s+([-\d.]+)\s+([-\d.]+)\)',sb);l=re.search(r'\(layer\s+"([^"]+)"\)',sb);w=re.search(r'\(width\s+([-\d.]+)\)',sb)
  if a and b:seg.append(((float(a.group(1)),float(a.group(2)),l.group(1) if l else '?'),(float(b.group(1)),float(b.group(2)),l.group(1) if l else '?'),float(w.group(1)) if w else 0))
 deg={}
 for a,b,w in seg:deg[a]=deg.get(a,0)+1;deg[b]=deg.get(b,0)+1
 for p,d in sorted(deg.items()):
  if d==1:lines.append(f'- {p[2]} ({p[0]:.3f},{p[1]:.3f})')
 OUT.write_text('\n'.join(lines)+'\n');print(OUT)
if __name__=='__main__':main()
