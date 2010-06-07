from django.contrib import admin
from purchase.models import *
from mksites.admin import SubdomainAdmin

class Paymentadmin(SubdomainAdmin):
   list_display = ('mode','description','invoice')
   list_filter = ('mode','description','invoice')


class PurchaseItemsInline(admin.TabularInline):
   model = PurchaseInvoiceItem
    

class PurchaseInvoiceadmin(SubdomainAdmin): 
   inlines = [PurchaseItemsInline,]
   list_filter = ('company','datetime')
   list_display = ('company','datetime')
   search_fields = ['company',]

admin.site.register(Payment,Paymentadmin)
admin.site.register(PurchaseInvoice,PurchaseInvoiceadmin)
