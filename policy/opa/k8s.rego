package kubernetes.admission

deny[msg] {
  input.kind.kind == "Deployment"
  not input.spec.template.spec.securityContext.runAsNonRoot
  msg := "Deployment must run as non-root"
}
