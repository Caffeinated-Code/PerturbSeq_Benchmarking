#!/usr/bin/env python3
"""Deterministic positive/null fixtures for routing, calibration, and failure tests."""
import argparse,csv,random
from pathlib import Path
def main():
 p=argparse.ArgumentParser();p.add_argument("--outdir",required=True);p.add_argument("--moi",choices=("low","high"),default="low");p.add_argument("--features",type=int,default=600);p.add_argument("--null",action="store_true");a=p.parse_args();random.seed(7)
 out=Path(a.outdir);out.mkdir(parents=True,exist_ok=True);genes=["TARGET"]+[f"G{i}" for i in range(a.features-1)];cells=[];expr=[]
 for pert in ("NTC","TARGET","NULL"):
  for i in range(40):
   cid=f"{pert}_{i}";counts={g:max(0,int(random.gauss(5,1.5))) for g in genes}
   if pert=="TARGET" and not a.null:counts["TARGET"]=max(0,counts["TARGET"]-4);counts["G0"]+=4
   cells.append({"cell_id":cid,"perturbation":pert,"guide_id":f"sg{pert}{i%2}","control_type":"non_targeting" if pert=="NTC" else "targeting","batch":f"b{i%2}","condition":"base","guide_count":2 if a.moi=="high" and i%3==0 else 1})
   expr.append({"cell_id":cid,**counts})
 for name,rows in (("cells.csv",cells),("expression.csv",expr)):
  with open(out/name,"w",newline="") as h:w=csv.DictWriter(h,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
if __name__=="__main__":main()
