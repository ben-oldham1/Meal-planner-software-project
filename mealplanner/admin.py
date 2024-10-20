from django.contrib import admin
from .models import Recipe, Ingredient, IngredientInRecipe, Tag, RecipeTag, MealPlan, MealPlanItem

# Custom admin for IngredientInRecipe to display related ingredient and recipe names
class IngredientInRecipeInline(admin.TabularInline):
    model = IngredientInRecipe
    extra = 1  # How many empty ingredient slots to show for adding

# Custom admin for MealPlanItem to display related recipe names
class MealPlanItemInline(admin.TabularInline):
    model = MealPlanItem
    extra = 1  # How many empty meal plan slots to show for adding

# Recipe admin configuration
@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'difficulty', 'time_needed', 'public')
    list_filter = ('difficulty', 'public')
    search_fields = ('name', 'instructions')
    inlines = [IngredientInRecipeInline]  # Allow adding ingredients directly in the Recipe admin

# Ingredient admin configuration
@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)

# IngredientInRecipe admin configuration (if you want it standalone, otherwise it's inline in Recipe)
@admin.register(IngredientInRecipe)
class IngredientInRecipeAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'measurement_amount', 'calories', 'fat', 'carbs', 'protein')
    search_fields = ('recipe__name', 'ingredient__name')
    list_filter = ('recipe', 'ingredient')

# Tag admin configuration
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# RecipeTag admin configuration
@admin.register(RecipeTag)
class RecipeTagAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'tag')
    list_filter = ('recipe', 'tag')

# MealPlan admin configuration
@admin.register(MealPlan)
class MealPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ('name', 'user__username')
    inlines = [MealPlanItemInline]  # Allow adding MealPlanItems directly in the MealPlan admin

# MealPlanItem admin configuration (if you want it standalone, otherwise it's inline in MealPlan)
@admin.register(MealPlanItem)
class MealPlanItemAdmin(admin.ModelAdmin):
    list_display = ('meal_plan', 'recipe', 'weekday')
    list_filter = ('meal_plan', 'weekday')
