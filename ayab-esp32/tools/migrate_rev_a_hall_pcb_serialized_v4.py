#!/usr/bin/env python3
"""Rev A Hall PCB migration v4.

v4 fixes the two root causes exposed by v3 DRC:
- divider pin numbering now exactly matches the validated schematic netlist;
- obsolete comparator copper is pruned by surviving-pad connectivity instead of
  deleting whole shared nets.

It also reuses most of the already DRC-clean legacy MCU Hall corridors. Only the
single B.Cu segment attached to each retained U701/J701 local branch is cut;
the downstream corridor is retagged as HALL_L_ADC/HALL_R_ADC. New In1 routes
therefore only need to reach those proven corridors rather than the dense MCU.
"""
from __future__ import annotations
import math
from pathlib import Path
from collections import defaultdict
import migrate_rev_a_hall_pcb_serialized_compat as compat

k=compat.migration
reference=compat.reference
value=compat.value
replace_property=compat.replace_property

RAW_L='/BROTHER-CONNECTORS/EOL_L'; RAW_R='/BROTHER-CONNECTORS/EOL_R'
OLD_LP='/ESP32/EOL_L_P'; OLD_LN='/ESP32/EOL_L_N'
ADC_L='/ESP32/HALL_L_ADC'; ADC_R='/ESP32/HALL_R_ADC'
GND='GND'; P5='+5V'
LK='/IO CONDITIONING/EOL_L_K'; LL='/IO CONDITIONING/EOL_L_L'
RN='/BROTHER-CONNECTORS/EOL_R_N'; RS='/BROTHER-CONNECTORS/EOL_R_S'
STRICT_REMOVE={'C703','C704','U702','U703',*(f'R{n}' for n in range(715,731))}
# Physical legacy resistor -> new schematic ref/pad nets. This mapping preserves
# one raw pad per side and makes the ADC junction a straight same-column/row link.
REPURPOSE={
 'R731':('R735',{'1':RAW_L,'2':ADC_L}),
 'R733':('R736',{'1':ADC_L,'2':GND}),
 'R732':('R737',{'1':RAW_R,'2':ADC_R}),
 'R734':('R738',{'1':ADC_R,'2':GND}),
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
LEFT_ADC_A=PAD[('R731','2')]; LEFT_ADC_B=PAD[('R733','1')]
RIGHT_ADC_A=PAD[('R732','2')]; RIGHT_ADC_B=PAD[('R734','1')]
LEFT_MID=((LEFT_ADC_A[0]+LEFT_ADC_B[0])/2,(LEFT_ADC_A[1]+LEFT_ADC_B[1])/2)
RIGHT_MID=((RIGHT_ADC_A[0]+RIGHT_ADC_B[0])/2,(RIGHT_ADC_A[1]+RIGHT_ADC_B[1])/2)
LEFT_GND_PAD=PAD[('R733','2')]; RIGHT_GND_PAD=PAD[('R734','2')]
LEFT_GND_T=(91.0628,140.6530); RIGHT_GND_VIA=(311.0,154.8)
LEFT_START=(94.0,136.5); RIGHT_START=(309.5,160.5)
# Downstream endpoints of the original B.Cu corridors after cutting them away
# from the retained J701 PTH pads.
LEFT_TARGET=(218.72,151.464898); RIGHT_TARGET=(213.88,156.304898)
LEFT_J701=(215.127498,155.0574); RIGHT_J701=(212.587498,157.5974)
LEFT_ROUTE=[LEFT_START,(100.0,136.5),(100.0,154.0),(112.0,162.0),(150.0,164.0),(185.0,164.0),(205.0,160.0),LEFT_TARGET]
RIGHT_ROUTE=[RIGHT_START,(300.0,164.0),(280.0,164.0),(260.0,164.0),(240.0,164.0),(225.0,161.0),RIGHT_TARGET]
ANON_COMPARATOR_TOKENS=('Net-(U702','Net-(U703','Net-(R719','Net-(R720','Net-(R721','Net-(R722')
PRUNE_NAMES={RAW_L,RAW_R,LK,LL,RN,RS,GND,P5}
POWER_NAMES={GND,P5}

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

def is_j701_bridge(name,b):
 if k.expr_head(b)!='segment' or k.item_layer(b)!='B.Cu':return False
 q=LEFT_J701 if name==OLD_LP else RIGHT_J701
 return any(k.near(p,q,0.002) for p in k.item_points(b))

def coord(p):return (round(p[0],4),round(p[1],4))

def footprint_anchors(text,nets_by_name):
 anchors=defaultdict(set)
 for s in k.root_children(text):
  if s.head!='footprint':continue
  fp=text[s.start:s.end]
  for pb in k.direct_pad_blocks(fp).values():
   pn=k.pad_net(pb)
   if not pn:continue
   anchors[pn[0]].add(coord(pxy(fp,pb)))
 return anchors

def prune_dead_leaves(text,names):
 """Trim routed leaves that no longer terminate on surviving pads.

 Coordinates are intentionally conservative: same-net crossings on different
 layers may keep extra copper, but cannot cause a valid branch to be deleted.
 Power vias are treated as anchors because they may legitimately terminate into
 copper zones/planes.
 """
 removed=defaultdict(int)
 for _round in range(40):
  ch=k.root_children(text); nets={}
  for s in ch:
   if s.head=='net':
    n=k.parse_net_definition(text[s.start:s.end])
    if n:nets[n[1]]=n[0]
  targets={nets[n]:n for n in names if n in nets}
  anchors=footprint_anchors(text,nets)
  items=[]; incidence=defaultdict(list); via_coords=defaultdict(set)
  for s in ch:
   if s.head not in {'segment','via','arc'}:continue
   b=text[s.start:s.end]; nid=k.item_net_id(b)
   if nid not in targets:continue
   pts=k.item_points(b)
   if not pts:continue
   ends=[coord(pts[0])] if s.head=='via' else [coord(pts[0]),coord(pts[-1])]
   idx=len(items);items.append((s,b,nid,ends))
   for q in ends:incidence[(nid,q)].append(idx)
   if s.head=='via':via_coords[nid].add(ends[0])
  doomed=set()
  for idx,(s,b,nid,ends) in enumerate(items):
   name=targets[nid]
   for q in ends:
    anchored=q in anchors.get(nid,set()) or (name in POWER_NAMES and q in via_coords.get(nid,set()))
    if not anchored and len(incidence[(nid,q)])==1:
     doomed.add(idx);break
  if not doomed:break
  edits=[]
  for idx in sorted(doomed):
   s,b,nid,ends=items[idx];edits.append((s.start,s.end,''));removed[targets[nid]]+=1
  for a,b,r in sorted(edits,key=lambda e:(e[0],e[1]),reverse=True):text=text[:a]+r+text[b:]
 else:raise RuntimeError('leaf pruning did not converge')
 return text,dict(removed)

def migrate(src:Path,dst:Path):
 text=src.read_text(encoding='utf-8'); ch,nets,fps=audit(text)
 adc={ADC_L:max(nets.values())+1,ADC_R:max(nets.values())+2}; idname={v:n for n,v in nets.items()}
 edits=[];lastnet=None;kept={OLD_LP:0,OLD_LN:0};retag={OLD_LP:0,OLD_LN:0};bridges={OLD_LP:0,OLD_LN:0};anon=0;changedc=0
 # Old copper at these pads must go because the physical pad changes net in v4.
 changed={(PAD[('R731','2')],nets[GND]),(PAD[('R733','1')],nets[P5]),(PAD[('R733','2')],nets[RAW_L]),
          (PAD[('R732','2')],nets[GND]),(PAD[('R734','1')],nets[P5]),(PAD[('R734','2')],nets[RAW_R])}
 for s in ch:
  b=text[s.start:s.end]
  if s.head=='net':lastnet=s.end;continue
  if s.head=='footprint':
   r=reference(b)
   if r in STRICT_REMOVE:edits.append((s.start,s.end,''));continue
   if r in REPURPOSE:
    nr,pmap=REPURPOSE[r];nb=replace_property(b,'Reference',nr);nb=replace_property(nb,'Value','10k')
    for pn,nn in pmap.items():nb=k.replace_pad_net_in_footprint(nb,pn,adc[nn] if nn in adc else nets[nn],nn)
    edits.append((s.start,s.end,nb));continue
   if r=='U201':
    nb=k.replace_pad_net_in_footprint(b,'5',adc[ADC_L],ADC_L);nb=k.replace_pad_net_in_footprint(nb,'6',adc[ADC_R],ADC_R);edits.append((s.start,s.end,nb));continue
  if s.head not in {'segment','via','arc'}:continue
  nid=k.item_net_id(b)
  if nid is None:continue
  old=OLD_LP if nid==nets[OLD_LP] else OLD_LN if nid==nets[OLD_LN] else None
  if old:
   if is_local_branch(old,b):kept[old]+=1;continue
   if is_j701_bridge(old,b):edits.append((s.start,s.end,''));bridges[old]+=1;continue
   edits.append((s.start,s.end,k.replace_item_net(b,adc[ADC_L if old==OLD_LP else ADC_R])));retag[old]+=1;continue
  nn=idname.get(nid,'')
  if any(tok in nn for tok in ANON_COMPARATOR_TOKENS):edits.append((s.start,s.end,''));anon+=1;continue
  if any(nid==oldnid and k.item_touches(b,pos) for pos,oldnid in changed):edits.append((s.start,s.end,''));changedc+=1;continue
 if kept!={OLD_LP:4,OLD_LN:2}:raise RuntimeError(f'local branches {kept}')
 if bridges!={OLD_LP:1,OLD_LN:1}:raise RuntimeError(f'J701 bridges {bridges}')
 if retag!={OLD_LP:7,OLD_LN:11}:raise RuntimeError(f'retagged corridor {retag}')
 if lastnet is None:raise RuntimeError('no net table')
 edits.append((lastnet,lastnet,f'\n\t(net {adc[ADC_L]} "{ADC_L}")\n\t(net {adc[ADC_R]} "{ADC_R}")'))
 rs=k.root_start(text);dep=0;ins=False;esc=False;rend=None
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
 # Divider junctions, ground restoration, and ADC taps.
 items.append(k.segment(LEFT_ADC_A,LEFT_ADC_B,'F.Cu',adc[ADC_L],'v4-left-divider'))
 items.append(k.segment(LEFT_MID,LEFT_START,'F.Cu',adc[ADC_L],'v4-left-tap'))
 items.append(k.segment(LEFT_GND_PAD,LEFT_GND_T,'F.Cu',nets[GND],'v4-left-gnd'))
 items.append(k.segment(RIGHT_ADC_A,RIGHT_ADC_B,'F.Cu',adc[ADC_R],'v4-right-divider'))
 items.append(k.segment(RIGHT_MID,RIGHT_START,'F.Cu',adc[ADC_R],'v4-right-tap'))
 items.append(k.segment(RIGHT_GND_PAD,(312.0,155.0),'F.Cu',nets[GND],'v4-right-gnd-a'))
 items.append(k.segment((312.0,155.0),RIGHT_GND_VIA,'F.Cu',nets[GND],'v4-right-gnd-b'))
 items.append(k.via(RIGHT_GND_VIA,nets[GND],'v4-right-gnd-via'))
 # ADC layer transitions and conservative lower-board routes.
 items.append(k.via(LEFT_START,adc[ADC_L],'v4-left-start'))
 items+=k.polyline(LEFT_ROUTE,'In1.Cu',adc[ADC_L],'v4-left-in1')
 items.append(k.via(LEFT_TARGET,adc[ADC_L],'v4-left-target'))
 items.append(k.via(RIGHT_START,adc[ADC_R],'v4-right-start'))
 items+=k.polyline(RIGHT_ROUTE,'In1.Cu',adc[ADC_R],'v4-right-in1')
 items.append(k.via(RIGHT_TARGET,adc[ADC_R],'v4-right-target'))
 edits.append((rend,rend,'\n\t'+'\n\t'.join(items)+'\n'))
 for a,b,r in sorted(edits,key=lambda e:(e[0],e[1]),reverse=True):text=text[:a]+r+text[b:]
 text,pruned=prune_dead_leaves(text,PRUNE_NAMES)
 validate(text);dst.write_text(text,encoding='utf-8')
 print('HALL_V4_MIGRATION_OK');print('ADC_NET_IDS',adc);print('KEPT_LOCAL',kept);print('CUT_J701_BRIDGES',bridges);print('RETAGGED_PROVEN_CORRIDOR',retag);print('REMOVED_ANON_COMPARATOR_COPPER',anon);print('REMOVED_CHANGED_PAD_COPPER',changedc);print('PRUNED_DEAD_LEAVES',pruned)

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
 exp={'R735':{'1':RAW_L,'2':ADC_L},'R736':{'1':ADC_L,'2':GND},'R737':{'1':RAW_R,'2':ADC_R},'R738':{'1':ADC_R,'2':GND}}
 for r,pmap in exp.items():
  if r not in fps or value(fps[r])!='10k':raise RuntimeError(f'bad {r}')
  ps=k.direct_pad_blocks(fps[r])
  for pn,nn in pmap.items():
   got=k.pad_net(ps[pn])
   if not got or got[1]!=nn:raise RuntimeError(f'{r}.{pn} {got} != {nn}')
 u=k.direct_pad_blocks(fps['U201'])
 if k.pad_net(u['5'])[1]!=ADC_L or k.pad_net(u['6'])[1]!=ADC_R:raise RuntimeError('U201 ADC mismatch')
 for s in ch:
  if s.head not in {'segment','via','arc'}:continue
  nid=k.item_net_id(text[s.start:s.end])
  if nid==nets.get(OLD_LP):oldc[OLD_LP]+=1
  elif nid==nets.get(OLD_LN):oldc[OLD_LN]+=1
 if oldc!={OLD_LP:4,OLD_LN:2}:raise RuntimeError(f'old local count {oldc}')
 if cc.get(nets[ADC_L],0)<15:raise RuntimeError(f'ADC_L copper too small {cc.get(nets[ADC_L],0)}')
 if cc.get(nets[ADC_R],0)<18:raise RuntimeError(f'ADC_R copper too small {cc.get(nets[ADC_R],0)}')

def main():
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument('input',type=Path);ap.add_argument('output',type=Path,nargs='?');ap.add_argument('--validate',action='store_true');a=ap.parse_args()
 if a.validate:validate(a.input.read_text(encoding='utf-8'));print('HALL_V4_VALIDATION_OK',a.input)
 else:
  if a.output is None:ap.error('output required')
  migrate(a.input,a.output)
if __name__=='__main__':main()
