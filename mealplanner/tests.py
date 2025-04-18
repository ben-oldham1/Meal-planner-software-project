from django.test import TestCase
from django.contrib.auth.models import User
from django.db.models import Sum
from datetime import timedelta
from .models import Recipe, RecipeNutrition, Ingredient, IngredientInRecipe, Tag, RecipeTag, MealPlan, MealPlanItem
from .views import get_nutrition_data
import os
from dotenv import load_dotenv

# Run tests using command: python manage.py test

# Test cases for the Recipe model
class RecipeModelTest(TestCase):
    def setUp(self):
        # Set up a user and a recipe instance for testing
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.recipe = Recipe.objects.create(
            user=self.user,
            name='Test Recipe',
            difficulty=1,
            time_needed=timedelta(minutes=30),
            public=True,
            image_url='http://example.com/image.jpg',
            instructions='Test instructions'
        )

    def test_recipe_creation(self):
        # Test that the recipe is created with the correct attributes
        self.assertEqual(self.recipe.name, 'Test Recipe')
        self.assertEqual(self.recipe.difficulty, 1)
        self.assertEqual(self.recipe.time_needed, timedelta(minutes=30))
        self.assertTrue(self.recipe.public)
        self.assertEqual(self.recipe.image_url, 'http://example.com/image.jpg')
        self.assertEqual(self.recipe.instructions, 'Test instructions')

    def test_recipe_str(self):
        # Test the string representation of the recipe
        self.assertEqual(str(self.recipe), 'Test Recipe')

# Test cases for the RecipeNutrition model
class RecipeNutritionModelTest(TestCase):
    def setUp(self):
        # Set up a user, recipe, and recipe nutrition instance for testing
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.recipe = Recipe.objects.create(
            user=self.user,
            name='Test Recipe',
            difficulty=1,
            time_needed=timedelta(minutes=30),
            public=True,
            image_url='http://example.com/image.jpg',
            instructions='Test instructions'
        )
        self.recipe_nutrition = RecipeNutrition.objects.create(
            recipe=self.recipe,
            calories=200.0,
            calorie_colour=1,
            fat=10.0,
            fat_colour=2,
            carbs=30.0,
            carbs_colour=3,
            protein=15.0,
            protein_colour=1
        )

    def test_recipe_nutrition_creation(self):
        # Test that the recipe nutrition is created with the correct attributes
        self.assertEqual(self.recipe_nutrition.calories, 200.0)
        self.assertEqual(self.recipe_nutrition.calorie_colour, 1)
        self.assertEqual(self.recipe_nutrition.fat, 10.0)
        self.assertEqual(self.recipe_nutrition.fat_colour, 2)
        self.assertEqual(self.recipe_nutrition.carbs, 30.0)
        self.assertEqual(self.recipe_nutrition.carbs_colour, 3)
        self.assertEqual(self.recipe_nutrition.protein, 15.0)
        self.assertEqual(self.recipe_nutrition.protein_colour, 1)

    def test_recipe_nutrition_str(self):
        # Test the string representation of the recipe nutrition
        self.assertEqual(str(self.recipe_nutrition), 'Test Recipe Nutrition')

# Test cases for the Ingredient model
class IngredientModelTest(TestCase):
    def setUp(self):
        # Set up an ingredient instance for testing
        self.ingredient = Ingredient.objects.create(
            name='Test Ingredient',
            measurement_unit='g'
        )

    def test_ingredient_creation(self):
        # Test that the ingredient is created with the correct attributes
        self.assertEqual(self.ingredient.name, 'Test Ingredient')
        self.assertEqual(self.ingredient.measurement_unit, 'g')

    def test_ingredient_str(self):
        # Test the string representation of the ingredient
        self.assertEqual(str(self.ingredient), 'Test Ingredient')

