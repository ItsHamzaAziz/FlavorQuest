from django.urls import path
from . import views

urlpatterns = [
    path('/add', views.add_recipe, name='add_recipe'),
    path('/edit/<pk>', views.edit_recipe, name='edit_recipe'),
    path('/delete/<pk>', views.delete_recipe, name='delete_recipe'),
    path('/search', views.search_recipe, name='search'),
    path('/filter', views.filter_recipes, name='filter'),
    path('/save/<pk>', views.save_recipe, name='save_recipe'),
    path('/unsave/<pk>', views.unsave_recipe, name='unsave_recipe'),
    path('/my-recipes', views.my_recipes, name='my_recipes'),
    path('/saved-recipes', views.saved_recipes, name='saved_recipes'),
    path('/<pk>', views.recipe_details, name='recipe_details'),
]
