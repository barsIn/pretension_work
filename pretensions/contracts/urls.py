from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('providers/', views.providers, name='providers'),
    path('provider/<int:prov_id>/', views.provider, name='provider_id'),
    path('providers/provider/<int:prov_id>/', views.provider, name='provider_id'),
]