from django.db import models
from django.contrib.auth import get_user_model
Usuario = get_user_model()
STATUS_SUBCRITION=((1, "ACTIVO"), (2, "INACTIVO"))
STATUS_CLIENT=((1, "ACTIVO"), (2, "INACTIVO"))
STATUS_PAGO=((1, "PENDIENTE"), (2, "APROBADO"))

class Cliente(models.Model):
    client_id = models.AutoField(primary_key=True)
    client_conekta_id = models.CharField(verbose_name="ID Conekta", max_length=255)
    client_status=models.IntegerField("Status Cliente", choices=STATUS_CLIENT)
    client_user=models.ForeignKey(Usuario, null=False, blank=False, on_delete=models.CASCADE, verbose_name="Usuario")
    client_creado=models.DateTimeField("Creado",auto_now_add=True)
    client_actualizado=models.DateTimeField("Actualizado", auto_now=True)

    def __str__(self):
        return str(self.client_user)
    class Meta():
        verbose_name_plural = "1.- Clientes"
        verbose_name = "Cliente"
    
class CaracteristicaSubcripcion(models.Model):
    cs_id = models.AutoField(primary_key=True)
    cs_descripcion = models.CharField("Descripción", max_length=250)
    def __str__(self):
        return self.cs_descripcion


class Tipo_subcripcion(models.Model):
    ts_id = models.AutoField(primary_key=True)
    ts_nombre = models.CharField(max_length=150, verbose_name="Nombre de subcripción")
    ts_descripcion = models.CharField(max_length=150, verbose_name="Brebe descripción")
    ts_precio=models.FloatField(verbose_name="Precio")
    ts_token=models.CharField(max_length=100, verbose_name="Token subcripción")
    ts_activo=models.BooleanField(verbose_name="Activar")
    POPULAR=(('popular', 'Mas popular'), ('No', 'No'))
    ts_most_popular = models.CharField("Popular", max_length=10, choices=POPULAR)
    TIEMPO=((1, 'Mensual'), (2, 'Trimestral'), (3, 'Semestral'), (4, 'Anual'))
    ts_tiempo = models.IntegerField("Elegir tiempo", choices=TIEMPO, default=1)
    ts_creado=models.DateTimeField(auto_now_add=True)
    ts_actualizado=models.DateTimeField(auto_now=True)
    ts_caracteristica = models.ManyToManyField(CaracteristicaSubcripcion, verbose_name="Añadir caracteristica")

    def __str__(self):
        return self.ts_nombre
    
    class Meta():
        verbose_name_plural = "2.- Tipo de subcripciones"
        verbose_name = "Tipo de subcripción"

class Type_Payment(models.Model):
    tpy_id = models.BigAutoField(primary_key=True)
    tpy_name=models.CharField("Nombre", max_length=150)
    tpy_description=models.CharField("Descripción", max_length=300)
    def __str__(self):
        return str(self.tpy_name)
    
    class Meta():
        verbose_name_plural = "3.- Tipo de pagos"
        verbose_name = "Tipo pago"

class Subcription(models.Model):
    sub_id = models.BigAutoField(primary_key=True)
    sub_tip = models.ForeignKey(Tipo_subcripcion, null=False, blank=False, on_delete=models.PROTECT, verbose_name="Tipo de subcripción")
    sub_cliente = models.ForeignKey(Cliente, null=False, blank=False, on_delete=models.PROTECT, verbose_name="Cliente")
    sub_inicial=models.DateTimeField(verbose_name="Subcripción ncial")
    sub_final=models.DateTimeField(verbose_name="Subcripción Final")
    sub_status=models.IntegerField(choices=STATUS_SUBCRITION, default=2)
    sub_token_cart=models.CharField(verbose_name="Token Cart", max_length=255)
    sub_creado=models.DateTimeField(auto_now_add=True, verbose_name="Creado")
    sub_actualizado=models.DateTimeField(auto_now=True, verbose_name="Actualizado")

    def __str__(self):
        return str(self.sub_id)
    
    class Meta():
        verbose_name_plural = "4.- Subcripciones"
        verbose_name = "Subcripción"



class Orden(models.Model):
    ord_id = models.BigAutoField(primary_key=True)
    ord_payment=models.ForeignKey(Type_Payment, null=False, blank=False, on_delete=models.PROTECT, verbose_name="Tipo pago")
    ord_cliente=models.ForeignKey(Subcription, null=False, blank=False, on_delete=models.PROTECT, verbose_name="Subcripción")
    ord_payment_status=models.IntegerField(verbose_name="Status de Pago", choices=STATUS_PAGO)
    ord_monto=models.FloatField("Monto")
    ord_order_id=models.CharField("Orden ID", max_length=400)
    ord_charger_id=models.CharField("Charger ID", max_length=400)
    ord_referencia=models.CharField("Referencia", max_length=250)
    ord_expira_en= models.DateTimeField("Orden espira en")
    ord_creado=models.DateTimeField("Creado", auto_now_add=True)
    ord_actualizado=models.DateTimeField("Actualizado", auto_now=True)

    def __str__(self):
        return str(self.ord_id)
    
    class Meta():
        verbose_name_plural = "5.- Ordenes"
        verbose_name = "Orden"




    




