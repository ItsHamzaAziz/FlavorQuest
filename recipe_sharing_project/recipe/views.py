from django.shortcuts import render, redirect
from .models import Recipe, Cuisine, SavedRecipe
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def add_recipe(request):
    try:
        if request.method == 'POST':
            name = request.POST['name']
            total_ingredients = int(request.POST['total_ingredients'])
            calories = int(request.POST['calories'])
            total_time = int(request.POST['total_time'])
            description = request.POST['description']
            image = request.FILES['image']
            cuisine = request.POST['cuisine']

            image_name = image.name
            extension = image_name.split('.')[-1]

            if extension not in ['jpg', 'jpeg', 'png', 'svg', 'webp']:
                messages.info(request, 'Invalid file. Select an image.')
                return render(request, 'recipe/add.html', {
                    'data': True,
                    'title': 'Add Recipe',
                    'name': name,
                    'total_ingredients': total_ingredients,
                    'calories': calories,
                    'total_time': total_time,
                    'description': description,
                    'cuisine_selected': cuisine,
                    'cuisines': Cuisine.objects.all()
                })

            selected_cuisine = Cuisine.objects.get(name=cuisine)
            user = request.user

            recipe = Recipe(user=user, name=name, calories=calories, total_time_in_minutes=total_time, total_ingredients=total_ingredients, description=description, image=image, cuisine=selected_cuisine)
            recipe.save()

            messages.success(request, 'Recipe added successfully')
            return render(request, 'recipe/add.html', {
                'data': False,
                'title': 'Add Recipe',
                'cuisines': Cuisine.objects.all()
            })


        return render(request, 'recipe/add.html', {
            'data': False,
            'title': 'Add Recipe',
            'cuisines': Cuisine.objects.all()
        })

    except:
        messages.info(request, 'An error occured')
        return redirect('add_recipe')


@login_required
def edit_recipe(request, pk):
    try:
        recipe = Recipe.objects.get(pk=pk)

        if request.method == 'POST':
            name = request.POST['name']
            total_ingredients = int(request.POST['total_ingredients'])
            calories = int(request.POST['calories'])
            total_time = int(request.POST['total_time'])
            description = request.POST['description']
            image = request.FILES.get('image')
            cuisine = request.POST['cuisine']

            if image:
                image_name = image.name
                extension = image_name.split('.')[-1]

                if extension not in ['jpg', 'jpeg', 'png', 'svg', 'webp']:
                    messages.info(request, 'Invalid file. Select an image.')
                    return render(request, 'recipe/edit.html', {
                        'data': True,
                        'title': 'Add Recipe',
                        'name': name,
                        'total_ingredients': total_ingredients,
                        'calories': calories,
                        'total_time': total_time,
                        'description': description,
                        'cuisine_selected': cuisine,
                        'cuisines': Cuisine.objects.all(),
                        'recipe': recipe
                    })
                    

                selected_cuisine = Cuisine.objects.get(name=cuisine)

                recipe.name = name
                recipe.calories = calories
                recipe.total_time_in_minutes = total_time
                recipe.description = description
                recipe.total_ingredients = total_ingredients
                recipe.cuisine = selected_cuisine
                recipe.image = image
                recipe.save()

                messages.success(request, 'Recipe updated successfully')
                return render(request, 'recipe/edit.html', {
                    'data': False,
                    'title': 'Add Recipe',
                    'cuisines': Cuisine.objects.all(),
                    'recipe': recipe
                })
            else:
                selected_cuisine = Cuisine.objects.get(name=cuisine)

                recipe.name = name
                recipe.calories = calories
                recipe.total_time_in_minutes = total_time
                recipe.description = description
                recipe.total_ingredients = total_ingredients
                recipe.cuisine = selected_cuisine
                recipe.save()


                messages.success(request, 'Recipe updated successfully')
                return render(request, 'recipe/edit.html', {
                    'data': False,
                    'title': 'Add Recipe',
                    'cuisines': Cuisine.objects.all(),
                    'recipe': recipe
                })

        return render(request, 'recipe/edit.html', {
            'data': False,
            'title': 'Add Recipe',
            'cuisines': Cuisine.objects.all(),
            'recipe': recipe
        })
    except:
        return redirect('home')


@login_required
def delete_recipe(request, pk):
    try:
        recipe = Recipe.objects.get(pk=pk)
        recipe.delete()
        return redirect('my_recipes')
    except:
        return redirect('home')


