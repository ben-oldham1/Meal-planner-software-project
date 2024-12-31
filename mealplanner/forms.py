from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Recipe, IngredientInRecipe, Tag

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
        fields = ['ingredient', 'measurement_amount', 'calories', 'fat', 'carbs', 'protein']
    
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
