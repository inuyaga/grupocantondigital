from django.db import models
from django.contrib.auth.models import AbstractUser
class User(AbstractUser):
    id_cliente_conekta = models.CharField(max_length=100, verbose_name="ID Conekta", null=True, blank=True)
    foto_perfil = models.ImageField('Foto Perfil', upload_to='foto_perfil/', null=True, blank=True)
    telefono = models.CharField('Telefono',max_length=12, null=True, blank=True)
    class Meta:
        db_table = 'auth_user'  