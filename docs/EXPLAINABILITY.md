# Explainability

- The `/v1/inference/explain` endpoint returns the score and the normalized features (`amount`, `velocity`, `country_risk`) used to compute it.
- For the current baseline model, the explanation is faithful because the score is a direct function of these features.
