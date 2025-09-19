package aegis.authz

test_admin_allowed {
  allow with input as {"role":"admin"}
}

test_user_denied {
  not allow with input as {"role":"user"}
}
