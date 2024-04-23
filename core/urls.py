"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.laptops import views
from apps.laptops.views import principal, funruta, Pagbusq


app_name="app"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',principal.as_view(),name='inicio'),
    path('registrarCompu/',views.registrar,name='registrar'),
    path('vistaed/<int:id>',views.vistaeditar, name='vistae'),
    path('funeditarCompu/<int:id>',views.funcioneditar, name='modificando'),
    path('eliminarcompu/<int:id>',views.eliminar, name='eliminarc'),
    path('vistaprueba/',views.vistaprb,name='vistprb'),
    path('nuevdd',funruta,name='nuevaruta'),
    #del login registrar
    # path('',views.inicio,name="inicio"),
    # path('user_data/',views.user_data,name="user_data"),
    path('profile/',views.profile,name="profile"),
    path('registro/',views.registro,name="registro"),
    # path("app/", include("apps.laptops.urls")),

    path("accounts/",include("django.contrib.auth.urls"),name="login"),
    # path("cambiar-clave/",auth_views.PasswordChangeView.as_view(template_name="registration/
    # password_change_form.html")),
    path('logout/', views.logout_view, name='logout'),
    path('pag/',views.paginacion,name="pagina"),
    path('buscar/', views.buscar, name='buscar'),
    path('busq/',Pagbusq.as_view(),name="busqueda"),


    
]

#Para consumir archivos media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
