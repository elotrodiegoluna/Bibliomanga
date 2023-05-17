from django.shortcuts import render
from store.models import Manga

# Create your views here.
def index(request):
    context = {}
    manga = Manga.objects.filter(digital=True)

    context = {
        'mangas': manga
    }
    return render(request, 'index.html', context)

def login(request):
    return render(request, 'login.html')