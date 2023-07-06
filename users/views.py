from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from django.db.models import Avg, Q
import os

import random
import string

from .forms import *
from mangas.forms import *
from store.models import Cart, Producto
from .models import *

#TRANSBANK
import transbank
from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions, IntegrationCommerceCodes, IntegrationApiKeys


@login_required
def change_username(request):
    if request.method == 'POST':
        print(request.POST)
        new_username = request.POST.get('username')
        # verificar que sea un nuevo nombre
        if new_username != request.user.username:
            if len(new_username) < 4 or len(new_username) > 64:
                messages.error(request, 'El nombre de usuario debe tener entre 4 a 64 caracteres')
            elif User.objects.filter(username=new_username).exists():
                messages.error(request, 'El nombre de usuario ya está en uso')
            else:
                usuario = User.objects.get(id=request.user.id)
                usuario.username = new_username
                usuario.save()
            
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    


@login_required
def change_avatar(request):
    print('changeavatar')
    print(request.POST)
    if request.user.is_authenticated:
        if request.method == 'POST':
            """""
            print('AVATAR POST')
            print(request.FILES)
            print(request.FILES['avatar_submit'])
            """""
            form = CambiarAvatarForm(request.POST, request.FILES, instance=request.user)
            if form.is_valid():
                usuario = User.objects.get(id=request.user.id)

                # conseguir archivo subido
                avatar_file = request.FILES['avatar_submit']
                if avatar_file.content_type not in ['image/jpeg', 'image/png']:
                    messages.success(request, 'El avatar que quieres subir no es un formato admitido.')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

                # guardar formulario
                form.save()
                #
                filename = avatar_file.name # nombre del archivo
                user_folder = str(usuario.username) # nombre de la carpeta

                # crear carpeta del usuario si no existe
                user_folder_path = os.path.join(settings.MEDIA_ROOT, 'avatars', user_folder)
                os.makedirs(user_folder_path, exist_ok=True)

                # construir ruta completa
                file_path = os.path.join(user_folder_path, filename)
                print(file_path)

                # guardar el archivo
                with open(file_path, 'wb+') as destination:
                    for chunk in avatar_file.chunks():
                        destination.write(chunk)

                # aca deberia eliminarse la foto anterior y renombrar la de ahora a avatar
                    # no da el tiempo / no tiene importancia ahora

                # path relativo a la foto (sin carpetas de windows)
                relative_path = os.path.relpath(file_path, settings.MEDIA_ROOT)

                usuario.avatar = relative_path
                usuario.save()

                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                print(form.errors)
        else:
            form = CambiarAvatarForm(instance=request.user)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def accountinfo_view(request):
    if request.user.is_authenticated:
        context = {}
        usuario = User.objects.get(id=request.user.id)
        
        context = {
            'usuario': usuario,
        }

        return render(request, 'myaccount/account_info.html', context)

@login_required
def accountpremium_view(request):
    if request.user.is_authenticated:
        context = {}
        usuario = User.objects.get(id=request.user.id)
        
        try:
            suscripcion = Suscripcion.objects.get(usuario=usuario)
            context = {
                'usuario': usuario,
                'suscripcion': suscripcion,
            }
            return render(request, 'myaccount/account_premium.html', context)
        except Suscripcion.DoesNotExist:
            pass

        context = {
            'usuario': usuario,
        }

        return render(request, 'myaccount/account_premium.html', context)

@login_required
def accountpwd_view(request):
    if request.user.is_authenticated:
        context = {}
        usuario = User.objects.get(id=request.user.id)
        
        context = {
            'usuario': usuario,
        }

        return render(request, 'myaccount/account_pwd.html', context)
     
@login_required
def accountdelete_view(request):
    if request.user.is_authenticated:
        context = {}
        usuario = User.objects.get(id=request.user.id)
        
        context = {
            'usuario': usuario,
        }

        return render(request, 'myaccount/account_delete.html', context)
    

