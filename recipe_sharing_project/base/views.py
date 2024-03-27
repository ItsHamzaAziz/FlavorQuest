from django.shortcuts import render, redirect
from recipe.models import Recipe

# Index or home page of website
def index(request):
    if request.method == 'POST':
        name = request.POST['name']
        return redirect('search', name)

    return render(request, 'base/index.html', {
        'title': 'FlavorQuest',
        'recipes': Recipe.objects.all().order_by('-created_at')[:12]    # Fetching latest 12 recipes
    })

# When page is not found or user enters an invalid url
def error_404(request):
    return render(request, 'base/404.html')

