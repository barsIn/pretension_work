from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('all/', views.all_contracts, name='all_contracts'),
    path('providers/', views.providers, name='providers'),
    path('provider/<int:prov_id>/', views.provider, name='provider_id'),
    path('providers/provider/<int:prov_id>/', views.provider, name='provider_id'),
    path('contracts/contract/<int:contract_id>/', views.show_contract, name='contract_id'),
    path('contracts/unfielded/', views.unfilded_contracts, name='unfielded'),
    path('contract/add/', views.create_contract, name='create_contract')
]