#!/usr/bin/env python3
"""Rev A Hall PCB migration v3.

Changes from v2:
- preserve/retag the proven DRC-clean MCU endpoint stubs and their existing vias;
- preserve the original raw-Hall and ground pad connections wherever possible by
  swapping which physical legacy resistor becomes the upper/lower divider part;
- remove only the middle legacy EOL_L_P/N corridors, keeping U701<->J701 local branches;
- remove copper on comparator-only nets, but do not broadly cut shared +5V/GND trunks;
- route new Hall ADC signals on In1.Cu to the existing MCU vias.
"""
from __future__ import annotations
import math
from pathlib import Path
import migrate_rev_a_hall_pcb_serialized_compat as compat

k=compat.migration
reference=compat.reference
value=compat.value
replace_property=compat.replace_property

RAW_L='/BROTHER-CONNECTORS/EOL_L'; RAW_R='/BROTHER-CONNECTORS/EOL_R'
OLD_LP='/ESP32/EOL_L_P'; OLD_LN='/ESP32/EOL_L_N'
ADC_L='/ESP32/HALL_L_ADC'; ADC_R='/ESP32/HALL_R_ADC'
GND='GND'; P5='+5V'
STRICT_REMOVE={'C703','C704','U702','U703',*(f'R{n}' for n in range(715,731))}
# Choose physical footprints to minimize changes to existing RAW/GND copper.
REPURPOSE={
 'R733':('R735',{'1':ADC_L,'2':RAW_L}),
 'R731':('R736',{'1':ADC_L,'2':GND}),
 'R734':('R737',{'1':ADC_R,'2':RAW_R}),
 'R732':('R738',{'1':ADC_R,'2':GND}),
}
AUDITED_NET_IDS={GND:2,OLD_LP:26,OLD_LN:27,RAW_L:63,RAW_R:64}
PAD={
 ('R731','1'):(90.1378,139.1030),('R731','2'):(91.7878,139.1030),
 ('R733','1'):(91.7878,140.6530),('R733','2'):(90.1378,140.6530),
 ('R732','1'):(314.6700,156.4250),('R732','2'):(314.6700,158.0750),
 ('R734','1'):(313.1200,158.0750),('R734','2'):(313.1200,156.4250),
 ('U201','5'):(217.1250,127.1250),('U201','6'):(217.1250,127.9750),
 ('U701','17'):(197.2025,158.5050),('U701','18'):(197.2025,157.8550),
}
LEFT_ADC_A=PAD[('R733','1')]; LEFT_ADC_B=PAD[('R731','1')]
RIGHT_ADC_A=PAD[('R734','1')]; RIGHT_ADC_B=PAD[('R732','1')]
LEFT_MID=((LEFT_ADC_A[0]+LEFT_ADC_B[0])/2,(LEFT_ADC_A[1]+LEFT_ADC_B[1])/2)
RIGHT_MID=((RIGHT_ADC_A[0]+RIGHT_ADC_B[0])/2,(RIGHT_ADC_A[1]+RIGHT_ADC_B[1])/2)
LEFT_START=(95.5,139.878); RIGHT_START=(309.5,160.5)
LEFT_MCU_VIA=(219.55,134.13); RIGHT_MCU_VIA=(218.8,134.13)
LEFT_ROUTE=[LEFT_START,(104.0,146.0),(130.0,146.0),(165.0,144.0),(195.0,140.0),LEFT_MCU_VIA]
RIGHT_ROUTE=[RIGHT_START,(300.0,164.0),(282.0,164.0),(260.0,159.0),(240.0,151.0),(225.0,141.0),RIGHT_MCU_VIA]
COMPARATOR_ONLY_TOKENS=(
 'Net-(U702','Net-(U703','Net-(R719','Net-(R720','Net-(R721','Net-(R722',
 '/IO CONDITIONING/EOL_L_K','/IO CONDITIONING/EOL_L_L',
 '/BROTHER-CONNECTORS/EOL_R_N','/BROTHER-CONNECTORS/EOL_R_S',
)

def pxy(fp,pb):
 fx,fy,deg=k.footprint_at(fp); px,py=k.pad_local_at(pb); r=math.radians(deg)
 return (round(fx+px*math.cos(r)+py*math.sin(r),6),round(fy-px*math.sin(r)+py*math.cos(r),6))

