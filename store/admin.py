from django.contrib import admin
from .models import Producto, Cart, CartItem, Categoria

# Register your models here.
admin.site.register(Producto)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Categoria)