# Agent Memory Lab — Starter v0.1

A reproducible **synthetic benchmark infrastructure prototype** comparing no-memory, recency, and hand-coded salience selection under a capacity of three records.

## Quickstart

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python generate_cases.py
python run_eval.py
pytest -q
streamlit run app.py
```

The Streamlit app displays case-level predictions and aggregate metrics. The evaluator writes `results/case_results.csv` and `results/experiments.duckdb`.

## Limitations (important)

- **Not an LLM benchmark yet:** answers use a deterministic provenance-aware rule, making this an evaluation pipeline baseline.
- **Not future-value learning:** `salience` is a transparent heuristic. Counterfactual paired continuations and a learned predictor are next-stage work.
- The synthetic examples use a small number of templates and are not evidence of real-world generalization.
- `capacity=3` measures number of records, **not tokens**. Token-precise budgets require implementing tokenization.
- The answer policy intentionally rejects untrusted documents; poisoning failures may be zero by construction. Future experiments must test LLM behavior without changing the ground truth or trust policy.
- The `train/test` split is for pipeline development only; shared templates leak across splits, so do not use it to claim out-of-distribution generalization.

## Next milestone

Implement task-family-disjoint scenarios, an actual LLM answerer, equal token budgets, then **paired keep/replace** memory continuations with outcomes hidden from the deployed selector. Add learned predictions only after generating branch labels.
