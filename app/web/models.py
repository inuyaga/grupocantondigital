from django.db import models
from app.usuario.models import User as Usuario
from django.core.validators import FileExtensionValidator
STATUS=(
    ('pending_payment', "Pago pendiente"), 
    ('declined', "Rechazada"),
    ('expired', "Caducado"),
    ('paid', "Pagado"),
    ('refunded', "reintegrado"),
    ('partially_refunded', "reintegrado parcialmente"),
    ('charged_back', "charged_back"),
    ('pre_authorized', "pre autorizado"),
    ('voided', "anulado"),
    )

    
class CaracteristicaSubcripcion(models.Model):
    cs_id = models.AutoField(primary_key=True)
    cs_descripcion = models.CharField("Descripción", max_length=250)
    def __str__(self):
        return self.cs_descripcion
    class Meta():
        verbose_name_plural = "1.- Caracteristicas de subcripcion"
        verbose_name = "Caracteristicas subcripción"


class Tipo_subcripcion(models.Model):
    ts_id = models.AutoField(primary_key=True)
    ts_nombre = models.CharField(max_length=150, verbose_name="Nombre de subcripción")
    ts_descripcion = models.CharField(max_length=150, verbose_name="Brebe descripción")
    ts_precio=models.FloatField(verbose_name="Precio")
    ts_activo=models.BooleanField(verbose_name="Activar")
    POPULAR=(('popular', 'Mas popular'), ('No', 'No'))
    ts_most_popular = models.CharField("Popular", max_length=10, choices=POPULAR)
    TIEMPO=((30, 'Mensual'), (90, 'Trimestral'), (180, 'Semestral'), (365, 'Anual'))
    ts_tiempo = models.IntegerField("Elegir tiempo", choices=TIEMPO, default=1)
    ts_creado=models.DateTimeField(auto_now_add=True)
    ts_actualizado=models.DateTimeField(auto_now=True)
    ts_caracteristica = models.ManyToManyField(CaracteristicaSubcripcion, verbose_name="Añadir caracteristica")

    def __str__(self):
        return self.ts_nombre
    
    class Meta():
        verbose_name_plural = "2.- Tipo de subcripciones"
        verbose_name = "Tipo de subcripción"



class Orden(models.Model):
    ord_id = models.BigAutoField(primary_key=True)
    ord_user=models.ForeignKey(Usuario, null=False, blank=False, on_delete=models.CASCADE, verbose_name="Usuario")
    ord_tipo_sub=models.ForeignKey(Tipo_subcripcion, null=False, blank=False, on_delete=models.CASCADE, verbose_name="Tipo subcripcion")
    ord_payment_status=models.CharField(max_length=80,verbose_name="Status de Pago", choices=STATUS)
    ord_monto=models.FloatField("Monto")
    ord_order_id=models.CharField("Orden ID", max_length=400)
    ord_charger_id=models.CharField("Charger ID", max_length=400)
    ord_referencia=models.CharField("Referencia", max_length=250)
    ord_barcode_url=models.CharField("Codigo de barras", max_length=500, blank=True, null=True)
    ord_expira_en= models.DateTimeField("Orden espira en")
    ord_creado=models.DateTimeField("Creado", auto_now_add=True)
    ord_type_cargo = models.CharField(max_length=60, verbose_name="Tipo de cargo", default="N/A")
    ord_actualizado=models.DateTimeField("Actualizado", auto_now=True)

    def __str__(self):
        return str(self.ord_id)
    
    class Meta():
        verbose_name_plural = "4.- Ordenes"
        verbose_name = "Orden"




class Subscription(models.Model):
    sub_id = models.BigAutoField(primary_key=True)
    sub_orden = models.ForeignKey(Orden, null=False, blank=False, on_delete=models.PROTECT, verbose_name="Orden")
    sub_inicial=models.DateTimeField(verbose_name="Subscripción ncial")
    sub_final=models.DateTimeField(verbose_name="Subscripción Final")
    sub_creado=models.DateTimeField(auto_now_add=True, verbose_name="Creado")
    sub_actualizado=models.DateTimeField(auto_now=True, verbose_name="Actualizado")
    sub_status=models.BooleanField(verbose_name="Estatus", default=0)

    def __str__(self):
        return str(self.sub_id)
    
    class Meta():
        verbose_name_plural = "5.- Subscripciones"
        verbose_name = "Subscripción"


    




class Diario(models.Model): 
    do_nombre = models.CharField(max_length=100, verbose_name="Nombre")
    do_fecha_creacion=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.do_nombre


class Edicion(models.Model):
    ed_doc_pdf = models.FileField(verbose_name="PDF", upload_to="ediciones_pdf/", validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    ed_portada = models.ImageField(verbose_name="Portada de la edicion", upload_to="portadas_ediciones")
    ed_creacion = models.DateField(auto_now_add=True)
    ed_fecha_publicacion = models.DateField(verbose_name="Feha de publicación")
    ed_pertene_diario = models.ForeignKey(Diario, on_delete=models.CASCADE, verbose_name="Pertenece al diario")

    def __str__(self):
        return str(self.ed_doc_pdf)

    class Meta:
        unique_together = ['ed_creacion', 'ed_pertene_diario']
