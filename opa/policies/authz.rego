package aegis.authz
default allow = false
allow {
  input.role == "admin"
}
