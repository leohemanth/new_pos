from django.contrib import admin
from product.models import *
from mksites.admin import SubdomainAdmin


class Categoryadmin(SubdomainAdmin):
    list_display = ('name','description')
    search_fields = ['name','description']



class Productadmin(SubdomainAdmin):
    list_display = ('name','description','shortcut','category','image')
    list_filter = ('name','description','shortcut','category')
    search_fields = ['name','description','shortcut']

admin.site.register(Product,Productadmin)
admin.site.register(ProductCategory,Categoryadmin)
