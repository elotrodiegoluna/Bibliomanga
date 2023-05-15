from django.shortcuts import render
from .models import Manga

# Create your views here.
def store_view(request):
    manga = Manga.objects.all()
    context = {
        'mangas': manga
    }
    return render(request, 'store.html', context)

def product_view(request, pk):
    manga = Manga.objects.get(id=pk)
    context = {
        'mangas': manga
    }
    return render(request, 'product.html', context)

    