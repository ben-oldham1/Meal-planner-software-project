from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden

from .models import Recipe, IngredientInRecipe, Ingredient, RecipeTag, Tag
from .forms import RecipeForm, IngredientForm, TagForm

def recipe_list(request):
    # Only show public recipes to non-logged in users
    if request.user.is_authenticated:
        recipes = Recipe.objects.filter(user=request.user)
    else:
        recipes = Recipe.objects.filter(public=True)


    context = {
        'recipes': recipes,
    }

    return render(request, 'mealplanner/recipe_list.html', context)

def recipe_detail(request, recipe_id):
    # Fetch the recipe or return a 404 if it doesn't exist
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    # Ensure the user can only view their own recipes or public ones
    if not recipe.public and recipe.user != request.user:
        return HttpResponseForbidden("You are not allowed to view this recipe.")
    
    # Get the ingredients associated with this recipe
    ingredients = IngredientInRecipe.objects.filter(recipe=recipe)

    context = {
        'recipe': recipe,
        'ingredients': ingredients
    }

    # Pass the recipe and its ingredients to the template
    return render(request, 'mealplanner/recipe_detail.html', context)

@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user  # Associate the recipe with the logged-in user
            recipe.save()
            return redirect('recipe_detail', recipe_id=recipe.id)
    else:
        form = RecipeForm()
    return render(request, 'mealplanner/add_recipe.html', {'form': form})

@login_required
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    ingredients = Ingredient.objects.all()

    # Ensure the user can only edit their own recipes
    if recipe.user != request.user:
        return HttpResponseForbidden("You are not allowed to edit this recipe.")

    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipe_detail', recipe_id=recipe.id)
    else:
        form = RecipeForm(instance=recipe)

    context = {
        'form': form,
        'ingredients': ingredients,
        'recipe': recipe
    }

    return render(request, 'mealplanner/edit_recipe.html', context)

@login_required
def add_ingredient(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if recipe.user != request.user:
        return HttpResponseForbidden("You are not allowed to add ingredients to this recipe.")

    if request.method == 'POST':
        ingredient_id = request.POST.get('ingredient')
        measurement_amount = request.POST.get('measurement_amount')
        calories = request.POST.get('calories')
        fat = request.POST.get('fat')
        carbs = request.POST.get('carbs')
        protein = request.POST.get('protein')

        # Create a new IngredientInRecipe instance
        ingredient_in_recipe = IngredientInRecipe(
            recipe=recipe,
            ingredient_id=ingredient_id,
            measurement_amount=measurement_amount,
            calories=calories,
            fat=fat,
            carbs=carbs,
            protein=protein
        )
        ingredient_in_recipe.save()

        context = {
            'ingredient': ingredient_in_recipe
        }

        return render(request, 'mealplanner/ingredient_item.html', context)

@login_required
def add_tag(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if recipe.user != request.user:
        return HttpResponseForbidden("You are not allowed to add tags to this recipe.")

    if request.method == 'POST':
        tag_name = request.POST.get('name')
        tag, created = Tag.objects.get_or_create(name=tag_name)
        
        # Create a RecipeTag instance to associate the tag with the recipe
        recipe_tag = RecipeTag(recipe=recipe, tag=tag)
        recipe_tag.save()

        context = {
            'tag': tag
        }

        return render(request, 'mealplanner/tag_item.html', context)
