from . import utils
from collections import Counter
from functools import lru_cache

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
        tags = set(recipes_tags[recipe])
        similarity[recipe] = dice_coefficient(usual_tags, tags)
    return similarity

def dice_coefficient(usual_tags, tags):
    return 2 * len(set(usual_tags).intersection(set(tags))) / (len(usual_tags) + len(tags))

def get_recommendations(username, recipes):
    # my_rated_recipes = utils.communicate("GET", "http://localhost:5000/api/v1/ratings", None, username)

    my_rated_recipes = set([1,4,6,76,32,89,45,23,67,12,34,56,78,90,100, 120, 150, 180, 200, 220, 250, 280, 300, 320, 350, 380, 400, 420, 450, 480, 500, 520, 550, 580, 600, 620, 650, 680, 700, 720, 750, 780, 800, 820, 850, 880, 900, 920, 950, 980, 1000, 1020, 1050, 1080, 1100, 1120, 1150, 1180, 1200, 1220, 1250, 1280, 1300, 1320, 1350, 1380, 1400, 1420, 1450, 1480, 1500, 1520, 1550, 1580, 1600, 1620, 1650, 1680, 1700, 1720, 1750, 1780, 1800, 1820, 1850, 1880, 1900, 1920, 1950, 1980, 2000, 2020, 2050, 2080, 2100, 2120, 2150, 2180, 2200, 2220, 2250, 2280, 2300, 2320, 2350, 2380, 2400, 2420, 2450, 2480, 2500, 2520, 2550, 2580, 2600, 2620, 2650, 2680, 2700, 2720, 2750, 2780, 2800, 2820, 2850, 2880, 2900, 2920, 2950, 2980, 3000, 3020, 3050, 3080, 3100, 3120, 3150, 3180, 3200, 3220, 3250, 3280, 3300, 3320, 3350, 3380, 3400, 3420, 3450, 348 ])
    
    rated_recipes = [{r["id"]: r["tags"]} for r in recipes if r["id"] in my_rated_recipes]
    non_rated_recipes = [r for r in recipes if r["id"] not in my_rated_recipes]

    usual_tags_cache = tuple(get_usual_tags(rated_recipes))
    recipes_tags_cache = tuple((r["id"], tuple(r["tags"])) for r in non_rated_recipes)

    similarity_with_cache = compute_similarity(usual_tags_cache, recipes_tags_cache)

    sorted_similarity = sorted(similarity_with_cache.items(), key=lambda x: x[1], reverse=True)
    recommended_recipes = [r[0] for r in sorted_similarity[:10]]

    return recommended_recipes
