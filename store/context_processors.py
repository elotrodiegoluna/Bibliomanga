def cart_total(request):
    cart_total = request.session.get('cart_total', 0)
    return {
        'cart_total': cart_total
    }
