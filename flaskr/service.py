from . import utils
from collections import Counter

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

def compute_similarity(usual_tags, recipes_tags):
    similarity = {}
    for recipe in recipes_tags:
        tags = set(recipes_tags[recipe])
        similarity[recipe] = dice_coefficient(usual_tags, tags)
    return similarity

def dice_coefficient(usual_tags, tags):
    return 2 * len(set(usual_tags).intersection(set(tags))) / (len(usual_tags) + len(tags))


def get_recommendations(username, recipes):
    # my_rated_recipes = utils.communicate("GET", "http://localhost:5000/api/v1/ratings", None, username)
    my_rated_recipes = set([1,2])
    
    rated_recipes = [{r["id"]: r["tags"]} for r in recipes if r["id"] in my_rated_recipes]
    non_rated_recipes = [r for r in recipes if r["id"] not in my_rated_recipes]

    # obtain common user tags 
    usual_tags = get_usual_tags(rated_recipes)
    recipes_tags = {r["id"]: r["tags"] for r in non_rated_recipes}
    
    # calculate simmilarity with non rated recipes
    similarity = compute_similarity(usual_tags, recipes_tags)

    sorted_similarity = sorted(similarity.items(), key=lambda x: x[1], reverse=True)
    recommended_recipes = [r[0] for r in sorted_similarity]
    return recommended_recipes
