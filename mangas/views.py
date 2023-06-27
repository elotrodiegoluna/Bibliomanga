from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Avg

from .forms import *
from .models import *
from users.models import MangaLeido, User, Review


import os

def delete_review(request, id):
    if request.user.is_authenticated:
        usuario = request.user

        review = get_object_or_404(Review, id=id)

        if review.usuario == usuario or usuario.is_staff:
            review.delete()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return redirect('index')

def mangapage_view(request, manga_name):
    context = {}

    try:
        mangas = MangaDigital.objects.filter(nombre=manga_name)
    except MangaDigital.DoesNotExist:
        # Manejar el caso en el que no se encuentre el manga
        return HttpResponse('Manga no encontrado', status=404)
    
    try:
        if request.user.is_authenticated:
            reviews = Review.objects.exclude(usuario=request.user).filter(manga__nombre=manga_name)
            user_review = Review.objects.filter(usuario=request.user, manga__nombre=manga_name).first()
            print(user_review)
            print(reviews)
        else:
            reviews = Review.objects.filter(manga__nombre=manga_name)
    except Review.DoesNotExist:
        pass
    

    if request.user.is_authenticated:
        try:
            existing_review = Review.objects.get(manga__nombre=manga_name, usuario=request.user)
            existing = True
        except Review.DoesNotExist:
            existing_review = None
            existing = False
    else:
        existing = False
    
    if request.method == 'POST':
        print('se hizo POST')
        form = ReviewForm(request.POST)
        if form.is_valid():
            print('form valido')
            if request.user.is_authenticated:
                usuario = request.user
                
                if existing_review is None:

                    titulo = form.cleaned_data['titulo']
                    comentario = form.cleaned_data['comentario']
                    rating = form.cleaned_data['rating']
                    manga = MangaDigital.objects.get(nombre=manga_name, tomo=1)
                    review = Review(titulo=titulo, comentario=comentario, puntuacion=rating, manga=manga, usuario=usuario)
                    review.save()
                    print('reseña guardada')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            else:
                return HttpResponse('Acceso no autorizado', status=401)
        else:
            print(form.errors)
    else:
        form = ReviewForm()

        #calcular calificacion
        all_review = Review.objects.filter(manga__nombre=manga_name)

        promedio = all_review.aggregate(promedio_puntuacion=Avg('puntuacion'))['promedio_puntuacion']
        print(promedio)
    
    if request.user.is_authenticated:
        context = {
            'mangas': mangas,
            'form': form,
            'existing': existing,
            'reviews': reviews,
            'promedio': promedio,
            'user_review': user_review
        }
    else:
        context = {
            'mangas': mangas,
            'form': form,
            'existing': existing,
            'promedio': promedio,
            'reviews': reviews,
        }
    return render(request, 'mangapage.html', context)

def mangas_view(request):
    mangas_nuevos = MangaDigital.objects.order_by('-timestamp').distinct()[:8]
    mangas = MangaDigital.objects.all()
    context = {
        'mangas_nuevos': mangas_nuevos,
        'mangas': mangas,
    }
    return render(request, 'mangas.html', context)

# Create your views here.
def reader_view(request, manga_id):
    #VOLVER A LA PAGINA DEL HISTORIAL
    try:
        user = User.objects.get(id=request.user.id)
    except:
        pass
    #FIN
    manga = MangaDigital.objects.get(id=manga_id)
    manga_folder = os.path.join('media', 'mangas', manga.nombre, str(manga.tomo))
    images = sorted([image for image in os.listdir(manga_folder) if image.endswith(('.jpg', '.jpeg', '.png'))])


    total_images = len(images)

    current_image = request.GET.get('image', 1)

    try:
        current_image = int(current_image)
    except ValueError:
        current_image = 1

    
    if current_image < 1:
        current_image = 1
    elif current_image > total_images:
        current_image = total_images
    
    current_image_path = os.path.join('/', manga_folder, images[current_image - 1])

    context = {
        'manga': manga,
        'current_image': current_image,
        'total_images': total_images,
        'current_image_path': current_image_path,
        'images': images,
    }

    return render(request, 'reader.html', context)