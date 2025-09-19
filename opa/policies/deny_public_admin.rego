package aegis.admin

default allow = false

# Example: deny admin when tenant is "public" in certain conditions
allow {
  input.tenant != "public"
}
