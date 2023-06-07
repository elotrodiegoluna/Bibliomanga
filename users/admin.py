from django.contrib import admin
from .models import User, Suscripcion, PlanPremium
# Register your models here.

admin.site.register(User)
admin.site.register(Suscripcion)
admin.site.register(PlanPremium)