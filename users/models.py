from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.sessions.models import Session
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
from dateutil.relativedelta import relativedelta

from .manager import MyUserManager
from store.models import CartItem, Cart, Producto
from mangas.models import MangaDigital as Manga
from .validators import validate_file_size, validate_file_extension


class User(AbstractBaseUser):
    email = models.EmailField(max_length=64,unique=True,)
    username = models.CharField(max_length=64, unique=True)
    premium = models.BooleanField(default=False)
    creador = models.BooleanField(default=False)
    fecha_nacimiento = models.DateField(null=True)

    avatar = models.ImageField(upload_to='avatars', default='avatars/default.png')
    
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    def get_cart_count(self):
        if self.is_authenticated:

            return CartItem.objects.filter(cart__is_paid = False, cart__user = self).count()
        else:
            cart_id = self.session.get('cart_id')
            if cart_id:
                return CartItem.objects.filter(cart_id=cart_id, cart__is_paid = False).count()
            else:
                return 0

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

import uuid
class Boleta(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    detalle_compra = models.JSONField()
    buy_order  = models.CharField(max_length=32, null=True)
    token_boleta = models.CharField(max_length=100, unique=True, blank=True, null=True)
    pagado = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.fecha = timezone.localtime()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"Boleta {self.pk} - Usuario: {self.usuario.username}"

class EstadoPedido(models.Model):
    texto = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.texto
    
class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    boleta = models.ForeignKey(Boleta, on_delete=models.CASCADE)
    tipo_entrega = models.CharField(max_length=64)
    estado = models.ForeignKey(EstadoPedido, on_delete=models.CASCADE) # preparacion/enviado/recibido || preparacion/listo para retirar
    comuna = models.CharField(max_length=64, null=True)
    direccion = models.CharField(max_length=64, null=True)
    n_depto = models.CharField(max_length=16, null=True)
    nombre_receptor = models.CharField(max_length=64, null=True)
    apellido_receptor = models.CharField(max_length=64, null=True)
    telefono = models.IntegerField(null=True)

class PlanPremium(models.Model):
    nombre_plan = models.CharField(max_length=64, unique=True)
    precio = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre_plan

class Suscripcion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(PlanPremium, on_delete=models.CASCADE, null=True)
    activo = models.BooleanField(default=False)
    fecha_inicio = models.DateTimeField(default=timezone.now)
    fecha_caducidad = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.fecha_caducidad = self.fecha_inicio + relativedelta(months=1)
        super().save(*args, **kwargs)

class MangaLeido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE)
    last_page = models.IntegerField(null=True)
    finished = models.BooleanField(default=False)

class Review(models.Model):
    titulo = models.CharField(max_length=64)
    comentario = models.TextField()
    puntuacion = models.IntegerField()
    likes = models.IntegerField(null=True)
    dislikes = models.IntegerField(null=True)
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def name_return(self):
        return "{}, {}". format(self.usuario.username, self.titulo)
    
    def __str__(self):
        return self.name_return()

class ListaFavorito(models.Model):
    nombre_lista = models.CharField(max_length=64)
    publica = models.BooleanField(default=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def name_return(self):
        return "{}, {}". format(self.usuario, self.nombre_lista)

    def __str__(self):
        return self.name_return()

class ItemFavorito(models.Model):
    lista = models.ForeignKey(ListaFavorito, on_delete=models.CASCADE)
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE)

    def name_return(self):
        return "{}, {}, {}". format(self.lista.usuario, self.lista.nombre_lista, self.manga.nombre)

    def __str__(self):
        return self.name_return()
    
class ListaDeseados(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

class ItemDeseado(models.Model):
    lista = models.ForeignKey(ListaDeseados, on_delete=models.CASCADE)
    item = models.ForeignKey(Producto, on_delete=models.CASCADE)