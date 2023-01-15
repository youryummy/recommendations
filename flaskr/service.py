from . import utils
from collections import Counter
from functools import lru_cache
import logging

logger = logging.getLogger(__name__)

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

def get_recommendations(username, plan):
    recipes = get_recipes()
    if type(recipes) is str:
        return recipes

    my_rated_recipes = get_rated_recipes(username)
    if type(my_rated_recipes) is str:
        return my_rated_recipes
    
    rated_recipes = [{r["_id"]: r["tags"]} for r in recipes if r["_id"] in my_rated_recipes]
    non_rated_recipes = [r for r in recipes if r["_id"] not in my_rated_recipes]

    usual_tags = tuple(get_usual_tags(rated_recipes))
    recipes_tags = tuple((r["_id"], tuple(r["tags"])) for r in non_rated_recipes)

    if plan == 'base':
        similarity = compute_similarity_without_cache(usual_tags, recipes_tags)
    else:
        similarity = compute_similarity(usual_tags, recipes_tags)

    sorted_similarity = sorted(similarity.items(), key=lambda x: x[1], reverse=True)
    recommended_recipes = [r[0] for r in sorted_similarity]

    return recommended_recipes

def get_recipes():
    logger.info(f'Obtaining the recipes')
    try:
        recipes = utils.communicate('GET', 'http://recipes/api/v1/recipes', None)
    except:
        logger.error("Failed to communicate with recipes service")
        return "Failed to communicate with recipes service"
    logger.info(f'The recipes has been obtained successfully')
    return recipes

def get_rated_recipes(username):
    ratings_uri = f'http://youryummy-ratings-service/api/v1/ratings/findByUserId/{username}' 

    logger.info(f'Obtaining the rated recipes for user {username}')
    try:
        my_rated_recipes = utils.communicate("GET", ratings_uri)
    except:
        logger.error("Failed to communicate with ratings service")
        return "Failed to communicate with ratings service"
    logger.info(f'The rated recipes for user {username} has been obtained successfully')
    my_rated_recipes = set(my_rated_recipes)
    return my_rated_recipes