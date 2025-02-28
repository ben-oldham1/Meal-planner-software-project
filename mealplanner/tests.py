from django.test import TestCase
from unittest.mock import patch
from django.contrib.auth.models import User
from datetime import timedelta
import time
from .models import Recipe, RecipeNutrition, Ingredient, IngredientInRecipe, Tag, RecipeTag, MealPlan, MealPlanItem

# Run tests using command: python manage.py test

class RecipeModelTest(TestCase):
    def setUp(self):
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
        self.assertEqual(self.recipe.name, 'Test Recipe')
        self.assertEqual(self.recipe.difficulty, 1)
        self.assertEqual(self.recipe.time_needed, timedelta(minutes=30))
        self.assertTrue(self.recipe.public)
        self.assertEqual(self.recipe.image_url, 'http://example.com/image.jpg')
        self.assertEqual(self.recipe.instructions, 'Test instructions')

    def test_recipe_str(self):
        self.assertEqual(str(self.recipe), 'Test Recipe')

class RecipeNutritionModelTest(TestCase):
    def setUp(self):
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
        self.assertEqual(self.recipe_nutrition.calories, 200.0)
        self.assertEqual(self.recipe_nutrition.calorie_colour, 1)
        self.assertEqual(self.recipe_nutrition.fat, 10.0)
        self.assertEqual(self.recipe_nutrition.fat_colour, 2)
        self.assertEqual(self.recipe_nutrition.carbs, 30.0)
        self.assertEqual(self.recipe_nutrition.carbs_colour, 3)
        self.assertEqual(self.recipe_nutrition.protein, 15.0)
        self.assertEqual(self.recipe_nutrition.protein_colour, 1)

    def test_recipe_nutrition_str(self):
        self.assertEqual(str(self.recipe_nutrition), 'Test Recipe Nutrition')

class IngredientModelTest(TestCase):
    def setUp(self):
        self.ingredient = Ingredient.objects.create(
            name='Test Ingredient',
            measurement_unit='g'
        )

    def test_ingredient_creation(self):
        self.assertEqual(self.ingredient.name, 'Test Ingredient')
        self.assertEqual(self.ingredient.measurement_unit, 'g')

    def test_ingredient_str(self):
        self.assertEqual(str(self.ingredient), 'Test Ingredient')

class IngredientInRecipeModelTest(TestCase):
    def setUp(self):
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
        self.assertEqual(self.ingredient_in_recipe.ingredient, self.ingredient)
        self.assertEqual(self.ingredient_in_recipe.recipe, self.recipe)
        self.assertEqual(self.ingredient_in_recipe.measurement_amount, 100.0)

    def test_ingredient_in_recipe_str(self):
        self.assertEqual(str(self.ingredient_in_recipe), '100.0 g of Test Ingredient')

class TagModelTest(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name='Test Tag')

    def test_tag_creation(self):
        self.assertEqual(self.tag.name, 'Test Tag')

    def test_tag_str(self):
        self.assertEqual(str(self.tag), 'Test Tag')

class RecipeTagModelTest(TestCase):
    def setUp(self):
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
        self.assertEqual(self.recipe_tag.recipe, self.recipe)
        self.assertEqual(self.recipe_tag.tag, self.tag)

    def test_recipe_tag_str(self):
        self.assertEqual(str(self.recipe_tag), 'Test Tag')

class MealPlanModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.meal_plan = MealPlan.objects.create(user=self.user, name='Test Meal Plan')

    def test_meal_plan_creation(self):
        self.assertEqual(self.meal_plan.name, 'Test Meal Plan')

    def test_meal_plan_str(self):
        self.assertEqual(str(self.meal_plan), 'Test Meal Plan')

class MealPlanItemModelTest(TestCase):
    def setUp(self):
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
        self.assertEqual(self.meal_plan_item.meal_plan, self.meal_plan)
        self.assertEqual(self.meal_plan_item.recipe, self.recipe)
        self.assertEqual(self.meal_plan_item.weekday, 0)

    def test_meal_plan_item_str(self):
        self.assertEqual(str(self.meal_plan_item), 'Test Meal Plan - Test Recipe on Monday')

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Recipe, MealPlan, MealPlanItem

class MealPlannerTests(TestCase):
    def setUp(self):
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
        response = self.client.get(reverse('recipe_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Recipe')

    def test_recipe_detail_view(self):
        response = self.client.get(reverse('recipe_detail', args=[self.recipe.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Recipe')

    def test_add_recipe_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('add_recipe'), {
            'name': 'Test Recipe',
            'difficulty': 1,
            'time_needed': '00:30:00',
            'public': 'True',
            'image_url': 'http://example.com/image.jpg'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful post

    def test_mealplan_list_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('mealplan_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test MealPlan')

    def test_mealplan_detail_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('mealplan_detail', args=[self.mealplan.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test MealPlan')

    def test_add_mealplan_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('add_mealplan'), {'name': 'New MealPlan'})
        self.assertEqual(response.status_code, 302)  # Redirect after successful post

class RecipePerformanceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        for i in range(100):
            Recipe.objects.create(
                user=self.user,
                name=f'Test Recipe {i}',
                difficulty=1,
                time_needed=timedelta(minutes=30),
                public=True,
                image_url='http://example.com/image.jpg',
                instructions='Test instructions'
            )

    def test_retrieve_100_recipes(self):
        start_time = time.time()
        response = self.client.get(reverse('recipe_list'))
        end_time = time.time()
        self.assertEqual(response.status_code, 200)
        self.assertTrue((end_time - start_time) < 2)  # Ensure it takes less than 2 seconds

class ErrorHandlingTest(TestCase):
    def test_404_error(self):
        response = self.client.get('/non-existent-page/')
        self.assertEqual(response.status_code, 404)
        self.assertContains(response, 'Page not found', status_code=404)

class DashboardLoadTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_dashboard_load_time(self):
        start_time = time.time()
        response = self.client.get(reverse('recipe_list'))
        end_time = time.time()
        self.assertEqual(response.status_code, 200)
        self.assertTrue((end_time - start_time) < 3)  # Ensure it takes less than 3 seconds