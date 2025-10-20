from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.dashboard, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('agenda/', views.agenda, name='agenda'),
    path('pacientes/', views.pacientes, name='pacientes'),
    path('financeiro/', views.financeiro, name='financeiro'),
]