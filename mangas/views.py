from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Avg, Q
from django.core.paginator import Paginator

from .forms import *
from .models import *
from users.models import MangaLeido, User, Review, MangaTomo


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
        mangas = MangaDigital.objects.filter(nombre=manga_name).order_by('tomo')
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
        promedio = 0
        if all_review:
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
    mangas_valor = (
    MangaDigital.objects
    .filter(tomo=1)  # Filtrar por tomo igual a 1
    .order_by('-promedio_puntuacion')
    .distinct()
    [:8]
)
    mangas = MangaDigital.objects.all()

    # Filtrar por nombre si se proporciona un valor en la consulta
    query = request.GET.get('q')
    print(query)
    if query:
        mangas = mangas.filter(Q(nombre__icontains=query))
        print('mangas')


    # paginación
    paginator = Paginator(mangas, 12) # listar por 5
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    for manga in mangas_nuevos:
        mangas_con_mismo_nombre = MangaDigital.objects.filter(nombre=manga.nombre)
        promedio_puntuacion = Review.objects.filter(manga__in=mangas_con_mismo_nombre, manga__tomo=1).aggregate(promedio=Avg('puntuacion'))['promedio']
        if promedio_puntuacion:
            mangas_con_mismo_nombre.update(promedio_puntuacion=promedio_puntuacion)

    context = {
        'mangas_nuevos': mangas_nuevos,
        'mangas': mangas,
        'page_obj': page_obj,
        'query': query,
        'mangas_valor': mangas_valor
    }
    return render(request, 'mangas.html', context)


""""
#calcular calificacion
    all_review = Review.objects.filter(manga=manga)

    promedio = all_review.aggregate(promedio_puntuacion=Avg('puntuacion'))['promedio_puntuacion']
    print(promedio)


def reader_view(request, manga_id):
    #VOLVER A LA PAGINA DEL HISTORIAL
    try:
        user = User.objects.get(id=request.user.id)
    except:
        pass
    #FIN
    manga = MangaTomo.objects.get(id=manga_id)

    manga_folder = os.path.join('media', 'mangas_comunidad', manga.manga.nombre, str(manga.tomo))
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
"""""

def reader_view(request, manga_id):
    #VOLVER A LA PAGINA DEL HISTORIAL
    try:
        user = User.objects.get(id=request.user.id)
    except:
        pass
    #FIN
    manga_comunidad = False

    try:
        manga = MangaDigital.objects.get(id=manga_id)
    except MangaDigital.DoesNotExist:
        manga = None

    if manga:
        manga_folder = os.path.join('media', 'mangas', manga.nombre, str(manga.tomo))
    else:
        manga = MangaTomo.objects.get(id=manga_id)
        manga_folder = os.path.join('media', 'mangas_comunidad', manga.manga.nombre, str(manga.tomo))
        manga_comunidad = True

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
        'manga_comunidad': manga_comunidad,
    }

    return render(request, 'reader.html', context)