from django.conf import settings
from django.db import models

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=64, unique=True)
    desc = models.TextField(default="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.");
    imagen = models.ImageField(upload_to='tienda/imagen', default='mangas/portadas/default.png')
    precio = models.IntegerField(default=10000)
    stock = models.IntegerField(null=True)
    timestamp = models.DateField(auto_now_add=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.nombre
    
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carts', null=True)
    is_paid = models.BooleanField(default=False)

    def get_cart_total(self):
        cart_items = self.cart_items.all()
        price = []
        for cart_item in cart_items:
            price.append(cart_item.product.precio)
        print(price)
        return sum(price)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True, blank=True)

    def get_product_price(self):
        price = [self.product.precio]
        return sum(price)
    