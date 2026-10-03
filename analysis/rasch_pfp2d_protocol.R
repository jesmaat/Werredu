# rasch_pfp2d_protocol.R  (edu-revision)
# ------------------------------------------------------------------
# Paired comparison of the 2-D PFP protocol (alpha = 0, 0.5, 1.0, 1.5)
# with every arm of the primary simulation (Saturn, Factory, CAT, 1-D PFP).
# All arms share the same simulated learners and response draws.
# Base R only. Run from the repository root:
#   Rscript analysis/rasch_pfp2d_protocol.R
# Inputs : data/edu_revision/rasch_students.csv, rasch_pfp2d_students.csv
# Outputs: data/edu_revision/r_pfp2d_means.csv, r_pfp2d_contrasts.csv, r_pfp2d_report.txt
# ------------------------------------------------------------------
set.seed(42)
dir <- file.path("data", "edu_revision")
base <- read.csv(file.path(dir, "rasch_students.csv"),       stringsAsFactors = FALSE)
p2d  <- read.csv(file.path(dir, "rasch_pfp2d_students.csv"), stringsAsFactors = FALSE)
metrics <- c("zpd", "zpd_40_60", "zpd_60_80", "zpd_40_70", "bored", "frustr", "mean_p", "gain", "track")
boot_ci <- function(x, B = 2000) unname(quantile(replicate(B, mean(sample(x, replace = TRUE))), c(.025, .975)))
out <- character(); say <- function(...) { l <- paste0(...); out <<- c(out, l); cat(l, "\n") }

p2d$arm <- paste0("PFP2D_a", p2d$alpha)
all <- rbind(base[, c("rule", "arm", "student", metrics)], p2d[, c("rule", "arm", "student", metrics)])
arms <- c("Saturn", "Factory", "CAT", "PFP", paste0("PFP2D_a", c(0, 0.5, 1, 1.5)))

means <- aggregate(all[, metrics], by = list(rule = all$rule, arm = all$arm), FUN = mean)
means <- means[order(means$rule, match(means$arm, arms)), ]
write.csv(means, file.path(dir, "r_pfp2d_means.csv"), row.names = FALSE)

con <- list()
for (rule in unique(all$rule)) for (a2 in paste0("PFP2D_a", c(0, 0.5, 1, 1.5))) {
  x <- all[all$rule == rule & all$arm == a2, ]
  for (ref in c("Saturn", "Factory", "CAT", "PFP")) {
    r <- all[all$rule == rule & all$arm == ref, ]
    stopifnot(identical(x$student, r$student))
    for (m in metrics) {
      d <- x[[m]] - r[[m]]; ci <- boot_ci(d)
      con[[length(con) + 1]] <- data.frame(rule = rule, arm = a2, reference = ref, metric = m,
        diff = mean(d), ci_low = ci[1], ci_high = ci[2], d_z = if (sd(d) > 0) mean(d) / sd(d) else NA)
    }
  }
}
con <- do.call(rbind, con)
write.csv(con, file.path(dir, "r_pfp2d_contrasts.csv"), row.names = FALSE)

for (rule in unique(all$rule)) {
  say("==== rule: ", rule, " -- arm means ====")
  mm <- means[means$rule == rule, ]
  say(sprintf("%-12s %s", "arm", paste(sprintf("%9s", metrics), collapse = "")))
  for (i in seq_len(nrow(mm))) say(sprintf("%-12s %s", mm$arm[i], paste(sprintf("%9.3f", unlist(mm[i, metrics])), collapse = "")))
  say("-- 2-D PFP (alpha = 1.0) minus reference, paired:")
  cc <- con[con$rule == rule & con$arm == "PFP2D_a1" & con$metric %in% c("zpd", "zpd_40_60", "gain", "frustr", "bored", "track"), ]
  for (i in seq_len(nrow(cc))) say(sprintf("  vs %-8s %-9s %+.3f [%+.3f, %+.3f] d_z=%+.2f",
                                           cc$reference[i], cc$metric[i], cc$diff[i], cc$ci_low[i], cc$ci_high[i], cc$d_z[i]))
  say("")
}
writeLines(out, file.path(dir, "r_pfp2d_report.txt"))
