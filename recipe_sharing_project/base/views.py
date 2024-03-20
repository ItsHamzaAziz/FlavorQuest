from django.shortcuts import render, redirect
from recipe.models import Recipe

def index(request):
    if request.method == 'POST':
        name = request.POST['name']
        return redirect('search', name)

    return render(request, 'base/index.html', {
        'title': 'FlavourQuest',
        'recipes': Recipe.objects.all().order_by('-created_at')[:12]
    })

def error_404(request):
    return render(request, 'base/404.html')

