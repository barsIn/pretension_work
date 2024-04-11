from django.contrib import admin
from .models import Provider, Contract, Company, Department, Staff, Deliver
# Register your models here.

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'start_date', 'amount', 'pretension_status')
    list_display_links = ('id', 'number')
    list_per_page = 10


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('id', 'cut_name', 'sap_code')
    list_display_links = ('id', 'cut_name')
    list_per_page = 10


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'cut_name', 'sap_code')
    list_display_links = ('id', 'cut_name')
    list_per_page = 10


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'cut')
    list_display_links = ('id', 'title')
    list_per_page = 10



@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('id', 'sap_id', 'user', 'dep_director', 'main_man')
    list_display_links = ('id', 'sap_id')
    list_per_page = 10


@admin.register(Deliver)
class DeliverAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'invoice_date', 'total')
    list_per_page = 10
    # list_display_links = ('invoice')




# admin.site.register(Provider)
# admin.site.register(Contract)
# admin.site.register(Company)
# admin.site.register(Department)
# admin.site.register(Staff)
# admin.site.register(Deliver)
