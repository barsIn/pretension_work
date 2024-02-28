from django.contrib import admin
from .models import Provider, Contract, Company, Department, Staff, Deliver
# Register your models here.

admin.site.register(Provider)
admin.site.register(Contract)
admin.site.register(Company)
admin.site.register(Department)
admin.site.register(Staff)
admin.site.register(Deliver)
