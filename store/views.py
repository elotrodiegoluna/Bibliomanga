from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Producto, Cart, CartItem
from users.models import Boleta

import random
import string
#TRANSBANK
import transbank
from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions, IntegrationCommerceCodes, IntegrationApiKeys

# Create your views here.
def store_view(request):
    context = {}
    productos = Producto.objects.all()

    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user, is_paid=False).first()
    else:
        session_cart_id = request.session.get('cart_id')
        if session_cart_id:
            cart = Cart.objects.get(id=session_cart_id)
        else:
            cart = None

    context = {
        'productos': productos
    }
    return render(request, 'store.html', context)

def product_view(request, pk):
    productos = Producto.objects.get(id=pk)
    context = {
        'productos': productos
    }
    return render(request, 'product.html', context)

def add_to_cart(request, pk):
    productos = Producto.objects.get(pk=pk)
    
    if request.user.is_authenticated: # usuario esta autenticado
        user = request.user
        cart , _ = Cart.objects.get_or_create(user = user, is_paid = False) # get carrito (el '_' es para omitir parametro)
    else: # anonimo > crear sesion en django
        session_cart_id = request.session.get('cart_id')
        if session_cart_id:
            cart = Cart.objects.get(id=session_cart_id)
        else:
            cart = Cart.objects.create()
            request.session['cart_id'] = cart.id

    cart_items = CartItem.objects.create(cart = cart, product = productos)

    # get carrito / actualizar sesion
    if request.user.is_authenticated:
        request.session['cart_total_quantity'] = cart.cart_items.count()
        request.session['cart_total_price'] = cart.get_cart_total()
    else:
        session_cart_id = request.session.get('cart_id')
        if session_cart_id:
            cart = Cart.objects.get(id=session_cart_id)
            request.session['cart_total_quantity'] = cart.cart_items.count()
            request.session['cart_total_price'] = cart.get_cart_total()
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def cart_view(request):
    print("cart")
    context = {}
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user, is_paid=False).first()
    else:
        session_cart_id = request.session.get('cart_id')
        if session_cart_id:
            cart = Cart.objects.get(id=session_cart_id)
        else:
            cart = None
    cart_items = CartItem.objects.filter(cart=cart).select_related('product') if cart else []

    if request.POST:
        if cart and cart_items.exists():
            random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
            buy_order = f"{random_string}{cart.id}"
            session_id = request.session.session_key
            amount = cart.get_cart_total()
            return_url = request.build_absolute_uri(reverse('payment_confirmation'))
            response = Transaction().create(
                buy_order=buy_order,
                session_id=session_id,
                amount=amount,
                return_url=return_url
            )
            context = {
                'cart_items': cart_items,
                'cart_total': cart.get_cart_total() if cart else 0,
                'response': response
            }
            return redirect(response["url"] + '?token_ws=' + response["token"])
        else:
            context = {
                'cart_items': cart_items,
                'cart_total': cart.get_cart_total() if cart else 0,
                'show_modal': True  # Agrega la clave 'show_modal' con valor True al contexto
            }
            return render(request, 'cart.html', context)
    
    context = {
        'cart_items': cart_items,
        'cart_total': cart.get_cart_total() if cart else 0
    }
    
    if request.session.get('pago_rechazado'):
        del request.session['pago_rechazado']
        context = {
            'cart_items': cart_items,
            'cart_total': cart.get_cart_total() if cart else 0,
            'pago_rechazado': True
        }
    return render(request, 'cart.html', context)

@login_required
def payment_confirm_view(request): # redireccionar aqui para confirmar el pago
    usuario = request.user # get usuario
    token_ws = request.GET.get('token_ws')

    #boleta = get_object_or_404(Boleta, token_boleta=token_ws) #verificar si el token ya se usó en una boleta
    boleta = Boleta.objects.filter(token_boleta=token_ws).first()
    if boleta:
        if boleta.pagado:
            # mostrar pagina error de pago duplicado
            return redirect('index') # por ahora al index
    
    # realizar el pago
    response = Transaction().commit(token=token_ws) # le hace commit al token para confirmar/rechazar el pago
    #print("response: {}".format(response))

    if response['status'] == 'AUTHORIZED':
        print("authorized")
        # si la compra se autoriza crear boleta
        cart = Cart.objects.filter(user=usuario, is_paid=False).first()

        detalle_compra = {
            "productos": [],
            "total": cart.get_cart_total()
        }
        # por cada item del carrito, agregar una linea al json del detalle_compra
        for item in cart.cart_items.all():
            product = {
                "nombre": item.product.nombre,
                "precio": item.product.precio
            }
            detalle_compra["productos"].append(product)

        # guardar boleta en la db
        boleta = Boleta(usuario=usuario, detalle_compra=detalle_compra)
        boleta.token_boleta = token_ws
        boleta.pagado = True
        boleta.save()
        
        # borrar productos del carrito
        cart_items = CartItem.objects.filter(cart=cart)
        cart_items.delete()
        # limpiar sesion
        request.session['cart_total_quantity'] = 0
        request.session['cart_total_price'] = 0

        context = {
            'token': token_ws,
            'response': response,
            'boleta': boleta
        }

        return render(request, 'payment_success.html', context)
    else: # pago rechazado
        print("error de pago")
        request.session['pago_rechazado'] = True
        return redirect('cart')
    


def payment_success_view(request, boleta_token):
    boleta = get_object_or_404(Boleta, token=boleta_token, usuario=request.user)

    usuario = request.user
    boleta = Boleta.objects.filter(usuario=usuario).first()

    context = {
        'boleta': boleta
    }

    return render(request, 'payment_success.html', context)



    #return render_template('webpay/plus/commit.html', token=token, response=response)