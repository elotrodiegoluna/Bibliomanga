from django.contrib import admin
from .models import *
# Register your models here.
class EstadoPedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'texto')

admin.site.register(User)
admin.site.register(Suscripcion)
admin.site.register(PlanPremium)
admin.site.register(Pedido)
admin.site.register(Boleta)
admin.site.register(EstadoPedido, EstadoPedidoAdmin)
admin.site.register(Review)
admin.site.register(MangaUsuario)
admin.site.register(MangaTomo)