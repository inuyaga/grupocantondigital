from django.db import models
from django.contrib.auth import get_user_model
Usuario = get_user_model()
STATUS_SUBCRITION=((1, "ACTIVO"), (2, "INACTIVO"))

class Cliente(models.Model):
    client_id = models.AutoField(primary_key=True)
    client_conekta_id = models.CharField(verbose_name="ID Conekta", max_length=255)
    client_status=models.IntegerField("Status Cliente")
    client_user=models.ForeignKey(Usuario, null=False, blank=False, on_delete=models.CASCADE, verbose_name="Usuario")
    ts_nombre = models.CharField(max_length=150, verbose_name="Nombre de subcripción")
    ts_precio=models.FloatField(verbose_name="Precio")
    ts_token=models.CharField(max_length=100, verbose_name="Token subcripción")
    ts_activo=models.BooleanField(verbose_name="Status")
    ts_creado=models.DateTimeField(auto_now_add=True,verbose_name="Creado")
    ts_actualizado=models.DateTimeField(auto_now=True, verbose_name="Actualizado")

    def __str__(self):
        return self.ts_nombre
    


class Tipo_subcripcion(models.Model):
    ts_id = models.AutoField(primary_key=True)
    ts_nombre = models.CharField(max_length=150, verbose_name="Nombre de subcripción")
    ts_precio=models.FloatField(verbose_name="Precio")
    ts_token=models.CharField(max_length=100, verbose_name="Token subcripción")
    ts_activo=models.BooleanField(verbose_name="Status")
    ts_creado=models.DateTimeField(auto_now_add=True)
    ts_actualizado=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ts_nombre
    
    class Meta():
        verbose_name_plural = "Tipo de subcripciones"
        verbose_name = "Tipo de subcripción"

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
        verbose_name_plural = "Subcripciones"
        verbose_name = "Subcripción"

class Type_Payment(models.Model):
    tpy_id = models.BigAutoField(primary_key=True)
    tpy_name=models.CharField("Nombre", max_length=150)
    tpy_descroption=models.CharField("Descripción", max_length=300)
    def __str__(self):
        return str(self.tpy_name)
    
    class Meta():
        verbose_name_plural = "Tipo de pagos"
        verbose_name = "Tipo pago"

class Orden(models.Model):
    ord_id = models.BigAutoField(primary_key=True)
    ord_payment=models.ForeignKey(Type_Payment, null=False, blank=False, on_delete=models.PROTECT, verbose_name="Tipo pago")
    ord_cliente=models.ForeignKey(Cliente, null=False, blank=False, on_delete=models.PROTECT, verbose_name="Cliente")
    ord_payment_status=models.IntegerField(verbose_name="Status de Pago")
    ord_monto=models.FloatField("Monto")
    ord_order_id=models.CharField("Orden ID", max_length=400)
    ord_charger_id=models.CharField("Orden ID", max_length=400)
    ord_referencia=models.CharField("Referencia", max_length=250)
    ord_referencia=models.CharField("Referencia", max_length=250)
    ord_expira_en= models.DateTimeField()
    ord_creado=models.DateTimeField("Creado", auto_now_add=True)
    ord_actualizado=models.DateTimeField("Actualizado", auto_now=True)

    def __str__(self):
        return str(self.ord_id)
    
    class Meta():
        verbose_name_plural = "Ordenes"
        verbose_name = "Orden"




    




