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
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/')

    def __str__(self):
        return self.nombre
    
class Contacto(models.Model):
    id = models.AutoField(primary_key=True)
    direccion = models.CharField(max_length=255)
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    mensaje = models.TextField()

    def __str__(self):
        return self.nombre

class DatoMeteorologico(models.Model):
    id = models.AutoField(primary_key=True)
    estacion = models.ForeignKey(EstacionMeteorologica, on_delete=models.CASCADE, related_name='datos')
    fecha = models.DateField()
    temperatura = models.FloatField(null=True, blank=True)
    precipitacion = models.FloatField(null=True, blank=True)
    velocidad_viento = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.estacion.nombre} - {self.fecha}"

    class Meta:
        unique_together = ('estacion', 'fecha')

class Pedido(models.Model):
    ESTADOS = (
        ('pendiente', 'Pendiente'),
        ('procesado', 'Procesado'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
    )
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pedidos')
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE, related_name='pedidos')
    cantidad = models.PositiveIntegerField(default=1)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Pedido {self.id} - {self.usuario.username} - {self.producto.nombre}"

    def save(self, *args, **kwargs):
        self.total = self.producto.precio * self.cantidad
        super().save(*args, **kwargs)