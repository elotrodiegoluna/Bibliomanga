from django.shortcuts import render
from .models import *
from users.models import MangaLeido, User

import os

# Create your views here.
def reader_view(request, manga_id):
    user = User.objects.get(id=request.user.id)
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