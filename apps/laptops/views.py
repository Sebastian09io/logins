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
from django.views.generic import TemplateView, ListView
from django.conf import settings
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from apps.laptops.models import UserPerfil
from .forms import CustomUserCreationForm, LaptopForm, UserPerfilform
from .models import Laptop

# funciones de vistas.
class principal(ListView):
    """
    funcion de la vista principal
    """
    model=Laptop
    template_name='contenido.html'
    context_object_name='compu'
    queryset=Laptop.objects.all()
    

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

def paginacion(request):
    """
    entra a la vista de paginacion
    """
    laptops_listadas = Laptop.objects.all()
    paginator=Paginator(laptops_listadas, 3)
    pagina=request.GET.get("page") or 1
    posts =paginator.get_page(pagina)
    pagina_actual=int(pagina)
    npagina = range(1,posts.paginator.num_pages + 1)
    return render(request,'paggina.html', {"posts":posts,
                                        "npagina":npagina, "pagina_actual":pagina_actual})
    
    # views.py

def buscar(request):
    # Recuperar la consulta de búsqueda del parámetro GET
    query = request.GET.get('buscar', '')

    # Inicializar resultados como una lista vacía
    resultados = []

    if query:
        # Filtrar resultados por coincidencias en varios campos
        resultados = Laptop.objects.filter(
            Q(procesador__icontains=query) | 
            Q(generacion__icontains=query) | 
            Q(sistema__icontains=query) | 
            Q(ram__icontains=query) | 
            Q(rom__icontains=query)
        )
    
    return render(request, 'busqueda.html', {'resultados': resultados, 'query': query})

class Pagbusq(TemplateView):
    
    template_name='busqueda.html'
    
    


