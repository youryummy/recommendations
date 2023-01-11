from flask import Blueprint
from . import service
import logging

bp = Blueprint('recommendation', __name__) 
logger = logging.getLogger(__name__)

@bp.route('/recommendation/<username>/<plan>', methods=['GET'])
def obtain_recommendations(username, plan):
    logger.info(f'Processing request for user {username} and plan {plan}')
    
    recommendations = service.get_recommendations(username, plan)
    return recommendations
    