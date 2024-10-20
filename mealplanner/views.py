from django.shortcuts import render, get_object_or_404
from .models import Recipe, IngredientInRecipe, Ingredient, RecipeTag

def recipe_list(request):
    # Start with all recipes
    recipes = Recipe.objects.filter(public=True)

    context = {
        'recipes': recipes,
    }

    return render(request, 'mealplanner/recipe_list.html', context)

def recipe_detail(request, recipe_id):
    # Retrieve the recipe or show a 404 error if it does not exist
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    # Get the ingredients associated with this recipe
    ingredients = IngredientInRecipe.objects.filter(recipe=recipe)

    context = {
        'recipe': recipe,
        'ingredients': ingredients
    }

    # Pass the recipe and its ingredients to the template
    return render(request, 'mealplanner/recipe_detail.html', context)