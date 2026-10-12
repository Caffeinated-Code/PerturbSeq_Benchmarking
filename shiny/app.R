library(shiny)
library(bslib)
library(DT)
library(ggplot2)

read_result <- function(path) {
  if (file.exists(path)) read.csv(path, stringsAsFactors = FALSE, check.names = FALSE) else data.frame()
}

result_path <- function(...) {
  local_path <- file.path("..", "results", ...)
  bundled_path <- file.path("results", ...)
  if (file.exists(local_path)) local_path else bundled_path
}

term_help <- list(
  "MOI" = "Multiplicity of infection is the average number of viral particles delivered to each cell. Guide count and guide collisions provide a practical estimate.",
  "guide collision rate" = "The fraction of cells assigned more than one guide. A high rate makes single-perturbation effects harder to interpret.",
  "pseudobulk" = "A pseudobulk profile sums cells within a biological group, such as a replicate and perturbation. It supports replicate-aware comparisons.",
  "evidence demo" = "Generated records that test the software and evidence rules. They are not biological findings.",
  "GWAS corroboration" = "A GWAS association links a genomic locus to disease risk. Gene mapping supports disease relevance, but does not prove that the mapped gene is causal.",
  "LOW_SUPPORT" = "The evidence demo did not meet its synthetic support rule. This label does not reject a biological result."
)

help_button <- function(label) {
  actionLink(paste0("help_", gsub("[^A-Za-z0-9]", "_", label)), label)
}

