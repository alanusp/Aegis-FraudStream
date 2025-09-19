from aegis_fraudstream import ping

def test_ping():
    assert ping() == 'pong'
