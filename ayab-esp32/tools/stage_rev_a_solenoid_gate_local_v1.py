#!/usr/bin/env python3
"""Stage the Rev A solenoid high-side fail-safe gate on the clean partition PCB.

This first gate stage deliberately uses KiCad to resolve the actual pad centres
after footprint placement. It does not reuse the incorrect historical manual
footprint-rotation transform.

Scope v1:
- place Q805/Q806/R820/R821/R822 below J401;
- establish RAW, switched, P-gate, N-gate and local ground copper;
- leave only the long GPIO21 -> R821 enable route for the next A* stage.

The workflow runs KiCad DRC and treats its report as authoritative.
"""
from pathlib import Path
import sys
import re
sys.path.insert(0,str(Path(__file__).resolve().parent))
import patch_rev_a_solenoid_pcb as u
import pcbnew

PATH=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[1]/"ayab-esp32.kicad_pcb"
SCH=Path(__file__).resolve().parents[1]/"solenoids.kicad_sch"
pcb=PATH.read_text(encoding="utf-8")
sch=SCH.read_text(encoding="utf-8")

for ref in ("Q805","Q806","R820","R821","R822"):
    if f'fp_text reference "{ref}"' in pcb or f'property "Reference" "{ref}"' in pcb:
        raise RuntimeError(f"refusing partial gate state: {ref} already on PCB")

defs=u.net_defs(pcb)
raw_net=next((n for n,s in defs.items() if s=="+12V"),0)
sw_net=next((n for n,s in defs.items() if s=="SOLENOID_12V_SW"),0)
en_net=next((n for n,s in defs.items() if s=="/ESP32/ESP21"),0)
gnd_net=next((n for n,s in defs.items() if s=="GND"),0)
if raw_net<=0 or sw_net<=0 or en_net<=0 or gnd_net<=0:
    raise RuntimeError(f"expected RAW/SW/ESP21/GND nets missing: raw={raw_net} sw={sw_net} en={en_net} gnd={gnd_net}")
maxnet=max(defs)
pg_net,ng_net=maxnet+1,maxnet+2
pg_name="Net-(Q805-G)"
ng_name="Net-(Q806-G)"
en_name="SOLENOID_PWR_EN"

pcb=pcb.replace('/ESP32/ESP21',en_name)
pcb=u.insert_before_first(pcb,'  (footprint ',f'  (net {pg_net} "{pg_name}")\n  (net {ng_net} "{ng_name}")')

_,_,q502=u.find_fp(pcb,"Q502")
_,_,q201=u.find_fp(pcb,"Q201")
_,_,r809=u.find_fp(pcb,"R809")
prefix=u.sheet_prefix_from_existing(pcb)
su={r:u.symbol_uuid_by_ref(sch,r) for r in ("Q805","Q806","R820","R821","R822")}
path=lambda r:prefix+'/'+su[r]

