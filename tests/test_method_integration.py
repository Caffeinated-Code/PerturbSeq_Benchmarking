import csv,subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def rows(path):
 with open(path,newline="") as h:return list(csv.DictReader(h))
class IntegrationTests(unittest.TestCase):
 def fixture(self,moi="low",features=600,null=False):
  d=Path(tempfile.mkdtemp());cmd=[sys.executable,str(ROOT/"scripts/make_benchmark_fixture.py"),"--outdir",str(d),"--moi",moi,"--features",str(features)]
  if null:cmd.append("--null")
  subprocess.run(cmd,check=True);return d
 def route(self,d,readout="auto"):
  o=d/"route";subprocess.run([sys.executable,str(ROOT/"bin/select_methods.py"),"--cells",str(d/"cells.csv"),"--expression",str(d/"expression.csv"),"--modality","RNA","--readout-class",readout,"--outdir",str(o)],check=True);return {r["method_id"]:r for r in rows(o/"method_decisions.csv")}
 def test_low_and_high_moi_sceptre_paths_are_exclusive(self):
  low=self.route(self.fixture("low"));high=self.route(self.fixture("high"))
  self.assertEqual(low["sceptre_low_moi"]["decision"],"RUN");self.assertEqual(low["sceptre_high_moi_or_mixed_moi"]["decision"],"INCOMPATIBLE")
  self.assertEqual(high["sceptre_low_moi"]["decision"],"INCOMPATIBLE");self.assertEqual(high["sceptre_high_moi_or_mixed_moi"]["decision"],"RUN")
 def test_targeted_panel_excludes_signature_methods(self):
  r=self.route(self.fixture(features=40),"targeted")
  self.assertEqual(r["mixscape"]["decision"],"INCOMPATIBLE");self.assertEqual(r["gsfa"]["decision"],"INCOMPATIBLE")
 def test_pseudobulk_executes_and_status_is_run(self):
  d=self.fixture(features=20);o=d/"method"
  subprocess.run([sys.executable,str(ROOT/"bin/run_method.py"),"--cells",str(d/"cells.csv"),"--expression",str(d/"expression.csv"),"--method","transparent_pseudobulk","--outdir",str(o)],check=True)
  self.assertEqual(rows(o/"method_status.csv")[0]["status"],"RUN");self.assertTrue((o/"effects.csv").exists())
  target=next(r for r in rows(o/"effects.csv") if r["perturbation"]=="TARGET" and r["gene"]=="TARGET");self.assertLess(float(target["effect"]),0)
 def test_unknown_adapter_is_not_available(self):
  d=self.fixture(features=20);o=d/"unknown"
  subprocess.run([sys.executable,str(ROOT/"bin/run_method.py"),"--cells",str(d/"cells.csv"),"--expression",str(d/"expression.csv"),"--method","not_real","--outdir",str(o)],check=True)
  self.assertEqual(rows(o/"method_status.csv")[0]["status"],"NOT_AVAILABLE")
if __name__=="__main__":unittest.main()
