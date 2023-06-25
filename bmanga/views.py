from django.shortcuts import render
from mangas.models import MangaDigital

# Create your views here.
def index(request):
    context = {} 
    try:
        manga = MangaDigital.objects.all()

        context = {
            'mangas': manga
        }
    except:
        pass
    return render(request, 'index.html', context)

def login(request):
    return render(request, 'login.html')