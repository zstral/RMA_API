from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegisterForm, EstacionMeteorologicaForm
from .models import EstacionMeteorologica, UserProfile
from django.contrib import messages
from .decorators import user_required, admin_required
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import EstacionMeteorologicaSerializer

def home(request, section=None):
    sections = {
        None: {'template': 'home.html', 'title': 'Inicio', 'stylesheet': 'css/home.css'},
        'dashboard': {'template': 'dashboard.html', 'title': 'Dashboard', 'stylesheet': 'css/dashboard.css', 'decorator': user_required},
        'dashboard-admin': {'template': 'dashboard-admin.html', 'title': 'Panel de Administración', 'stylesheet': 'css/dashboard-admin.css', 'decorator': admin_required},
        'map': {'template': 'map.html', 'title': 'Mapa', 'stylesheet': 'css/map.css'},
        'contact': {'template': 'contact.html', 'title': 'Contacto', 'stylesheet': 'css/contact.css'},
        'api': {'template': 'api.html', 'title': 'API', 'stylesheet': 'css/api.css'},
        'products': {'template': 'products.html', 'title': 'Productos', 'stylesheet': 'css/products.css'},
        'signup': {'template': 'signup.html', 'title': 'Registrarse', 'stylesheet': 'css/signup.css'},
    }
    data_section = sections.get(section, sections[None])
    
    if 'decorator' in data_section:
        context = {
            'current_section': section,
            'title': data_section['title'],
            'stylesheet': data_section['stylesheet'],
            'estaciones': EstacionMeteorologica.objects.all(),
        }
        view_func = data_section['decorator'](lambda req: render(req, data_section['template'], context))
        return view_func(request)

    if section == 'signup':
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                try:
                    user = form.save()
                    UserProfile.objects.create(user=user, nombre=form.cleaned_data['nombre'], rol='user')
                    messages.success(request, f'¡Cuenta creada! Inicia sesión.')
                    return redirect('home')
                except IntegrityError:
                    messages.error(request, 'El nombre de usuario o email ya está en uso.')
            else:
                messages.error(request, 'Corrige los errores en el formulario.')
            context = {
                'current_section': section,
                'title': data_section['title'],
                'stylesheet': data_section['stylesheet'],
                'form': form,
            }
            return render(request, data_section['template'], context)
        else:
            form = UserRegisterForm()
        context = {
            'current_section': section,
            'title': data_section['title'],
            'stylesheet': data_section['stylesheet'],
            'form': form,
        }
        return render(request, data_section['template'], context)

    if section is None:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            if not username or not password:
                messages.error(request, 'Por favor, completa todos los campos.')
            else:
                user = authenticate(request, username=username, password=password)
                if user is None:
                    messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
                else:
                    login(request, user)
                    messages.success(request, '¡Sesión iniciada!')
                    if hasattr(user, 'profile') and user.profile.rol == 'admin':
                        return redirect('dashboard-admin')
                    return redirect('dashboard')
        context = {
            'current_section': section,
            'title': data_section['title'],
            'stylesheet': data_section['stylesheet'],
        }
        return render(request, data_section['template'], context)
    
    context = {
        'current_section': section,
        'title': data_section['title'],
        'stylesheet': data_section['stylesheet'],
    }
    return render(request, data_section['template'], context)

def logout_view(request):
    logout(request)
    messages.success(request, '¡Sesión cerrada!')
    return redirect('home')

@require_POST
@admin_required
def create_estacion(request):
    form = EstacionMeteorologicaForm(request.POST)
    if form.is_valid():
        estacion = form.save()
        return JsonResponse({
            'success': True,
            'estacion': {
                'codigo_nacional': estacion.codigo_nacional,
                'nombre': estacion.nombre,
                'latitud': estacion.latitud,
                'longitud': estacion.longitud,
                'altura': estacion.altura,
                'zona_geografica': estacion.zona_geografica,
            }
        })
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)

@admin_required
def edit_estacion(request, codigo_nacional):
    estacion = get_object_or_404(EstacionMeteorologica, codigo_nacional=codigo_nacional)
    if request.method == 'POST':
        form = EstacionMeteorologicaForm(request.POST, instance=estacion)
        if form.is_valid():
            estacion = form.save()
            return JsonResponse({
                'success': True,
                'estacion': {
                    'codigo_nacional': estacion.codigo_nacional,
                    'nombre': estacion.nombre,
                    'latitud': estacion.latitud,
                    'longitud': estacion.longitud,
                    'altura': estacion.altura,
                    'zona_geografica': estacion.zona_geografica,
                }
            })
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    form = EstacionMeteorologicaForm(instance=estacion)
    return JsonResponse({'success': True, 'form': form.as_p()})

@require_POST
@admin_required
def delete_estacion(codigo_nacional):
    estacion = get_object_or_404(EstacionMeteorologica, codigo_nacional=codigo_nacional)
    estacion.delete()
    return JsonResponse({'success': True})

# Vistas para la API

class EstacionesLista(generics.ListAPIView):
    queryset = EstacionMeteorologica.objects.all()
    serializer_class = EstacionMeteorologicaSerializer
    permission_classes = [IsAuthenticated]

class EstacionCodigo(generics.RetrieveAPIView):
    queryset = EstacionMeteorologica.objects.all()
    serializer_class = EstacionMeteorologicaSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'codigo_nacional'