def recipe_details(request, pk):
    try:
        recipe = Recipe.objects.get(pk=pk)
        saved=False

        if request.user.is_authenticated:
            if SavedRecipe.objects.filter(recipe=recipe, user=request.user).exists():
                saved = True

        return render(request, 'recipe/details.html', {
            'recipe': recipe,
            'title': recipe.name,
            'saved': saved
        })
    except:
        return redirect('home')


def search_recipe(request):
    try:
        if request.method == 'GET':
            name = request.GET.get('name', '')    
            recipes = Recipe.objects.filter(name__icontains=name)
            return render(request, 'recipe/search.html', {
                'title': 'Search Recipe',
                'recipes': recipes,
                'name': name
            })
    except:
        return redirect('home')

def filter_recipes(request):
    try:
        if request.method == 'POST':
            cuisine_name = request.POST['cuisine']
            calories = request.POST['calories']
            total_time = request.POST['total_time']
            total_ingredients = request.POST['total_ingredients']

            recipes = Recipe.objects.all()

            if cuisine_name != '' and cuisine_name != 'any':
                cuisine = Cuisine.objects.get(name=cuisine_name)
                recipes = Recipe.objects.filter(cuisine=cuisine)

            if calories != 'any' and '+' not in calories and calories != '':
                ll_calories, ul_calories = int(calories.split('-')[0]), int(calories.split('-')[1])
            if total_time != 'any' and '+' not in total_time and total_time != '':
                ll_total_time, ul_total_time = int(total_time.split('-')[0]), int(total_time.split('-')[1])
            if total_ingredients != 'any' and '+' not in total_ingredients and total_ingredients != '':
                ll_total_ingredeients, ul_total_ingredients = int(total_ingredients.split('-')[0]), int(total_ingredients.split('-')[1])

            if calories != 'any' and '+' not in calories and calories != '':
                recipes = recipes.filter(calories__gte=ll_calories, calories__lte=ul_calories)
            elif '+' in calories:
                recipes = recipes.filter(calories__gt=500)
            
            if total_time != 'any' and '+' not in total_time and total_time != '':
                recipes = recipes.filter(total_time_in_minutes__gte=ll_total_time, total_time_in_minutes__lte=ul_total_time)
            elif '+' in total_time:
                recipes = recipes.filter(total_time_in_minutes__gt=60)
            
            if total_ingredients != 'any' and '+' not in total_ingredients and total_ingredients != '':
                recipes = recipes.filter(total_ingredients__gte=ll_total_ingredeients, total_ingredients__lte=ul_total_ingredients)
            elif '+' in total_ingredients:
                recipes = recipes.filter(total_ingredients__gt=20)

            return render(request, 'recipe/filter.html', {
                'title': 'Filter Recipes',
                'cuisines': Cuisine.objects.all(),
                'filtered': True,
                'recipes': recipes
            })

        return render(request, 'recipe/filter.html', {
            'title': 'Filter Recipes',
            'cuisines': Cuisine.objects.all(),
            'filtered': False
        })
    except:
        return redirect('filter')


@login_required
def save_recipe(request, pk):
    try:
        recipe = Recipe.objects.get(pk=pk)

        saved_recipe = SavedRecipe(recipe=recipe, user=request.user)
        saved_recipe.save()

        messages.success(request, 'Recipe Saved.')
        return redirect('recipe_details', pk)
    except:
        return redirect('home')


@login_required
def unsave_recipe(request, pk):
    try:
        recipe = Recipe.objects.get(pk=pk)
        saved_recipe = SavedRecipe.objects.get(recipe=recipe, user=request.user)
        saved_recipe.delete()

        messages.success(request, 'Recipe Unsaved.')
        return redirect('recipe_details', pk)
    except:
        return redirect('home')
    

@login_required
def my_recipes(request):
    try:
        recipes = Recipe.objects.filter(user=request.user).order_by('-created_at')
        return render(request, 'recipe/myrecipes.html', {
            'title': 'My Recipes',
            'recipes': recipes
        })
    except:
        return redirect('home')


@login_required
def saved_recipes(request):
    try:
        recipes = request.user.user_saved_recipe.all().order_by('-created_at')
        return render(request, 'recipe/savedrecipes.html', {
            'title': 'Saved Recipes',
            'recipes': recipes
        })
    except:
        return redirect('home')