def clone9(template,new_ref,value,x,y,angle,new_path,lcsc,padmap):
    out=re.sub(r'\((uuid|tstamp) [0-9a-f-]+\)',lambda m:f'({m.group(1)} {u.uid()})',template)
    out,n=re.subn(r'^(\(footprint.*?)(\(at\s+[-\d.]+\s+[-\d.]+(?:\s+[-\d.]+)?\))',lambda m:m.group(1)+f'(at {x:g} {y:g} {angle:g})',out,count=1,flags=re.S)
    if n!=1: raise RuntimeError(f"could not relocate cloned footprint {new_ref}")
    out,npath=re.subn(r'\(path "[^"]+"\)',f'(path "{new_path}")',out,count=1)
    if npath!=1: raise RuntimeError(f"path anchor missing in {new_ref}")
    if re.search(r'\(fp_text reference "[^"]+"',out): out=re.sub(r'\(fp_text reference "[^"]+"',f'(fp_text reference "{new_ref}"',out,count=1)
    else:
        out,nref=re.subn(r'\(property "Reference" "[^"]+"',f'(property "Reference" "{new_ref}"',out,count=1)
        if nref!=1: raise RuntimeError(f"reference field missing in {new_ref}")
    if re.search(r'\(fp_text value "[^"]+"',out): out=re.sub(r'\(fp_text value "[^"]+"',f'(fp_text value "{value}"',out,count=1)
    else:
        out,nval=re.subn(r'\(property "Value" "[^"]+"',f'(property "Value" "{value}"',out,count=1)
        if nval!=1: raise RuntimeError(f"value field missing in {new_ref}")
    if '(property "LCSC ID"' in out: out=re.sub(r'\(property "LCSC ID" "[^"]*"\)',f'(property "LCSC ID" "{lcsc}")',out,count=1)
    else:
        anchor=re.search(r'\n\s*\(path "[^"]+"\)',out)
        if not anchor: raise RuntimeError(f"LCSC insertion anchor missing in {new_ref}")
        out=out[:anchor.start()]+f'\n  (property "LCSC ID" "{lcsc}")'+out[anchor.start():]
    for pn,(ni,nn) in padmap.items(): out=u.replace_pad_net(out,pn,ni,nn)
    return out

newfps=[
    clone9(q502,"Q805","LP9435LT1G",117.0,160.25,0,path("Q805"),"C383257",{"1":(pg_net,pg_name),"2":(raw_net,"+12V"),"3":(sw_net,"SOLENOID_12V_SW")}),
    clone9(q201,"Q806","AO3400A",121.0,160.25,0,path("Q806"),"C20917",{"1":(ng_net,ng_name),"2":(gnd_net,"GND"),"3":(pg_net,pg_name)}),
    clone9(r809,"R820","100k",113.0,161.9,0,path("R820"),"C25803",{"1":(raw_net,"+12V"),"2":(pg_net,pg_name)}),
    clone9(r809,"R821","10k",125.0,159.2,0,path("R821"),"C25804",{"1":(en_net,en_name),"2":(ng_net,ng_name)}),
    clone9(r809,"R822","100k",128.0,161.5,0,path("R822"),"C25803",{"1":(gnd_net,"GND"),"2":(ng_net,ng_name)}),
]
pcb=u.insert_before_first(pcb,'  (segment ','\n'.join(newfps))
PATH.write_text(pcb,encoding="utf-8")

b=pcbnew.LoadBoard(str(PATH))
if b is None: raise RuntimeError("KiCad could not reload staged gate board")
b.BuildConnectivity()
fps={f.GetReference():f for f in b.GetFootprints()}
MM=pcbnew.ToMM

def pad(ref,pn):
    f=fps.get(ref)
    if f is None: raise RuntimeError(f"missing staged footprint {ref}")
    p=next((q for q in f.Pads() if q.GetNumber()==str(pn)),None)
    if p is None: raise RuntimeError(f"missing pad {ref}.{pn}")
    q=p.GetPosition(); return p,(MM(q.x),MM(q.y))
def net(ref,pn): return pad(ref,pn)[0].GetNetname()
def addseg(a,z,netcode,width=0.25,layer=pcbnew.F_Cu):
    t=pcbnew.PCB_TRACK(b); t.SetStart(pcbnew.VECTOR2I_MM(*a)); t.SetEnd(pcbnew.VECTOR2I_MM(*z)); t.SetWidth(pcbnew.FromMM(width)); t.SetLayer(layer); t.SetNetCode(netcode); b.Add(t)
def addvia(xy,netcode,size=0.6,drill=0.3):
    v=pcbnew.PCB_VIA(b); v.SetPosition(pcbnew.VECTOR2I_MM(*xy)); v.SetWidth(pcbnew.FromMM(size)); v.SetDrill(pcbnew.FromMM(drill)); v.SetLayerPair(pcbnew.F_Cu,pcbnew.B_Cu); v.SetNetCode(netcode); b.Add(v)

