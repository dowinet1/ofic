from django.db import models
from django.contrib.auth.models import User, AbstractUser
import json

# from __future__ import unicode_literals
# import os, sys
# from django.utils import timezone
# import datetime
# from django.db import migrations
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.conf import settings


# Create your models here.

TIPOS_USUARIO = (
	('Jefactura ISC','Jefactura ISC'),
	('Secretaria','Secretaria'),
    ('Jefactura de Docencia', 'Jefactura de Docencia'),
    ('Jefactura de Vinculacion', 'Jefactura de Vinculacion'),
    ('Jefactura de Investigacion', 'Jefactura de Investigacion'),
    ('Jefactura de Laboratorio', 'Jefactura de Laboratorio'),
    ('Docentes', 'Docentes'),
)

class Usuarios(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=100, choices=TIPOS_USUARIO)

    
class Comunicados(models.Model):
    titulo = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.CharField(max_length=50, blank=True, null=True)
    documento = models.FileField(upload_to ='doc_comunicados/', blank=True, null=True) 
    imagen = models.ImageField(verbose_name="Imagen", upload_to="img_comunicados")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    link = models.URLField(null=True, blank=True)


class Mi_comunicado(models.Model):
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    comunicado = models.ForeignKey(Comunicados, on_delete=models.CASCADE)


class Documentos(models.Model):
    titulo = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.CharField(max_length=50, blank=True, null=True)
    documento = models.FileField(upload_to ='doc_documentos/', blank=True, null=True) 
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

class Mi_documento(models.Model):
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    documento = models.ForeignKey(Documentos, on_delete=models.CASCADE)

class Mi_documento_enviado(models.Model):
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    documento = models.ForeignKey(Documentos, on_delete=models.CASCADE)





