from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings

class ensure_has_subdomain(object):
    def __init__(self, func):
        self.func = func
        
    def __call__(self, request, *args, **kwargs):
        if request.subdomain:
            return self.func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse(settings.REGISTER_SUBDOMAIN_REDIRECT))
        
class ensure_is_main_subdomain(object):
    def __init__(self, func):
        self.func = func
        
    def __call__(self, request, *args, **kwargs):
        if request.main_site:
            return self.func(request, *args, **kwargs)
        else:
            url = 'http://%s.%s%s' % (settings.MAIN_SITE[0], settings.BASE_DOMAIN, '')
            return HttpResponseRedirect(reverse(settings.REGISTER_SUBDOMAIN_REDIRECT))
            