from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout

from users.forms import RegistrationForm, AuthForm
from store.models import Cart

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