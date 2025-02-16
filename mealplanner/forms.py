from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Recipe, MealPlan, RecipeNutrition, IngredientInRecipe, Tag, MealPlanItem

# New recipe
class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'difficulty', 'time_needed', 'public', 'image_url']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Save Changes', css_class='btn btn-primary'))

# New mealplan
class MealPlanForm(forms.ModelForm):
    class Meta:
        model = MealPlan
        fields = ['name']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Save Changes', css_class='btn btn-primary'))

# Edit recipe nutrition
class RecipeNutritionForm(forms.ModelForm):
    class Meta:
        model = RecipeNutrition
        fields = ['calories', 'calorie_colour', 'fat', 'fat_colour', 'carbs', 'carbs_colour', 'protein', 'protein_colour']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Save Changes', css_class='btn btn-primary'))

        # Give more useful labels
        self.fields['calories'].label = "Calories (Kcal)"
        self.fields['fat'].label = "Total fat (grams)"
        self.fields['carbs'].label = "Total carbs (grams)"
        self.fields['protein'].label = "Protein (grams)"

# Edit recipe instructions
class RecipeInstructionsForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['instructions']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Save Changes', css_class='btn btn-primary'))

class IngredientForm(forms.ModelForm):
    class Meta:
        model = IngredientInRecipe
        fields = ['ingredient', 'measurement_amount']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Add Ingredient', css_class='btn btn-secondary'))

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Add Tag', css_class='btn btn-secondary'))

# Add recipe to mealplan
class MealplanRecipeForm(forms.ModelForm):
    class Meta:
        model = MealPlanItem
        fields = ['recipe']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Add Tag', css_class='btn btn-secondary'))
