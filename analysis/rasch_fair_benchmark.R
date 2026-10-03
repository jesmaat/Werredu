# rasch_fair_benchmark.R  (edu-revision)
# ------------------------------------------------------------------
# Inference for sim/rasch_fair_benchmark.py. Base R only.
# Run from the repository root:  Rscript analysis/rasch_fair_benchmark.R
# Inputs : data/edu_revision/rasch_students.csv, rasch_grid.csv
# Outputs: data/edu_revision/r_rasch_arm_means.csv
#          data/edu_revision/r_rasch_pfp_contrasts.csv
#          data/edu_revision/r_rasch_grid_summary.csv
#          data/edu_revision/r_rasch_report.txt
# Comparisons are paired by student (common random numbers: same theta_0
# and same response draws in every arm).  Effect size: d_z = mean(diff)/sd(diff).
# Multiple comparisons: Holm correction within each learning rule.
# ------------------------------------------------------------------
set.seed(42)
dir_in <- file.path("data", "edu_revision")
s  <- read.csv(file.path(dir_in, "rasch_students.csv"), stringsAsFactors = FALSE)
g  <- read.csv(file.path(dir_in, "rasch_grid.csv"),     stringsAsFactors = FALSE)
metrics <- c("zpd", "zpd_40_60", "zpd_60_80", "zpd_40_80", "zpd_40_70", "bored", "frustr", "mean_p", "gain", "track")
arms    <- c("Saturn", "Factory", "CAT_50", "CAT_70", "CAT_85", "CAT", "PFP")
out <- character(); say <- function(...) { l <- paste0(...); out <<- c(out, l); cat(l, "\n") }

boot_ci <- function(x, B = 2000) unname(quantile(replicate(B, mean(sample(x, replace = TRUE))), c(.025, .975)))

# 1. Arm means with 95% bootstrap CI (student level)
means <- list()
for (rule in unique(s$rule)) for (arm in arms) for (m in metrics) {
  x  <- s[s$rule == rule & s$arm == arm, m]
  ci <- boot_ci(x)
  means[[length(means) + 1]] <- data.frame(rule = rule, arm = arm, metric = m, mean = mean(x),
                                           ci_low = ci[1], ci_high = ci[2])
}
means <- do.call(rbind, means)
write.csv(means, file.path(dir_in, "r_rasch_arm_means.csv"), row.names = FALSE)

# 2. PFP vs each other arm, paired by student
con <- list()
for (rule in unique(s$rule)) {
  base <- s[s$rule == rule & s$arm == "PFP", ]
  for (arm in setdiff(arms, "PFP")) {
    other <- s[s$rule == rule & s$arm == arm, ]
    stopifnot(identical(base$student, other$student))
    for (m in metrics) {
      d  <- base[[m]] - other[[m]]
      ci <- boot_ci(d)
      wt <- suppressWarnings(wilcox.test(d, mu = 0, exact = FALSE))
      con[[length(con) + 1]] <- data.frame(rule = rule, comparison = paste0("PFP - ", arm), metric = m,
        mean_diff = mean(d), ci_low = ci[1], ci_high = ci[2],
        d_z = if (sd(d) > 0) mean(d) / sd(d) else NA, wilcoxon_p = wt$p.value)
    }
  }
}
con <- do.call(rbind, con)
con$p_holm <- ave(con$wilcoxon_p, con$rule, FUN = function(p) p.adjust(p, "holm"))
write.csv(con, file.path(dir_in, "r_rasch_pfp_contrasts.csv"), row.names = FALSE)

# 3. Grid: every setting, mean over seeds
gs <- aggregate(g[, metrics], by = list(rule = g$rule, arm = g$arm, setting = g$setting), FUN = mean)
write.csv(gs, file.path(dir_in, "r_rasch_grid_summary.csv"), row.names = FALSE)

# 4. Report
for (rule in unique(s$rule)) {
  say("==== learning rule: ", rule, " (primary settings, N = ", sum(s$rule == rule & s$arm == "PFP"), " per arm) ====")
  for (m in c("zpd", "zpd_40_60", "zpd_60_80", "zpd_40_70", "mean_p", "gain", "frustr", "bored", "track")) {
    mm <- means[means$rule == rule & means$metric == m, ]
    say(sprintf("%-10s %s", m, paste(sprintf("%s %.3f [%.3f, %.3f]", mm$arm, mm$mean, mm$ci_low, mm$ci_high), collapse = " | ")))
  }
  say("PFP contrasts (mean diff, 95% CI, d_z, Holm p):")
  cc <- con[con$rule == rule & con$metric %in% c("zpd", "gain", "frustr", "track"), ]
  for (i in seq_len(nrow(cc))) say(sprintf("  %-18s %-7s %+.3f [%+.3f, %+.3f]  d_z = %+.2f  p_holm = %.3g",
                                           cc$comparison[i], cc$metric[i], cc$mean_diff[i], cc$ci_low[i],
                                           cc$ci_high[i], cc$d_z[i], cc$p_holm[i]))
  best <- function(arm) { x <- gs[gs$rule == rule & gs$arm == arm, ]; x[which.max(x$zpd), ] }
  bp <- best("PFP"); bc <- best("CAT")
  say(sprintf("Best grid cell by zpd: PFP %s zpd = %.3f | CAT %s zpd = %.3f", bp$setting, bp$zpd, bc$setting, bc$zpd))
  say("")
}
writeLines(out, file.path(dir_in, "r_rasch_report.txt"))
