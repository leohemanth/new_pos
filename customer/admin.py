from django.contrib import admin
from customer.models import *
from mksites.admin import SubdomainAdmin

class Customeradmin(SubdomainAdmin):
	def thumbnail(self,url):
            return """<img src="%s" />""" %("http://asimpleerp.com/media/"+str(url.image))
    
	thumbnail.allow_tags = True
	list_display = ('name','phone_number','details','thumbnail','image')

class Categoryadmin(SubdomainAdmin):
     list_display = ('name','description')
     search_fields = ['name','description']

      
      

admin.site.register(Customer,Customeradmin)
admin.site.register(CustomerCategory,Categoryadmin)
