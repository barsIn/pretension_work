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
    path('contract/add/', views.create_contract, name='create_contract'),
    path('provider/add/', views.create_provider, name='create_provider'),
    path('deliver/add/<int:contract_id>/', views.create_deliver, name='create_deliver'),
    path('deliver/pay/add/<int:deliver_id>/', views.add_payment, name='add_payment'),
]