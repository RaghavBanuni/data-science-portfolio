# Data Science and ML Engineering Portfolio

Twenty-seven end-to-end projects. Each one is built around a decision somebody has to make, and each
README argues for its own design choices instead of listing library calls.

The common thread is that **the modelling is rarely the hard part**. The hard part is the leak that
makes an offline score meaningless, the threshold that turns a probability into an action, the metric
that is misleading on imbalanced data, the monitor that gets muted because it cries wolf, the join that
attaches a feature value that did not exist yet, and the validation split that flatters a model whose
vocabulary drifts weekly. That is what these repositories are about.

```bash
# verify this index is not rotting
python scripts/check_links.py --readme
pytest                                  # registry/index consistency
```

---

## Risk and Finance

| Project | The decision it supports | Stack |
| --- | --- | --- |
| [**Portfolio Optimization**](https://github.com/RaghavBanuni/portfolio-optimization-quant) | How much of each asset to hold, and when to rebalance | NumPy, SciPy |
| [**Credit Risk Scorecard**](https://github.com/RaghavBanuni/credit-risk-scorecard-ml) | Approve, decline, or price a loan | scikit-learn, gradient boosting |
| [**Card Fraud Detection**](https://github.com/RaghavBanuni/fraud-detection-imbalanced-ml) | Block, review, or allow a transaction | scikit-learn |
| [**Fraud Ring Detection on Graphs**](https://github.com/RaghavBanuni/graph-fraud-ring-detection-community) | Which accounts to investigate together, rather than one at a time | Python stdlib |

- **Portfolio Optimization** — mean-variance weights are unstable because sample covariance is badly
  conditioned; Ledoit–Wolf shrinkage and risk parity show the instability and what damps it, evaluated
  walk-forward with VaR/CVaR rather than in-sample.
- **Credit Risk Scorecard** — a regulated decision has to be explainable, so it is a WOE/IV scorecard
  with monotonic binning translated into integer points, and the accuracy given up relative to raw
  boosting is measured rather than asserted.
- **Card Fraud Detection** — at 0.2% positives both accuracy and ROC-AUC mislead, and velocity
  features leak the future unless computed strictly backwards. PR-AUC plus an explicit cost matrix
  sets the threshold.
- **Fraud Ring Detection on Graphs** — a ring is invisible per account and obvious as a subgraph, so
  detection is community structure: IDF-weighted bipartite projection, Louvain from scratch, label
  propagation. Modularity's resolution limit is demonstrated, because it hides small rings inside
  large communities without complaining.

## Customer and Growth

| Project | The decision it supports | Stack |
| --- | --- | --- |
| [**Churn Prediction Service**](https://github.com/RaghavBanuni/churn-prediction-ml-service) | Who to spend retention budget on | scikit-learn, FastAPI, Docker, CI |
| [**A/B Testing Engine**](https://github.com/RaghavBanuni/ab-testing-experimentation-engine) | Ship the variant, or do not | NumPy, SciPy |
| [**Uplift Modeling**](https://github.com/RaghavBanuni/uplift-modeling-causal-marketing) | Who to target, given that most responders would convert anyway | scikit-learn |
| [**Implicit-Feedback Recommender**](https://github.com/RaghavBanuni/recommender-implicit-feedback-coldstart) | What to show a user, including one never seen before | NumPy, sparse linear algebra |
| [**Bayesian Marketing Mix Modeling**](https://github.com/RaghavBanuni/bayesian-marketing-mix-modeling) | How to split next quarter's budget across channels | Python stdlib |
| [**Survival Analysis for Churn**](https://github.com/RaghavBanuni/survival-analysis-customer-churn) | *When* a customer will leave, not merely whether | Python stdlib |

- **Churn Prediction Service** — a ranked list is not a decision: probabilities are calibrated and the
  threshold comes from expected value given offer cost and margin saved, then served behind an API
  that shares preprocessing with training.
- **A/B Testing Engine** — fixed-horizon p-values are invalid the moment somebody peeks, which
  everybody does. Always-valid sequential tests, CUPED, sample-ratio-mismatch gating and FDR control,
  with a simulator that scores the *analysis method* for false positive rate.
- **Uplift Modeling** — the individual treatment effect is never observed, so no row has a label.
  S/T/X/R-learners and the transformed outcome make it estimable; Qini curves evaluate the ranking.
- **Implicit-Feedback Recommender** — a non-click is not a dislike. ALS with confidence weighting from
  scratch, content-based cold-start routing, and re-ranking for diversity, availability and margin.
- **Bayesian Marketing Mix Modeling** — spend is correlated across channels and adstock/saturation are
  weakly identified, so the posterior is the deliverable and point estimates mislead. R-hat and ESS
  diagnostics, and an explicit statement that regression on observational spend is not causal without
  geo experiments to anchor it.
- **Survival Analysis for Churn** — binary classification silently discards censoring: a customer who
  has not yet churned is not a negative. Kaplan–Meier with Greenwood intervals, Cox PH with Efron ties
  by Newton–Raphson, Schoenfeld residuals testing the proportionality assumption the model depends on,
  and IPCW Brier scores that stay honest under censoring.

## Healthcare

| Project | The decision it supports | Stack |
| --- | --- | --- |
| [**Hospital Readmission Risk**](https://github.com/RaghavBanuni/hospital-readmission-risk-ml) | Which discharged patients get a follow-up call | scikit-learn |

- Capacity is the constraint, not the AUC, so the evaluation is a decision curve under a fixed daily
  call budget — plus a subgroup audit of calibration and error-rate gaps, because an unequal error
  rate is a clinical harm and not a footnote.

## NLP and LLM Systems

| Project | The decision it supports | Stack |
| --- | --- | --- |
| [**Citation-Verified RAG**](https://github.com/RaghavBanuni/rag-qa-citation-verified) | Answer the question, or admit you cannot | BM25 + TF-IDF from scratch |
| [**Support Ticket Routing**](https://github.com/RaghavBanuni/ticket-routing-nlp-classifier) | Which queue a ticket goes to, and when a human decides | scikit-learn |
| [**LLM Eval and Guardrails**](https://github.com/RaghavBanuni/llm-eval-guardrails-harness) | Is this prompt or model change a regression? | Python, statistics |
| [**Transformer From Scratch**](https://github.com/RaghavBanuni/transformer-language-model-from-scratch) | — proof the mechanism is understood, not borrowed | NumPy only |

- **Citation-Verified RAG** — a fluent unsupported answer is worse than no answer, so every claim is
  verified against its cited span, abstention is calibrated, and retrieval is scored with recall@k,
  MRR and nDCG on a labelled set.
- **Support Ticket Routing** — random validation flatters a model whose vocabulary drifts weekly, so
  validation is temporal; word + character n-grams survive typos; a coverage curve prices the accuracy
  bought by deferring the least confident tickets.
- **LLM Eval and Guardrails** — an LLM judge is a measuring instrument, so it is validated against
  human labels before being trusted. Paired McNemar tests gate releases; guardrails fail closed.
- **Transformer From Scratch** — every backward pass derived by hand and verified against finite
  differences: the softmax Jacobian, LayerNorm's two correction terms, causal masking, AdamW's
  decoupled decay. Byte-level BPE and KV-cache generation included.

## Ranking and Information Retrieval

| Project | The decision it supports | Stack |
| --- | --- | --- |
| [**Search Reranking and Learning to Rank**](https://github.com/RaghavBanuni/search-reranking-learning-to-rank) | What order to show results in, learned from logs nobody labelled | Python stdlib |

- Clicks measure attention as much as relevance, so a model trained on raw clicks reproduces the
  incumbent ranker — including the mistakes that never got clicked and therefore never got corrected.
  Pointwise, RankNet and LambdaRank on one model class isolate the loss; inverse propensity weighting
  corrects position bias, with the propensity estimator's own bias demonstrated rather than hidden.
  NDCG's per-query normalisation and the gain-function choice are spelled out, because they are why
  two published NDCG numbers are usually not comparable.

## Forecasting and Operations

| Project | The decision it supports | Stack |
| --- | --- | --- |
| [**Demand Forecasting and Inventory**](https://github.com/RaghavBanuni/demand-forecasting-inventory-quantiles) | How much to reorder, and when | scikit-learn, pandas |
| [**Multivariate Anomaly Detection**](https://github.com/RaghavBanuni/multivariate-time-series-anomaly-detection) | Is this deviation worth waking somebody for? | Python stdlib |

- **Demand Forecasting and Inventory** — a point forecast cannot set a reorder point, because the
  service level lives in the tail. Quantile forecasts feed reorder points whose achieved service level
  and holding cost are measured in simulation, with rolling-origin backtesting and leakage-safe lags.
- **Multivariate Anomaly Detection** — per-signal thresholds miss what matters, because a fleet
  failure is a change in the *correlation structure* while every series stays in range. Mahalanobis
  distance, PCA reconstruction error and a spectral residual, scored with range-based precision/recall
  and detection delay — point-wise F1 rewards a detector that fires once in a long event and sleeps
  through the rest.

## Optimization and Decision Systems

| Project | The decision it supports | Stack |
| --- | --- | --- |
| [**Vehicle Routing with Time Windows**](https://github.com/RaghavBanuni/vehicle-routing-capacitated-time-windows) | Which driver visits which stops, in what order | Python stdlib |
| [**Dynamic Pricing with Contextual Bandits**](https://github.com/RaghavBanuni/dynamic-pricing-contextual-bandits) | What price to quote this customer, now | Python stdlib |

- **Vehicle Routing with Time Windows** — CVRPTW is NP-hard and its constraints interact: a route that
  respects capacity can violate a time window. Clarke–Wright savings then guided local search over
  2-opt, Or-opt and cross-exchange, with feasibility checked exactly rather than penalised, and the
  gap to a lower bound reported instead of a claim of optimality.
- **Dynamic Pricing with Contextual Bandits** — a pricing experiment costs money on every impression,
  so exploration is paid for deliberately. LinUCB and linear Thompson sampling with Sherman–Morrison
  rank-1 updates, regret against an oracle, and off-policy evaluation (IPS, SNIPS, doubly robust) so a
  policy can be judged before deployment — including where each estimator breaks.

## Computer Vision

| Project | The decision it supports | Stack |
| --- | --- | --- |
| [**Vision, Grad-CAM and Distillation**](https://github.com/RaghavBanuni/pytorch-vision-gradcam-distillation) | Can this classifier be trusted, and can it run small? | PyTorch |

- A background shortcut is *planted deliberately* so that Grad-CAM pointing-game scores can catch a
  model that is right for the wrong reason. Calibration (ECE), robustness gaps under corruption, and
  distillation into a 10× smaller student are all measured rather than claimed.

## Data and Platform Engineering

| Project | The decision it supports | Stack |
| --- | --- | --- |
| [**SQL Analytics Warehouse**](https://github.com/RaghavBanuni/sql-ecommerce-analytics-warehouse) | What the business actually did last quarter | PostgreSQL |
| [**Pipeline Orchestration and Data Contracts**](https://github.com/RaghavBanuni/data-pipeline-orchestration-contracts) | Should this data be published at all? | Python stdlib, SQLite |
| [**Feature Store and Point-in-Time Joins**](https://github.com/RaghavBanuni/feature-store-point-in-time-joins) | Is this training set actually reproducible in production? | Python stdlib, SQLite |
| [**Streaming Event Processor**](https://github.com/RaghavBanuni/streaming-event-processor-sliding-windows) | What the aggregate is right now, with events out of order | Python stdlib |
| [**Drift Monitoring Service**](https://github.com/RaghavBanuni/mlops-drift-monitoring-service) | Is the model still fit for production? | Python, SciPy, FastAPI |

- **SQL Analytics Warehouse** — cohort retention, RFM, LTV and multi-touch attribution as
  window-function SQL over a normalised schema, with SQL-only reproducible seed data and data-quality
  assertions that fail loudly.
- **Pipeline Orchestration and Data Contracts** — content-addressed fingerprints give incremental runs
  with early cutoff; contracts validate *before* publishing and never coerce; PSI bins come from the
  baseline; lineage answers "what else is wrong?" by traversal instead of memory.
- **Feature Store and Point-in-Time Joins** — training-serving skew is a correctness bug no metric
  reveals: a naive join attaches feature values that did not exist when the label was generated. As-of
  joins with explicit event-time versus processing-time semantics, late-arriving data, and a skew
  detector comparing offline and online reads on the same keys.
- **Streaming Event Processor** — event time and processing time diverge, so a window can never be
  closed with certainty, only with a watermark that trades completeness for latency. Tumbling, sliding
  and session windows over pane decomposition, allowed lateness with explicit retractions,
  Space-Saving top-k under bounded memory, and checkpoints that make replay idempotent.
- **Drift Monitoring Service** — a monitor that cries wolf gets muted, so drift tests carry FDR
  control and effect-size gating, labels arrive late by design, and a harness scores the monitor
  itself on detection delay against false alarms.

## Privacy and Trustworthy ML

| Project | The decision it supports | Stack |
| --- | --- | --- |
| [**Differential Privacy for Tabular ML**](https://github.com/RaghavBanuni/differential-privacy-tabular-ml) | Can this model be released without leaking the people in it? | Python stdlib |

- Epsilon is a bound on a mechanism, not a measurement of leakage — and the guarantee is void if
  sensitivity is mis-stated, so clipping bias and small-cell error sit next to it. RDP accounting for
  the subsampled Gaussian, DP-SGD with per-example clipping, and a membership-inference audit whose
  empirical epsilon is reported beside the accounted one, in both directions: a successful attack
  proves a leak, a failed attack proves only that *this* attack failed. The disparate impact on a
  minority subgroup is measured, because the aggregate accuracy figure hides it.

---

## Standards applied across every repository

| | |
| --- | --- |
| **Leakage discipline** | Every transform is fitted inside cross-validation; temporal features look strictly backwards; validation is temporal wherever time matters; joins are as-of wherever a feature has a timestamp. |
| **Metrics that match the problem** | PR-AUC on imbalanced data, MASE/WAPE/pinball for forecasts, Qini for uplift, nDCG for ranking, range-based precision/recall for anomaly events, ECE for calibration. Never accuracy on a 0.2% base rate. |
| **Decisions, not scores** | A probability becomes an action through an explicit cost model or capacity constraint, and the threshold is derived rather than defaulted to 0.5. |
| **Runnable** | Synthetic or public data with fixed seeds, pinned dependencies, and a documented command that reproduces every number in the README. |
| **Tested** | Unit tests for the parts that are easy to get quietly wrong: leakage, splitting, metric edge cases, and hand-derived gradients against finite differences. |
| **Honest limitations** | Each README states what the project does not do and where its assumptions break. Synthetic data is labelled as synthetic; illustrative numbers are labelled as illustrative. |

## Reading order

| If you have | Read |
| --- | --- |
| five minutes | [A/B Testing Engine](https://github.com/RaghavBanuni/ab-testing-experimentation-engine) — the statistics most teams get wrong, and why |
| ten minutes and you care about engineering | [Streaming Event Processor](https://github.com/RaghavBanuni/streaming-event-processor-sliding-windows) — why a window can never be closed with certainty |
| ten minutes and you care about correctness bugs | [Feature Store and Point-in-Time Joins](https://github.com/RaghavBanuni/feature-store-point-in-time-joins) — the leak that no metric reveals |
| ten minutes and you care about fundamentals | [Transformer From Scratch](https://github.com/RaghavBanuni/transformer-language-model-from-scratch) — hand-derived gradients, checked numerically |
| ten minutes and you care about what a guarantee means | [Differential Privacy for Tabular ML](https://github.com/RaghavBanuni/differential-privacy-tabular-ml) — a bound, and what an attack actually recovers |
| an interview loop to plan | Any repository above: the READMEs are written as design arguments, so they double as talking points |

## Repository layout

```
projects.json          machine-readable registry: slug, category, stack, decision, hard part
README.md              this index, generated from and tested against the registry
scripts/check_links.py stdlib link checker (--readme also sizes each README)
tests/test_registry.py offline consistency tests: no drift between index and registry
```

## License

MIT — see [LICENSE](LICENSE). Each project repository carries its own license.
