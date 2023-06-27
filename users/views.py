from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
import random
import string

from users.forms import RegistrationForm, AuthForm
from store.models import Cart, Producto
from .models import *

#TRANSBANK
import transbank
from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions, IntegrationCommerceCodes, IntegrationApiKeys

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