#!/usr/bin/env python3
"""Audit compact Q805/Q806 placement pockets on the promoted partition board.

Movable graphics-only G*** footprints are intentionally excluded from the
hard-blocker set. Connector/component footprints and the board edge remain hard
blockers. This is only a shortlist generator; staged KiCad DRC is authoritative.
"""
from pathlib import Path
import sys
import pcbnew

P=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[1]/"ayab-esp32.kicad_pcb"
b=pcbnew.LoadBoard(str(P))
MM=pcbnew.ToMM

def bb(fp):
    q=fp.GetBoundingBox()
    return (MM(q.GetX()),MM(q.GetY()),MM(q.GetX()+q.GetWidth()),MM(q.GetY()+q.GetHeight()))
def wh(fp):
    q=bb(fp); return (q[2]-q[0],q[3]-q[1])
def overlap(a,c,margin=0.15):
    return not (a[2]+margin<c[0] or a[0]-margin>c[2] or a[3]+margin<c[1] or a[1]-margin>c[3])
def fp(ref):
    return next(x for x in b.GetFootprints() if x.GetReference()==ref)

print("TEMPLATES")
for ref in ("Q502","Q201","R809"):
    f=fp(ref)
    print(ref,"AT",MM(f.GetPosition().x),MM(f.GetPosition().y),"ROT",f.GetOrientationDegrees(),"BBOX",tuple(round(v,3) for v in bb(f)),"WH",tuple(round(v,3) for v in wh(f)))

# Board lower edge in the relevant x range from Edge.Cuts bounding box is near
# y=164.214; use a conservative usable limit of 163.75 for courtyard scanning.
XMIN,XMAX,YMIN,YMAX=105.0,145.0,157.25,163.75
hard=[]
for f in b.GetFootprints():
    r=f.GetReference()
    if r.startswith("G") or r.startswith("kibuzzard"):
        continue
    q=bb(f)
    if not (q[2]<XMIN or q[0]>XMAX or q[3]<YMIN or q[1]>YMAX):
        hard.append((r,q))
print("HARD_BLOCKERS")
for r,q in hard:
    print(r,tuple(round(v,3) for v in q))

# Conservative envelope sizes derived from existing board template bounding
# boxes, rounded upward. We test both orientations of each MOSFET envelope.
q_envs=[(4.0,3.6),(3.6,4.0)]
r_envs=[(2.4,1.8),(1.8,2.4)]

def free_box(cx,cy,w,h):
    a=(cx-w/2,cy-h/2,cx+w/2,cy+h/2)
    if a[0]<XMIN or a[2]>XMAX or a[1]<YMIN or a[3]>YMAX:
        return False,[]
    hits=[r for r,q in hard if overlap(a,q)]
    return not hits,hits

print("Q_CANDIDATES")
qs=[]
for w,h in q_envs:
    for yi in range(int(YMIN*4),int(YMAX*4)+1):
        cy=yi/4
        for xi in range(int(XMIN*4),int(XMAX*4)+1):
            cx=xi/4
            ok,_=free_box(cx,cy,w,h)
            if ok:
                qs.append((cx,cy,w,h))
# Condense: only print candidates near the J401 switched feed or raw backbone,
# sorted by distance to J401.9 (116.84,153.785) plus bottom-backbone y=163.1.
def score(c):
    x,y,w,h=c
    return abs(x-116.84)*0.35 + abs(y-160.3)
for c in sorted(qs,key=score)[:30]:
    print("QFREE",*c)

# Search for two non-overlapping Q envelopes plus three resistor envelopes in a
# compact 14x6 mm cluster. This is a coarse feasibility screen, not placement.
print("PAIR_CANDIDATES")
for i,a in enumerate(sorted(qs,key=score)[:120]):
    ab=(a[0]-a[2]/2,a[1]-a[3]/2,a[0]+a[2]/2,a[1]+a[3]/2)
    for c in sorted(qs,key=score)[:120]:
        cb=(c[0]-c[2]/2,c[1]-c[3]/2,c[0]+c[2]/2,c[1]+c[3]/2)
        if overlap(ab,cb,0.3): continue
        if abs(a[0]-c[0])>12 or abs(a[1]-c[1])>5: continue
        print("PAIR",*a,"|",*c)
        if i>10: raise SystemExit
        break
