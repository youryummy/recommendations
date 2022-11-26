from flask import Blueprint, request
from . import service

bp = Blueprint('recommendation', __name__) 

@bp.route('/recommendation', methods=['GET'])
def obtain_recommendations():
    # username = request.cookies.get('username')
    username = "username_test"

    # recipes = request.get_json()["recipes"]
    recipes = [{"id": 1, "tags": ["tag1", "tag2"]}, {"id": 2, "tags": ["tag2", "tag3"]}, {"id": 3, "tags": ["tag1", "tag4", "tag5"]}, {"id": 4, "tags": ["tag1", "tag2", "tag3"]}, {"id": 5, "tags": ["tag2", "tag3"]}]
    
    recommendations = service.get_recommendations(username, recipes)
    return recommendations