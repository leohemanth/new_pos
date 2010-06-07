from django.contrib import admin
from product.models import *
from mksites.admin import SubdomainAdmin


class Categoryadmin(SubdomainAdmin):
    list_display = ('name','description')
    search_fields = ['name','description']



class Productadmin(SubdomainAdmin):
    def thumbnail(self,url):
        return """<img src="%s" />""" %("http://asimpleerp.com/media/"+str(url.image))
    
    thumbnail.allow_tags = True
    list_display = ('name','description','shortcut','category','thumbnail','image')

    list_filter = ('name','description','shortcut','category')
    search_fields = ['name','description','shortcut']

admin.site.register(Product,Productadmin)
admin.site.register(ProductCategory,Categoryadmin)
