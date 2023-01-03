from flask import Blueprint, request, Response
from . import service
import logging
import jwt
import os
from dotenv import load_dotenv

bp = Blueprint('recommendation', __name__) 
logger = logging.getLogger(__name__)
load_dotenv()
JWT_SECRET = os.getenv('JWT_SECRET')

@bp.route('/recommendation', methods=['GET'])
def obtain_recommendations():
    auth_token = request.cookies.get('authToken')
    logger.info(f'Authtoken: {auth_token}')
    if auth_token is None:
        return Response(None, status=401)
    encoded_jwt = jwt.decode(auth_token, JWT_SECRET, algorithms=['HS256'])
    username = encoded_jwt['username']
    logger.info(f'Processing request for user {username}')

    #TODO get recipes
    recipes = [{"id": 1, "tags": ["tag1", "tag2"]}, {"id": 2, "tags": ["tag2", "tag3"]}, {"id": 3, "tags": ["tag1", "tag4", "tag5"]}, {"id": 4, "tags": ["tag1", "tag2", "tag3"]}, {"id": 5, "tags": ["tag2", "tag3"]}]
    for i in range(6, 2000000):
        recipes.append({"id": i, "tags": ["tag1", "tag2"]})
    
    recommendations = service.get_recommendations(username, recipes)
    return recommendations
    