#!/usr/bin/env python3
"""Pairwise effect agreement; intentionally produces no composite leaderboard."""
import argparse,csv,itertools,math
from pathlib import Path
def read(p):
    with open(p,newline="") as h:return list(csv.DictReader(h))
def corr(xs,ys):
    if len(xs)<3:return ""
    mx,my=sum(xs)/len(xs),sum(ys)/len(ys);a=sum((x-mx)*(y-my) for x,y in zip(xs,ys));b=sum((x-mx)**2 for x in xs);c=sum((y-my)**2 for y in ys)
    return a/math.sqrt(b*c) if b and c else ""
def main():
    p=argparse.ArgumentParser();p.add_argument("--effects",nargs="+",required=True);p.add_argument("--out",required=True);a=p.parse_args()
    tables={}
    for f in a.effects:
        rows=read(f);m=rows[0].get("method",Path(f).parent.name) if rows else Path(f).parent.name
        tables[m]={(r.get("perturbation"),r.get("gene")):float(r["effect"]) for r in rows if r.get("effect") not in (None,"")}
    out=[]
    for x,y in itertools.combinations(sorted(tables),2):
        keys=set(tables[x])&set(tables[y]);xs=[tables[x][k] for k in keys];ys=[tables[y][k] for k in keys]
        out.append({"method_a":x,"method_b":y,"n_shared":len(keys),"effect_pearson":corr(xs,ys),"state":"ESTIMATED" if len(keys)>=3 else "NOT_AVAILABLE"})
    Path(a.out).parent.mkdir(parents=True,exist_ok=True)
    with open(a.out,"w",newline="") as h:
        w=csv.DictWriter(h,fieldnames=["method_a","method_b","n_shared","effect_pearson","state"]);w.writeheader();w.writerows(out)
if __name__=="__main__":main()
