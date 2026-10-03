# rasch_ablation_mandelbrot.R  (edu-revision)
# ------------------------------------------------------------------
# Paired comparison of Mandelbrot PFP (alpha = 0.5, 1.0, 1.5) against plain
# PFP (alpha = 0) on the same simulated learners. Base R only.
# Run from the repository root:  Rscript analysis/rasch_ablation_mandelbrot.R
# Input : data/edu_revision/rasch_ablation_students.csv
# Output: data/edu_revision/r_ablation_contrasts.csv, r_ablation_report.txt
# ------------------------------------------------------------------
set.seed(42)
d  <- read.csv(file.path("data", "edu_revision", "rasch_ablation_students.csv"), stringsAsFactors = FALSE)
metrics <- c("zpd", "zpd_40_60", "zpd_60_80", "zpd_40_70", "bored", "frustr", "mean_p", "gain", "track")
boot_ci <- function(x, B = 2000) unname(quantile(replicate(B, mean(sample(x, replace = TRUE))), c(.025, .975)))
out <- character(); say <- function(...) { l <- paste0(...); out <<- c(out, l); cat(l, "\n") }

res <- list()
for (rule in unique(d$rule)) {
  base <- d[d$rule == rule & d$alpha == 0, ]
  for (a in setdiff(sort(unique(d$alpha)), 0)) {
    m_ <- d[d$rule == rule & d$alpha == a, ]
    stopifnot(identical(base$student, m_$student))
    for (m in metrics) {
      diff <- m_[[m]] - base[[m]]; ci <- boot_ci(diff)
      res[[length(res) + 1]] <- data.frame(rule = rule, alpha = a, metric = m,
        plain = mean(base[[m]]), mandelbrot = mean(m_[[m]]), diff = mean(diff),
        ci_low = ci[1], ci_high = ci[2], d_z = if (sd(diff) > 0) mean(diff) / sd(diff) else NA)
    }
  }
}
res <- do.call(rbind, res)
write.csv(res, file.path("data", "edu_revision", "r_ablation_contrasts.csv"), row.names = FALSE)

for (rule in unique(res$rule)) {
  say("==== rule: ", rule, " -- Mandelbrot PFP minus plain PFP (paired, 95% bootstrap CI) ====")
  for (m in c("zpd", "zpd_40_60", "gain", "frustr", "bored", "track")) {
    x <- res[res$rule == rule & res$metric == m, ]
    say(sprintf("%-10s plain %.3f | %s", m, x$plain[1],
                paste(sprintf("a=%.1f: %+.3f [%+.3f, %+.3f] d_z=%+.2f", x$alpha, x$diff, x$ci_low, x$ci_high, x$d_z), collapse = " | ")))
  }
  say("")
}
writeLines(out, file.path("data", "edu_revision", "r_ablation_report.txt"))
