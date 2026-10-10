nextflow.enable.dsl = 2

params.gse178317_archive = "data/raw/GSE178317/GSE178317_RAW.tar"
params.gse207628_archive = "data/raw/GSE207628/GSE207628_RAW.tar"
params.replogle_file = "data/raw/replogle_k562_essential/K562_essential_raw_bulk_01.h5ad"
params.outdir = "results/real_data_full"
params.drager_cells_per_lane = 0
repoDir = file("${projectDir}/..").canonicalPath

process PROCESS_REAL_DATA {
  tag "three-public-datasets"
  cpus 8
  memory "48 GB"
  time "12h"
  publishDir params.outdir, mode: "copy"

  input:
  path gse178317_archive
  path gse207628_archive
  path replogle

  output:
  path "summary/*"
  path "products/*.h5ad"

  script:
  """
  mkdir -p staged/GSE178317 staged/GSE207628 staged/replogle_k562_essential summary products
  tar -xf ${gse178317_archive} -C staged/GSE178317
  tar -xf ${gse207628_archive} -C staged/GSE207628
  cp ${replogle} staged/replogle_k562_essential/K562_essential_raw_bulk_01.h5ad
  python ${repoDir}/scripts/process_real_datasets.py \
    --dataset all \
    --outdir \$PWD/summary \
    --product-dir \$PWD/products \
    --gse178317-dir \$PWD/staged/GSE178317 \
    --gse207628-dir \$PWD/staged/GSE207628 \
    --replogle-file \$PWD/staged/replogle_k562_essential/K562_essential_raw_bulk_01.h5ad \
    --drager-cells-per-lane ${params.drager_cells_per_lane}
  """
}

workflow {
  drager = Channel.fromPath("${repoDir}/${params.gse178317_archive}", checkIfExists: true)
  hypr = Channel.fromPath("${repoDir}/${params.gse207628_archive}", checkIfExists: true)
  replogle = Channel.fromPath("${repoDir}/${params.replogle_file}", checkIfExists: true)
  PROCESS_REAL_DATA(drager, hypr, replogle)
}
