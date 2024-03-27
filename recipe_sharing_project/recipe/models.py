from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel

# Create your models here.
class Cuisine(BaseModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Cuisine'
        verbose_name = 'Cuisine'
        verbose_name_plural = 'Cuisines'

class Recipe(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    name = models.CharField(max_length=50)
    calories = models.IntegerField()
    total_time_in_minutes = models.IntegerField()
    total_ingredients = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='recipe_images', max_length=250, null=True, default=None)
    cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE, related_name='cuisine')

    def total_time_in_hours(self):
        hours = int(self.total_time_in_minutes / 60)    # Typecasting to get the number of hours as it is an integer value
        remaining_minutes = self.total_time_in_minutes % 60     # Remiander will give us remaining minutes
        final_time = ''     # Final time is initially an empty string. It'll be appended it as necessary

        if hours == 1:
            final_time += '1 hour'
        else:
            final_time += f'{hours} hours'
        
        # If remaining minutes are zero then there is no need to display them
        if remaining_minutes == 0:
            return final_time
        elif remaining_minutes == 1:
            final_time += ' 1 minute'
        else:
            final_time += f' {remaining_minutes} minutes'

        return final_time
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'Recipe'
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'


class SavedRecipe(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_saved_recipe')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_saved_recipe')

    class Meta:
        db_table = 'SavedRecipe'
        verbose_name = 'SavedRecipe'
        verbose_name_plural = 'SavedRecipes'

    def __str__(self):
        return f'{self.recipe.name}: {self.user.username}'


