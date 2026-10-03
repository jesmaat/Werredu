# rasch_pfp2d_isolated.R  (edu-revision)
# ------------------------------------------------------------------
# Inference for sim/rasch_pfp2d_isolated.py (single-variable 2-D protocol).
# Base R only. Run from the repository root:
#   Rscript analysis/rasch_pfp2d_isolated.R
# Inputs : data/edu_revision/rasch_students.csv, rasch_pfp2d_iso_students.csv
# Outputs: data/edu_revision/r_iso_means.csv, r_iso_contrasts.csv, r_iso_report.txt
# Key contrasts (paired, same learners and response draws):
#   2D a=0  vs 1-D PFP  -> effect of the jump rule alone
#   2D a>0  vs 2D a=0   -> effect of the Mandelbrot term
#   2D a    vs Saturn / Factory / CAT
# ------------------------------------------------------------------
set.seed(42)
dir <- file.path("data", "edu_revision")
base <- read.csv(file.path(dir, "rasch_students.csv"),          stringsAsFactors = FALSE)
iso  <- read.csv(file.path(dir, "rasch_pfp2d_iso_students.csv"), stringsAsFactors = FALSE)
metrics <- c("zpd", "zpd_40_60", "zpd_60_80", "zpd_40_70", "bored", "frustr", "mean_p", "gain", "track")
boot_ci <- function(x, B = 2000) unname(quantile(replicate(B, mean(sample(x, replace = TRUE))), c(.025, .975)))
out <- character(); say <- function(...) { l <- paste0(...); out <<- c(out, l); cat(l, "\n") }

iso$arm <- paste0("2D_a", iso$alpha)
all  <- rbind(base[, c("rule", "arm", "student", metrics)], iso[, c("rule", "arm", "student", metrics)])
arms <- c("Saturn", "Factory", "CAT", "PFP", paste0("2D_a", c(0, 0.5, 1, 1.5)))
means <- aggregate(all[, metrics], by = list(rule = all$rule, arm = all$arm), FUN = mean)
means <- means[order(means$rule, match(means$arm, arms)), ]
write.csv(means, file.path(dir, "r_iso_means.csv"), row.names = FALSE)

pairs <- rbind(
  data.frame(arm = "2D_a0", ref = "PFP"),
  data.frame(arm = paste0("2D_a", c(0.5, 1, 1.5)), ref = "2D_a0"),
  expand.grid(arm = paste0("2D_a", c(0, 0.5, 1, 1.5)), ref = c("Saturn", "Factory", "CAT"), stringsAsFactors = FALSE))
con <- list()
for (rule in unique(all$rule)) for (k in seq_len(nrow(pairs))) {
  x <- all[all$rule == rule & all$arm == pairs$arm[k], ]; r <- all[all$rule == rule & all$arm == pairs$ref[k], ]
  stopifnot(identical(x$student, r$student))
  for (m in metrics) {
    d <- x[[m]] - r[[m]]; ci <- boot_ci(d)
    con[[length(con) + 1]] <- data.frame(rule = rule, arm = pairs$arm[k], reference = pairs$ref[k], metric = m,
      diff = mean(d), ci_low = ci[1], ci_high = ci[2], d_z = if (sd(d) > 0) mean(d) / sd(d) else NA)
  }
}
con <- do.call(rbind, con)
write.csv(con, file.path(dir, "r_iso_contrasts.csv"), row.names = FALSE)

show <- c("zpd", "zpd_40_60", "gain", "frustr", "bored", "track")
for (rule in unique(all$rule)) {
  say("==== rule: ", rule, " ====")
  mm <- means[means$rule == rule, ]
  say(sprintf("%-8s %s", "arm", paste(sprintf("%10s", metrics), collapse = "")))
  for (i in seq_len(nrow(mm))) say(sprintf("%-8s %s", mm$arm[i], paste(sprintf("%10.3f", unlist(mm[i, metrics])), collapse = "")))
  for (lab in list(c("2D_a0", "PFP", "Jump rule alone (2D a=0 minus 1-D PFP)"),
                   c("2D_a1", "2D_a0", "Mandelbrot term (2D a=1 minus 2D a=0)"),
                   c("2D_a0.5", "2D_a0", "Mandelbrot term (2D a=0.5 minus 2D a=0)"),
                   c("2D_a1", "CAT", "2D a=1 minus CAT"))) {
    cc <- con[con$rule == rule & con$arm == lab[1] & con$reference == lab[2] & con$metric %in% show, ]
    say("-- ", lab[3])
    for (i in seq_len(nrow(cc))) say(sprintf("   %-9s %+.3f [%+.3f, %+.3f] d_z=%+.2f", cc$metric[i], cc$diff[i], cc$ci_low[i], cc$ci_high[i], cc$d_z[i]))
  }
  say("")
}
writeLines(out, file.path(dir, "r_iso_report.txt"))
