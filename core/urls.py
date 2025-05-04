from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.home, {'section': 'dashboard'}, name='dashboard'),
    path('dashboard-admin/', views.home, {'section': 'dashboard-admin'}, name='dashboard-admin'),
    path('map/', views.home, {'section': 'map'}, name='map'),
    path('contact/', views.home, {'section': 'contact'}, name='contact'),
    path('api/', views.home, {'section': 'api'}, name='api'),
    path('products/', views.home, {'section': 'products'}, name='products'),
    path('signup/', views.home, {'section': 'signup'}, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('estacion/create/', views.create_estacion, name='create_estacion'),
    path('estacion/<int:codigo_nacional>/edit/', views.edit_estacion, name='edit_estacion'),
    path('estacion/<int:codigo_nacional>/delete/', views.delete_estacion, name='delete_estacion'),
    path('api/estaciones/', views.EstacionesLista.as_view(), name='estacion-list'),
    path('api/estaciones/<int:codigo_nacional>/', views.EstacionCodigo.as_view(), name='estacion-detail'),
]