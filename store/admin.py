from django.contrib import admin
from .models import Manga, Cart, CartItem

# Register your models here.
admin.site.register(Manga)
admin.site.register(Cart)
admin.site.register(CartItem)