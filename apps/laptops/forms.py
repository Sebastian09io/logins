"""
formularios
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from .models import Laptop
from .models import UserPerfil

class LaptopForm(forms.ModelForm):
    """
    clase de formulario
    """
    class Meta:
        """
        maneja metadatos
        """
        model = Laptop
        fields = ['procesador', 'generacion', 'sistema', 'ram', 'rom',]

    def clean_generacion(self):
        """
        valida que no se ingrese generacion 0 o -
        """
        generacion = self.cleaned_data['generacion']
        if generacion <= 0:
            raise forms.ValidationError("La generación debe ser un número entero positivo.")
        return generacion

class CustomUserCreationForm(UserCreationForm):
    """
    form de user
    """
    email=forms.EmailField(required=True, label="Correoelectronico",max_length=50,
                           help_text="coloca tu correoelectronico",error_messages={
                               'invalid':'Solo puedes colocar caracteres validos para el email'})

    def clean_email(self):
        """
        clean email
        """
        email=self.cleaned_data["email"].lower()
        u=User.objects.filter(email=email)
        if u.count():
            raise ValidationError("Email ya ha sido tomado")
        return email

    def save(self,commit=True):
        user=User.objects.create_user(
            self.cleaned_data["username"],
            self.cleaned_data["email"],
            self.cleaned_data["password1"]
        )
        return user

class UserPerfilform(forms.ModelForm):
    """
    ...
    """
    class Meta:
        """
        ...
        """
        model=UserPerfil
        fields=("avatar","user")

    def __init__(self,*args,** kwargs) :
        super(UserPerfilform, self).__init__( args,** kwargs)
        self.fields["user"].widget=forms.HiddenInput()
        self.fields["user"].required=False

    def clean_avatar(self):
        """
        ...
        """
        #dimensiones de la img
        avatar=self.cleaned_data["avatar"]

        #Devuelve w-h por ello los ponemos en sus respectivas variables
        w,h=get_image_dimensions(avatar)

        #validacion por tamaño de la img
        max_width=500
        max_height=500

        if w > max_width or h > max_height:

            raise forms.ValidationError("la imagen no puede superar los %spx, %spx"%(
                max_width,max_height))

        #condicion para formato permitido de img
        m,t=avatar.content_type.split("/")

        if not(m == 'image' and t in ["jpeg",'jpg','gif','png']):
            raise forms.ValidationError("Imagen no soportada")

        if len(avatar)>(30 *1024):
            raise forms.ValidationError("Imagen muy pesada")

        return avatar
