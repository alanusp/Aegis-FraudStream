package aegis.admin

test_public_denied {
  not allow with input as {"tenant": "public"}
}

test_private_allowed {
  allow with input as {"tenant": "tenantA"}
}