def audit(text):
 ch=k.root_children(text); nets={}; fps={}
 for s in ch:
  b=text[s.start:s.end]
  if s.head=='net':
   n=k.parse_net_definition(b)
   if n:nets[n[1]]=n[0]
  elif s.head=='footprint':
   r=reference(b)
   if r:fps[r]=b
 for n,i in AUDITED_NET_IDS.items():
  if nets.get(n)!=i:raise RuntimeError(f'net audit {n}: {nets.get(n)} != {i}')
 if ADC_L in nets or ADC_R in nets:raise RuntimeError('ADC nets already present')
 req=STRICT_REMOVE|set(REPURPOSE)|{'U201','U701'}
 if req-set(fps):raise RuntimeError(f'missing refs {sorted(req-set(fps))}')
 exp={
  ('R731','1'):RAW_L,('R731','2'):GND,('R733','1'):P5,('R733','2'):RAW_L,
  ('R732','1'):RAW_R,('R732','2'):GND,('R734','1'):P5,('R734','2'):RAW_R,
  ('U201','5'):OLD_LP,('U201','6'):OLD_LN,('U701','17'):OLD_LN,('U701','18'):OLD_LP,
 }
 for (r,p),nn in exp.items():
  pb=k.direct_pad_blocks(fps[r])[p]; got=k.pad_net(pb)
  if not got or got[1]!=nn:raise RuntimeError(f'{r}.{p} net {got} expected {nn}')
  if not k.near(pxy(fps[r],pb),PAD[(r,p)],0.003):raise RuntimeError(f'{r}.{p} xy mismatch')
 return ch,nets,fps

def is_local_branch(name,b):
 return k.expr_head(b)=='segment' and k.item_layer(b)=='F.Cu' and max(y for _x,y in k.item_points(b))>150

def is_mcu_stub(name,b):
 pts=k.item_points(b)
 if name==OLD_LP:
  via=LEFT_MCU_VIA
 else: via=RIGHT_MCU_VIA
 if k.expr_head(b)=='via':return any(k.near(p,via,0.002) for p in pts)
 # Proven baseline F.Cu stub lies entirely at/above y=134.13 near x>=217.
 return k.item_layer(b)=='F.Cu' and pts and all(p[1]<=134.131 for p in pts) and max(p[0] for p in pts)>=217.0

def migrate(src:Path,dst:Path):
 text=src.read_text(encoding='utf-8'); ch,nets,fps=audit(text)
 adc={ADC_L:max(nets.values())+1,ADC_R:max(nets.values())+2}; idname={v:n for n,v in nets.items()}
 edits=[]; lastnet=None; kept={OLD_LP:0,OLD_LN:0}; stubs={OLD_LP:0,OLD_LN:0}; deleted={OLD_LP:0,OLD_LN:0}; compc=0; changedc=0
 # Only these four old pad roles change; GND and retained RAW pads are untouched.
 changed={(PAD[('R733','1')],nets[P5]),(PAD[('R731','1')],nets[RAW_L]),(PAD[('R734','1')],nets[P5]),(PAD[('R732','1')],nets[RAW_R])}
 for s in ch:
  b=text[s.start:s.end]
  if s.head=='net':lastnet=s.end;continue
  if s.head=='footprint':
   r=reference(b)
   if r in STRICT_REMOVE:edits.append((s.start,s.end,''));continue
   if r in REPURPOSE:
    nr,pmap=REPURPOSE[r]; nb=replace_property(b,'Reference',nr); nb=replace_property(nb,'Value','10k')
    for pn,nn in pmap.items():nb=k.replace_pad_net_in_footprint(nb,pn,adc[nn] if nn in adc else nets[nn],nn)
    edits.append((s.start,s.end,nb));continue
   if r=='U201':
    nb=k.replace_pad_net_in_footprint(b,'5',adc[ADC_L],ADC_L); nb=k.replace_pad_net_in_footprint(nb,'6',adc[ADC_R],ADC_R); edits.append((s.start,s.end,nb));continue
  if s.head not in {'segment','via','arc'}:continue
  nid=k.item_net_id(b)
  if nid is None:continue
  old=OLD_LP if nid==nets[OLD_LP] else OLD_LN if nid==nets[OLD_LN] else None
  if old:
   if is_local_branch(old,b):kept[old]+=1;continue
   if is_mcu_stub(old,b):
    edits.append((s.start,s.end,k.replace_item_net(b,adc[ADC_L if old==OLD_LP else ADC_R])));stubs[old]+=1;continue
   edits.append((s.start,s.end,''));deleted[old]+=1;continue
  nn=idname.get(nid,'')
  if any(tok in nn for tok in COMPARATOR_ONLY_TOKENS):edits.append((s.start,s.end,''));compc+=1;continue
  if any(nid==oldnid and k.item_touches(b,pos) for pos,oldnid in changed):edits.append((s.start,s.end,''));changedc+=1;continue
 if kept!={OLD_LP:4,OLD_LN:2}:raise RuntimeError(f'local branch {kept}')
 if stubs!={OLD_LP:4,OLD_LN:4}:raise RuntimeError(f'MCU stubs {stubs}')
 if deleted!={OLD_LP:4,OLD_LN:8}:raise RuntimeError(f'deleted middle {deleted}')
 if lastnet is None:raise RuntimeError('no net table')
 edits.append((lastnet,lastnet,f'\n\t(net {adc[ADC_L]} "{ADC_L}")\n\t(net {adc[ADC_R]} "{ADC_R}")'))
 # root closing paren
 rs=k.root_start(text); dep=0; ins=False; esc=False; rend=None
 for i in range(rs,len(text)):
  c=text[i]
  if ins:
   if esc:esc=False
   elif c=='\\':esc=True
   elif c=='"':ins=False
   continue
  if c=='"':ins=True
  elif c=='(':dep+=1
  elif c==')':
   dep-=1
   if dep==0:rend=i;break
 if rend is None:raise RuntimeError('root end')
 items=[]
 items.append(k.segment(LEFT_ADC_A,LEFT_ADC_B,'F.Cu',adc[ADC_L],'v3-left-divider'))
 items.append(k.segment(LEFT_MID,LEFT_START,'F.Cu',adc[ADC_L],'v3-left-tap'))
 items.append(k.via(LEFT_START,adc[ADC_L],'v3-left-start'))
 items+=k.polyline(LEFT_ROUTE,'In1.Cu',adc[ADC_L],'v3-left-in1')
 items.append(k.segment(RIGHT_ADC_A,RIGHT_ADC_B,'F.Cu',adc[ADC_R],'v3-right-divider'))
 items.append(k.segment(RIGHT_MID,RIGHT_START,'F.Cu',adc[ADC_R],'v3-right-tap'))
 items.append(k.via(RIGHT_START,adc[ADC_R],'v3-right-start'))
 items+=k.polyline(RIGHT_ROUTE,'In1.Cu',adc[ADC_R],'v3-right-in1')
 edits.append((rend,rend,'\n\t'+'\n\t'.join(items)+'\n'))
 for a,b,r in sorted(edits,key=lambda e:(e[0],e[1]),reverse=True):text=text[:a]+r+text[b:]
 validate(text);dst.write_text(text,encoding='utf-8')
 print('HALL_V3_MIGRATION_OK');print('ADC_NET_IDS',adc);print('KEPT_LOCAL',kept);print('RETAGGED_MCU_STUBS',stubs);print('DELETED_MIDDLE',deleted);print('REMOVED_COMPARATOR_COPPER',compc);print('REMOVED_CHANGED_PAD_COPPER',changedc)

