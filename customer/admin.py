from django.contrib import admin
from customer.models import *
from mksites.admin import SubdomainAdmin

class Customeradmin(SubdomainAdmin):
     list_display = ('name','phone_number','details')

class Categoryadmin(SubdomainAdmin):
     list_display = ('name','description')
     search_fields = ['name','description']

      
      

admin.site.register(Customer,Customeradmin)
admin.site.register(CustomerCategory,Categoryadmin)