@login_required
def orderdetails_view(request, buy_order):
    if request.user.is_authenticated:
        boleta = Boleta.objects.get(buy_order=buy_order)
        estados = EstadoPedido.objects.all()
        if boleta.usuario == request.user:
            pedido = Pedido.objects.get(boleta=boleta)
            
            mis_productos = []
            for producto in boleta.detalle_compra['productos']:
                try:
                    producto_obj = Producto.objects.get(id=producto['id'])
                    mis_productos.append(producto_obj)
                except:
                    pass

            context = {
                'pedido': pedido,
                'mis_productos': mis_productos,
                'estados': estados,
            }

            return render(request, 'order/order_details.html', context)
    return redirect('index')

@login_required
def order_view(request):
    if request.user.is_authenticated:
        usuario = request.user
        pedidos = Pedido.objects.filter(usuario=usuario)

        datos_json = []

        for pedido in pedidos:
            boleta = pedido.boleta
            detalle_compra = boleta.detalle_compra

            dato_json = detalle_compra.get('total')
            datos_json.append(dato_json)


        context = {
            'pedidos': pedidos,
            'datos_json': datos_json,
        }
        return render(request, 'order/order.html', context)
    return redirect('index')

def premiumplans_view(request):
    return render(request, 'premium_plans.html')

@login_required
def premium_success_view(request, boleta_token):
    boleta = get_object_or_404(Boleta, token=boleta_token, usuario=request.user)

    usuario = request.user
    boleta = Boleta.objects.filter(usuario=usuario).first()

    context = {
        'boleta': boleta
    }

    return render(request, 'premium_success.html', context)

@login_required
def premium_pay(request):
    usuario = request.user
    token_ws = request.GET.get('token_ws')

    boleta = Boleta.objects.filter(token_boleta=token_ws).first()
    if boleta:
        if boleta.pagado:
            return redirect('index') # error boleta duplicada
    
    # realizar el pago
    response = Transaction().commit(token=token_ws) # commit pago

    if response['status'] == 'AUTHORIZED': # pago autorizado
        # crear boleta
        if request.session.get('plan_comprado'):
            plan_comprado = request.session.get('plan_comprado')
            del request.session['plan_comprado']
        detalle_compra = {
            "producto": 'Premium '+plan_comprado,
            "total": response['amount']
        }
        # guardar boleta
        boleta = Boleta(usuario=usuario, detalle_compra=detalle_compra)
        boleta.token_boleta = token_ws
        boleta.pagado = True
        boleta.save()
        # asignar premium al usuario y crear suscripción
        sub , _ = Suscripcion.objects.get_or_create(usuario=usuario) # el nombre lo dice
        sub.activo = True # tambien deberia poner fecha limite y correr un PLSQL para verificar la fecha y quitarle el activo
        sub.plan = PlanPremium.objects.filter(nombre_plan=plan_comprado).first()
        sub.fecha_caducidad = sub.fecha_inicio + relativedelta(months=1)
        sub.save()

        user_db = User.objects.get(id=request.user.id)
        user_db.premium = True
        user_db.save()
        
        context = {
            'token': token_ws,
            'response': response,
            'boleta': boleta
        }
        return render(request, 'premium_success.html', context)
    else: # pago rechazado
        print("error de pago")
        request.session['pago_rechazazdo'] = True
        return redirect('premium_confirm')


@login_required
def premiumconfirm_view(request, plan):
    usuario = User.objects.get(id=request.user.id)
    try:
        subscription = Suscripcion.objects.get(usuario=usuario)
    except:
        subscription = None
    print(subscription)

    if plan == 'basico':
        plan_premium = PlanPremium.objects.filter(nombre_plan='Plan Básico').first()
    elif plan == 'avanzado':
        plan_premium = PlanPremium.objects.filter(nombre_plan='Plan Avanzado').first()

    context = {}
    if not usuario.premium:
        if request.POST:
            # crear compra
            random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
            buy_order = f"{random_string}{usuario.id}"
            session_id = request.session.session_key
            amount = plan_premium.precio
            return_url = request.build_absolute_uri(reverse('premium_confirmation'))
            response = Transaction().create(
                buy_order=buy_order,
                session_id=session_id,
                amount=amount,
                return_url=return_url
            )
            request.session['plan_comprado'] = plan_premium.nombre_plan
            return redirect(response["url"] + '?token_ws=' + response["token"])
    else:
        context = {
            'already_premium': True
        }
    
    fecha_actual = timezone.now()
    prox_mes = fecha_actual + relativedelta(months=1)
    context = {
        'fecha_actual': fecha_actual,
        'prox_mes': prox_mes
    }
    return render(request, 'premium_confirm.html', context)


