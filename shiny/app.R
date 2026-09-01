library(shiny)
library(bslib)
library(DT)
library(ggplot2)

read_result <- function(path) {
  if (file.exists(path)) read.csv(path, stringsAsFactors = FALSE, check.names = FALSE) else data.frame()
}

term_help <- list(
  "MOI" = "Multiplicity of infection. In this benchmark it is approximated from guide count per cell and guide collision rate.",
  "guide collision rate" = "Fraction of cells with more than one guide. High collision rates can confound single-perturbation interpretation.",
  "pseudobulk" = "Aggregation of cells within perturbation or replicate groups before differential testing or effect estimation.",
  "regulatory validation" = "Comparison of perturbation hits against chromatin accessibility, peak-to-gene, motif, and disease-locus evidence.",
  "LOW_SUPPORT" = "The current regulatory resources do not provide strong support for the hit. This is not evidence that the perturbation result is false."
)

help_button <- function(label) {
  actionLink(paste0("help_", gsub("[^A-Za-z0-9]", "_", label)), label)
}

ui <- page_navbar(
  title = "PerturbSeq Benchmarking",
  theme = bs_theme(version = 5, bootswatch = "flatly", primary = "#24506f", secondary = "#6c7a89", success = "#2f7d5c", warning = "#b7791f", danger = "#a94442"),
  header = tags$style(HTML("
    body { background: #f7faf9; color: #17201d; }
    .card { border-radius: 8px; border: 1px solid #d8e3df; box-shadow: none; }
    .navbar { border-bottom: 1px solid #d8e3df; }
    .metric { font-size: 1.5rem; font-weight: 700; color: #17384f; }
    .small-note { color: #51615c; font-size: 0.92rem; }
    .plot-card { min-height: 420px; }
  ")),
  nav_panel(
    "Overview",
    layout_columns(
      card(card_header("Dataset"), uiOutput("dataset_metric")),
      card(card_header("Effects"), uiOutput("effect_metric")),
      card(card_header("Regulatory validation"), uiOutput("regulatory_metric"))
    ),
    card(
      card_header("Analysis summary"),
      p("This browser displays generated benchmark outputs. Run the Nextflow workflow before using it for real datasets."),
      p(help_button("MOI"), " and ", help_button("regulatory validation"), " are explained through clickable terms.")
    )
  ),
  nav_panel(
    "Dataset QC",
    navset_card_tab(
      nav_panel("Dataset profile", DTOutput("dataset_qc")),
      nav_panel("Guide QC", DTOutput("guide_qc")),
      nav_panel("Cell states", DTOutput("cell_states"))
    )
  ),
  nav_panel(
    "Method Selection",
    card(card_header("Dataset-aware method decisions"), DTOutput("method_decisions")),
    card(card_header("Method selection plot"), plotOutput("method_plot", height = "360px"))
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
    card(card_header("Effect-size plot"), plotOutput("effect_plot", height = "420px"))
  ),
  nav_panel(
    "Regulatory Validation",
    layout_columns(
      col_widths = c(3, 9),
      card(
        card_header("Filters"),
        uiOutput("regulatory_filters")
      ),
      card(card_header("Validation table"), DTOutput("regulatory_table"))
    ),
    card(card_header("Validation score plot"), plotOutput("regulatory_plot", height = "420px"))
  ),
  nav_panel(
    "Report",
    card(card_header("Generated report"), verbatimTextOutput("report_text"))
  )
)

server <- function(input, output, session) {
  paths <- list(
    dataset_qc = "../results/qc/dataset_qc.csv",
    guide_qc = "../results/qc/guide_qc.csv",
    cell_states = "../results/qc/cell_state_summary.csv",
    method_decisions = "../results/method_selection/method_decisions.csv",
    effects = "../results/method/simple_pseudobulk_effects.csv",
    regulatory = "../results/regulatory_validation/regulatory_validation.csv",
    regulatory_summary = "../results/regulatory_validation/regulatory_validation_summary.csv",
    report = "../results/report/demo_report.md"
  )

  data <- reactive({
    list(
      dataset_qc = read_result(paths$dataset_qc),
      guide_qc = read_result(paths$guide_qc),
      cell_states = read_result(paths$cell_states),
      method_decisions = read_result(paths$method_decisions),
      effects = read_result(paths$effects),
      regulatory = read_result(paths$regulatory),
      regulatory_summary = read_result(paths$regulatory_summary)
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
    tagList(div(class = "metric", x$n_cells[1]), div(class = "small-note", paste(x$n_perturbations[1], "perturbations")))
  })

  output$effect_metric <- renderUI({
    x <- read_result("../results/benchmark/benchmark_summary.csv")
    if (!nrow(x)) return(p("No benchmark summary found."))
    tagList(div(class = "metric", x$n_non_neutral_effects[1]), div(class = "small-note", "non-neutral effects"))
  })

  output$regulatory_metric <- renderUI({
    x <- data()$regulatory_summary
    if (!nrow(x)) return(p("No regulatory validation summary found."))
    tagList(div(class = "metric", x$n_pass[1]), div(class = "small-note", "validated hits"))
  })

  datatable_opts <- list(pageLength = 12, scrollX = TRUE, searchHighlight = TRUE)
  output$dataset_qc <- renderDT(datatable(data()$dataset_qc, filter = "top", options = datatable_opts))
  output$guide_qc <- renderDT(datatable(data()$guide_qc, filter = "top", options = datatable_opts))
  output$cell_states <- renderDT(datatable(data()$cell_states, filter = "top", options = datatable_opts))
  output$method_decisions <- renderDT(datatable(data()$method_decisions, filter = "top", options = datatable_opts))

  output$method_plot <- renderPlot({
    x <- data()$method_decisions
    req(nrow(x))
    ggplot(x, aes(x = decision, fill = decision)) +
      geom_bar(width = 0.65) +
      scale_fill_manual(values = c(RUN = "#2f7d5c", SKIP = "#9aa6a1")) +
      labs(x = NULL, y = "Methods", title = "Dataset-aware method routing") +
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
    top <- x[order(abs(as.numeric(x$log2fc)), decreasing = TRUE), ][seq_len(min(25, nrow(x))), ]
    ggplot(top, aes(x = reorder(paste(perturbation, gene, sep = " -> "), as.numeric(log2fc)), y = as.numeric(log2fc), fill = effect_direction)) +
      geom_col() +
      coord_flip() +
      scale_fill_manual(values = c(up = "#b7791f", down = "#24506f", neutral = "#9aa6a1")) +
      labs(x = NULL, y = "log2 fold change", title = "Top perturbation effects") +
      theme_minimal(base_size = 13)
  })

  output$regulatory_filters <- renderUI({
    x <- data()$regulatory
    req(nrow(x))
    tagList(
      selectInput("reg_status", "Validation status", c("All", sort(unique(x$regulatory_validation_status)))),
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

  output$regulatory_plot <- renderPlot({
    x <- filtered_regulatory()
    req(nrow(x))
    ggplot(x, aes(x = reorder(paste(perturbation, gene, sep = " -> "), regulatory_validation_score), y = regulatory_validation_score, fill = regulatory_validation_status)) +
      geom_col() +
      coord_flip() +
      scale_fill_manual(values = c(PASS = "#2f7d5c", WARN = "#b7791f", LOW_SUPPORT = "#9aa6a1")) +
      labs(x = NULL, y = "Validation score", title = "Chromatin-supported perturbation effects") +
      theme_minimal(base_size = 13)
  })

  output$report_text <- renderText({
    if (!file.exists(paths$report)) return("No report file found.")
    paste(readLines(paths$report, warn = FALSE), collapse = "\n")
  })
}

shinyApp(ui, server)

