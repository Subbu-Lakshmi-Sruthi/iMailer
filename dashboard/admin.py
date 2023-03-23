from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Templates)
admin.site.register(models.Mail)
admin.site.register(models.Log)
