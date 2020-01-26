from django.conf.urls import url
from django.contrib import admin
from . import views
from django.urls import path, re_path


urlpatterns = [
    path('', views.index),
    path('iniciosesion/', views.iniciosesion),
    path('cerrarsesion/', views.cerrarsesion),

    path('comunicados/', views.comunicados),
    path('subir_comunicados/', views.subir_comunicados),
    path('documentos/', views.documentos),
    path('subir_documentos/', views.subir_documentos),
    path('subir_documentos_enviados/', views.subir_documentos_enviados),

    path('secretaria/', views.secretaria),
    path('docencia/', views.docencia),
    path('vinculacion/', views.vinculacion),
    path('investigacion/', views.investigacion),
    path('laboratorio/', views.laboratorio),
    path('docentes/', views.docentes),

    path('eliminar_comunicado/', views.eliminar_comunicado),
    path('eliminar_documento/', views.eliminar_documento),
    path('eliminar_documento_enviado/', views.eliminar_documento_enviado),

    path('usuarios/', views.usuarios),
    path('crear_usuario/', views.crear_usuario),
    path('eliminar_usuario/', views.eliminar_usuario),
    path('eliminar_usuario/', views.eliminar_usuario),
    path('reset_pass/', views.reset_pass),
    re_path('restablecerpass/(?P<usuario>[\w.@+-]+)/', views.restablecerpass),
    path('new_pass/', views.new_pass),
]
