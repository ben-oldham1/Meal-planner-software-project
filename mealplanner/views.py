# Import necessary modules and libraries
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.db.models import Q, Sum
from django.views.decorators.csrf import csrf_exempt
from collections import defaultdict

import json
import markdown
import requests

# Import models, forms, and filters used in the views
from .models import Recipe, RecipeNutrition, IngredientInRecipe, Ingredient, RecipeTag, Tag, MealPlan, MealPlanItem
from .forms import RecipeForm, MealPlanForm, RecipeNutritionForm, RecipeInstructionsForm, IngredientForm, TagForm, MealplanRecipeForm
from .filters import RecipeFilter

# View to list recipes with optional search and filtering
def recipe_list(request):
    # Show public recipes to non-logged-in users, and both public and user-specific recipes to logged-in users
    if request.user.is_authenticated:
        recipes = Recipe.objects.filter(user=request.user) | Recipe.objects.filter(public=True)
    else:
        recipes = Recipe.objects.filter(public=True)
    
    query = request.GET.get('q')

    # Create filters form and apply search query if provided
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

    # Render the recipe list template with the filtered recipes and context
    context = {
        'active_path': 'recipes',
        'new_recipe_form': RecipeForm(),
        'recipe_filter': recipe_filter,
        'recipes': recipes,
        'query': query,
    }

    return render(request, 'mealplanner/recipe_list.html', context)

# View to search for recipes by name
def recipe_search(request, search_query):
    # Filter recipes based on the search query and user authentication
    if request.user.is_authenticated:
        recipes = Recipe.objects.filter(user=request.user) | Recipe.objects.filter(public=True)
        recipes = recipes.filter(name=search_query)
    else:
        recipes = Recipe.objects.filter(public=True).filter(name=search_query)

    # Render the recipe list template with the search results
    context = {
        'active_path': 'recipes',
        'recipes': recipes,
    }

    return render(request, 'mealplanner/recipe_list.html', context)

# View to display the details of a specific recipe
def recipe_detail(request, recipe_id):
    # Fetch the recipe and ensure the user has permission to view it
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    # Ensure the user can only view their own recipes or public ones
    if not recipe.public and recipe.user != request.user:
        return HttpResponseForbidden("You are not allowed to view this recipe.")
    
    # Retrieve associated ingredients and nutrition data
    ingredients = IngredientInRecipe.objects.filter(recipe=recipe)

    try:
        nutrition = RecipeNutrition.objects.get(recipe=recipe)
    except:
        nutrition = None

    # Convert recipe instructions from Markdown to HTML
    md = markdown.Markdown()
    recipe.instructions = md.convert(recipe.instructions)

    # Render the recipe detail template with the recipe data
    context = {
        'active_path': 'recipes',
        'recipe': recipe,
        'ingredients': ingredients,
        'nutrition': nutrition
    }

    return render(request, 'mealplanner/recipe_detail.html', context)

# Utility function to fetch nutrition data from an external API
def get_nutrition_data(query, app_id, app_key):
    # Define the API endpoint and headers
    url = 'https://trackapi.nutritionix.com/v2/natural/nutrients'
    headers = {
        'Content-Type': 'application/json',
        'x-app-id': app_id,
        'x-app-key': app_key
    }
    body = {
        "query": query
    }

    # Make a POST request to the API and handle errors
    try:
        response = requests.post(url, headers=headers, data=json.dumps(body))
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# View to add a new recipe
@login_required
def add_recipe(request):
    # Handle form submission for creating a new recipe
    if request.method == 'POST':
        new_recipe_form = RecipeForm(request.POST)
        if new_recipe_form.is_valid():
            recipe = new_recipe_form.save(commit=False)
            recipe.user = request.user  # Associate the recipe with the logged-in user
            recipe.save()
            return redirect('edit_recipe', recipe_id=recipe.id)
    
    # Render the add recipe template with the form
    form = RecipeForm()
    return render(request, 'mealplanner/add_recipe.html', {'new_recipe_form': form})

# View to add a new meal plan
@login_required
def add_mealplan(request):
    # Handle form submission for creating a new meal plan
    if request.method == 'POST':
        new_mealplan_form = MealPlanForm(request.POST)
        if new_mealplan_form.is_valid():
            mealplan = new_mealplan_form.save(commit=False)
            mealplan.user = request.user  # Associate the recipe with the logged-in user
            mealplan.save()
            return redirect('mealplan_edit', mealplan_id=mealplan.id)
    
    # Render the add meal plan template with the form
    form = MealPlanForm()
    return render(request, 'mealplanner/add_mealplan.html', {'new_mealplan_form': form})

# View to add a recipe to a meal plan
@login_required
def add_recipe_to_mealplan(request, mealplan_id):
    # Handle form submission for adding a recipe to a meal plan
    if request.method == 'POST':
        add_recipe_form = MealplanRecipeForm(request.POST)
        if add_recipe_form.is_valid():
            mealplan_item = add_recipe_form.save(commit=False)
            mealplan_item.weekday = 0
            mealplan_item.meal_plan = MealPlan.objects.get(id=mealplan_id)
            mealplan_item.save()
    return redirect('mealplan_edit', mealplan_id=mealplan_id)

