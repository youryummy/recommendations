import pytest
from flaskr import create_app
from unittest.mock import Mock
import jwt

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True

    return app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

def test_health_check(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.data == b'The server is running!'

def test_swagger_schema(client):
    response = client.get('/docs/swagger.json')
    assert response.status_code == 200
    assert response.json['info']['title'] == 'Recommendation Service'

def test_recommendations(client, monkeypatch):
    stub = Mock()
    stub.return_value = ["6", "7", "8"]
    monkeypatch.setattr('flaskr.controller.service.utils.communicate' , stub)

    token = jwt.encode({'username': 'javivm17', 'plan': 'base'}, 'youryummysecret', algorithm='HS256')
    client.set_cookie('localhost', 'authToken', token)
    response = client.get('/api/v1/recommendation')
    assert response.status_code == 200

def test_recommendations_without_ratings(client, monkeypatch):
    stub = Mock()
    stub.return_value = []
    monkeypatch.setattr('flaskr.controller.service.utils.communicate' , stub)

    token = jwt.encode({'username': 'javivm17', 'plan': 'base'}, 'youryummysecret', algorithm='HS256')
    client.set_cookie('localhost', 'authToken', token)
    response = client.get('/api/v1/recommendation')
    assert response.status_code == 200

def test_recommendations_plan_premium(client, monkeypatch):
    stub = Mock()
    stub.return_value = []
    monkeypatch.setattr('flaskr.controller.service.utils.communicate' , stub)

    token = jwt.encode({'username': 'javivm17', 'plan': 'premium'}, 'youryummysecret', algorithm='HS256')
    client.set_cookie('localhost', 'authToken', token)
    response = client.get('/api/v1/recommendation')
    assert response.status_code == 200

def test_recommendations_without_auth(client):
    response = client.get('/api/v1/recommendation')
    assert response.status_code == 401


