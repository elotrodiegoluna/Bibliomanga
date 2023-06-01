from django.db import models
from django.contrib.sessions.models import Session
from django.contrib.auth.models import AbstractBaseUser
from .manager import MyUserManager
from store.models import CartItem, Cart


class User(AbstractBaseUser):
    email = models.EmailField(max_length=64,unique=True,)
    username = models.CharField(max_length=64, unique=True,)
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
    token_boleta = models.CharField(max_length=100, unique=True, blank=True, null=True)
    pagado = models.BooleanField(default=False)

    def __str__(self):
        return f"Boleta {self.pk} - Usuario: {self.usuario.username}"