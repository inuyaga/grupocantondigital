from django.contrib import admin

from app.web.models import *

# Register your models here.

class EdicionConfig(admin.ModelAdmin):
    list_display = [
        'id',
        'ed_doc_pdf',
        'ed_portada',
        'ed_creacion',
        'ed_fecha_publicacion',
        'ed_pertene_diario',
        ]

admin.site.register(Orden)
admin.site.register(Subscription)
admin.site.register(Tipo_subcripcion)
admin.site.register(CaracteristicaSubcripcion)
admin.site.register(Diario)
admin.site.register(Edicion, EdicionConfig)