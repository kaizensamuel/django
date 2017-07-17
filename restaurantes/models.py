from __future__ import unicode_literals


from django.db import models
from django.utils import timezone
 
class Articulo(models.Model):
	idRestaurante = models.CharField(max_length = 50)
	restaurante = models.CharField(max_length = 50)
	tipo = models.CharField(max_length = 50)
	ciudad = models.CharField(max_length = 50)
	direccion =  models.CharField(max_length = 50)
	cpostal = models.CharField(max_length = 50)
	coordenadax = models.CharField(max_length = 25)
	coordenaday = models.CharField(max_length = 25)
	
