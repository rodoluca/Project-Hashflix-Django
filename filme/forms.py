from  django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from django import forms


class FormHomepage(forms.Form): #formulario padrao Django
    email = forms.EmailField(label=False)


class CriarContaForm(UserCreationForm): #formulario personalizado
    # email = forms.EmailField(required=False)
    email = forms.EmailField()

    class Meta:
        # para formularios de criação de usuario
        model = Usuario
        # os campos abaixo ja sao padronizados do Django
        fields = ('username', 'email', 'password1', 'password2')