def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)

            session_cart_id = request.session.get('cart_id')
            if session_cart_id:
                session_cart = Cart.objects.get(id=session_cart_id)
                session_cart.user = user
                session_cart.save()
                user.carts.add(session_cart) # asignar carrito al usuario en la bd
            
            return redirect('index')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'register.html', context)

def login_view(request):
    context = {}
    print("login")
    user = request.user

    next_url = request.GET.get('next')
    if user.is_authenticated:
        return redirect("index")
    if request.POST:
        form = AuthForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                #request.session.flush() # al loguear se borra la session (carrito)
                login(request, user)
                cart = Cart.objects.filter(user=user, is_paid=False).first()

                if cart is not None: # si el usuario tiene carrito
                    request.session['cart_id'] = cart.id
                    request.session['cart_total_quantity'] = cart.cart_items.count()
                    request.session['cart_total_price'] = cart.get_cart_total()
                    #print(request.session['cart_total_price'])
                
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect("index")
        else:
            context['login_form'] = form
    else:
        form = AuthForm()
    context['login_form'] = form
    return render(request, 'login.html', context)

def logout_view(request):
    logout(request)
    return redirect('index')




# MANGAS DE LA COMUNIDAD
def comunidad_view(request):
    context = {}

    mangas_usuario = None
    try:
        # Obtener los MangaUsuario que tienen al menos un MangaTomo asociado
        mangas_usuario = MangaUsuario.objects.filter(mangatomo__isnull=False).distinct()

        query = request.GET.get('q')
        if query:
            mangas_usuario = mangas_usuario.filter(Q(nombre__icontains=query))

    except MangaUsuario.DoesNotExist:
        mangas_usuario = None
    
    # paginación
    paginator = Paginator(mangas_usuario, 12) # listar por 5
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    context = {
        'mangas': mangas_usuario,
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'comunidad/comunidad.html', context)

def comunidad_manga_view(request, manga_name):
    context = {}
    manga = MangaUsuario.objects.get(nombre=manga_name)

    try:
        tomos = MangaTomo.objects.filter(manga__nombre=manga_name).order_by('tomo')
    except MangaTomo.DoesNotExist:
        # Manejar el caso en el que no se encuentre el manga
        return HttpResponse('Manga no encontrado', status=404)
    
    try:
        if request.user.is_authenticated:
            reviews = Review.objects.exclude(usuario=request.user).filter(mangaUsuario__nombre=manga_name)
            user_review = Review.objects.filter(usuario=request.user, mangaUsuario__nombre=manga_name).first()
            print(user_review)
            print(reviews)
        else:
            reviews = Review.objects.filter(mangaUsuario__nombre=manga_name)
    except Review.DoesNotExist:
        pass
    

    if request.user.is_authenticated:
        try:
            existing_review = Review.objects.get(mangaUsuario__nombre=manga_name, usuario=request.user)
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
                    review = Review(titulo=titulo, comentario=comentario, puntuacion=rating, mangaUsuario=manga, usuario=usuario)
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
        all_review = Review.objects.filter(mangaUsuario__nombre=manga_name)
        promedio = 0
        if all_review:
            promedio = all_review.aggregate(promedio_puntuacion=Avg('puntuacion'))['promedio_puntuacion']
            manga.promedio_puntuacion = promedio
            manga.save()

    
    if request.user.is_authenticated:
        context = {
            'tomos': tomos,
            'manga': manga,
            'form': form,
            'existing': existing,
            'reviews': reviews,
            'promedio': promedio,
            'user_review': user_review
        }
    else:
        context = {
            'tomos': tomos,
            'manga': manga,
            'form': form,
            'existing': existing,
            'promedio': promedio,
            'reviews': reviews,
        }
    return render(request, 'comunidad/comunidad_mangapage.html', context)

