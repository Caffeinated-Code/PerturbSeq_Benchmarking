#!/usr/bin/env Rscript
# Thin adapters deliberately call the upstream packages; no fallback is relabeled as that method.
args <- commandArgs(trailingOnly = TRUE)
method <- args[[1]]; cells_path <- args[[2]]; expression_path <- args[[3]]; outdir <- args[[4]]
dir.create(outdir, recursive = TRUE, showWarnings = FALSE)
required <- switch(method,
  sceptre_low_moi="sceptre", sceptre_high_moi_or_mixed_moi="sceptre",
  mixscape="Seurat", ps="scMAGeCK", gsfa="GSFA", NA_character_)
if (is.na(required) || !requireNamespace(required, quietly=TRUE)) {
  message(sprintf("Required R package '%s' is not installed", required)); quit(status=69)
}
cells <- read.csv(cells_path, check.names=FALSE, stringsAsFactors=FALSE)
expr <- read.csv(expression_path, check.names=FALSE, stringsAsFactors=FALSE)
rownames(expr) <- expr$cell_id; expr$cell_id <- NULL
expr <- as.matrix(expr); storage.mode(expr) <- "numeric"
rownames(cells) <- cells$cell_id; cells <- cells[rownames(expr),,drop=FALSE]
n_results <- 0L

if (method == "mixscape") {
  counts <- t(expr)
  obj <- Seurat::CreateSeuratObject(counts=counts, meta.data=cells)
  obj <- Seurat::NormalizeData(obj, verbose=FALSE)
  obj <- Seurat::FindVariableFeatures(obj, verbose=FALSE)
  obj <- Seurat::ScaleData(obj, verbose=FALSE)
  obj <- Seurat::RunPCA(obj, verbose=FALSE)
  obj <- Seurat::CalcPerturbSig(obj, assay="RNA", slot="data", gd.class="perturbation", nt.cell.class="NTC", reduction="pca", ndims=10, num.neighbors=20, verbose=FALSE)
  obj <- Seurat::RunMixscape(obj, assay="PRTB", slot="scale.data", labels="perturbation", nt.class.name="NTC", de.assay="RNA", verbose=FALSE)
  out <- data.frame(cell_id=colnames(obj), perturbation=obj$perturbation,
                    escapee_class=obj$mixscape_class.global, posterior_probability=obj$p_ko)
  write.csv(out, file.path(outdir,"classifications.csv"), row.names=FALSE); n_results <- nrow(out)
} else if (method == "ps") {
  obj <- Seurat::CreateSeuratObject(counts=t(expr), meta.data=cells)
  obj <- Seurat::NormalizeData(obj, verbose=FALSE)
  guides <- data.frame(cell=cells$cell_id, barcode=cells$guide_id, sgrna=cells$guide_id,
                       gene=cells$perturbation, read_count=1, umi_count=1)
  targets <- setdiff(unique(cells$perturbation), "NTC"); output <- list()
  for (target in targets) {
    fit <- scMAGeCK::scmageck_eff_estimate(obj, guides, perturb_gene=target, non_target_ctrl="NTC")
    score_col <- grep("_eff$", colnames(fit$rds@meta.data), value=TRUE)[1]
    output[[target]] <- data.frame(cell_id=rownames(fit$rds@meta.data), perturbation=target,
                                  response_score=fit$rds@meta.data[[score_col]])
  }
  out <- do.call(rbind, output); write.csv(out,file.path(outdir,"scores.csv"),row.names=FALSE); n_results <- nrow(out)
} else if (method == "gsfa") {
  Y <- log1p(expr); targets <- setdiff(sort(unique(cells$perturbation)), "NTC")
  G <- sapply(targets, function(x) as.numeric(cells$perturbation == x)); colnames(G) <- targets
  fit <- GSFA::fit_gsfa_multivar(Y=Y, G=G, K=min(10,ncol(Y)-1), niter=500, verbose=FALSE)
  saveRDS(fit,file.path(outdir,"gsfa_fit.rds"))
  beta <- if (!is.null(fit$beta_mean)) fit$beta_mean else fit$beta
  out <- as.data.frame(beta); out$perturbation <- rownames(out)
  write.csv(out,file.path(outdir,"program_effects.csv"),row.names=FALSE); n_results <- nrow(out)
} else {
  # SCEPTRE keeps distinct MOI entry points through explicit analysis_method.
  response <- t(expr); grnas <- unique(cells$guide_id)
  grna_matrix <- sapply(cells$guide_id, function(x) as.numeric(grnas == x)); rownames(grna_matrix) <- grnas
  grna_target <- unique(cells[c("guide_id","perturbation")]); names(grna_target) <- c("grna_id","grna_target")
  grna_target$grna_target[grna_target$grna_target == "NTC"] <- NA
  covars <- model.matrix(~ 0 + batch + condition, data=cells)
  obj <- sceptre::import_data(response_matrix=response, grna_matrix=grna_matrix,
    extra_covariates=covars, grna_target_data_frame=grna_target,
    moi=if (method == "sceptre_low_moi") "low" else "high")
  targets <- na.omit(unique(grna_target$grna_target))
  discovery <- expand.grid(response_id=rownames(response), grna_target=targets, stringsAsFactors=FALSE)
  positive <- subset(discovery, response_id == grna_target)
  obj <- sceptre::set_analysis_parameters(obj, discovery_pairs=discovery, positive_control_pairs=positive)
  obj <- sceptre::assign_grnas(obj); obj <- sceptre::run_qc(obj)
  obj <- sceptre::run_calibration_check(obj); obj <- sceptre::run_power_check(obj)
  obj <- sceptre::run_discovery_analysis(obj)
  out <- sceptre::get_discovery_results(obj)
  write.csv(out,file.path(outdir,"effects.csv"),row.names=FALSE); n_results <- nrow(out)
}
meta <- sprintf('{"version":"%s","n_results":%d}', as.character(utils::packageVersion(required)), n_results)
writeLines(meta, file.path(outdir,"adapter_metadata.json"))
