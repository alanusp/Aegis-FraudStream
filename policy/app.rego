package app

default allow = true

# Example: deny auto-approve when amount exceeds threshold unless risk_score < 0.2
deny[msg] {
  input.amount > 1000
  not input.risk_score
  msg := "high_amount_requires_risk_score"
}

deny[msg] {
  input.amount > 1000
  input.risk_score >= 0.2
  msg := "high_amount_high_risk_denied"
}
