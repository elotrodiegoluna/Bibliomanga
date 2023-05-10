from django.shortcuts import render
from .models import Manga

# Create your views here.
def store_view(request):
    manga = Manga.objects.all()
    context = {
        'mangas': manga
    }
    return render(request, 'store.html', context)

    