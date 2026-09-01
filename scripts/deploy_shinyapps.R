app_dir <- normalizePath("shiny", mustWork = TRUE)

rsconnect::deployApp(
  appDir = app_dir,
  appName = "PerturbSeq_Benchmarking",
  appTitle = "PerturbSeq Benchmarking",
  forceUpdate = TRUE
)
