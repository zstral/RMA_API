from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.UserProfile)
admin.site.register(models.EstacionMeteorologica)
admin.site.register(models.Productos)
admin.site.register(models.Contacto)