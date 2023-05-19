from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Manga, Cart, CartItem

# Create your views here.
def store_view(request):
    context = {}
    manga = Manga.objects.all()

    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user, is_paid=False).first()
    else:
        session_cart_id = request.session.get('cart_id')
        if session_cart_id:
            cart = Cart.objects.get(id=session_cart_id)
        else:
            cart = None

    cart_total = cart.get_cart_total() if cart else 0
    
    request.session['cart_total'] = cart_total

    context = {
        'mangas': manga,
        'cart_total': cart_total
    }
    return render(request, 'store.html', context)

def product_view(request, pk):
    manga = Manga.objects.get(id=pk)
    context = {
        'mangas': manga
    }
    return render(request, 'product.html', context)

def add_to_cart(request, pk):
    manga = Manga.objects.get(pk=pk)
    
    if request.user.is_authenticated:
        # Usuario autenticado
        user = request.user
        cart , _ = Cart.objects.get_or_create(user = user, is_paid = False)
    else:
        # Anonimo => crear sesión
        session_cart_id = request.session.get('cart_id')
        if session_cart_id:
            cart = Cart.objects.get(id=session_cart_id)
        else:
            cart = Cart.objects.create()
            request.session['cart_id'] = cart.id

    cart_items = CartItem.objects.create(cart = cart, product = manga)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
