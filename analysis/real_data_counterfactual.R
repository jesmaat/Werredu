# real_data_counterfactual.R  (edu-revision)
# ------------------------------------------------------------------
# Inferential statistics and ZPD-band sensitivity analysis for the
# counterfactual demonstration produced by
#   sim/process_real_student_datasets.py
# Base R only (no packages). Run from the repository root:
#   Rscript analysis/real_data_counterfactual.R
# Inputs : data/edu_revision/real_counterfactual_students.csv
#          data/edu_revision/real_counterfactual_steps.csv
# Outputs: data/edu_revision/r_real_tests.csv
#          data/edu_revision/r_real_zpd_sensitivity.csv
#          data/edu_revision/r_real_report.txt
# ------------------------------------------------------------------

set.seed(42)
dir_in  <- file.path("data", "edu_revision")
stu     <- read.csv(file.path(dir_in, "real_counterfactual_students.csv"), stringsAsFactors = FALSE)
steps   <- read.csv(file.path(dir_in, "real_counterfactual_steps.csv"),    stringsAsFactors = FALSE)
stu     <- stu[stu$variant == "revised", ]
steps   <- steps[steps$variant == "revised", ]
out     <- character()
say     <- function(...) { line <- paste0(...); out <<- c(out, line); cat(line, "\n") }

boot_ci <- function(x, B = 5000) {
  m <- replicate(B, mean(sample(x, replace = TRUE)))
  unname(quantile(m, c(.025, .975)))
}

tests <- list()
for (ds in c("ASSISTments", "OULAD")) {
  d <- stu[stu$dataset == ds, ]
  say("== ", ds, " (n = ", nrow(d), ") ==")

  # 1. Operational 'ZPD' ratio: PFP vs unconstrained (paired)
  diff <- d$p_zpd_ratio - d$u_zpd_ratio
  ci   <- boot_ci(diff)
  wt   <- suppressWarnings(wilcox.test(d$p_zpd_ratio, d$u_zpd_ratio, paired = TRUE, exact = FALSE))
  say(sprintf("ZPD ratio: unconstrained mean = %.4f, PFP mean = %.4f, PFP SD = %.4f",
              mean(d$u_zpd_ratio), mean(d$p_zpd_ratio), sd(d$p_zpd_ratio)))
  say(sprintf("  paired mean difference = %.4f, bootstrap 95%% CI [%.4f, %.4f], Wilcoxon V = %.1f, p = %.3g",
              mean(diff), ci[1], ci[2], unname(wt$statistic), wt$p.value))

  # 2. Escape (|z| > 2): McNemar on paired binary outcome
  tab <- table(factor(d$u_escaped, 0:1), factor(d$p_escaped, 0:1))
  mc  <- mcnemar.test(tab)
  say(sprintf("Escape: unconstrained = %.3f, PFP = %.3f, McNemar chi2 = %.2f, p = %.3g",
              mean(d$u_escaped), mean(d$p_escaped), unname(mc$statistic), mc$p.value))

  tests[[length(tests) + 1]] <- data.frame(
    dataset = ds, n = nrow(d),
    u_zpd_mean = mean(d$u_zpd_ratio), p_zpd_mean = mean(d$p_zpd_ratio),
    zpd_diff = mean(diff), zpd_diff_ci_low = ci[1], zpd_diff_ci_high = ci[2],
    wilcoxon_p = wt$p.value,
    u_escape = mean(d$u_escaped), p_escape = mean(d$p_escaped),
    mcnemar_chi2 = unname(mc$statistic), mcnemar_p = mc$p.value)

  # 3. Where does the PFP arm end up?  |z| at the last step
  last <- steps[steps$dataset == ds & steps$step == max(steps$step), ]
  say(sprintf("PFP |z| at last step: median = %.4f, IQR = [%.4f, %.4f]  (fixed point |z*| at c = 0.25+0.18i is 0.3606)",
              median(last$abs_z_pfp), quantile(last$abs_z_pfp, .25), quantile(last$abs_z_pfp, .75)))

  # 4. OULAD only: does unconstrained escape relate to the real outcome?
  if (ds == "OULAD") {
    risk <- ifelse(d$outcome %in% c("Fail", "Withdrawn"), "Fail/Withdrawn", "Pass/Distinction")
    ft   <- fisher.test(table(risk, d$u_escaped))
    say("Unconstrained escape by real outcome:")
    print(table(risk, escaped = d$u_escaped))
    say(sprintf("  escapes: Fail/Withdrawn %d/%d, Pass/Distinction %d/%d; Fisher exact p = %.3g",
                sum(d$u_escaped[risk == "Fail/Withdrawn"]), sum(risk == "Fail/Withdrawn"),
                sum(d$u_escaped[risk == "Pass/Distinction"]), sum(risk == "Pass/Distinction"),
                ft$p.value))
  }
  say("")
}
tests <- do.call(rbind, tests)
write.csv(tests, file.path(dir_in, "r_real_tests.csv"), row.names = FALSE)

# 5. Sensitivity of the 'ZPD' result to the arbitrary band limits
lows  <- c(0.05, 0.10, 0.20, 0.30, 0.40)
highs <- c(0.60, 0.80, 1.00, 1.20, 1.50)
sens  <- list()
for (ds in c("ASSISTments", "OULAD")) {
  s <- steps[steps$dataset == ds, ]
  for (lo in lows) for (hi in highs) {
    u <- tapply(s$abs_z_unconstrained >= lo & s$abs_z_unconstrained <= hi, s$student, mean)
    p <- tapply(s$abs_z_pfp           >= lo & s$abs_z_pfp           <= hi, s$student, mean)
    sens[[length(sens) + 1]] <- data.frame(dataset = ds, band_low = lo, band_high = hi,
                                           u_zpd_mean = mean(u), p_zpd_mean = mean(p),
                                           diff = mean(p - u))
  }
}
sens <- do.call(rbind, sens)
write.csv(sens, file.path(dir_in, "r_real_zpd_sensitivity.csv"), row.names = FALSE)
say("ZPD-band sensitivity (PFP minus unconstrained, mean per-student ratio):")
for (ds in unique(sens$dataset)) {
  x <- sens[sens$dataset == ds, ]
  say(sprintf("  %s: diff ranges from %.3f to %.3f; PFP ratio ranges from %.3f to %.3f",
              ds, min(x$diff), max(x$diff), min(x$p_zpd_mean), max(x$p_zpd_mean)))
}
writeLines(out, file.path(dir_in, "r_real_report.txt"))
