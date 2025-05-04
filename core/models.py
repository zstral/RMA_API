from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    USER_ROLES = (
        ('user', 'User'),
        ('admin', 'Admin'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    nombre = models.CharField(max_length=100)
    rol = models.CharField(max_length=10, choices=USER_ROLES, default='user')

    def __str__(self):
        return f"{self.nombre} ({self.user.username})"

class EstacionMeteorologica(models.Model):
    codigo_nacional = models.IntegerField(primary_key=True)
    codigo_omm = models.CharField(max_length=10, blank=True)
    codigo_oaci = models.CharField(max_length=10, blank=True)
    nombre = models.CharField(max_length=255)
    latitud = models.FloatField()
    longitud = models.FloatField()
    altura = models.IntegerField()
    region = models.IntegerField()
    zona_geografica = models.CharField(max_length=100)
    url_datos = models.URLField()

    def __str__(self):
        return self.nombre
    
class Productos(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/')

    def __str__(self):
        return self.nombre
    
class Contacto(models.Model):
    direccion = models.CharField(max_length=255)
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    mensaje = models.TextField()

    def __str__(self):
        return self.nombre
