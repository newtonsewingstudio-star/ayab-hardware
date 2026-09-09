#!/usr/bin/env python3
from __future__ import annotations
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PCB=ROOT/'ayab-esp32.kicad_pcb'
OUT=ROOT/'KH910_REV_A_HALL_LOCAL_COPPER.md'
BOXES={
 'LEFT':(83.0,96.0,128.0,146.5),
 'RIGHT':(308.0,329.0,151.0,163.0),
 'U701':(176.0,194.0,153.0,163.0),
 'MCU_ROUTE':(195.0,222.0,126.0,142.0),
}
TARGET_NAMES={'GND','+5V','/BROTHER-CONNECTORS/EOL_L','/BROTHER-CONNECTORS/EOL_R',
 '/IO CONDITIONING/EOL_L_K','/IO CONDITIONING/EOL_L_L',
 '/BROTHER-CONNECTORS/EOL_R_N','/BROTHER-CONNECTORS/EOL_R_S',
 '/ESP32/EOL_L_P','/ESP32/EOL_L_N'}

def balanced(t,s):
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
 raise RuntimeError('unterminated')

def blocks(t,token):
 p=0
 while 1:
  p=t.find(token,p)
  if p<0:return
  b,e=balanced(t,p);yield b;p=e

def point(b,kind):
 m=re.search(rf'\({kind}\s+([-+0-9.eE]+)\s+([-+0-9.eE]+)',b)
 return (float(m.group(1)),float(m.group(2))) if m else None

def points(b):
 return [p for p in (point(b,'start'),point(b,'mid'),point(b,'end'),point(b,'at')) if p]

def intersects(pts,box):
 x0,x1,y0,y1=box
 return any(x0<=x<=x1 and y0<=y<=y1 for x,y in pts)

def main():
 t=PCB.read_text(errors='replace')
 nets={}
 for b in blocks(t,'(net '):
  m=re.fullmatch(r'\(net\s+(\d+)\s+"([^"]*)"\)',b.strip(),re.S)
  if m:nets[int(m.group(1))]=m.group(2)
 rows=[]
 for kind,token in [('segment','(segment '),('via','(via '),('arc','(arc ')]:
  for b in blocks(t,token):
   nm=re.search(r'\(net\s+(\d+)\)',b)
   if not nm:continue
   nid=int(nm.group(1));name=nets.get(nid,'')
   pts=points(b)
   hit=[k for k,box in BOXES.items() if intersects(pts,box)]
   if not hit:continue
   if name not in TARGET_NAMES and not any(x in name for x in ('U702','U703','R719','R720','R721','R722')):continue
   layer=re.search(r'\(layer\s+"([^"]+)"\)',b)
   uid=re.search(r'\(uuid\s+"?([^"\s)]+)',b)
   rows.append((hit,nid,name,kind,layer.group(1) if layer else 'F.Cu-B.Cu',pts,uid.group(1) if uid else ''))
 lines=['# KH910 Rev A — Hall Local Copper Audit','',
        'Baseline board is DRC-clean. This report enumerates Hall-adjacent copper so v4 can prune/reconnect exact branches rather than broad nets.','']
 for boxname in BOXES:
  lines += [f'## {boxname}', '']
  subset=[r for r in rows if boxname in r[0]]
  lines.append(f'Items: **{len(subset)}**')
  lines.append('')
  for hit,nid,name,kind,layer,pts,uid in subset:
   lines.append(f'- `{name}` #{nid} — {kind} `{layer}` — points `{pts}` — uuid `{uid}`')
  lines.append('')
 OUT.write_text('\n'.join(lines)+'\n')
 print(OUT)

if __name__=='__main__':main()
