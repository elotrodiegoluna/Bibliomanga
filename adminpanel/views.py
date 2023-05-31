from django.shortcuts import render
from users.models import User
from store.models import Manga

# Create your views here.
def adminmain_view(request):
    return render(request, 'admin_main.html')

def adminmangas_view(request):
    context = {}
    mangas = Manga.objects.all()

    context = {
        'mangas': mangas
    }
    return render(request, 'admin_mangas.html', context)

def adminstore_view(request):
    context = {}
    mangas = Manga.objects.all()

    context = {
        'mangas': mangas
    }
    return render(request, 'admin_store.html', context)

def adminusers_view(request):
    context = {}
    usuarios = User.objects.all()

    context = {
        'users': usuarios
    }
    print(context)
    return render(request, 'admin_users.html', context)