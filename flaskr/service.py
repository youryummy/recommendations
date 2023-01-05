from . import utils
from collections import Counter
from functools import lru_cache
from dotenv import load_dotenv
import logging
import os

logger = logging.getLogger(__name__)
load_dotenv()

def get_usual_tags(rated_recipes):
    tags_frequency = {}
    for recipe in rated_recipes:
        for tag in recipe[list(recipe.keys())[0]]:
            if tag in tags_frequency:
                tags_frequency[tag] += 1
            else:
                tags_frequency[tag] = 1
                
    most_common = Counter(tags_frequency).most_common(10)
    return set([tag for tag, _ in most_common])

@lru_cache()
def compute_similarity(usual_tags, recipes_tags):
    similarity = {}
    for recipe in recipes_tags:
        tags = set(recipe[1])
        similarity[recipe[0]] = dice_coefficient(usual_tags, tags)
    return similarity

def compute_similarity_without_cache(usual_tags, recipes_tags):
    similarity = {}
    for recipe in recipes_tags:
        tags = set(recipe[1])
        similarity[recipe[0]] = dice_coefficient(usual_tags, tags)
    return similarity

def dice_coefficient(usual_tags, tags):
    return 2 * len(set(usual_tags).intersection(set(tags))) / (len(usual_tags) + len(tags))

def get_recommendations(username, recipes, plan):
    if os.getenv('PYTHON_ENV') == 'development':
        ratings_uri = f'http://rating-service/api/v1/ratings/findByUserId/{username}' 
    else:
        ratings_uri = f'http://youryummy-ratings-service/api/v1/ratings/findByUserId/{username}' 

    logger.info(f'Obtaining the rated recipes for user {username}')
    my_rated_recipes = utils.communicate("GET", ratings_uri)
    logger.info(f'The rated recipes for user {username} has been obtained successfully')
    my_rated_recipes = set(my_rated_recipes)

    rated_recipes = [{r["id"]: r["tags"]} for r in recipes if r["id"] in my_rated_recipes]
    non_rated_recipes = [r for r in recipes if r["id"] not in my_rated_recipes]

    usual_tags = tuple(get_usual_tags(rated_recipes))
    recipes_tags = tuple((r["id"], tuple(r["tags"])) for r in non_rated_recipes)

    if plan == 'base':
        similarity = compute_similarity_without_cache(usual_tags, recipes_tags)
    else:
        similarity = compute_similarity(usual_tags, recipes_tags)

    sorted_similarity = sorted(similarity.items(), key=lambda x: x[1], reverse=True)
    recommended_recipes = [r[0] for r in sorted_similarity[:10]]

    return recommended_recipes
