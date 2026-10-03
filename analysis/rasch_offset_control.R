# rasch_offset_control.R  (edu-revision)
# ------------------------------------------------------------------
# Is the Mandelbrot term more than a constant difficulty shift?
# Paired comparison 2D alpha = 1 vs 2D_offset (same learners, same draws).
# Pre-specified criteria (Volkan Dagli, 2026-09-29): alpha = 1 is superior if
#   (i) per-learner SD of |b - theta| is lower, or (ii) share of P in [0.40, 0.60]
#   is higher, or (iii) Rule 2 ability gain is higher.
# A criterion counts as met only if the 95% bootstrap CI of the paired
# difference excludes 0 in the favourable direction.
# Base R only. Run from the repository root: Rscript analysis/rasch_offset_control.R
# Input : data/edu_revision/rasch_offset_students.csv, rasch_offset_meta.csv
# Output: data/edu_revision/r_offset_contrasts.csv, r_offset_report.txt
# ------------------------------------------------------------------
set.seed(42)
dir  <- file.path("data", "edu_revision")
d    <- read.csv(file.path(dir, "rasch_offset_students.csv"), stringsAsFactors = FALSE)
meta <- read.csv(file.path(dir, "rasch_offset_meta.csv"),     stringsAsFactors = FALSE)
metrics <- c("zpd", "zpd_40_60", "zpd_60_80", "bored", "frustr", "mean_p", "gain", "track", "track_sd")
boot_ci <- function(x, B = 2000) unname(quantile(replicate(B, mean(sample(x, replace = TRUE))), c(.025, .975)))
out <- character(); say <- function(...) { l <- paste0(...); out <<- c(out, l); cat(l, "\n") }

res <- list()
for (rule in unique(d$rule)) for (cmp in list(c("2D_a1", "2D_offset"), c("2D_offset", "2D_a0"), c("2D_a1", "2D_a0"))) {
  a <- d[d$rule == rule & d$arm == cmp[1], ]; b <- d[d$rule == rule & d$arm == cmp[2], ]
  stopifnot(identical(a$student, b$student))
  for (m in metrics) {
    x <- a[[m]] - b[[m]]; ci <- boot_ci(x)
    res[[length(res) + 1]] <- data.frame(rule = rule, comparison = paste(cmp, collapse = " - "), metric = m,
      mean_first = mean(a[[m]]), mean_second = mean(b[[m]]), diff = mean(x), ci_low = ci[1], ci_high = ci[2],
      d_z = if (sd(x) > 0) mean(x) / sd(x) else NA)
  }
}
res <- do.call(rbind, res)
write.csv(res, file.path(dir, "r_offset_contrasts.csv"), row.names = FALSE)

for (rule in unique(d$rule)) {
  say("==== rule: ", rule, "  (Delta_b_static = ", sprintf("%.4f", meta$delta_b_static[meta$rule == rule]), ") ====")
  for (cmp in unique(res$comparison)) {
    say("-- ", cmp)
    x <- res[res$rule == rule & res$comparison == cmp, ]
    for (i in seq_len(nrow(x))) say(sprintf("   %-9s %.3f vs %.3f  diff %+.3f [%+.3f, %+.3f] d_z=%+.2f",
      x$metric[i], x$mean_first[i], x$mean_second[i], x$diff[i], x$ci_low[i], x$ci_high[i], x$d_z[i]))
  }
  say("")
}
k <- res[res$comparison == "2D_a1 - 2D_offset", ]
crit <- data.frame(
  criterion = c("(i) lower SD of |b-theta|, Rule 1", "(i) lower SD of |b-theta|, Rule 2",
                "(ii) more time in P 0.40-0.60, Rule 1", "(ii) more time in P 0.40-0.60, Rule 2",
                "(iii) higher Rule 2 ability gain"),
  met = c(k$ci_high[k$rule == "volkan" & k$metric == "track_sd"] < 0,
          k$ci_high[k$rule == "difficulty" & k$metric == "track_sd"] < 0,
          k$ci_low[k$rule == "volkan" & k$metric == "zpd_40_60"] > 0,
          k$ci_low[k$rule == "difficulty" & k$metric == "zpd_40_60"] > 0,
          k$ci_low[k$rule == "difficulty" & k$metric == "gain"] > 0))
say("==== Pre-specified criteria: 2D alpha = 1 superior to 2D_offset? ====")
for (i in seq_len(nrow(crit))) say(sprintf("   %-40s %s", crit$criterion[i], ifelse(crit$met[i], "MET", "not met")))
writeLines(out, file.path(dir, "r_offset_report.txt"))
