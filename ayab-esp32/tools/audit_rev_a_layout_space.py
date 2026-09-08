#!/usr/bin/env python3
from __future__ import annotations
import math,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; PCB=ROOT/'ayab-esp32.kicad_pcb'; OUT=ROOT/'KH910_REV_A_LAYOUT_SPACE_AUDIT.md'
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
 raise RuntimeError
def blocks(t,token):
 p=0
 while 1:
  p=t.find(token,p)
  if p<0:return
  b,e=block(t,p);yield b;p=e
def prop(b,k):
 m=re.search(r'\(property "'+re.escape(k)+r'" "([^"]+)"',b);return m.group(1) if m else ''
def ref(b):
 return prop(b,'Reference') or (re.search(r'\(fp_text reference "([^"]+)"',b).group(1) if re.search(r'\(fp_text reference "([^"]+)"',b) else '')
def val(b):
 return prop(b,'Value') or (re.search(r'\(fp_text value "([^"]+)"',b).group(1) if re.search(r'\(fp_text value "([^"]+)"',b) else '')
def pos(b):
 m=re.search(r'^\(footprint.*?\(at\s+([-\d.]+)\s+([-\d.]+)(?:\s+([-\d.]+))?\)',b,re.S);return tuple(float(m.group(i) or 0) for i in (1,2,3)) if m else (0,0,0)
def global_pads(b):
 x0,y0,a=pos(b);th=math.radians(a);ca=math.cos(th);sa=math.sin(th);out=[]
 for pb in blocks(b,'(pad '):
  mn=re.match(r'\(pad\s+"?([^"\s)]*)"?',pb);n=mn.group(1) if mn else '?';ma=re.search(r'\(at\s+([-\d.]+)\s+([-\d.]+)',pb);lx=float(ma.group(1)) if ma else 0;ly=float(ma.group(2)) if ma else 0;x=x0+lx*ca-ly*sa;y=y0+lx*sa+ly*ca;net=re.search(r'\(net\s+(\d+)\s+"([^"]+)"\)',pb);out.append((n,x,y,net.group(2) if net else '',int(net.group(1)) if net else 0))
 return out
def main():
 t=PCB.read_text(errors='replace');fps=list(blocks(t,'(footprint '));lines=['# KH910 Rev A — Layout Space Audit','']
 lines+=['## Footprints in candidate lower-center region (X 135..250, Y 148..163.5)','']
 for b in fps:
  x,y,a=pos(b)
  if 135<=x<=250 and 148<=y<=163.5: lines.append(f'- {ref(b)} `{val(b)}` at ({x:.3f},{y:.3f}) rot {a:g}')
 lines+=['','## ESP32 module footprint and pad 25','']
 for b in fps:
  if 'ESP32' in val(b).upper() or 'ESP32' in b[:1200].upper():
   lines.append(f'- {ref(b)} `{val(b)}` at {pos(b)}')
   for p in global_pads(b):
    if p[0] in ('25','8','5','6'):lines.append(f'  - pad {p[0]} global ({p[1]:.3f},{p[2]:.3f}) net `{p[3]}` #{p[4]}')
 lines+=['','## Copper segments crossing candidate region','']
 for sb in blocks(t,'(segment '):
  a=re.search(r'\(start\s+([-\d.]+)\s+([-\d.]+)\)',sb);b=re.search(r'\(end\s+([-\d.]+)\s+([-\d.]+)\)',sb)
  if not a or not b:continue
  x1,y1,x2,y2=map(float,(a.group(1),a.group(2),b.group(1),b.group(2)))
  if max(x1,x2)<135 or min(x1,x2)>250 or max(y1,y2)<148 or min(y1,y2)>163.5:continue
  net=re.search(r'\(net\s+(\d+)\)',sb);layer=re.search(r'\(layer\s+"([^"]+)"\)',sb);w=re.search(r'\(width\s+([-\d.]+)\)',sb)
  lines.append(f'- {layer.group(1) if layer else "?"} net {net.group(1) if net else "?"} w {w.group(1) if w else "?"}: ({x1:.3f},{y1:.3f})->({x2:.3f},{y2:.3f})')
 OUT.write_text('\n'.join(lines)+'\n');print(OUT)
if __name__=='__main__':main()
