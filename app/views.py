from django.shortcuts import render, redirect
from django.utils import timezone
from .models import *
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import JsonResponse, HttpResponse, HttpRequest, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import login, authenticate, logout
from django.core.mail import EmailMessage
from django.conf import settings
from django.core import serializers
from django.contrib.auth.hashers import check_password
import json
import smtplib
import sweetify
import datetime

# Create your views here.

# LOGIN Y CERRAR SESION
def iniciosesion(request):
    username = request.POST.get("usuario")
    password = request.POST.get("password")
    print("Esto llego: ", username)
    
    try: 
        username = authenticate(request, username=username, password=password)
        login(request,username)
        return redirect('/')
    except Exception as e:
        sweetify.error(request, 'Oops!', text='¡El Usuario y/o Contraseña es Incorrecto!', persistent=':´(')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

def cerrarsesion(request):
	logout(request)
	return HttpResponseRedirect("/")

#index
def index(request):
    usuario = request.user
    print("usuario logeado: ", usuario)
    if usuario.is_active:
        usuarios = Usuarios.objects.get(usuario=usuario)

        datos = {"usuario":usuarios}
        return render (request, 'index.html', datos)
    else:
        return render(request, 'login.html',{})

#Vistas para departamentos de JEFACTURA

def secretaria(request):
    usu = request.user
    usuario_actual = Usuarios.objects.get(usuario=usu)

    usuario = "Secretaria"
   
    usuarios = Usuarios.objects.get(tipo=usuario)

    documentos_enviados = Mi_documento.objects.filter(usuario__tipo= usuarios.tipo)
    documentos_recibidos = Mi_documento_enviado.objects.filter(usuario__tipo= usuarios.tipo)
   
    datos = {"usuario": usuario_actual, "documentos_enviados":documentos_enviados, "documentos_recibidos":documentos_recibidos}

    return render(request, 'secretaria.html', datos)

def docencia(request):
    usu = request.user
    usuario_actual = Usuarios.objects.get(usuario=usu)

    usuario = "Jefactura de Docencia"
   
    usuarios = Usuarios.objects.get(tipo=usuario)

    documentos_enviados = Mi_documento.objects.filter(usuario__tipo= usuarios.tipo)
    documentos_recibidos = Mi_documento_enviado.objects.filter(usuario__tipo= usuarios.tipo)
   
   
    datos = {"usuario": usuario_actual, "documentos_enviados":documentos_enviados, "documentos_recibidos":documentos_recibidos}

    return render(request, 'docencia.html', datos)

def vinculacion(request):
    usu = request.user
    usuario_actual = Usuarios.objects.get(usuario=usu)

    usuario = "Jefactura de Vinculacion"
   
    usuarios = Usuarios.objects.get(tipo=usuario)

    documentos_enviados = Mi_documento.objects.filter(usuario__tipo= usuarios.tipo)
    documentos_recibidos = Mi_documento_enviado.objects.filter(usuario__tipo= usuarios.tipo)
   
    datos = {"usuario": usuario_actual, "documentos_enviados":documentos_enviados, "documentos_recibidos":documentos_recibidos}

    return render(request, 'vinculacion.html', datos)

def investigacion(request):
    usu = request.user
    usuario_actual = Usuarios.objects.get(usuario=usu)

    usuario = "Jefactura de Investigacion"
   
    usuarios = Usuarios.objects.get(tipo=usuario)

    documentos_enviados = Mi_documento.objects.filter(usuario__tipo= usuarios.tipo)
    documentos_recibidos = Mi_documento_enviado.objects.filter(usuario__tipo= usuarios.tipo)
   
    datos = {"usuario": usuario_actual,"documentos_enviados":documentos_enviados, "documentos_recibidos":documentos_recibidos}

    return render(request, 'investigacion.html', datos)

def laboratorio(request):
    usu = request.user
    usuario_actual = Usuarios.objects.get(usuario=usu)

    usuario = "Jefactura de Laboratorio"
   
    usuarios = Usuarios.objects.get(tipo=usuario)

    documentos_enviados = Mi_documento.objects.filter(usuario__tipo= usuarios.tipo)
    documentos_recibidos = Mi_documento_enviado.objects.filter(usuario__tipo= usuarios.tipo)
   
    datos = {"usuario": usuario_actual,"documentos_enviados":documentos_enviados, "documentos_recibidos":documentos_recibidos}

    return render(request, 'laboratorio.html', datos)

def docentes(request):
    usu = request.user
    usuario_actual = Usuarios.objects.get(usuario=usu)

    usuario = "Docentes"
   
    usuarios = Usuarios.objects.get(tipo=usuario)

    documentos_enviados = Mi_documento.objects.filter(usuario__tipo= usuarios.tipo)
    documentos_recibidos = Mi_documento_enviado.objects.filter(usuario__tipo= usuarios.tipo)
   
    datos = {"usuario": usuario_actual, "documentos_enviados":documentos_enviados, "documentos_recibidos":documentos_recibidos}

    return render(request, 'docentes.html', datos)

#guarda los comunicados
def comunicados(request):
    usuario = request.user
    usuarios = Usuarios.objects.get(usuario=usuario)
    comunicados = Comunicados.objects.all()
    comunicados_secretaria = Mi_comunicado.objects.filter(usuario__tipo= usuarios.tipo)

    datos = {"comunicados":comunicados, "usuario":usuarios,"comunicados_secretaria":comunicados_secretaria}

    return render(request, 'avisos.html', datos)