# Test cases for the IngredientInRecipe model
class IngredientInRecipeModelTest(TestCase):
    def setUp(self):
        # Set up a user, recipe, ingredient, and ingredient-in-recipe instance for testing
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.recipe = Recipe.objects.create(
            user=self.user,
            name='Test Recipe',
            difficulty=1,
            time_needed=timedelta(minutes=30),
            public=True,
            image_url='http://example.com/image.jpg',
            instructions='Test instructions'
        )
        self.ingredient = Ingredient.objects.create(
            name='Test Ingredient',
            measurement_unit='g'
        )
        self.ingredient_in_recipe = IngredientInRecipe.objects.create(
            ingredient=self.ingredient,
            recipe=self.recipe,
            measurement_amount=100.0
        )

    def test_ingredient_in_recipe_creation(self):
        # Test that the ingredient-in-recipe is created with the correct attributes
        self.assertEqual(self.ingredient_in_recipe.ingredient, self.ingredient)
        self.assertEqual(self.ingredient_in_recipe.recipe, self.recipe)
        self.assertEqual(self.ingredient_in_recipe.measurement_amount, 100.0)

    def test_ingredient_in_recipe_str(self):
        # Test the string representation of the ingredient-in-recipe
        self.assertEqual(str(self.ingredient_in_recipe), '100.0 g of Test Ingredient')

# Test cases for the Tag model
class TagModelTest(TestCase):
    def setUp(self):
        # Set up a tag instance for testing
        self.tag = Tag.objects.create(name='Test Tag')

    def test_tag_creation(self):
        # Test that the tag is created with the correct attributes
        self.assertEqual(self.tag.name, 'Test Tag')

    def test_tag_str(self):
        # Test the string representation of the tag
        self.assertEqual(str(self.tag), 'Test Tag')

# Test cases for the RecipeTag model
class RecipeTagModelTest(TestCase):
    def setUp(self):
        # Set up a user, recipe, tag, and recipe-tag instance for testing
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.recipe = Recipe.objects.create(
            user=self.user,
            name='Test Recipe',
            difficulty=1,
            time_needed=timedelta(minutes=30),
            public=True,
            image_url='http://example.com/image.jpg',
            instructions='Test instructions'
        )
        self.tag = Tag.objects.create(name='Test Tag')
        self.recipe_tag = RecipeTag.objects.create(recipe=self.recipe, tag=self.tag)

    def test_recipe_tag_creation(self):
        # Test that the recipe-tag is created with the correct attributes
        self.assertEqual(self.recipe_tag.recipe, self.recipe)
        self.assertEqual(self.recipe_tag.tag, self.tag)

    def test_recipe_tag_str(self):
        # Test the string representation of the recipe-tag
        self.assertEqual(str(self.recipe_tag), 'Test Tag')

# Test cases for the MealPlan model
class MealPlanModelTest(TestCase):
    def setUp(self):
        # Set up a user and meal plan instance for testing
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.meal_plan = MealPlan.objects.create(user=self.user, name='Test Meal Plan')

    def test_meal_plan_creation(self):
        # Test that the meal plan is created with the correct attributes
        self.assertEqual(self.meal_plan.name, 'Test Meal Plan')

    def test_meal_plan_str(self):
        # Test the string representation of the meal plan
        self.assertEqual(str(self.meal_plan), 'Test Meal Plan')

# Test cases for the MealPlanItem model
class MealPlanItemModelTest(TestCase):
    def setUp(self):
        # Set up a user, meal plan, recipe, and meal plan item instance for testing
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.meal_plan = MealPlan.objects.create(user=self.user, name='Test Meal Plan')
        self.recipe = Recipe.objects.create(
            user=self.user,
            name='Test Recipe',
            difficulty=1,
            time_needed=timedelta(minutes=30),
            public=True,
            image_url='http://example.com/image.jpg',
            instructions='Test instructions'
        )
        self.meal_plan_item = MealPlanItem.objects.create(
            meal_plan=self.meal_plan,
            recipe=self.recipe,
            weekday=0
        )

    def test_meal_plan_item_creation(self):
        # Test that the meal plan item is created with the correct attributes
        self.assertEqual(self.meal_plan_item.meal_plan, self.meal_plan)
        self.assertEqual(self.meal_plan_item.recipe, self.recipe)
        self.assertEqual(self.meal_plan_item.weekday, 0)

    def test_meal_plan_item_str(self):
        # Test the string representation of the meal plan item
        self.assertEqual(str(self.meal_plan_item), 'Test Meal Plan - Test Recipe on Monday')

# Integration tests for views in the MealPlanner app
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Recipe, MealPlan, MealPlanItem

