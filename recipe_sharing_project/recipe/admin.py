from django.contrib import admin
from .models import *

# Register your models here.
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'calories']
    list_per_page = 15

admin.site.register(Cuisine)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(SavedRecipe)