# View to edit an existing recipe
@login_required
def edit_recipe(request, recipe_id):
    # Fetch the recipe and ensure the user has permission to edit it
    recipe = get_object_or_404(Recipe, id=recipe_id)
    ingredients = Ingredient.objects.all().order_by('name')

    # Ensure the user can only edit their own recipes
    if recipe.user != request.user:
        return HttpResponseForbidden("You are not allowed to edit this recipe.")

    # Handle form submissions for updating recipe details, instructions, or nutrition
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

    # Render the edit recipe template with the forms and recipe data
    context = {
        'active_path': 'recipes',
        'recipedetailsform': recipedetailsform,
        'recipeinstructionsform': recipeinstructionsform,
        'receipenutritionform': receipenutritionform,
        'ingredients': ingredients,
        'recipe': recipe
    }

    return render(request, 'mealplanner/edit_recipe.html', context)

# Utility view to fetch nutrition data for a recipe
@login_required
def get_nutri_for_recipe(request, recipe_id):
    # Fetch the recipe and its ingredients
    recipe = get_object_or_404(Recipe, id=recipe_id)
    ingredients_in_recipe = IngredientInRecipe.objects.filter(recipe=recipe)

    APP_ID = "d360df73"  # Replace with your actual App ID
    APP_KEY = "58f5b744482f26ff48588149cb1508bb"  # Replace with your actual App Key

    # String to store the natural language list of ingredients
    ingredients_natural = ""
    
    # Iterate through ingredients and add to string
    for ingredient in ingredients_in_recipe:
        ingredients_natural += str(ingredient.measurement_amount) + ' ' + str(ingredient.ingredient.measurement_unit) + ' of ' + str(ingredient.ingredient.name) + '; '

    # Call the external API to retrieve nutrition data
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

# View to add an ingredient to a recipe
@login_required
def add_ingredient(request, recipe_id):
    # Ensure the user has permission to add ingredients to the recipe
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if recipe.user != request.user:
        return HttpResponseForbidden("You are not allowed to add ingredients to this recipe.")

    # Handle form submission for adding a new ingredient
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

# View to delete an ingredient from a recipe
@login_required
def delete_ingredient(request, ingredient_id):
    # Ensure the user has permission to delete the ingredient
    ingredient_in_recipe = get_object_or_404(IngredientInRecipe, id=ingredient_id)

    if ingredient_in_recipe.recipe.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete ingredients from this recipe.")

    # Delete the ingredient and return a success response
    ingredient_in_recipe.delete()
    return HttpResponse(status=200)  # Empty response with status 204

# View to add a tag to a recipe
@login_required
def add_tag(request, recipe_id):
    # Ensure the user has permission to add tags to the recipe
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if recipe.user != request.user:
        return HttpResponseForbidden("You are not allowed to add tags to this recipe.")

    # Handle form submission for adding a new tag
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

# View to list all meal plans for the logged-in user
@login_required
def mealplan_list(request):
    # Fetch meal plans associated with the logged-in user
    mealplans = MealPlan.objects.filter(user=request.user)

    # Render the meal plan list template with the meal plans
    context = {
        'active_path': 'mealplans',
        'new_mealplan_form': MealPlanForm(),
        'mealplans': mealplans,
    }

    return render(request, 'mealplanner/mealplan_list.html', context)

# View to display the details of a specific meal plan
@login_required
def mealplan_detail(request, mealplan_id):
    # Fetch the meal plan and ensure the user has permission to view it
    mealplan = get_object_or_404(MealPlan, id=mealplan_id)

    # Ensure the user can only view their own meal plans
    if mealplan.user != request.user:
        return HttpResponseForbidden("You are not allowed to view this meal plan.")
    
    # Retrieve associated meal plan items and aggregate shopping list data
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

    WEEKDAY_NAMES = dict(WEEKDAY_CHOICES)

    # Initialize nutrition data with all days (ensures all weekdays are included)
    nutrition_data = {day: {'calories': 0, 'fat': 0, 'carbs': 0, 'protein': 0} for day in WEEKDAY_NAMES}

    # Count occurrences of each recipe per weekday
    recipe_counts = defaultdict(lambda: defaultdict(int))  # {weekday: {recipe_id: count}}

    for item in mealplanitems:
        recipe_counts[item.weekday][item.recipe.id] += 1  # Count how many times each recipe appears

    # Populate nutrition data with correct multipliers
    for weekday, recipes in recipe_counts.items():
        for recipe_id, count in recipes.items():
            recipe_nutrition = RecipeNutrition.objects.filter(recipe_id=recipe_id).first()
            if recipe_nutrition:
                nutrition_data[weekday]['calories'] += recipe_nutrition.calories * count
                nutrition_data[weekday]['fat'] += recipe_nutrition.fat * count
                nutrition_data[weekday]['carbs'] += recipe_nutrition.carbs * count
                nutrition_data[weekday]['protein'] += recipe_nutrition.protein * count

    # Convert to list for template rendering
    nutrition_summary = [
        {'day': WEEKDAY_NAMES[day], **values} for day, values in sorted(nutrition_data.items())
    ]

    # Render the meal plan detail template with the meal plan data
    context = {
        'active_path': 'mealplans',
        'mealplan': mealplan,
        'mealplanitems': mealplanitems,
        'weekdays': WEEKDAY_CHOICES,
        'shopping_list': shopping_list,
        'nutrition_summary': nutrition_summary
    }

    return render(request, 'mealplanner/mealplan_detail.html', context)

# View to edit a meal plan
@csrf_exempt
def mealplan_edit(request, mealplan_id):
    # Handle POST requests to update meal plan items
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

    # Handle GET requests to fetch meal plan data for editing
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