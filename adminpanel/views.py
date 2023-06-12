from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import user_passes_test
from django.conf import settings
from django.db.models import Sum, FloatField
from django.db.models.functions import Cast
import plotly.graph_objects as go
import calendar, locale, datetime

from django.core.files.storage import default_storage

from users.models import User, Boleta
from mangas.models import MangaDigital
from store.models import Producto
from .forms import *

def is_admin(user):
    return user.is_staff  # Verifica si el usuario es un administrador

#añadir mangas digitales
@user_passes_test(is_admin, login_url='index', redirect_field_name=None)
def add_manga_view(request):
    if request.method == 'POST':
        form = MangaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminstore')
    else:
        form = MangaForm()
    context = {
        'form': form,
    }
    return render(request, 'mangas/manga_add.html', context)
#añadir productos
@user_passes_test(is_admin, login_url='index', redirect_field_name=None)
def add_product_view(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminstore')
    else:
        form = ProductoForm()
    context = {
        'form': form,
    }
    return render(request, 'products/product_add.html', context)

@user_passes_test(is_admin, login_url='index', redirect_field_name=None)
def adminmain_view(request):
    context = {}
    boletas = Boleta.objects.filter(pagado=True)
    total_boletas = boletas.count() # boletas generadas
    locale.setlocale(locale.LC_TIME, 'es_CL.UTF-8')
    
    # GRAFICO GANANCIAS
    ganancia_productos = 0
    ganancia_suscripciones = 0

    for boleta in boletas:
        detalle_compra = boleta.detalle_compra
        ganancia_productos += float(detalle_compra["total"])
        
        if "producto" in detalle_compra and "total" in detalle_compra:
            boleta_premium = detalle_compra["producto"]
            if "premium" in boleta_premium.lower():
                ganancia_suscripciones += float(detalle_compra["total"])
    labels = ["Ganancia Productos", "Ganancia Suscripciones"] # labels separados por ,
    values = [ganancia_productos, ganancia_suscripciones] # valores separados por ,

    # formatear los values en clp
    formatted_values = ['${:,.0f} CLP'.format(value) for value in values]

    # crear la figura tipo donut
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='text+label', textposition='outside')])
    # color del fondo
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        legend=dict(font=dict(color='white')) # color de los textos labels
    )
    # cambiar color de los valores
    fig.update_traces(
        title='Ganancias',
        title_font=dict(color='white'),
        textfont_color='white',
        marker=dict(colors=['#00DFA2', '#F6FA70']), # color de los valores en el pie
        outsidetextfont=dict(color='white'), # mover los labels y lineas hacia afuera
        text=formatted_values, # mostrar valor formateado
        hovertemplate='<b>%{label}</b><br><br>%{percent}<extra></extra>' # mostrar porcentajes al hacer hover
    )
    
    # crear grafico
    graph_ganancias = fig.to_html(full_html=False)

    # GRAFICO USUARIOS REGISTRADOS POR MES
    actual_year = datetime.datetime.now().year
    usuarios_registrados = User.objects.filter(date_joined__year=actual_year)
    registros_mes = {}
    for usuario in usuarios_registrados:
        month_registro = usuario.date_joined.month
        year_registro = usuario.date_joined.year
        clave_month_year = f'{month_registro:02d}/{year_registro}'
        registros_mes[clave_month_year] = registros_mes.get(clave_month_year, 0) + 1

    registros_mes = dict(sorted(registros_mes.items()))
    labels_usuarios_registrados = []
    for clave_month_year in registros_mes.keys():
        month, year = clave_month_year.split('/')
        month_name = calendar.month_name[int(month)]
        label = f'{month_name} {year}'
        labels_usuarios_registrados.append(label)

    values_usuarios_registrados = list(registros_mes.values())

    color_palette = ['#0079FF', '#FF0060', '#F6FA70', '#00DFA2', '#581845', '#581845']  # Lista de colores personalizados

    fig_usuarios_registrados = go.Figure(data=go.Bar(x=labels_usuarios_registrados, y=values_usuarios_registrados, marker=dict(color=color_palette)))
    fig_usuarios_registrados.update_layout(
        title='Usuarios registrados por mes',
        title_font=dict(color='white'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(title='Meses'),
        yaxis=dict(title='Cantidad de Usuarios'),
        font=dict(color='white'),
        showlegend=False,
    )
    graph_usuarios_registrados = fig_usuarios_registrados.to_html(full_html=False)



    context = {
        'boletas': boletas,
        'total_boletas': total_boletas,
        'graph_ganancias': graph_ganancias,
        'graph_usuarios_registrados': graph_usuarios_registrados
    }

    return render(request, 'admin_main.html', context)

@user_passes_test(is_admin, login_url='index', redirect_field_name=None)
def adminmangas_view(request):
    context = {}
    mangas = MangaDigital.objects.all()

    context = {
        'mangas': mangas
    }
    return render(request, 'admin_mangas.html', context)

@user_passes_test(is_admin, login_url='index', redirect_field_name=None)
def adminstore_view(request):
    context = {}
    productos = Producto.objects.all()

    context = {
        'productos': productos
    }
    return render(request, 'admin_store.html', context)

@user_passes_test(is_admin, login_url='index', redirect_field_name=None)
def adminusers_view(request):
    context = {}
    usuarios = User.objects.all()

    context = {
        'users': usuarios
    }
    return render(request, 'admin_users.html', context)


import os, tempfile, shutil, patoolib
from patoolib import extract_archive
@user_passes_test(is_admin, login_url='index', redirect_field_name=None)
def subir_manga(request):
    if request.method == 'POST':
        form = MangaForm(request.POST, request.FILES)
        if form.is_valid():
            manga = form.save(commit=False)
            archivo = form.cleaned_data['archivo']

            temp_dir = tempfile.mkdtemp()
            file_path = os.path.join(temp_dir, archivo.name)

            with open(file_path, 'wb') as file:
                for chunk in archivo.chunks():
                    file.write(chunk)

            # extraer archivo en temp
            patoolib.extract_archive(file_path, outdir=temp_dir)

            # obtener carpeta
            inner_dir = next(os.walk(temp_dir))[1][0] if len(next(os.walk(temp_dir))[1]) > 0 else None

            imagenes_dir = os.path.join(settings.MEDIA_ROOT, 'mangas')
            manga_dir = os.path.join(imagenes_dir, manga.nombre, str(manga.tomo))

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

            manga.path = manga_dir
            manga.activo = True

            manga.save()

            return redirect('adminmangas')
    else:
        form = MangaForm()

    context = {'form': form}
    return render(request, 'mangas/manga_add.html', context)