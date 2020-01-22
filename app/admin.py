from django.contrib import admin
from .models import *
from django.contrib.auth.models import User, AbstractUser

# Register your models here.

class Usuario(admin.ModelAdmin):
    list_display = ["id","usuario"]
    list_display_links = ["usuario"]
    search_fields = ['usuario']
    
    class Meta:
        model = Usuarios

class Comunicado(admin.ModelAdmin):
    list_display = ["id","titulo"]
    list_display_links = ["titulo"]
    search_fields = ['titulo']
    
    class Meta:
        model = Comunicados


class Mi_comunicad(admin.ModelAdmin):
    list_display = ["id","usuario"]
    list_display_links = ["usuario"]
    search_fields = ['usuario']
    
    class Meta:
        model = Mi_comunicado


admin.site.register(Comunicados, Comunicado),
admin.site.register(Usuarios, Usuario),
admin.site.register(Mi_comunicado, Mi_comunicad),
admin.site.register(Documentos),
admin.site.register(Mi_documento),
admin.site.register(Mi_documento_enviado),
