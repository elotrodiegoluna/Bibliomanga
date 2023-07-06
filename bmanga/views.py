from django.shortcuts import render
from django.db.models import Avg, Q

from mangas.models import MangaDigital
from users.models import Review, MangaUsuario
from store.models import Producto

# Create your views here.
def index(request):
    context = {} 
    manga = None
    try:
        manga = MangaDigital.objects.all()
    except:
        pass

    productos_nuevos = Producto.objects.order_by('-timestamp').distinct()[:8]

    mangas_nuevos = MangaDigital.objects.order_by('-timestamp').distinct()[:8]
    cmangas_nuevos = MangaUsuario.objects.order_by('-timestamp').distinct()[:8]
    mangas_valor = (
        MangaDigital.objects
        .filter(tomo=1)  # Filtrar por tomo igual a 1
        .order_by('-promedio_puntuacion')
        .distinct()
        [:8]
    )
    cmangas_valor = (
        MangaUsuario.objects
        .order_by('-promedio_puntuacion')
        .distinct()
        [:8]
    )

    for manga in mangas_nuevos:
        mangas_con_mismo_nombre = MangaDigital.objects.filter(nombre=manga.nombre)
        promedio_puntuacion = Review.objects.filter(manga__in=mangas_con_mismo_nombre, manga__tomo=1).aggregate(promedio=Avg('puntuacion'))['promedio']
        if promedio_puntuacion:
            mangas_con_mismo_nombre.update(promedio_puntuacion=promedio_puntuacion)


    context = {
        'mangas': manga,
        'mangas_nuevos': mangas_nuevos,
        'mangas_valor': mangas_valor,
        'cmangas_nuevos': cmangas_nuevos,
        'cmangas_valor': cmangas_valor,
        'productos_nuevos': productos_nuevos,
    }
    return render(request, 'index.html', context)

def login(request):
    return render(request, 'login.html')