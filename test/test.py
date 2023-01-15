import pytest
from flaskr import create_app
from unittest.mock import Mock
import jwt
import os
from dotenv import load_dotenv

load_dotenv()
JWT_SECRET = os.getenv('JWT_SECRET')

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
    recipes_stub = Mock()
    recipes_stub.return_value = [
        {
            "_id": "1",
            "tags": ["tag1", "tag2"]
        },
        {
            "_id": "2",
            "tags": ["tag3", "tag4"]
        },
        {
            "_id": "3",
            "tags": ["tag5", "tag6"]
        }
    ]
    monkeypatch.setattr('flaskr.controller.service.get_recipes' , recipes_stub)

    ratings_stub = Mock()
    ratings_stub.return_value = ["1",]
    monkeypatch.setattr('flaskr.controller.service.get_rated_recipes' , ratings_stub)

    response = client.get('/api/v1/recommendation/javivm/base')
    assert response.status_code == 200

def test_recommendations_without_ratings(client, monkeypatch):
    recipes_stub = Mock()
    recipes_stub.return_value = [
        {
            "_id": "1",
            "tags": ["tag1", "tag2"]
        },
        {
            "_id": "2",
            "tags": ["tag3", "tag4"]
        },
        {
            "_id": "3",
            "tags": [""]
        }
    ]
    monkeypatch.setattr('flaskr.controller.service.get_recipes' , recipes_stub)

    ratings_stub = Mock()
    ratings_stub.return_value = []
    monkeypatch.setattr('flaskr.controller.service.get_rated_recipes' , ratings_stub)

    response = client.get('/api/v1/recommendation/javivm/base')
    assert response.status_code == 200

def test_recommendations_plan_premium(client, monkeypatch):
    recipes_stub = Mock()
    recipes_stub.return_value = [
        {
            "_id": "1",
            "tags": ["tag1", "tag2"]
        },
        {
            "_id": "2",
            "tags": ["tag3", "tag4"]
        },
        {
            "_id": "3",
            "tags": [""]
        }
    ]
    monkeypatch.setattr('flaskr.controller.service.get_recipes' , recipes_stub)

    ratings_stub = Mock()
    ratings_stub.return_value = []
    monkeypatch.setattr('flaskr.controller.service.get_rated_recipes' , ratings_stub)

    response = client.get('/api/v1/recommendation/javivm/premium')
    assert response.status_code == 200

def test_recommendations_and_fail_communication_with_recipes(client, monkeypatch):
    ratings_stub = Mock()
    ratings_stub.return_value = ["1",]
    monkeypatch.setattr('flaskr.controller.service.get_rated_recipes' , ratings_stub)

    response = client.get('/api/v1/recommendation/javivm/base')
    assert response.status_code == 500

def test_recommendations_and_fail_communication_with_ratings(client, monkeypatch):
    recipes_stub = Mock()
    recipes_stub.return_value = [
        {
            "_id": "1",
            "tags": ["tag1", "tag2"]
        },
        {
            "_id": "2",
            "tags": ["tag3", "tag4"]
        },
        {
            "_id": "3",
            "tags": ["tag5", "tag6"]
        }
    ]
    monkeypatch.setattr('flaskr.controller.service.get_recipes' , recipes_stub)

    response = client.get('/api/v1/recommendation/javivm/base')
    assert response.status_code == 500

