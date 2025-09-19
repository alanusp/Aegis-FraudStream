package aegis.authz

default allow = false

allow {
  input.method == "POST"
  startswith(input.path, "/v1/")
  input.user == "service-a"
}
