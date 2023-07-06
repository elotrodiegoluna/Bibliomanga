"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from users.views import (
    registration_view,
    login_view,
    logout_view,
    premiumplans_view,
    premiumconfirm_view,
    premium_pay,
    premium_success_view,
    order_view,
    orderdetails_view,
    accountinfo_view,
    accountdelete_view,
    accountpremium_view,
    accountpwd_view,
    change_avatar,
    change_username,
    creador_view,
    creador_crear_view,
    creador_administrar_view,
    subir_tomo,
    eliminar_tomo,
    eliminar_cuenta,
    editar_manga_comunidad,
    eliminar_manga_comunidad,
    comunidad_view,
    comunidad_manga_view,
)

from bmanga.views import (
    index,
)

from store.views import (
    store_view,
    product_view,
    add_to_cart,
    remove_from_cart,
    cart_view,
    payment_confirm_view,
    payment_success_view,
    descargar_boleta,
)

from adminpanel.views import (
    adminmain_view,
    adminusers_view,
    adminstore_view,
    adminmangas_view,
    adminorder_view,
    subir_manga,
    eliminar_usuario,
    bloquear_usuario,
    eliminar_producto,
    eliminar_manga,
    add_product_view,
    edit_product_view,
    add_manga_view,
    edit_manga_view,

)

from mangas.views import (
    reader_view,
    mangas_view,
    mangapage_view,
    delete_review,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    # premium
    path('premium/', premiumplans_view, name="premiumplans"),
    path('premium/confirm-<str:plan>/', premiumconfirm_view, name="premiumconfirm"),
    path('premium-confirmation/', premium_pay, name='premium_confirmation'),
    path('premium-success/<uuid:boleta_token>', premium_success_view, name='premium_success'),
    # registro y login
    path('register/', registration_view, name="register"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    # tienda
    path('store/', store_view, name="store"),
    path('product/<pk>', product_view, name="product"),
    path('add-to-cart/<pk>/', add_to_cart, name="add_to_cart"),
    path('remove_from_cart/<pk>/', remove_from_cart, name='remove_from_cart'),
    path('cart/', cart_view, name="cart"),
    # admin
    path('adminpanel/main/', adminmain_view, name="adminmain"),
    path('adminpanel/mangas/', adminmangas_view, name="adminmangas"),
    path('adminpanel/orders/', adminorder_view, name="adminorder"),
    # admin users
    path('adminpanel/users/', adminusers_view, name="adminusers"),
    path('adminpanel/users/delete-user_<user_id>', eliminar_usuario, name='deleteuser'),
    path('adminpanel/users/block-user_<user_id>', bloquear_usuario, name='blockuser'),
    # admin store
    path('adminpanel/store/', adminstore_view, name="adminstore"),
    path('adminpanel/store/add-product', add_product_view, name="addproduct"),
    path('adminpanel/store/edit-product/<int:product_id>', edit_product_view, name="editproduct"),
    path('adminpanel/store/delete-product_<int:product_id>', eliminar_producto, name="deleteproduct"),
    # pago
    path('payment-confirmation/', payment_confirm_view, name='payment_confirmation'),
    path('payment-success/<uuid:boleta_token>', payment_success_view, name='payment_success'),
    path('payment-succes/descargar-boleta/<int:boleta_id>', descargar_boleta, name='descargarboleta'),
    # mangas digitales
    path('adminpanel/mangas/add', add_manga_view, name='addmanga'),
    path('adminpanel/manga/delete/<int:manga_id>', eliminar_manga, name='deletemanga'),
    path('adminpanel/mangas/edit/<int:manga_id>', edit_manga_view, name='editmanga'),
    path('adminpanel/mangas-upload', subir_manga, name='subirmanga'),
    path('manga/<int:manga_id>/reader/', reader_view, name='reader'),
    path('mangas/', mangas_view, name='mangas'),
    path('mangas/<str:manga_name>', mangapage_view, name='mangapage'),
    path('mangas/delete-review/<int:id>', delete_review, name='deletereview'),
    # usuarios
    path('users/account/delete-account/', eliminar_cuenta, name='eliminarcuenta'),
    path('users/account/change-username/', change_username, name='changeusername'),
    path('users/account/change-avatar/', change_avatar, name='changeavatar'),
    path('users/account/information', accountinfo_view, name='myaccount'),
    path('users/account/premium', accountpremium_view, name='myaccount-premium'),
    path('users/account/password', accountpwd_view, name='myaccount-pwd'),
    path('users/account/delete', accountdelete_view, name='myaccount-del'),
    path('user/orders', order_view, name='myorders'),
    path('user/order-details/<str:buy_order>/', orderdetails_view, name='order-details'),
    # creador
    path('creator/administrar', creador_view, name='creador'),
    path('creator/crear', creador_crear_view, name='creador-crear'),
    path('creador/manga/<str:manga_name>', creador_administrar_view, name='creador-administrar'),
    path('creador/manga/subir-tomo/<int:manga_id>', subir_tomo, name='subirtomo'),
    path('creador/manga/editar-manga/<int:manga_id>', editar_manga_comunidad, name='editarmanga'),
    path('creador/manga/eliminar-manga/<int:manga_id>', eliminar_manga_comunidad, name='eliminarmanga'),
    path('creador/manga/eliminar-tomo/<int:tomo_id>', eliminar_tomo, name='eliminartomo'),
    # comunidad
    path('comunidad/', comunidad_view, name='comunidad'),
    path('comunidad/<str:manga_name>', comunidad_manga_view, name='mangapage-comunidad'),
    #
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
