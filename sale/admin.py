from django.contrib import admin
from mksites.admin import SubdomainAdmin
from sale.models import *

class SaleItemsInline(admin.TabularInline):
    model = SaleInvoiceItem

class SaleInvoiceadmin(SubdomainAdmin):
    inlines = [SaleItemsInline,]
    list_filter = ('customer','datetime')
    list_display = ('customer','datetime')
    search_fields = ['customer',]

admin.site.register(SaleInvoice,SaleInvoiceadmin)
