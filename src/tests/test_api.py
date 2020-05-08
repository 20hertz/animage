import main


def test_main():
    main.app.testing = True
    client = main.app.test_client()

    r = client.get('/v1/hello')
    assert r.status_code == 200
    assert 'Hello World' in r.data.decode('utf-8')
