from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from core.models import EstacionMeteorologica

class UserRegisterForm(UserCreationForm):
    nombre = forms.CharField(max_length=100, required=True, label="Nombre completo")
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'nombre', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, label="Nombre de usuario")
    password = forms.CharField(widget=forms.PasswordInput, required=True, label="Contraseña")
    
class EstacionMeteorologicaForm(forms.ModelForm):
    class Meta:
        model = EstacionMeteorologica
        fields = ['codigo_nacional', 'codigo_omm', 'codigo_oaci', 'nombre', 'latitud', 'longitud', 'altura', 'region', 'zona_geografica', 'url_datos']
        widgets = {
            'url_datos': forms.URLInput(attrs={'placeholder': 'https://example.com'}),
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre de la estación'}),
            'zona_geografica': forms.TextInput(attrs={'placeholder': 'Zona geográfica'}),
        }