@login_required
def creador_view(request):
    context = {}

    usuario = get_object_or_404(User, id=request.user.id)

    try:
        mangas = MangaUsuario.objects.filter(autor=request.user)
        # paginación
        paginator = Paginator(mangas, 6) # listar por 5
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'usuario': usuario,
            'mangas': mangas,
            'page_obj': page_obj
        }

    except MangaUsuario.DoesNotExist:
        mangas = None
        context = {
            'usuario': usuario,
            'mangas': mangas,
        }

    return render(request, 'comunidad/creador/creador_main.html', context)

@login_required
def creador_crear_view(request):
    context = {}

    usuario = get_object_or_404(User, id=request.user.id)

    if request.method == 'POST':
        form = MangaUsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            portada_file = request.FILES['portada']
            if portada_file.content_type not in ['image/jpeg', 'image/png']:
                messages.success(request, 'La portada que quieres subir no es un formato admitido.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            manga_usuario = form.save(commit=False)
            manga_usuario.autor = request.user
            manga_usuario.save()

            # nombre del manga
            nombre_manga = manga_usuario.nombre

            # ruta de la carpeta del manga
            manga_folder = os.path.join('mangas_comunidad', nombre_manga)

            # crear la carpeta
            media_root = settings.MEDIA_ROOT
            manga_folder_path = os.path.join(media_root, manga_folder)
            if not os.path.exists(manga_folder_path):
                os.makedirs(manga_folder_path)

            # cambiar nombre de la foto
            portada = request.FILES['portada']
            portada_extension = os.path.splitext(portada.name)[1]
            portada_nombre = 'portada' + portada_extension
            portada_path = os.path.join(manga_folder_path, portada_nombre)

            # guardar portada con el nuevo nombre
            with open(portada_path, 'wb') as file:
                for chunk in portada.chunks():
                    file.write(chunk)

            messages.success(request, 'Tu manga {} se ha creado correctamente.'.format(nombre_manga))
            return redirect('creador')
        
        else:
            messages.success(request, 'Hubo un error con el formulario, tu manga no se pudo crear.')
            HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
    else:
        form = MangaUsuarioForm()

    context = {
        'form': form,
        'usuario': usuario
    }
    return render(request, 'comunidad/creador/creador_crear.html', context)

def creador_administrar_view(request, manga_name):
    context = {}

    manga = get_object_or_404(MangaUsuario, nombre=manga_name)

    if manga:
        try:
            tomos = MangaTomo.objects.filter(manga=manga).order_by('tomo')
        except MangaTomo.DoesNotExist:
            tomos = None


    try:
        if request.user.is_authenticated:
            reviews = Review.objects.exclude(usuario=request.user).filter(mangaUsuario__nombre=manga_name)
            user_review = Review.objects.filter(usuario=request.user, mangaUsuario__nombre=manga_name).first()
            print(user_review)
            print(reviews)
        else:
            reviews = Review.objects.filter(mangaUsuario__nombre=manga_name)
    except Review.DoesNotExist:
        pass
    

    if request.user.is_authenticated:
        try:
            existing_review = Review.objects.get(mangaUsuario__nombre=manga_name, usuario=request.user)
            existing = True
        except Review.DoesNotExist:
            existing_review = None
            existing = False
    else:
        existing = False
    


    #calcular calificacion
    all_review = Review.objects.filter(mangaUsuario__nombre=manga_name)
    promedio = 0
    if all_review:
        promedio = all_review.aggregate(promedio_puntuacion=Avg('puntuacion'))['promedio_puntuacion']
        manga.promedio_puntuacion = promedio
        manga.save()

    
    if request.user.is_authenticated:
        context = {
            'manga': manga,
            'existing': existing,
            'reviews': reviews,
            'user_review': user_review,
            'tomos': tomos,
        }
    else:
        context = {
            'manga': manga,
            'existing': existing,
            'reviews': reviews,
            'tomos': tomos,
        }
    return render(request, 'comunidad/creador/creador_manga.html', context)



import os, tempfile, shutil, patoolib
from patoolib import extract_archive
def subir_tomo(request, manga_id):
    manga = MangaUsuario.objects.get(id=manga_id)
    if request.method == 'POST':
        print('POST:'+str(request.POST))
        print(request.FILES)
        form = MangaTomoForm(request.POST, request.FILES)
        if form.is_valid():
            manga_tomo = form.save(commit=False)
            print(request.FILES)
            tomo = form.cleaned_data['tomo']
            desc = form.cleaned_data['desc']
            archivo = form.cleaned_data['archivo']

            if not archivo.name.lower().endswith(('.cbz', '.cbr')):
                messages.success(request, 'El tomo que quieres subir no es un formato admitido, por favor usa un formato .cbr o .cbz')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            # verificar si ya esta subido un tomo con el mismo numero
            try:
                tomo_existente = MangaTomo.objects.get(manga=manga, tomo=tomo)
                # redirigir
                messages.error(request, 'Ya subiste un tomo con esa numeración.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            except MangaTomo.DoesNotExist: # no existe
                pass # seguir


            # extraer archivo

            temp_dir = tempfile.mkdtemp()
            file_path = os.path.join(temp_dir, archivo.name)

            with open(file_path, 'wb') as file:
                for chunk in archivo.chunks():
                    file.write(chunk)
            
            # extraer archivo en temp
            patoolib.extract_archive(file_path, outdir=temp_dir)
            # obtener carpeta
            inner_dir = next(os.walk(temp_dir))[1][0] if len(next(os.walk(temp_dir))[1]) > 0 else None

            imagenes_dir = os.path.join(settings.MEDIA_ROOT, 'mangas_comunidad')
            manga_dir = os.path.join(imagenes_dir, manga.nombre, str(tomo))

            if os.path.exists(manga_dir):
                shutil.rmtree(manga_dir)
            os.makedirs(manga_dir)

            if inner_dir:
                inner_temp_dir = os.path.join(temp_dir, inner_dir)
                for filename in os.listdir(inner_temp_dir):
                    archivo_actual = os.path.join(inner_temp_dir, filename)
                    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                        try:
                            shutil.move(archivo_actual, manga_dir)
                        except Exception as e:
                            print("Error al mover el archivo:", str(e))
            else:
                for filename in os.listdir(temp_dir):
                    archivo_actual = os.path.join(temp_dir, filename)
                    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                        shutil.move(archivo_actual, manga_dir)

            shutil.rmtree(temp_dir)

            manga_tomo.path = os.path.relpath(manga_dir, settings.MEDIA_ROOT)
            manga_tomo.manga = manga
            manga_tomo.save()

            messages.error(request, 'El tomo se subió correctamente')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, 'Hubo un error con el formulario, el tomo no se subió.')
            print(form.errors)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    messages.error(request, 'Sucedió un error, no se realizó ningún cambio')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def editar_manga_comunidad(request, manga_id):
    if request.method == 'POST':
        manga = MangaUsuario.objects.get(id=manga_id)
        form = EditarMangaForm(request.POST, instance=manga)
        if form.is_valid():
            form.save()
            messages.success(request, 'El manga se editó correctamente.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, 'Hubo un error con el formumlario.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
def eliminar_manga_comunidad(request, manga_id):
    if request.method == 'POST':
        try:
            manga = MangaUsuario.objects.get(id=manga_id)
            manga.delete()
            messages.success(request, 'El manga se eliminó correctamente.')
            return redirect('creador')
        except Exception as e:
            messages.error(request, 'No se pudo eliminar el manga: {}'.format(e))
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def eliminar_tomo(request, tomo_id):
    if request.method == 'POST':
        try:
            tomo = MangaTomo.objects.get(id=tomo_id)
            tomo.delete()
            messages.success(request, 'Tomo eliminado correctamente.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        except Exception as e:
            messages.error(request, 'No se pudo eliminar este tomo.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))