# Data Science and ML Engineering Portfolio

Seventeen end-to-end projects. Each one is built around a decision somebody has to make, and each
README argues for its own design choices instead of listing library calls.

The common thread is that **the modelling is rarely the hard part**. The hard part is the leak that
makes an offline score meaningless, the threshold that turns a probability into an action, the metric
that is misleading on imbalanced data, the monitor that gets muted because it cries wolf, and the
validation split that flatters a model whose vocabulary drifts weekly. That is what these repositories
are about.

```bash
# verify this index is not rotting
python scripts/check_links.py --readme
pytest                                     # registry/index consistency
```

---

## Risk and Finance

| Project | The decision it supports | Stack |
| --- | --- | --- |
| [**Portfolio Optimization**](https://github.com/RaghavBanuni/portfolio-optimization-quant) | How much of each asset to hold, and when to rebalance | NumPy, SciPy |
| [**Credit Risk Scorecard**](https://github.com/RaghavBanuni/credit-risk-scorecard-ml) | Approve, decline, or price a loan | scikit-learn, gradient boosting |
| [**Card Fraud Detection**](https://github.com/RaghavBanuni/fraud-detection-imbalanced-ml) | Block, review, or allow a transaction | scikit-learn |

- **Portfolio Optimization** — mean-variance weights are unstable because sample covariance is badly
  conditioned; Ledoit–Wolf shrinkage and risk parity show the instability and what damps it, evaluated
  walk-forward with VaR/CVaR rather than in-sample.
- **Credit Risk Scorecard** — a regulated decision has to be explainable, so it is a WOE/IV scorecard
  with monotonic binning translated into integer points, and the accuracy given up relative to raw
  boosting is measured rather than asserted.
- **Card Fraud Detection** — at 0.2% positives both accuracy and ROC-AUC mislead, and velocity
  features leak the future unless computed strictly backwards. PR-AUC plus an explicit cost matrix
  sets the threshold.

## Customer and Growth

| Project | The decision it supports | Stack |
| --- | --- | --- |
| [**Churn Prediction Service**](https://github.com/RaghavBanuni/churn-prediction-ml-service) | Who to spend retention budget on | scikit-learn, FastAPI, Docker, CI |
| [**A/B Testing Engine**](https://github.com/RaghavBanuni/ab-testing-experimentation-engine) | Ship the variant, or do not | NumPy, SciPy |
| [**Uplift Modeling**](https://github.com/RaghavBanuni/uplift-modeling-causal-marketing) | Who to target, given that most responders would convert anyway | scikit-learn |
| [**Implicit-Feedback Recommender**](https://github.com/RaghavBanuni/recommender-implicit-feedback-coldstart) | What to show a user, including one never seen before | NumPy, sparse linear algebra |

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

## Forecasting and Operations

| Project | The decision it supports | Stack |
| --- | --- | --- |
| [**Demand Forecasting and Inventory**](https://github.com/RaghavBanuni/demand-forecasting-inventory-quantiles) | How much to reorder, and when | scikit-learn, pandas |

- A point forecast cannot set a reorder point, because the service level lives in the tail. Quantile
  forecasts feed reorder points whose achieved service level and holding cost are measured in
  simulation, with rolling-origin backtesting and leakage-safe lag features throughout.

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
| [**Drift Monitoring Service**](https://github.com/RaghavBanuni/mlops-drift-monitoring-service) | Is the model still fit for production? | Python, SciPy, FastAPI |

- **SQL Analytics Warehouse** — cohort retention, RFM, LTV and multi-touch attribution as
  window-function SQL over a normalised schema, with SQL-only reproducible seed data and data-quality
  assertions that fail loudly.
- **Pipeline Orchestration and Data Contracts** — content-addressed fingerprints give incremental runs
  with early cutoff; contracts validate *before* publishing and never coerce; PSI bins come from the
  baseline; lineage answers "what else is wrong?" by traversal instead of memory.
- **Drift Monitoring Service** — a monitor that cries wolf gets muted, so drift tests carry FDR
  control and effect-size gating, labels arrive late by design, and a harness scores the monitor
  itself on detection delay against false alarms.

---

## Standards applied across every repository

| | |
| --- | --- |
| **Leakage discipline** | Every transform is fitted inside cross-validation; temporal features look strictly backwards; validation is temporal wherever time matters. |
| **Metrics that match the problem** | PR-AUC on imbalanced data, MASE/WAPE/pinball for forecasts, Qini for uplift, nDCG for ranking, ECE for calibration. Never accuracy on a 0.2% base rate. |
| **Decisions, not scores** | A probability becomes an action through an explicit cost model or capacity constraint, and the threshold is derived rather than defaulted to 0.5. |
| **Runnable** | Synthetic or public data with fixed seeds, pinned dependencies, and a documented command that reproduces every number in the README. |
| **Tested** | Unit tests for the parts that are easy to get quietly wrong: leakage, splitting, metric edge cases, and hand-derived gradients against finite differences. |
| **Honest limitations** | Each README states what the project does not do and where its assumptions break. Synthetic data is labelled as synthetic. |

## Reading order

| If you have | Read |
| --- | --- |
| five minutes | [A/B Testing Engine](https://github.com/RaghavBanuni/ab-testing-experimentation-engine) — the statistics most teams get wrong, and why |
| ten minutes and you care about engineering | [Pipeline Orchestration and Data Contracts](https://github.com/RaghavBanuni/data-pipeline-orchestration-contracts) — failure modes where every task reports success |
| ten minutes and you care about fundamentals | [Transformer From Scratch](https://github.com/RaghavBanuni/transformer-language-model-from-scratch) — hand-derived gradients, checked numerically |
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
