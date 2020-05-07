from main import app


def test_main():
    app.testing = True
    client = app.test_client()

    r = client.get('/hello')
    # assert r.status_code == 200
    assert 'Hello World' in r.data.decode('utf-8')
