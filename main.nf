nextflow.enable.dsl = 2

params.dataset_manifest = "configs/datasets.yml"
params.method_manifest = "configs/methods.yml"
params.outdir = "results/demo"
params.demo_outdir = "demo_data"
params.method = "transparent_pseudobulk"

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

process MAKE_DEMO_REGULATORY_DATA {
  tag "demo_regulatory"
  publishDir "${params.outdir}/inputs", mode: "copy"

  output:
  path "demo_regulatory/demo_regulatory_peaks.csv", emit: peaks
  path "demo_regulatory/demo_peak_to_gene.csv", emit: peak_to_gene
  path "demo_regulatory/demo_motifs.csv", emit: motifs

  script:
  """
  python ${projectDir}/scripts/make_demo_regulatory_data.py --outdir demo_regulatory
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

process SELECT_METHODS {
  tag "method_selection"
  publishDir "${params.outdir}/method_selection", mode: "copy"

  input:
  path cells
  path expression

  output:
  path "selection/dataset_profile.csv", emit: dataset_profile
  path "selection/method_decisions.csv", emit: method_decisions

  script:
  """
  python ${projectDir}/bin/select_methods.py \
    --cells ${cells} \
    --expression ${expression} \
    --modality RNA \
    --outdir selection
  """
}

process RUN_METHOD {
  tag "${params.method}"
  publishDir "${params.outdir}/methods/${params.method}", mode: "copy"

  input:
  path cells
  path expression
  path method_decisions

  output:
  path "method/method_status.csv", emit: method_status
  path "method/effects.csv", optional: true, emit: effects

  script:
  """
  python ${projectDir}/bin/run_method.py \
    --cells ${cells} \
    --expression ${expression} \
    --method ${params.method} \
    --decision-file ${method_decisions} \
    --outdir method
  """
}

process SCORE_BENCHMARK {
  tag "${params.method}"
  publishDir "${params.outdir}/benchmark", mode: "copy"

  input:
  path effects
  path method_status

  output:
  path "benchmark/benchmark_metrics.csv", emit: benchmark_summary

  script:
  """
  python ${projectDir}/bin/score_benchmark.py \
    --effects ${effects} \
    --status ${method_status} \
    --outdir benchmark
  """
}

process REGULATORY_VALIDATION {
  tag "demo_regulatory_validation"
  publishDir "${params.outdir}/regulatory_validation", mode: "copy"

  input:
  path effects
  path peaks
  path peak_to_gene
  path motifs

  output:
  path "regulatory/regulatory_validation.csv", emit: regulatory_validation
  path "regulatory/regulatory_validation_summary.csv", emit: regulatory_summary
  path "regulatory/validated_ad_microglia_hits.csv", emit: validated_hits

  script:
  """
  python ${projectDir}/bin/run_regulatory_validation.py \
    --effects ${effects} \
    --peaks ${peaks} \
    --peak-to-gene ${peak_to_gene} \
    --motifs ${motifs} \
    --synthetic \
    --outdir regulatory
  """
}

process MAKE_REPORT {
  tag "demo_report"
  publishDir "${params.outdir}/report", mode: "copy"

  input:
  path dataset_qc
  path benchmark_summary
  path method_decisions
  path regulatory_summary

  output:
  path "report/demo_report.md", emit: report

  script:
  """
  python ${projectDir}/bin/make_report.py \
    --dataset-qc ${dataset_qc} \
    --benchmark-summary ${benchmark_summary} \
    --method-decisions ${method_decisions} \
    --regulatory-summary ${regulatory_summary} \
    --out report/demo_report.md
  """
}

workflow {
  demo = MAKE_DEMO_DATASET()
  regulatory_demo = MAKE_DEMO_REGULATORY_DATA()
  qc = BASELINE_QC(demo.cells, demo.expression)
  selection = SELECT_METHODS(demo.cells, demo.expression)
  method = RUN_METHOD(demo.cells, demo.expression, selection.method_decisions)
  score = SCORE_BENCHMARK(method.effects, method.method_status)
  regulatory = REGULATORY_VALIDATION(method.effects, regulatory_demo.peaks, regulatory_demo.peak_to_gene, regulatory_demo.motifs)
  MAKE_REPORT(qc.dataset_qc, score.benchmark_summary, selection.method_decisions, regulatory.regulatory_summary)
}
