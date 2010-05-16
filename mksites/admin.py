from django.contrib import admin
from django.http import Http404
from debug import ipython,idebug

class SubdomainAdmin(admin.ModelAdmin):
    
    exclude = ('subdomain',)
    
    def queryset(self, request):
        """
        Filter the objects displayed in the change_list to only
        display those for the currently signed in user.
        """
        qs = super(SubdomainAdmin, self).queryset(request)
        if request.main_site and request.user.is_superuser:
            return qs
        elif request.user.is_superuser or request.subdomain.user == request.user:
            return qs.filter(subdomain=request.subdomain)
        else:
            raise Http404
        
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        the_model = db_field.related.parent_model
        
        if hasattr(the_model,'subdomain'):
            kwargs['queryset'] = the_model.objects.filter(subdomain=request.subdomain)
        return super(SubdomainAdmin,self).formfield_for_foreignkey(db_field, request, **kwargs)
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.subdomain = request.subdomain
        obj.save()