ui <- page_navbar(
  title = "PerturbSeq Benchmarking",
  fillable = FALSE,
  theme = bs_theme(version = 5, bootswatch = "flatly", primary = "#24506f", secondary = "#6c7a89", success = "#2f7d5c", warning = "#b7791f", danger = "#a94442"),
  header = tagList(
    tags$style(HTML("
    body { background: #f7faf9; color: #17201d; }
    .container-fluid { max-width: 1440px; }
    .card { border-radius: 8px; border: 1px solid #d8e3df; box-shadow: none; margin-bottom: 1rem; }
    .card-body { padding: 1rem 1.1rem; }
    .navbar { border-bottom: 1px solid #d8e3df; }
    .navbar-nav .nav-link { border-radius: 4px; margin: 0 0.08rem; }
    .navbar-nav .nav-link.active, .navbar-nav .show > .nav-link { background: #c85f46; color: #ffffff !important; }
    .dropdown-menu .dropdown-item.active { background: #c85f46; color: #ffffff; }
    .metric { font-size: 1.5rem; font-weight: 700; color: #17384f; }
    .small-note { color: #51615c; font-size: 0.92rem; }
    .shiny-plot-output { width: 100% !important; }
    .dataTables_wrapper { overflow-x: auto; }
    .source-link a { color: #17384f; font-weight: 650; }
    .demo-banner { background: #fff7d6; border: 1px solid #dfc96f; padding: 0.75rem 1rem; margin: 0.8rem 0; font-weight: 600; }
    .report-list li { margin-bottom: 0.45rem; }
    @media (max-width: 768px) {
      .container-fluid { padding-left: 0.65rem; padding-right: 0.65rem; }
      .card-body { padding: 0.85rem; }
      .demo-banner { font-size: 0.92rem; }
      .metric { font-size: 1.3rem; }
    }
    ")),
    tags$div(class = "demo-banner", "Method comparisons use generated test data. Public-data tabs show measured QC and paper-native summaries. The two microglia datasets lack cell-to-guide assignments, so they do not support perturbation-effect estimates.")
  ),
  nav_panel(
    "Overview",
    layout_columns(
      card(card_header("Dataset"), uiOutput("dataset_metric")),
      card(card_header("Generated effects"), uiOutput("effect_metric")),
      card(card_header("GWAS-supported candidates"), uiOutput("gwas_metric"))
    ),
    card(
      card_header("Read this first"),
      p("The app separates measured public-data summaries from generated software tests. Run the workflow on guide-resolved data before drawing perturbation conclusions."),
      p("Select ", help_button("MOI"), ", ", help_button("pseudobulk"), ", or ", help_button("GWAS corroboration"), " for a short explanation.")
    )
  ),
  nav_menu(
    "Data",
  nav_panel(
    "Real Data",
    card(
      card_header("Processing status"),
      p("These rows report what was measured from deposited public files and what remains unavailable."),
      DTOutput("real_dataset_status")
    ),
    navset_card_tab(
      nav_panel("Drager lane QC", DTOutput("real_drager_lane_qc")),
      nav_panel("Drager guide audit", DTOutput("real_drager_guide_audit")),
      nav_panel("Drager state baseline", DTOutput("real_drager_state")),
      nav_panel("AD HyPR-seq QC", DTOutput("real_hypr_qc")),
      nav_panel("AD replicate baseline", DTOutput("real_hypr_baseline")),
      nav_panel("Replogle QC", DTOutput("real_replogle_qc")),
      nav_panel("Replogle native baseline", DTOutput("real_replogle_baseline"))
    ),
    card(
      card_header("Interpretation boundary"),
      p("GSE178317 supports lane-aware expression QC and microglial state summaries. Its deposited matrices do not contain the authors' consensus cell-to-guide assignments."),
      p("GSE207628 supports targeted-panel QC and replicate agreement. Its public matrices do not provide a cell-to-guide or cCRE mapping."),
      p("The Replogle object is an author-deposited guide-pair pseudobulk object. It supports audit summaries, not cell-level escapee or donor analysis.")
    )
  ),
  nav_panel(
    "Design / MOI",
    card(card_header("Experimental design"), p("Guide multiplicity, controls, donor/replicate structure, and readout breadth determine which methods are applicable."), DTOutput("dataset_qc_design"))
  ),
  nav_panel(
    "Dataset QC",
    navset_card_tab(
      nav_panel("Dataset profile", DTOutput("dataset_qc")),
      nav_panel("Guide QC", DTOutput("guide_qc")),
      nav_panel("Cell states", DTOutput("cell_states"))
    )
  ),
  ),
  nav_menu(
    "Analysis",
  nav_panel(
    "Method Selection",
    card(card_header("Method eligibility"), p("ELIGIBLE means that the test dataset meets the method's basic input rules. It does not mean that the method ran."), DTOutput("method_decisions")),
    card(card_header("Eligibility summary"), plotOutput("method_plot", height = "300px"))
  ),
  nav_panel(
    "Perturbation Effects",
    layout_columns(
      col_widths = c(3, 9),
      card(
        card_header("Filters"),
        uiOutput("effect_filters")
      ),
      card(card_header("Effect table"), DTOutput("effects"))
    ),
    card(card_header("Largest generated effects"), p("Bars show the largest absolute log2 fold changes in the generated test data."), plotOutput("effect_plot", height = "480px"))
  ),
  ),
  nav_menu(
    "Evidence",
  nav_panel(
    "Synthetic Evidence Demo",
    layout_columns(
      col_widths = c(3, 9),
      card(
        card_header("Filters"),
        uiOutput("regulatory_filters")
      ),
      card(card_header("Generated support table"), DTOutput("regulatory_table"))
    ),
    card(card_header("Generated support score"), p("This score tests display and evidence rules. It is not biological validation."), plotOutput("regulatory_plot", height = "420px"))
  ),
  nav_panel(
    "GWAS Corroboration",
    card(
      card_header("Alzheimer disease locus corroboration"),
      p("This table contains a reproducible NHGRI-EBI GWAS Catalog query. YES means that the gene maps to at least one Alzheimer association with p <= 5e-8."),
      p("This supports disease relevance. It does not prove causality, perturbation direction, or microglial specificity."),
      DTOutput("gwas_corroboration")
    )
  ),
  ),
  nav_panel(
    "Limitations & Provenance",
    card(card_header("Interpretation limits"), p("Generated regulatory tables test the evidence model. GWAS Catalog is the only external evidence source analyzed here. The project has not analyzed an external chromatin, QTL, clinical-variant, or independent perturbation matrix.")),
    card(card_header("Provenance"), DTOutput("provenance_table")),
    downloadButton("download_regulatory", "Download displayed support table")
  ),
  nav_panel(
    "Public Dataset Audit",
    layout_columns(
      card(card_header("Public files"), DTOutput("download_manifest")),
      card(card_header("Dataset provenance"), DTOutput("public_provenance"))
    ),
    navset_card_tab(
      nav_panel("GSE207628 matrices", DTOutput("gse207628_summary")),
      nav_panel("GSE207628 probes", DTOutput("gse207628_probes")),
      nav_panel("GSE178317 abundance", DTOutput("gse178317_summary")),
      nav_panel("GSE178317 samples", DTOutput("gse178317_sample_qc")),
      nav_panel("GSE178317 markers", DTOutput("gse178317_markers"))
    ),
    card(
      card_header("Interpretation"),
      p("GSE207628 is treated as a targeted single-cell CRISPRi HYPR-seq dataset. The public matrices support count-depth, feature-panel, and replicate-level audits now."),
      p("The Public Dataset Audit preserves the earlier lightweight discovery tables. The Real Data tab contains the newer matrix-derived QC summaries. Full matrices remain outside the hosted app and are processed through the local or AWS Batch workflow."),
      tags$div(class = "source-link",
        tags$a(href = "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE207628", target = "_blank", "GSE207628"),
        " | ",
        tags$a(href = "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE178317", target = "_blank", "GSE178317")
      )
    )
  ),
  nav_panel(
    "Report",
    card(card_header("Project report"), uiOutput("report_summary"))
  )
)

server <- function(input, output, session) {
  paths <- list(
    dataset_qc = result_path("qc", "dataset_qc.csv"),
    guide_qc = result_path("qc", "guide_qc.csv"),
    cell_states = result_path("qc", "cell_state_summary.csv"),
    method_decisions = result_path("method_selection", "method_decisions.csv"),
    effects = result_path("method", "simple_pseudobulk_effects.csv"),
    regulatory = result_path("regulatory_validation", "regulatory_validation.csv"),
    regulatory_summary = result_path("regulatory_validation", "regulatory_validation_summary.csv"),
    gwas_corroboration = result_path("external_corroboration", "gwas_catalog_ad_corroboration.csv"),
    download_manifest = result_path("real_public", "download_manifest.csv"),
    public_provenance = result_path("real_public", "public_dataset_provenance.csv"),
    gse207628_summary = result_path("real_public", "gse207628_hyprseq_matrix_summary.csv"),
    gse207628_probes = result_path("real_public", "gse207628_hyprseq_probe_panel.csv"),
    gse178317_summary = result_path("real_public", "gse178317_abundance_summary.csv"),
    gse178317_sample_qc = result_path("real_public", "gse178317_sample_qc.csv"),
    gse178317_markers = result_path("real_public", "gse178317_microglia_marker_context.csv"),
    real_dataset_status = result_path("real_data", "real_dataset_status.csv"),
    real_drager_lane_qc = result_path("real_data", "gse178317_lane_qc.csv"),
    real_drager_guide_audit = result_path("real_data", "gse178317_guide_archive_audit.csv"),
    real_drager_state = result_path("real_data", "gse178317_state_baseline.csv"),
    real_hypr_qc = result_path("real_data", "gse207628_cell_qc.csv"),
    real_hypr_baseline = result_path("real_data", "gse207628_targeted_replicate_baseline.csv"),
    real_replogle_qc = result_path("real_data", "replogle_k562_pseudobulk_qc.csv"),
    real_replogle_baseline = result_path("real_data", "replogle_k562_paper_native_baseline.csv"),
    report = result_path("report", "demo_report.md")
  )

  data <- reactive({
    list(
      dataset_qc = read_result(paths$dataset_qc),
      guide_qc = read_result(paths$guide_qc),
      cell_states = read_result(paths$cell_states),
      method_decisions = read_result(paths$method_decisions),
      effects = read_result(paths$effects),
      regulatory = read_result(paths$regulatory),
      regulatory_summary = read_result(paths$regulatory_summary),
      gwas_corroboration = read_result(paths$gwas_corroboration),
      download_manifest = read_result(paths$download_manifest),
      public_provenance = read_result(paths$public_provenance),
      gse207628_summary = read_result(paths$gse207628_summary),
      gse207628_probes = read_result(paths$gse207628_probes),
      gse178317_summary = read_result(paths$gse178317_summary),
      gse178317_sample_qc = read_result(paths$gse178317_sample_qc),
      gse178317_markers = read_result(paths$gse178317_markers),
      real_dataset_status = read_result(paths$real_dataset_status),
      real_drager_lane_qc = read_result(paths$real_drager_lane_qc),
      real_drager_guide_audit = read_result(paths$real_drager_guide_audit),
      real_drager_state = read_result(paths$real_drager_state),
      real_hypr_qc = read_result(paths$real_hypr_qc),
      real_hypr_baseline = read_result(paths$real_hypr_baseline),
      real_replogle_qc = read_result(paths$real_replogle_qc),
      real_replogle_baseline = read_result(paths$real_replogle_baseline)
    )
  })

  lapply(names(term_help), function(label) {
    observeEvent(input[[paste0("help_", gsub("[^A-Za-z0-9]", "_", label))]], {
      showModal(modalDialog(title = label, term_help[[label]], easyClose = TRUE, footer = modalButton("Close")))
    })
  })

  output$dataset_metric <- renderUI({
    x <- data()$dataset_qc
    if (!nrow(x)) return(p("No dataset QC file found."))
    tagList(div(class = "metric", x$n_cells[1]), div(class = "small-note", paste(x$n_perturbations[1] - 1, "perturbations plus control")))
  })

  output$effect_metric <- renderUI({
    x <- read_result(result_path("benchmark", "benchmark_summary.csv"))
    if (!nrow(x)) return(p("No benchmark summary found."))
    tagList(div(class = "metric", x$n_non_neutral_effects[1]), div(class = "small-note", "non-neutral effects"))
  })

  output$gwas_metric <- renderUI({
    x <- data()$gwas_corroboration
    if (!nrow(x)) return(p("No GWAS result found."))
    n <- sum(x$genome_wide_corroboration == "YES")
    tagList(div(class = "metric", n), div(class = "small-note", "genes with genome-wide AD support"))
  })

  datatable_opts <- list(pageLength = 12, scrollX = TRUE, searchHighlight = TRUE)
  output$dataset_qc <- renderDT(datatable(data()$dataset_qc, filter = "top", options = datatable_opts))
  output$dataset_qc_design <- renderDT(datatable(data()$dataset_qc, filter = "top", options = datatable_opts))
  output$guide_qc <- renderDT(datatable(data()$guide_qc, filter = "top", options = datatable_opts))
  output$cell_states <- renderDT(datatable(data()$cell_states, filter = "top", options = datatable_opts))
  method_display <- reactive({
    x <- data()$method_decisions
    x$decision[x$decision == "RUN"] <- "ELIGIBLE"
    x
  })
  output$method_decisions <- renderDT(datatable(method_display(), filter = "top", options = datatable_opts))

  output$method_plot <- renderPlot({
    x <- method_display()
    req(nrow(x))
    ggplot(x, aes(x = decision, fill = decision)) +
      geom_bar(width = 0.65) +
      scale_fill_manual(values = c(ELIGIBLE = "#2f7d5c", INCOMPATIBLE = "#8c9893", FAILED = "#a94442", NOT_AVAILABLE = "#b7791f")) +
      labs(x = NULL, y = "Method routes", title = "Eligibility for the generated 20-gene test dataset") +
      theme_minimal(base_size = 13) +
      theme(legend.position = "none")
  })

  output$effect_filters <- renderUI({
    x <- data()$effects
    req(nrow(x))
    tagList(
      selectInput("effect_perturbation", "Perturbation", c("All", sort(unique(x$perturbation)))),
      selectInput("effect_direction", "Direction", c("All", sort(unique(x$effect_direction))))
    )
  })

  filtered_effects <- reactive({
    x <- data()$effects
    if (!nrow(x)) return(x)
    if (!is.null(input$effect_perturbation) && input$effect_perturbation != "All") x <- x[x$perturbation == input$effect_perturbation, ]
    if (!is.null(input$effect_direction) && input$effect_direction != "All") x <- x[x$effect_direction == input$effect_direction, ]
    x
  })

  output$effects <- renderDT(datatable(filtered_effects(), filter = "top", options = datatable_opts))

  output$effect_plot <- renderPlot({
    x <- filtered_effects()
    req(nrow(x))
    width <- session$clientData$output_effect_plot_width
    mobile <- !is.null(width) && width < 600
    n_show <- if (mobile) 8 else 15
    top <- x[order(abs(as.numeric(x$log2fc)), decreasing = TRUE), ][seq_len(min(n_show, nrow(x))), ]
    ggplot(top, aes(x = reorder(paste(perturbation, gene, sep = " -> "), as.numeric(log2fc)), y = as.numeric(log2fc), fill = effect_direction)) +
      geom_col() +
      coord_flip() +
      scale_fill_manual(values = c(up = "#b7791f", down = "#24506f", neutral = "#9aa6a1")) +
      labs(x = NULL, y = "log2 fold change") +
      theme_minimal(base_size = 14) +
      theme(axis.text.y = element_text(size = 10.5), legend.position = if (mobile) "bottom" else "right")
  })

  output$regulatory_filters <- renderUI({
    x <- data()$regulatory
    req(nrow(x))
    tagList(
      selectInput("reg_status", "Legacy demo support status", c("All", sort(unique(x$regulatory_validation_status)))),
      selectInput("reg_motif", "Motif", c("All", sort(unique(x$best_microglia_motif[x$best_microglia_motif != ""]))))
    )
  })

  filtered_regulatory <- reactive({
    x <- data()$regulatory
    if (!nrow(x)) return(x)
    if (!is.null(input$reg_status) && input$reg_status != "All") x <- x[x$regulatory_validation_status == input$reg_status, ]
    if (!is.null(input$reg_motif) && input$reg_motif != "All") x <- x[x$best_microglia_motif == input$reg_motif, ]
    x
  })

  output$regulatory_table <- renderDT(datatable(filtered_regulatory(), filter = "top", options = datatable_opts))
  output$gwas_corroboration <- renderDT(datatable(data()$gwas_corroboration, filter = "top", options = datatable_opts))
  output$download_manifest <- renderDT(datatable(data()$download_manifest, filter = "top", options = datatable_opts))
  output$public_provenance <- renderDT(datatable(data()$public_provenance, filter = "top", options = datatable_opts))
  output$provenance_table <- renderDT(datatable(data()$public_provenance, filter = "top", options = datatable_opts))
  output$gse207628_summary <- renderDT(datatable(data()$gse207628_summary, filter = "top", options = datatable_opts))
  output$gse207628_probes <- renderDT(datatable(data()$gse207628_probes, filter = "top", options = datatable_opts))
  output$gse178317_summary <- renderDT(datatable(data()$gse178317_summary, filter = "top", options = datatable_opts))
  output$gse178317_sample_qc <- renderDT(datatable(data()$gse178317_sample_qc, filter = "top", options = datatable_opts))
  output$gse178317_markers <- renderDT(datatable(data()$gse178317_markers, filter = "top", options = datatable_opts))
  output$real_dataset_status <- renderDT(datatable(data()$real_dataset_status, filter = "top", options = datatable_opts))
  output$real_drager_lane_qc <- renderDT(datatable(data()$real_drager_lane_qc, filter = "top", options = datatable_opts))
  output$real_drager_guide_audit <- renderDT(datatable(data()$real_drager_guide_audit, filter = "top", options = datatable_opts))
  output$real_drager_state <- renderDT(datatable(data()$real_drager_state, filter = "top", options = datatable_opts))
  output$real_hypr_qc <- renderDT(datatable(data()$real_hypr_qc, filter = "top", options = datatable_opts))
  output$real_hypr_baseline <- renderDT(datatable(data()$real_hypr_baseline, filter = "top", options = datatable_opts))
  output$real_replogle_qc <- renderDT(datatable(data()$real_replogle_qc, filter = "top", options = datatable_opts))
  output$real_replogle_baseline <- renderDT(datatable(data()$real_replogle_baseline, filter = "top", options = datatable_opts))

  output$regulatory_plot <- renderPlot({
    x <- filtered_regulatory()
    req(nrow(x))
    width <- session$clientData$output_regulatory_plot_width
    mobile <- !is.null(width) && width < 600
    if (mobile && nrow(x) > 8) x <- x[order(x$regulatory_validation_score, decreasing = TRUE), ][seq_len(8), ]
    ggplot(x, aes(x = reorder(paste(perturbation, gene, sep = " -> "), regulatory_validation_score), y = regulatory_validation_score, fill = regulatory_validation_status)) +
      geom_col() +
      coord_flip() +
      scale_fill_manual(values = c(PASS = "#2f7d5c", WARN = "#b7791f", LOW_SUPPORT = "#9aa6a1")) +
      labs(x = NULL, y = "Generated support score", title = "Evidence-rule software test") +
      theme_minimal(base_size = 14) +
      theme(axis.text.y = element_text(size = 10.5), legend.position = if (mobile) "bottom" else "right")
  })

  output$download_regulatory <- downloadHandler(
    filename = function() "regulatory_support_display.csv",
    content = function(file) write.csv(filtered_regulatory(), file, row.names = FALSE)
  )

  output$report_summary <- renderUI({
    benchmark <- read_result(result_path("benchmark", "benchmark_summary.csv"))
    gwas <- data()$gwas_corroboration
    supported <- paste(gwas$gene[gwas$genome_wide_corroboration == "YES"], collapse = ", ")
    tagList(
      h4("Scope"),
      tags$ul(class = "report-list",
        tags$li("Three public datasets were processed. One generated dataset tests the workflow."),
        tags$li("Paper-native summaries and a transparent pseudobulk baseline produced results."),
        tags$li("The two microglia deposits lack cell-to-guide assignments. Their results are QC summaries, not perturbation effects.")
      ),
      h4("Generated benchmark"),
      tags$ul(class = "report-list",
        tags$li(paste(benchmark$n_effects[1], "perturbation-gene pairs were tested.")),
        tags$li(paste(benchmark$n_non_neutral_effects[1], "pairs were non-neutral across 11 response genes.")),
        tags$li("These values test expected software behavior. They are not biological discoveries.")
      ),
      h4("Disease corroboration"),
      tags$ul(class = "report-list",
        tags$li(paste("GWAS Catalog supports Alzheimer disease relevance for", supported, "at p <= 5e-8.")),
        tags$li("GWAS overlap does not prove the causal gene or validate perturbation direction.")
      ),
      h4("Next analysis"),
      p("Obtain guide-resolved microglia data. Then compare compatible methods with shared contrasts, replicate-aware models, and prespecified error control.")
    )
  })
}

shinyApp(ui, server)
