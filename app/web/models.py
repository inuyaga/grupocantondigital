from django.db import models

# Create your models here.
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
