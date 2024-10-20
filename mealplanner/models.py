# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# Constants for choices
DIFFICULTY_CHOICES = [
    (1, 'Easy'),
    (2, 'Medium'),
    (3, 'Hard')
]

WEEKDAY_CHOICES = [
    (0, 'Monday'),
    (1, 'Tuesday'),
    (2, 'Wednesday'),
    (3, 'Thursday'),
    (4, 'Friday'),
    (5, 'Saturday'),
    (6, 'Sunday'),
]

MEASUREMENT_UNITS = [
    ('g', 'grams'),
    ('ml', 'milliliters'),
    ('unit', 'units'),
]

class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    name = models.CharField(max_length=255)
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES)
    time_needed = models.DurationField()  # Stores time in hours, minutes, etc.
    public = models.BooleanField(default=False)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    instructions = models.TextField()

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    measurement_unit = models.CharField(max_length=10, choices=MEASUREMENT_UNITS)

    def __str__(self):
        return self.name

class IngredientInRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='ingredient_recipes')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_ingredients')
    measurement_amount = models.FloatField()
    calories = models.FloatField()
    fat = models.FloatField()
    carbs = models.FloatField()
    protein = models.FloatField()

    def __str__(self):
        return f"{self.measurement_amount} {self.ingredient.measurement_unit} of {self.ingredient.name}"

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class RecipeTag(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='recipes')

    class Meta:
        unique_together = ('recipe', 'tag')  # Ensure a recipe can't have the same tag twice

    def __str__(self):
        return f"{self.tag.name}"

class MealPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meal_plans')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class MealPlanItem(models.Model):
    meal_plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name='meal_plan_items')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='meal_plan_items')
    weekday = models.IntegerField(choices=WEEKDAY_CHOICES)

    def __str__(self):
        return f"{self.meal_plan.name} - {self.recipe.name} on {self.get_weekday_display()}"