#consulta los documentos en otros usuarios
def documentos(request):
    usuario = request.user
    usuarios = Usuarios.objects.get(usuario=usuario)

    documentos_recibidos = Mi_documento.objects.filter(usuario__tipo= usuarios.tipo)
    documentos_enviados = Mi_documento_enviado.objects.filter(usuario__tipo= usuarios.tipo)
    print("Enviando objetos: ", documentos_enviados)

    datos = {"usuario":usuarios,"documentos_recibidos":documentos_recibidos, "documentos_enviados":documentos_enviados}

    return render(request, 'documentos.html', datos)

#vista para control de subir comunicados
def subir_comunicados(request):
    usuarios = request.POST.getlist("usuario")
    
    titulo = request.POST.get("titulo")
    descripcion = request.POST.get("descripcion")
    documento = request.POST.get("documento")
    imagen = request.POST.get("imagen")
    link = request.POST.get("link")

    comunicado = Comunicados.objects.create(titulo=titulo, descripcion=descripcion, documento=documento,
    imagen=imagen, link=link)

    for b in usuarios:
        c = Usuarios.objects.get(tipo=b)
        mi_comunicado = Mi_comunicado.objects.create(usuario=c, comunicado=comunicado)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

def subir_documentos(request):
    usuario = request.POST.get("usuario")

    titulo = request.POST.get("titulo")
    descripcion = request.POST.get("descripcion")
    documento = request.POST.get("documento")

    save_documento = Documentos.objects.create(titulo=titulo,descripcion=descripcion,documento=documento)

    mi_usuario = Usuarios.objects.get(tipo=usuario)
    mi_documento = Mi_documento.objects.create(usuario=mi_usuario, documento=save_documento)

    print("Documento guardado con éxito")


    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))


def subir_documentos_enviados(request):
    usu = request.POST.get("usuario")
    print("usuario logeado: ", usu)
    usuario = User.objects.get(username=usu)

    titulo = request.POST.get("titulo")
    descripcion = request.POST.get("descripcion")
    documento = request.POST.get("documento")

    mi_usuario = Usuarios.objects.get(usuario=usuario)
    save_documento = Documentos.objects.create(titulo=titulo,descripcion=descripcion,documento=documento)
    mi_documento = Mi_documento_enviado.objects.create(usuario=mi_usuario, documento=save_documento)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))


#vistas para eliminar los documentos
def eliminar_comunicado(request):
    id_comunicado = request.POST.get("deletecomunicado")
    print("Recibiendo id: ", id_comunicado)

    comunicado = Comunicados.objects.get(id= id_comunicado)
    print("Mi comunicado: ", comunicado)
    comunicado.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))


def eliminar_documento(request):
    id_comunicado = request.POST.get("deletedocumento")
    print("Recibiendo id: ", id_comunicado)

    comunicado = Mi_documento.objects.get(id= id_comunicado)
    print("Mi comunicado: ", comunicado)

    comunicado.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

def eliminar_documento_enviado(request):
    id_comunicado = request.POST.get("deletedocumentoenviado")
    print("Recibiendo id: ", id_comunicado)

    comunicado = Mi_documento_enviado.objects.get(id= id_comunicado)
    print("Mi comunicado: ", comunicado)

    comunicado.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

#Creacion y control de usuarios para la jefactura

def usuarios(request):
    usu = request.user
    usuario_actual = Usuarios.objects.get(usuario=usu)

    todos_usuarios = Usuarios.objects.all()


    datos = {"usuario":usuario_actual, "todos_usuarios":todos_usuarios}

    return render(request, 'usuarios.html', datos)

def crear_usuario(request):
    nombre = request.POST.get("nombre")
    apellidos = request.POST.get("apellido")
    correo = request.POST.get("correo")
    usuario = request.POST.get("usuario")
    password = request.POST.get("contrasena")

    tipo = request.POST.get("tipo")

    user = User.objects.filter(username=usuario).exists()
    if user == False:
        user = User.objects.create_user(first_name=nombre,
        last_name = apellidos,
        email = correo,
        username = usuario,
        password = password)
        user = authenticate(request, username=usuario, password=password)
        
        print("usuario creado con exito ")

        tipo_usuario = Usuarios.objects.create(usuario=user, tipo=tipo)


    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))


def eliminar_usuario(request):
    id_usuario = request.POST.get("deleteuser")
    print("Recibiendo id: ", id_usuario)

    usuario = User.objects.get(id= id_usuario)
    print("Mi comunicado: ", usuario)

    usuario.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))


def reset_pass(request):
    correo = User.objects.filter(email=request.POST.get("correo")).exists()
    print("si existe el correo")
    if correo==True:
        usuario = User.objects.get(email=request.POST.get("correo"))
        sesion = "Se ha enviado un enlace a su correo para que recupere su contraseña"
        email = EmailMessage('Recuperar contraseña', 'Para poder ingresar de nuevo  de click en el siguiente enlace\nhttp://localhost:8000/restablecerpass/'+usuario.username+"/",to = [request.POST.get("correo")])
        #email = EmailMessage('Recuperar contraseña de Tecnodidáctica', 'Para poder ingresar de nuevo a TECNODIDÁCTICA de click en el siguiente enlace\nhttps://wwww.tecnodidactica.com/resetpass/'+usuario.username+"/",to = [request.POST.get("correo")])
        email.send()
        a = "Por favor, verifique su bandeja de entrada"
        data = {"a":a}
        print("Envio exitoso de correo")
        
        return JsonResponse(data)


def restablecerpass(request, usuario):
	return render(request, 'new_pass.html', {'usuario':usuario})


def new_pass(request):
    usuario =  request.POST.get("usuario")
    contrasena = request.POST.get("newpass")
    validar_contrasena = request.POST.get("newpassdos")
    if contrasena == validar_contrasena:
        mi_usuario = User.objects.get(username = request.POST.get('usuario'))
        mi_usuario.set_password(contrasena)
        mi_usuario.save()
        # resultado = 1
        # # data = {"resultado":resultado}
        return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/")
        