def validate(text):
 ch=k.root_children(text);nets={};fps={};cc={};oldc={OLD_LP:0,OLD_LN:0}
 for s in ch:
  b=text[s.start:s.end]
  if s.head=='net':
   n=k.parse_net_definition(b)
   if n:nets[n[1]]=n[0]
  elif s.head=='footprint':
   r=reference(b)
   if r:fps[r]=b
  elif s.head in {'segment','via','arc'}:
   nid=k.item_net_id(b)
   if nid is not None:cc[nid]=cc.get(nid,0)+1
 for n in (ADC_L,ADC_R):
  if n not in nets:raise RuntimeError(f'missing {n}')
 if STRICT_REMOVE&set(fps):raise RuntimeError(f'obsolete refs {STRICT_REMOVE&set(fps)}')
 exp={'R735':{'1':ADC_L,'2':RAW_L},'R736':{'1':ADC_L,'2':GND},'R737':{'1':ADC_R,'2':RAW_R},'R738':{'1':ADC_R,'2':GND}}
 for r,pmap in exp.items():
  if r not in fps or value(fps[r])!='10k':raise RuntimeError(f'bad {r}')
  ps=k.direct_pad_blocks(fps[r])
  for pn,nn in pmap.items():
   got=k.pad_net(ps[pn]);
   if not got or got[1]!=nn:raise RuntimeError(f'{r}.{pn} {got} != {nn}')
 u=k.direct_pad_blocks(fps['U201'])
 if k.pad_net(u['5'])[1]!=ADC_L or k.pad_net(u['6'])[1]!=ADC_R:raise RuntimeError('U201 ADC mismatch')
 for s in ch:
  if s.head not in {'segment','via','arc'}:continue
  nid=k.item_net_id(text[s.start:s.end])
  if nid==nets.get(OLD_LP):oldc[OLD_LP]+=1
  elif nid==nets.get(OLD_LN):oldc[OLD_LN]+=1
 if oldc!={OLD_LP:4,OLD_LN:2}:raise RuntimeError(f'old local count {oldc}')
 # 4 reused MCU copper items + divider + tap + start via + In1 route segments.
 if cc.get(nets[ADC_L],0)!=12:raise RuntimeError(f'ADC_L copper {cc.get(nets[ADC_L],0)}')
 if cc.get(nets[ADC_R],0)!=13:raise RuntimeError(f'ADC_R copper {cc.get(nets[ADC_R],0)}')

def main():
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument('input',type=Path);ap.add_argument('output',type=Path,nargs='?');ap.add_argument('--validate',action='store_true');a=ap.parse_args()
 if a.validate:validate(a.input.read_text(encoding='utf-8'));print('HALL_V3_VALIDATION_OK',a.input)
 else:
  if a.output is None:ap.error('output required')
  migrate(a.input,a.output)
if __name__=='__main__':main()
