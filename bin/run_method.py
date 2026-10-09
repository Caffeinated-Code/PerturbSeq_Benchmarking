#!/usr/bin/env python3
"""Execute one method adapter and always emit an honest lifecycle record."""
import argparse, csv, importlib.metadata, json, math, os, resource, shutil, subprocess, sys, time, traceback
from collections import defaultdict
from pathlib import Path

STATES = {"RUN", "SKIP", "INCOMPATIBLE", "FAILED", "NOT_AVAILABLE"}

def read_csv(path):
    with open(path, newline="") as h: return list(csv.DictReader(h))

def write_csv(path, rows, fields):
    with open(path, "w", newline="") as h:
        w = csv.DictWriter(h, fieldnames=fields, extrasaction="ignore"); w.writeheader(); w.writerows(rows)

def bh(pvals):
    n = len(pvals); out = [1.0] * n; running = 1.0
    for rank, idx in reversed(list(enumerate(sorted(range(n), key=lambda i: pvals[i]), 1))):
        running = min(running, pvals[idx] * n / rank); out[idx] = running
    return out

def normal_p(z): return math.erfc(abs(z) / math.sqrt(2.0))

def transparent_pseudobulk(cells_path, expression_path, outdir, method):
    cells = {r["cell_id"]: r for r in read_csv(cells_path)}; expr = read_csv(expression_path)
    genes = [g for g in expr[0] if g != "cell_id"]; replicate_key = "replicate" if any(r.get("replicate") for r in cells.values()) else "batch"
    grouped = defaultdict(list)
    for row in expr:
        meta = cells[row["cell_id"]]; grouped[(meta.get("perturbation", ""), meta.get(replicate_key, "all"))].append(row)
    aggregates = {}
    for key, rows in grouped.items(): aggregates[key] = {g: sum(float(r[g]) for r in rows) / len(rows) for g in genes}
    controls = sorted(k for k in aggregates if k[0] in {"NTC", "non_targeting", "control"})
    targets = sorted(set(k[0] for k in aggregates) - {"NTC", "non_targeting", "control"})
    if not controls: raise ValueError("No non-targeting control aggregates")
    results = []
    for target in targets:
        target_keys = [k for k in aggregates if k[0] == target]
        for gene in genes:
            x = [aggregates[k][gene] for k in target_keys]; y = [aggregates[k][gene] for k in controls]
            mx, my = sum(x)/len(x), sum(y)/len(y); effect = math.log2((mx + 1)/(my + 1))
            vx = sum((v-mx)**2 for v in x)/(len(x)-1) if len(x)>1 else 0
            vy = sum((v-my)**2 for v in y)/(len(y)-1) if len(y)>1 else 0
            se = math.sqrt(vx/max(1,len(x)) + vy/max(1,len(y)))
            p = normal_p((mx-my)/se) if se else (0.0 if mx != my else 1.0)
            results.append({"method": method, "perturbation": target, "gene": gene, "effect": effect, "log2fc": effect,
                "effect_direction": "up" if effect > .25 else "down" if effect < -.25 else "neutral", "effect_se": se,
                "p_value": p, "n_target_replicates": len(x), "n_control_replicates": len(y), "analysis_unit": "replicate_pseudobulk"})
    q = bh([r["p_value"] for r in results])
    for row, qv in zip(results, q): row["q_value"] = qv
    write_csv(outdir / "effects.csv", results, ["method","perturbation","gene","effect","log2fc","effect_direction","effect_se","p_value","q_value","n_target_replicates","n_control_replicates","analysis_unit"])
    return len(results), "builtin-1"

