from django.contrib import admin

from app.web.models import Orden, Subscription, Type_Payment, Tipo_subcripcion, CaracteristicaSubcripcion

# Register your models here.

admin.site.register(Orden)
admin.site.register(Subscription)
admin.site.register(Type_Payment)
admin.site.register(Tipo_subcripcion)
admin.site.register(CaracteristicaSubcripcion)