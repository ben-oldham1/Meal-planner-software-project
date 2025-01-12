from django.urls import path

from . import views

urlpatterns = [
    path("", views.recipe_list, name="recipe_list"),
    path('recipes/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('recipes/add/', views.add_recipe, name='add_recipe'),
    path('recipes/edit/<int:recipe_id>/', views.edit_recipe, name='edit_recipe'),
    path('recipes/<int:recipe_id>/add_ingredient/', views.add_ingredient, name='add_ingredient'),
    path('recipes/ingredient/delete/<int:ingredient_id>/', views.delete_ingredient, name='delete_ingredient'),
    path('recipes/<int:recipe_id>/add_tag/', views.add_tag, name='add_tag'),
    path('recipes/<int:recipe_id>/nutri_data/', views.get_nutri_for_recipe, name='get_nutri_data'),
    path('mealplans/', views.mealplan_list, name='mealplan_list'),
    path('mealplans/<int:mealplan_id>/', views.mealplan_detail, name='mealplan_detail'),
    path('mealplans/edit/<int:mealplan_id>/', views.mealplan_edit, name='mealplan_edit'),
    path('mealplans/addrecipe/<int:mealplan_id>', views.add_recipe_to_mealplan, name='add_recipe_to_mealplan'),
]