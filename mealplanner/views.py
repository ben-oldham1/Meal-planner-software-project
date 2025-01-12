from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.db.models import Q, Sum
from django.views.decorators.csrf import csrf_exempt

import json
import markdown
import requests

from .models import Recipe, RecipeNutrition, IngredientInRecipe, Ingredient, RecipeTag, Tag, MealPlan, MealPlanItem
from .forms import RecipeForm, RecipeNutritionForm, RecipeInstructionsForm, IngredientForm, TagForm, MealplanRecipeForm
from .filters import RecipeFilter

def recipe_list(request):
    # Only show public recipes to non-logged in users
    if request.user.is_authenticated:
        recipes = Recipe.objects.filter(user=request.user) | Recipe.objects.filter(public=True)
    else:
        recipes = Recipe.objects.filter(public=True)
    
    query = request.GET.get('q')

    # Create filters form
    recipe_filter = RecipeFilter(request.GET, queryset=recipes)

    # If a search has been made
    if query:
        # Filter recipes based on search term in the name field
        recipes = recipes.filter(
            Q(name__icontains=query) | Q(instructions__icontains=query)
        ).distinct()
    else:
        # If no search, use the values from filter
        recipes = recipe_filter.qs

    context = {
        'active_path': 'recipes',
        'new_recipe_form': RecipeForm(),
        'recipe_filter': recipe_filter,
        'recipes': recipes,
        'query': query,
    }

    return render(request, 'mealplanner/recipe_list.html', context)