class MealPlannerTests(TestCase):
    def setUp(self):
        # Set up a client, user, meal plan, recipe, and meal plan item for testing
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.mealplan = MealPlan.objects.create(user=self.user, name='Test MealPlan')
        self.recipe = Recipe.objects.create(
            user=self.user,
            name='Test Recipe',
            difficulty=1,
            time_needed=timedelta(minutes=30),
            public=True,
            image_url='http://example.com/image.jpg',
            instructions='Test instructions'
        )
        self.mealplan_item = MealPlanItem.objects.create(
            meal_plan=self.mealplan,
            recipe=self.recipe,
            weekday=0
        )

    def test_recipe_list_view(self):
        # Test the recipe list view
        response = self.client.get(reverse('recipe_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Recipe')

    def test_recipe_detail_view(self):
        # Test the recipe detail view
        response = self.client.get(reverse('recipe_detail', args=[self.recipe.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Recipe')

    def test_add_recipe_view(self):
        # Test the add recipe view
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('add_recipe'), {'name': 'New Recipe', 'public': True})
        self.assertEqual(response.status_code, 302)  # Redirect after successful post

    def test_mealplan_list_view(self):
        # Test the meal plan list view
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('mealplan_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test MealPlan')

    def test_mealplan_detail_view(self):
        # Test the meal plan detail view
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('mealplan_detail', args=[self.mealplan.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test MealPlan')

    def test_add_mealplan_view(self):
        # Test the add meal plan view
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('add_mealplan'), {'name': 'New MealPlan'})
        self.assertEqual(response.status_code, 302)  # Redirect after successful post

class APITestCase(TestCase):
    def test_get_nutrition_data_live(self):
        # Load environment variables from env file
        load_dotenv()

        # Call the actual API with a sample query
        app_id = 'd360df73'  # Replace with your actual app ID
        app_key = '58f5b744482f26ff48588149cb1508bb'  # Replace with your actual app key
        query = '1 apple'

        result = get_nutrition_data(query, os.getenv('APP_ID'), os.getenv('APP_KEY'))

        # Assert the response is valid
        self.assertIsNotNone(result)
        self.assertIn('foods', result)
        self.assertGreater(len(result['foods']), 0)
        self.assertIn('food_name', result['foods'][0])
        self.assertEqual(result['foods'][0]['food_name'].lower(), 'apple')

class ShoppingListTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='12345')

        # Create ingredients
        self.ingredient1 = Ingredient.objects.create(name='Flour', measurement_unit='g')
        self.ingredient2 = Ingredient.objects.create(name='Sugar', measurement_unit='g')

        # Create a recipe
        self.recipe = Recipe.objects.create(
            user=self.user,
            name='Cake',
            difficulty=2,
            time_needed=timedelta(minutes=30),
            public=True,
            instructions='Mix and bake.'
        )

        # Add ingredients to the recipe
        IngredientInRecipe.objects.create(recipe=self.recipe, ingredient=self.ingredient1, measurement_amount=200)
        IngredientInRecipe.objects.create(recipe=self.recipe, ingredient=self.ingredient2, measurement_amount=100)

        # Create a meal plan
        self.meal_plan = MealPlan.objects.create(user=self.user, name='Weekly Plan')

        # Add the recipe to the meal plan
        MealPlanItem.objects.create(meal_plan=self.meal_plan, recipe=self.recipe, weekday=0)

    def test_aggregate_shopping_list(self):
        # Aggregate ingredients for the shopping list
        shopping_list = (
            IngredientInRecipe.objects
            .filter(recipe__meal_plan_items__meal_plan=self.meal_plan)
            .values('ingredient__name', 'ingredient__measurement_unit')
            .annotate(total_amount=Sum('measurement_amount'))
            .order_by('ingredient__name')
        )

        # Expected results
        expected_shopping_list = [
            {'ingredient__name': 'Flour', 'ingredient__measurement_unit': 'g', 'total_amount': 200},
            {'ingredient__name': 'Sugar', 'ingredient__measurement_unit': 'g', 'total_amount': 100},
        ]

        # Assert the aggregated shopping list matches the expected results
        self.assertEqual(list(shopping_list), expected_shopping_list)