nextflow.enable.dsl = 2

params.dataset_manifest = "configs/datasets.yml"
params.method_manifest = "configs/methods.yml"
params.outdir = "results/demo"
params.demo_outdir = "demo_data"
params.method = "simple_pseudobulk"

process MAKE_DEMO_DATASET {
  tag "demo_synthetic"
  publishDir "${params.outdir}/inputs", mode: "copy"

  output:
  path "demo_data/demo_cells.csv", emit: cells
  path "demo_data/demo_expression.csv", emit: expression
  path "demo_data/README.md", emit: demo_readme

  script:
  """
  python ${projectDir}/scripts/make_demo_dataset.py --outdir demo_data
  """
}

process BASELINE_QC {
  tag "demo_synthetic"
  publishDir "${params.outdir}/qc", mode: "copy"

  input:
  path cells
  path expression

  output:
  path "qc/dataset_qc.csv", emit: dataset_qc
  path "qc/guide_qc.csv", emit: guide_qc
  path "qc/cell_state_summary.csv", emit: cell_state_summary

  script:
  """
  python ${projectDir}/bin/run_baseline_qc.py \
    --cells ${cells} \
    --expression ${expression} \
    --outdir qc
  """
}

process RUN_METHOD {
  tag "${params.method}"
  publishDir "${params.outdir}/methods/${params.method}", mode: "copy"

  input:
  path cells
  path expression

  output:
  path "method/${params.method}_effects.csv", emit: effects

  script:
  """
  python ${projectDir}/bin/run_method.py \
    --cells ${cells} \
    --expression ${expression} \
    --method ${params.method} \
    --outdir method
  """
}

process SCORE_BENCHMARK {
  tag "${params.method}"
  publishDir "${params.outdir}/benchmark", mode: "copy"

  input:
  path effects

  output:
  path "benchmark/benchmark_summary.csv", emit: benchmark_summary

  script:
  """
  python ${projectDir}/bin/score_benchmark.py \
    --effects ${effects} \
    --outdir benchmark
  """
}

process MAKE_REPORT {
  tag "demo_report"
  publishDir "${params.outdir}/report", mode: "copy"

  input:
  path dataset_qc
  path benchmark_summary

  output:
  path "report/demo_report.md", emit: report

  script:
  """
  python ${projectDir}/bin/make_report.py \
    --dataset-qc ${dataset_qc} \
    --benchmark-summary ${benchmark_summary} \
    --out report/demo_report.md
  """
}

workflow {
  demo = MAKE_DEMO_DATASET()
  qc = BASELINE_QC(demo.cells, demo.expression)
  method = RUN_METHOD(demo.cells, demo.expression)
  score = SCORE_BENCHMARK(method.effects)
  MAKE_REPORT(qc.dataset_qc, score.benchmark_summary)
}
