from django import forms
from .models import Recipe, IngredientInRecipe, Tag

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'difficulty', 'time_needed', 'public', 'image_url', 'instructions']

class IngredientForm(forms.ModelForm):
    class Meta:
        model = IngredientInRecipe
        fields = ['ingredient', 'measurement_amount', 'calories', 'fat', 'carbs', 'protein']

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']