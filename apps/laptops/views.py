"""
    vistas
"""
import os
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as make_login
from django.contrib.auth import logout
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from apps.laptops.models import UserPerfil
from .forms import CustomUserCreationForm, LaptopForm, UserPerfilform
from .models import Laptop

# funciones de vistas.
def principal(request):
    """
    funcion de la vista principal
    """
    laptops_listadas = Laptop.objects.all()
    return render(request,'contenido.html', {"compu":laptops_listadas})

#crud
def registrar(request):
    """
    funcion que registra compus
    """
    if request.method== 'POST':
        procesador = request.POST['kprocesador']
        generacion = request.POST['kgeneracion']
        sistema = request.POST['ksistema']
        ram = request.POST['kram']
        rom = request.POST['krom']
        comp=Laptop.objects.create(procesador=procesador,generacion=generacion,
                                   sistema=sistema,ram=ram,rom=rom)
        return redirect('/')

def eliminar(request, id):
    """
    funcion que elimina con id
    """
    if request.method=='GET':
        copp=Laptop.objects.get(id=id)
        copp.delete()
        return redirect('/')

def vistaeditar(request,id):
    """
    funcion que envia a la vista de editar
    """
    laptop = Laptop.objects.get(id=id)  # Obtener la instancia existente

    return render(request,'editfrm.html', {"laptop":laptop})

def funcioneditar(request, id):
    """
    Función que edita los objetos Laptop.
    """
    if request.method=='POST':
        procesador = request.POST['kprocesador']
        generacion = request.POST['kgeneracion']
        sistema = request.POST['ksistema']
        ram = request.POST['kram']
        rom = request.POST['krom']
        laptop = Laptop.objects.get(id=id)
        laptop.procesador=procesador
        laptop.generacion=generacion
        laptop.sistema=sistema
        laptop.ram=ram
        laptop.rom=rom
        laptop.save()
        return redirect('/')

def vistaprb(request):
    """
    Función que manda a la vista prb .
    """
    if request.method == 'POST':
        form = LaptopForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = LaptopForm()
    return render(request,'prb.html', {'form': form})

#login
def registro(request):
    """
    funcion registra usuarios
    """
    form= UserCreationForm()
    if request.method == "POST":
        form=CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            user=form.save()
            if user is not None:
                make_login(request,user)
                return redirect(reverse("profile"))
    return render(request,'registro.html',{'form':form})

@login_required
def profile(request):
    """
    perfil
    """
    form=UserPerfilform()
    if request.method == "POST":
        #Sim esta la imagen la reemplaza de lo contrario la crea
        try: #avatar anterior

            Userperfil=UserPerfil.objects.get(user=request.user)
            form=UserPerfilform(request.POST,request.FILES,instance=Userperfil)
            #Eliminar el avatar anterior, obtenemos el path
            pathAvatarViejo=os.path.join(settings.MEDIA_ROOT,Userperfil.avatar.name)

        except ObjectDoesNotExist:
            form=UserPerfilform(request.POST,request.FILES)

        if form.is_valid():
            #Preguntamos si existe el avatar viejo
            if pathAvatarViejo is not None and os.path.isfile(pathAvatarViejo):
                os.remove(pathAvatarViejo)
            userProfile=form.save(commit=False)
            userProfile.user=request.user
            userProfile.save()

    return render(request, 'registration/profile.html',{'form':form})

def logout_view(request):
    """
    perfil out
    """
    logout(request)
    return redirect('login')

def funruta(request):
    """
    pasa de login a principal
    """
    return render(request,'registration/profile.html')
