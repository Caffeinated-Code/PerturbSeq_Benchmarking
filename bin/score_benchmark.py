#!/usr/bin/env python3
"""Emit benchmark metrics without inventing values for unavailable estimands."""
import argparse, csv, math
from pathlib import Path

PROGRAMS={"ad_risk":{"TREM2","APOE","INPP5D","BIN1","PICALM","CD33","ABCA7","CR1","SORL1"},
          "microglia_state":{"SPP1","CST7","LPL","P2RY12","CX3CR1","TMEM119","CSF1R","ISG15","IFIT1"}}

def read(path):
    with open(path,newline="") as h:return list(csv.DictReader(h))
def finite(x):
    try: return math.isfinite(float(x))
    except (TypeError,ValueError): return False
def main():
    p=argparse.ArgumentParser();p.add_argument("--effects");p.add_argument("--status",required=True);p.add_argument("--outdir",required=True);p.add_argument("--fdr",type=float,default=.05)
    p.add_argument("--null-effects");p.add_argument("--guide-effects");p.add_argument("--stability-effects");p.add_argument("--classifications");a=p.parse_args()
    out=Path(a.outdir);out.mkdir(parents=True,exist_ok=True);status=read(a.status)[0];method=status["method_id"]
    rows=[]
    def metric(name,value="",lo="",hi="",state="ESTIMATED",detail=""):
        rows.append({"method_id":method,"method_status":status["status"],"metric":name,"value":value,"ci_low":lo,"ci_high":hi,"metric_state":state,"detail":detail})
    metric("runtime_seconds",status.get("runtime_seconds",""),state="MEASURED")
    metric("peak_memory_mb",status.get("peak_memory_mb",""),state="MEASURED")
    metric("failure_reason",state="OBSERVED" if status["status"]!="RUN" else "NOT_APPLICABLE",detail=status.get("reason",""))
    if status["status"] != "RUN" or not a.effects or not Path(a.effects).exists():
        for name in ("fdr_discoveries","target_engagement_rate","null_type_i_error","guide_concordance","effect_size_stability","escapee_fraction","biological_program_recovery"):
            metric(name,state="NOT_AVAILABLE",detail="Method did not emit compatible effect estimates.")
    else:
        effects=read(a.effects); qkey="q_value" if effects and "q_value" in effects[0] else None
        hits=[r for r in effects if qkey and finite(r.get(qkey)) and float(r[qkey])<=a.fdr]
        metric("fdr_discoveries",len(hits),state="MEASURED")
        target_rows=[r for r in effects if r.get("gene")==r.get("perturbation") and finite(r.get("effect"))]
        engaged=[r for r in target_rows if float(r["effect"])<0 and (not qkey or float(r[qkey])<=a.fdr)]
        rate=len(engaged)/len(target_rows) if target_rows else None
        if target_rows:
            z=1.96;n=len(target_rows);center=(rate+z*z/(2*n))/(1+z*z/n);half=z*math.sqrt(rate*(1-rate)/n+z*z/(4*n*n))/(1+z*z/n)
            metric("target_engagement_rate",rate,max(0,center-half),min(1,center+half),state="ESTIMATED",detail=f"{len(engaged)}/{len(target_rows)} targets show significant negative effect; Wilson interval")
        else: metric("target_engagement_rate",state="NOT_AVAILABLE",detail="No on-target effect rows.")
        for program,genes in PROGRAMS.items():
            found={r.get("gene") for r in hits}&genes
            metric(f"biological_program_recovery:{program}",len(found)/len(genes),state="DESCRIPTIVE",detail=";".join(sorted(found)))
        if a.null_effects and Path(a.null_effects).exists():
            nulls=read(a.null_effects); tested=[r for r in nulls if finite(r.get("p_value"))]; false=sum(float(r["p_value"])<=a.fdr for r in tested); rate=false/len(tested) if tested else None
            if rate is None: metric("null_type_i_error",state="NOT_AVAILABLE",detail="No finite null p-values.")
            else:
                se=math.sqrt(rate*(1-rate)/len(tested));metric("null_type_i_error",rate,max(0,rate-1.96*se),min(1,rate+1.96*se),detail=f"{false}/{len(tested)} null tests at alpha={a.fdr}")
        else: metric("null_type_i_error",state="NOT_AVAILABLE",detail="Requires null/control perturbation tests.")
        if a.guide_effects and Path(a.guide_effects).exists():
            guides=read(a.guide_effects); by={}
            for r in guides: by.setdefault((r.get("perturbation"),r.get("gene")),[]).append(float(r["effect"]))
            signs=[sum(v>0 for v in vals)/len(vals) for vals in by.values() if len(vals)>1]
            concord=[max(x,1-x) for x in signs];metric("guide_concordance",sum(concord)/len(concord) if concord else "",state="ESTIMATED" if concord else "NOT_AVAILABLE",detail="Mean majority-sign agreement across perturbation-gene pairs.")
        else: metric("guide_concordance",state="NOT_AVAILABLE",detail="Requires guide-level effects.")
        if a.stability_effects and Path(a.stability_effects).exists():
            other={(r.get("perturbation"),r.get("gene")):float(r["effect"]) for r in read(a.stability_effects) if finite(r.get("effect"))}; base={(r.get("perturbation"),r.get("gene")):float(r["effect"]) for r in effects if finite(r.get("effect"))}; keys=set(base)&set(other)
            delta=sum(abs(base[k]-other[k]) for k in keys)/len(keys) if keys else None;metric("effect_size_stability",delta if delta is not None else "",state="ESTIMATED" if keys else "NOT_AVAILABLE",detail=f"Mean absolute effect change across {len(keys)} matched effects; lower is more stable.")
        else: metric("effect_size_stability",state="NOT_AVAILABLE",detail="Requires replicate/downsample reruns.")
        if a.classifications and Path(a.classifications).exists():
            classes=read(a.classifications); target=[r for r in classes if r.get("escapee_class") not in {"NT",""}]; escaped=sum(r.get("escapee_class") in {"NP","escapee"} for r in target);metric("escapee_fraction",escaped/len(target) if target else "",state="ESTIMATED" if target else "NOT_AVAILABLE",detail=f"{escaped}/{len(target)} target-assigned cells classified non-perturbed.")
        else: metric("escapee_fraction",state="NOT_APPLICABLE",detail="No cell-classification output for this method.")
    with open(out/"benchmark_metrics.csv","w",newline="") as h:
        w=csv.DictWriter(h,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
if __name__=="__main__":main()