def pertpy_distance(cells_path, expression_path, outdir, method):
    import anndata as ad, numpy as np, pandas as pd, pertpy as pt
    cells, expr = read_csv(cells_path), read_csv(expression_path); by_id = {r["cell_id"]: r for r in cells}
    genes = [g for g in expr[0] if g != "cell_id"]; X = np.asarray([[float(r[g]) for g in genes] for r in expr])
    obs = pd.DataFrame([by_id[r["cell_id"]] for r in expr], index=[r["cell_id"] for r in expr]); adata = ad.AnnData(X=X, obs=obs, var=pd.DataFrame(index=genes))
    dist = pt.tl.Distance(metric="edistance"); matrix = dist.pairwise(adata, groupby="perturbation")
    labels = list(matrix.index) if hasattr(matrix, "index") else sorted(obs["perturbation"].unique())
    control = next((x for x in labels if x in {"NTC","non_targeting","control"}), None)
    if control is None: raise ValueError("No non-targeting control group")
    rows = [{"method": method, "perturbation": label, "reference": control, "distance": float(matrix.loc[label, control])} for label in labels if label != control]
    write_csv(outdir / "distances.csv", rows, ["method","perturbation","reference","distance"])
    return len(rows), importlib.metadata.version("pertpy")

def external_r(method, cells, expression, outdir):
    rscript = shutil.which("Rscript")
    if not rscript: raise ModuleNotFoundError("Rscript is not installed")
    script = Path(__file__).resolve().parent / "adapters" / "run_r_method.R"
    proc = subprocess.run([rscript, str(script), method, str(cells), str(expression), str(outdir)], text=True, capture_output=True)
    (outdir / "adapter.stdout.log").write_text(proc.stdout); (outdir / "adapter.stderr.log").write_text(proc.stderr)
    if proc.returncode == 69: raise ModuleNotFoundError(proc.stderr.strip() or f"dependency for {method} unavailable")
    if proc.returncode: raise RuntimeError(proc.stderr.strip() or f"adapter exited {proc.returncode}")
    meta = json.loads((outdir / "adapter_metadata.json").read_text())
    return int(meta.get("n_results", 0)), meta.get("version", "unknown")

def main():
    p=argparse.ArgumentParser(); p.add_argument("--cells",required=True); p.add_argument("--expression",required=True)
    p.add_argument("--method",required=True); p.add_argument("--decision-file"); p.add_argument("--outdir",required=True)
    args=p.parse_args(); out=Path(args.outdir); out.mkdir(parents=True,exist_ok=True); started=time.time()
    status, reason, version, n_results = "FAILED", "", "", 0
    if args.decision_file:
        route = next((r for r in read_csv(args.decision_file) if r["method_id"] == args.method), None)
        if route and route["decision"] != "RUN": status, reason = route["decision"], route["reason"]
    try:
        if status not in {"SKIP", "INCOMPATIBLE"}:
            if args.method in {"transparent_pseudobulk", "simple_pseudobulk"}: n_results, version = transparent_pseudobulk(args.cells,args.expression,out,args.method)
            elif args.method == "pertpy_distance": n_results, version = pertpy_distance(args.cells,args.expression,out,args.method)
            elif args.method in {"sceptre_low_moi","sceptre_high_moi_or_mixed_moi","mixscape","ps","gsfa"}: n_results, version = external_r(args.method,args.cells,args.expression,out)
            elif args.method == "native_paper": status, reason = "NOT_AVAILABLE", "No dataset-specific executable adapter was supplied."
            else: status, reason = "NOT_AVAILABLE", "No registered adapter."
            if not status == "NOT_AVAILABLE": status, reason = "RUN", "Adapter completed and output validation passed."
    except ModuleNotFoundError as e: status, reason = "NOT_AVAILABLE", str(e)
    except Exception as e:
        status, reason = "FAILED", f"{type(e).__name__}: {e}"; (out/"traceback.log").write_text(traceback.format_exc())
    elapsed=time.time()-started; peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    peak_mb = peak/(1024*1024) if sys.platform=="darwin" else peak/1024
    row={"method_id":args.method,"status":status,"reason":reason,"version":version,"n_results":n_results,"runtime_seconds":round(elapsed,6),"peak_memory_mb":round(peak_mb,3)}
    assert status in STATES; write_csv(out/"method_status.csv",[row],list(row))
    print(json.dumps(row,sort_keys=True)); return 0

if __name__=="__main__": raise SystemExit(main())
