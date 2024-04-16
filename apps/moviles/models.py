"""
Este módulo define los modelos de la aplicación de moviles.
"""
from django.db import models

# modelo de laptop
class Movil(models.Model):
    """
    Modelo que representa un movil.
    """
    numero_nucleos = models.IntegerField()
    marca = models.CharField(max_length=100)
    sistema = models.CharField(max_length=100)
    ram = models.CharField(max_length=100)
    rom = models.CharField(max_length=100)
