from django.contrib import admin
from .models import Producto, Cart, CartItem

# Register your models here.
admin.site.register(Producto)
admin.site.register(Cart)
admin.site.register(CartItem)