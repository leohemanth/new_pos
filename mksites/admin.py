from django.contrib import admin

class SubdomainAdmin(admin.ModelAdmin):
    def queryset(self, request):
        """
        Filter the objects displayed in the change_list to only
        display those for the currently signed in user.
        """
        qs = super(SubdomainAdmin, self).queryset(request)
        if request.main_site and request.user.is_superuser:
            print 'yay, all records'
            return qs
        print 'Umm subset'
        return qs.filter(subdomain=request.subdomain)
