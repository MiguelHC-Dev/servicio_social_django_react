from django.contrib import admin
from .models import Usuario, Carrera, TiposFormatos, Formato, ServicioSocial



# Register your models here.
admin.site.register(Usuario)
admin.site.register(Carrera)
admin.site.register(TiposFormatos)
admin.site.register(Formato)
admin.site.register(ServicioSocial)