expect={("Q805","1"):pg_name,("Q805","2"):"+12V",("Q805","3"):"SOLENOID_12V_SW",("Q806","1"):ng_name,("Q806","2"):"GND",("Q806","3"):pg_name,("R820","1"):"+12V",("R820","2"):pg_name,("R821","1"):en_name,("R821","2"):ng_name,("R822","1"):"GND",("R822","2"):ng_name}
for k,v in expect.items():
    if net(*k)!=v: raise RuntimeError(f"net mismatch {k}: {net(*k)!r} != {v!r}")
pins={"Q805":("1","2","3"),"Q806":("1","2","3"),"R820":("1","2"),"R821":("1","2"),"R822":("1","2")}
pos={f"{r}.{p}":pad(r,p)[1] for r in pins for p in pins[r]}
for k in sorted(pos): print("GATE_PAD",k,*(round(x,4) for x in pos[k]),net(*k.split('.')))

# High-current switched path stays just below J401.
j401p9=pad("J401","9")[1]; q805d=pos["Q805.3"]
addseg(q805d,(q805d[0],158.0),sw_net,1.0)
addseg((q805d[0],158.0),(j401p9[0],158.0),sw_net,1.0)
addseg((j401p9[0],158.0),j401p9,sw_net,1.0)

# Q805 source to raw B.Cu backbone; R820 raw leg doglegs below the gate traces.
q805s=pos["Q805.2"]; rawvia=(q805s[0],162.35)
addseg(q805s,rawvia,raw_net,0.9); addvia(rawvia,raw_net,1.0,0.5)
addseg(rawvia,(rawvia[0],163.10),raw_net,1.0,pcbnew.B_Cu)
rraw=pos["R820.1"]; raw_y=162.65
addseg(rraw,(rraw[0],raw_y),raw_net,0.35)
addseg((rraw[0],raw_y),(q805s[0],raw_y),raw_net,0.35)
addseg((q805s[0],raw_y),q805s,raw_net,0.35)

# P-gate is moved to In2.  This avoids the existing GND via at
# (114.59,159.99), the 1 mm switched-power F.Cu route, and the N-gate In1 route.
qg=pos["Q805.1"]; q6d=pos["Q806.3"]; rpg=pos["R820.2"]
pg0=(113.35,160.90); pg1=(115.35,158.55); pg2=(122.65,160.90)
addseg(rpg,pg0,pg_net,0.25); addvia(pg0,pg_net)
addseg(qg,pg1,pg_net,0.25); addvia(pg1,pg_net)
addseg(q6d,pg2,pg_net,0.25); addvia(pg2,pg_net)
addseg(pg0,pg1,pg_net,0.25,pcbnew.In2_Cu)
addseg(pg1,pg2,pg_net,0.25,pcbnew.In2_Cu)

# N-gate stays on In1 so it cannot cross the P-gate or enable pad on F.Cu.
ng0=(119.15,158.45); ng1=(126.55,158.25); ng2=(129.65,160.75)
addseg(pos["Q806.1"],ng0,ng_net,0.25); addvia(ng0,ng_net)
addseg(pos["R821.2"],ng1,ng_net,0.25); addvia(ng1,ng_net)
addseg(pos["R822.2"],ng2,ng_net,0.25); addvia(ng2,ng_net)
addseg(ng0,ng1,ng_net,0.25,pcbnew.In1_Cu)
addseg(ng1,ng2,ng_net,0.25,pcbnew.In1_Cu)

# Let the existing GND zones connect Q806.2 and R822.1 after refill.  A local
# through-via here sits too close to the raw B.Cu +12V backbone at y=163.10.

pcbnew.SaveBoard(str(PATH),b)
print("SOL_GATE_LOCAL_STAGE_OK",PATH)
print("SOL_GATE_ENABLE_ENDPOINT",*(round(x,4) for x in pos["R821.1"]))
