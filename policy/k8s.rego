package k8s.security

deny[msg] {
  input.kind == "Deployment"
  c := input.spec.template.spec.containers[_]
  not c.securityContext.runAsNonRoot
  msg := "Containers must set runAsNonRoot"
}

deny[msg] {
  input.kind == "Deployment"
  c := input.spec.template.spec.containers[_]
  not c.readinessProbe
  msg := "Containers must define readinessProbe"
}
