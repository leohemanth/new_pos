from django.contrib import admin
from django.http import Http404

class SubdomainAdmin(admin.ModelAdmin):
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
            raise Http404()
