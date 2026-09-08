#!/usr/bin/env python3
from __future__ import annotations
import math,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; PCB=ROOT/'ayab-esp32.kicad_pcb'; OUT=ROOT/'KH910_REV_A_FAILSAFE_LAYOUT_AUDIT.md'
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
 while True:
  p=t.find(token,p)
  if p<0:return
  b,e=block(t,p);yield b;p=e
def prop(b,k):
 m=re.search(r'\(property "'+re.escape(k)+r'" "([^"]+)"',b);return m.group(1) if m else ''
def ref(b):
 m=re.search(r'\(fp_text reference "([^"]+)"',b);return prop(b,'Reference') or (m.group(1) if m else '')
def val(b):
 m=re.search(r'\(fp_text value "([^"]+)"',b);return prop(b,'Value') or (m.group(1) if m else '')
def pos(b):
 m=re.search(r'^\(footprint.*?\(at\s+([-\d.]+)\s+([-\d.]+)(?:\s+([-\d.]+))?\)',b,re.S);return tuple(float(m.group(i) or 0) for i in (1,2,3)) if m else (0,0,0)
def pads(b):
 x0,y0,a=pos(b);th=math.radians(a);ca=math.cos(th);sa=math.sin(th);out=[]
 for pb in blocks(b,'(pad '):
  mn=re.match(r'\(pad\s+"?([^"\s)]*)"?',pb);n=mn.group(1) if mn else '?';ma=re.search(r'\(at\s+([-\d.]+)\s+([-\d.]+)',pb);lx=float(ma.group(1)) if ma else 0;ly=float(ma.group(2)) if ma else 0;x=x0+lx*ca-ly*sa;y=y0+lx*sa+ly*ca;net=re.search(r'\(net\s+(\d+)\s+"([^"]+)"\)',pb);out.append((n,x,y,int(net.group(1)) if net else 0,net.group(2) if net else ''))
 return out
def segdata(sb):
 a=re.search(r'\(start\s+([-\d.]+)\s+([-\d.]+)\)',sb);b=re.search(r'\(end\s+([-\d.]+)\s+([-\d.]+)\)',sb)
 if not a or not b:return None
 vals=tuple(map(float,(a.group(1),a.group(2),b.group(1),b.group(2))));net=re.search(r'\(net\s+(\d+)\)',sb);layer=re.search(r'\(layer\s+"([^"]+)"\)',sb);w=re.search(r'\(width\s+([-\d.]+)\)',sb)
 return vals+(int(net.group(1)) if net else 0,layer.group(1) if layer else '?',float(w.group(1)) if w else 0)
def main():
 t=PCB.read_text(errors='replace');fps=list(blocks(t,'(footprint '));lines=['# KH910 Rev A — Fail-Safe Layout Corridor Audit','']
 lines+=['## Right-side placement region (X 260..320, Y 145..162)','']
 for b in fps:
  x,y,a=pos(b)
  if 260<=x<=320 and 145<=y<=162:lines.append(f'- {ref(b)} `{val(b)}` at ({x:.3f},{y:.3f}) rot {a:g}')
 lines+=['','## Pads currently on GPIO21 PCB net 148','']
 for b in fps:
  for n,x,y,ni,nn in pads(b):
   if ni==148:lines.append(f'- {ref(b)} pad {n} at ({x:.3f},{y:.3f}) `{nn}`')
 lines+=['','## Solenoid-sheet +12V pads expected to become switched','']
 for b in fps:
  if ref(b) in {'J401','J403','J406','U302','U303','U304','C302','C303','C304'}:
   for n,x,y,ni,nn in pads(b):
    if ni==4:lines.append(f'- {ref(b)} pad {n} at ({x:.3f},{y:.3f})')
 lines+=['','## Copper in proposed switched-bus corridor (X 90..320, Y 158.5..162.2)','']
 for sb in blocks(t,'(segment '):
  d=segdata(sb)
  if not d:continue
  x1,y1,x2,y2,ni,ly,w=d
  if max(x1,x2)<90 or min(x1,x2)>320 or max(y1,y2)<158.5 or min(y1,y2)>162.2:continue
  lines.append(f'- {ly} net {ni} w {w:.3f}: ({x1:.3f},{y1:.3f})->({x2:.3f},{y2:.3f})')
 lines+=['','## Raw +12V copper in right-side switch region (X 285..320, Y 145..162)','']
 for sb in blocks(t,'(segment '):
  d=segdata(sb)
  if not d:continue
  x1,y1,x2,y2,ni,ly,w=d
  if ni!=4 or max(x1,x2)<285 or min(x1,x2)>320 or max(y1,y2)<145 or min(y1,y2)>162:continue
  lines.append(f'- {ly} w {w:.3f}: ({x1:.3f},{y1:.3f})->({x2:.3f},{y2:.3f})')
 OUT.write_text('\n'.join(lines)+'\n');print(OUT)
if __name__=='__main__':main()