def recipe_search(request, search_query):
    # Only show public recipes to non-logged in users
    if request.user.is_authenticated:
        recipes = Recipe.objects.filter(user=request.user) | Recipe.objects.filter(public=True)
        recipes = recipes.filter(name=search_query)
    else:
        recipes = Recipe.objects.filter(public=True).filter(name=search_query)

    context = {
        'active_path': 'recipes',
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

    # Get the nutrition data associated with this recipe
    try:
        nutrition = RecipeNutrition.objects.get(recipe=recipe)
    except:
        nutrition = None

    # Format the markdown
    md = markdown.Markdown()
    recipe.instructions = md.convert(recipe.instructions)

    context = {
        'active_path': 'recipes',
        'recipe': recipe,
        'ingredients': ingredients,
        'nutrition': nutrition
    }

    # Pass the recipe and its ingredients to the template
    return render(request, 'mealplanner/recipe_detail.html', context)

def get_nutrition_data(query, app_id, app_key):
    url = 'https://trackapi.nutritionix.com/v2/natural/nutrients'
    headers = {
        'Content-Type': 'application/json',
        'x-app-id': app_id,
        'x-app-key': app_key
    }
    body = {
        "query": query
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(body))
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

@login_required
def add_recipe(request):
    if request.method == 'POST':
        new_recipe_form = RecipeForm(request.POST)
        if new_recipe_form.is_valid():
            recipe = new_recipe_form.save(commit=False)
            recipe.user = request.user  # Associate the recipe with the logged-in user
            recipe.save()
            return redirect('edit_recipe', recipe_id=recipe.id)
    else:
        form = RecipeForm()
    return render(request, 'mealplanner/add_recipe.html', {'new_recipe_form': form})

@login_required
def add_recipe_to_mealplan(request, mealplan_id):
    if request.method == 'POST':
        add_recipe_form = MealplanRecipeForm(request.POST)
        if add_recipe_form.is_valid():
            mealplan_item = add_recipe_form.save(commit=False)
            mealplan_item.weekday = 0
            mealplan_item.meal_plan = MealPlan.objects.get(id=mealplan_id)
            mealplan_item.save()
    return redirect('mealplan_edit', mealplan_id=mealplan_id)

@login_required
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    ingredients = Ingredient.objects.all().order_by('name')

    # Ensure the user can only edit their own recipes
    if recipe.user != request.user:
        return HttpResponseForbidden("You are not allowed to edit this recipe.")

    if request.method == 'POST':
        if request.POST['form_id'] == 'recipe_details':
            recipedetailsform = RecipeForm(request.POST, instance=recipe)
            if recipedetailsform.is_valid():
                recipedetailsform.save()
            
            return redirect('edit_recipe', recipe_id=recipe.id)

        if request.POST['form_id'] == 'recipe_instructions':
            recipeinstructionsform = RecipeInstructionsForm(request.POST, instance=recipe)
            if recipeinstructionsform.is_valid():
                recipeinstructionsform.save()
            
            return redirect('edit_recipe', recipe_id=recipe.id)
      

        if request.POST['form_id'] == 'recipe_nutrition':
            receipenutritionform = RecipeNutritionForm(request.POST)
            if receipenutritionform.is_valid():
                nutrition = receipenutritionform.save(commit=False)
                nutrition.recipe = recipe
                nutrition.save()
            
            return redirect('edit_recipe', recipe_id=recipe.id)
            

    else:
        recipedetailsform = RecipeForm(instance=recipe)
        recipeinstructionsform = RecipeInstructionsForm(instance=recipe)
        
        try:
            recipenutrition = RecipeNutrition.objects.get(recipe=recipe)
            receipenutritionform = RecipeNutritionForm(instance=recipenutrition)
        except:
            receipenutritionform = RecipeNutritionForm()

    context = {
        'active_path': 'recipes',
        'recipedetailsform': recipedetailsform,
        'recipeinstructionsform': recipeinstructionsform,
        'receipenutritionform': receipenutritionform,
        'ingredients': ingredients,
        'recipe': recipe
    }

    return render(request, 'mealplanner/edit_recipe.html', context)

# Utility/CRUD views
@login_required
def get_nutri_for_recipe(request, recipe_id):
    # Get the recipe and it's ingredients
    recipe = get_object_or_404(Recipe, id=recipe_id)
    ingredients_in_recipe = IngredientInRecipe.objects.filter(recipe=recipe)

    APP_ID = "d360df73"  # Replace with your actual App ID
    APP_KEY = "58f5b744482f26ff48588149cb1508bb"  # Replace with your actual App Key

    # String to store the natural language list of ingredients
    ingredients_natural = ""
    
    # Iterate through ingredients and add to string
    for ingredient in ingredients_in_recipe:
        ingredients_natural += str(ingredient.measurement_amount) + ' ' + str(ingredient.ingredient.measurement_unit) + ' of ' + str(ingredient.ingredient.name) + '; '

    # Call the API function to retrieve the data
    nutrition_data = get_nutrition_data(ingredients_natural, APP_ID, APP_KEY)

    # Vars to store the nutrition parameters
    calories = 0
    fat = 0
    carbs = 0
    protein = 0

    if nutrition_data:
        # Iterate through response and extract nutri params
        for food in nutrition_data['foods']:
            calories += food['nf_calories']
            fat += food['nf_total_fat']
            carbs += food['nf_total_carbohydrate']
            protein += food['nf_protein']

        # Provide response in JSON format for easy JS interpretation
        return JsonResponse({
            'calories': round(calories, 1),
            'fat': round(fat, 1),
            'carbs': round(carbs, 1),
            'protein': round(protein, 1),
        })

@login_required
def add_ingredient(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if recipe.user != request.user:
        return HttpResponseForbidden("You are not allowed to add ingredients to this recipe.")

    if request.method == 'POST':
        ingredient_id = request.POST.get('ingredient')
        measurement_amount = request.POST.get('measurement_amount')

        # Create a new IngredientInRecipe instance
        ingredient_in_recipe = IngredientInRecipe(
            recipe=recipe,
            ingredient_id=ingredient_id,
            measurement_amount=measurement_amount,
        )
        ingredient_in_recipe.save()

        context = {
            'ingredient': ingredient_in_recipe
        }

        return render(request, 'mealplanner/ingredient_item.html', context)

@login_required
def delete_ingredient(request, ingredient_id):
    ingredient_in_recipe = get_object_or_404(IngredientInRecipe, id=ingredient_id)

    if ingredient_in_recipe.recipe.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete ingredients from this recipe.")

    ingredient_in_recipe.delete()
    return HttpResponse(status=200)  # Empty response with status 204

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

# Meal plan views
@login_required
def mealplan_list(request):
    mealplans = MealPlan.objects.filter(user=request.user)

    context = {
        'active_path': 'mealplans',
        'mealplans': mealplans,
    }

    return render(request, 'mealplanner/mealplan_list.html', context)

@login_required
def mealplan_detail(request, mealplan_id):
    # Fetch the meal plan or return a 404 if it doesn't exist
    mealplan = get_object_or_404(MealPlan, id=mealplan_id)

    # Ensure the user can only view their own meal plans
    if mealplan.user != request.user:
        return HttpResponseForbidden("You are not allowed to view this meal plan.")
    
    # Get the meal plan items associated with this meal plan
    mealplanitems = MealPlanItem.objects.filter(meal_plan=mealplan)

    # Aggregate ingredients for the shopping list
    shopping_list = (
        IngredientInRecipe.objects
        .filter(recipe__meal_plan_items__meal_plan=mealplan)
        .values('ingredient__name', 'ingredient__measurement_unit')
        .annotate(total_amount=Sum('measurement_amount'))
        .order_by('ingredient__name')
    )

    WEEKDAY_CHOICES = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]

    context = {
        'active_path': 'mealplans',
        'mealplan': mealplan,
        'mealplanitems': mealplanitems,
        'weekdays': WEEKDAY_CHOICES,
        'shopping_list': shopping_list,
    }

    return render(request, 'mealplanner/mealplan_detail.html', context)

@csrf_exempt
def mealplan_edit(request, mealplan_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            meal_plan_items = data.get('meal_plan_items', [])

            # Update each MealPlanItem's weekday
            for item in meal_plan_items:
                try:
                    meal_item = MealPlanItem.objects.get(id=item['id'])
                    meal_item.weekday = item['weekday']
                    meal_item.save()
                except MealPlanItem.DoesNotExist:
                    continue

            return JsonResponse({"status": "success"})
        except:
            return JsonResponse({"status": "error"}, status=400)

    elif request.method == "GET":
        # Fetch the meal plan or return a 404 if it doesn't exist
        mealplan = get_object_or_404(MealPlan, id=mealplan_id)

        # Ensure the user can only view their own meal plans
        if mealplan.user != request.user:
            return HttpResponseForbidden("You are not allowed to view this meal plan.")
        
        # Get the meal plan items associated with this meal plan
        mealplanitems = MealPlanItem.objects.filter(meal_plan=mealplan)

        WEEKDAY_CHOICES = [
            (0, 'Monday'),
            (1, 'Tuesday'),
            (2, 'Wednesday'),
            (3, 'Thursday'),
            (4, 'Friday'),
            (5, 'Saturday'),
            (6, 'Sunday'),
        ]

        context = {
            'active_path': 'mealplans',
            'mealplan': mealplan,
            'mealplan_recipe_form': MealplanRecipeForm(),
            'mealplanitems': mealplanitems,
            'weekdays': WEEKDAY_CHOICES,
        }

        return render(request, 'mealplanner/mealplan_edit.html', context)