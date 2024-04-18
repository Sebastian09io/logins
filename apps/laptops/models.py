"""
Este módulo define los modelos de la aplicación de laptops.
"""
from django.db import models
from django.contrib.auth.models import User
# modelo de laptop, relacion uno a muchos laptop-entorno
class Laptop(models.Model):
    """
    Modelo que representa una laptop.
    """
    procesador = models.CharField(max_length=100)
    generacion = models.IntegerField()
    sistema = models.CharField(max_length=100)
    ram = models.CharField(max_length=100)
    rom = models.CharField(max_length=100)

    objects = models.Manager()

    def __str__(self):
        texto = "{0} ({1})"
        return texto.format(self.procesador,self.generacion,self.sistema,self.ram,self.rom)

#uno a muchos
class Entorno(models.Model):
    """
    Modelo de entornos de inicio de sesion.
    """
    usuario = models.CharField(max_length=100)
    contrasena = models.CharField(max_length=100)
    laptop = models.ForeignKey(Laptop, on_delete=models.CASCADE)

#muchos a muchos
class Cargador(models.Model):
    """
    modelo de cargador de laptop
    """
    voltaje = models.IntegerField()
    color = models.CharField(max_length=100)
    cargadores = models.ManyToManyField(Laptop)

#uno a uno
class Oficina(models.Model):
    """
    modelo de oficina que pertenece la laptop
    """
    linea = models.CharField(max_length=100)
    ofis = models.OneToOneField(Laptop, on_delete=models.CASCADE)

#modelo del login
class UserPerfil(models.Model):
    """
    modelo userperfil
    """
    objects = models.Manager()
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    avatar=models.ImageField(upload_to="user/avatar/")
    
    
    
