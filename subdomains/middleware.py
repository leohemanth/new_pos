from django.contrib.sites.models import Site
from django.conf import settings

import urlparse

from subdomains.models import Subdomain

class GetSubdomainMiddleware:
    
    def process_request(self, request):
        bits = urlparse.urlparse(request.build_absolute_uri()).hostname.split('.')
        request.subdomain_text = bits[0]
        probable_domain =  '.'.join(bits[1:])
        current_site = Site.objects.get_current()
        if settings.BASE_DOMAIN == probable_domain:
            #User is using a subdomain.
            if request.subdomain_text == settings.MAIN_SITE:
                request.subdomain = None
                request.main_site = True
                print 'Main Site'
                return None
            try:
                request.main_site = False
                subdomain = Subdomain.objects.get(subdomain_text = request.subdomain_text)
                request.subdomain = subdomain
                print 'Subdomain %s'%subdomain
            except Subdomain.DoesNotExist:
                request.subdomain = None
                print 'Invalid Subdomain'
            return None
        else:
            #User is using a Custom Domain
            request.main_site = False
            try:
                domain = urlparse.urlsplit(request.build_absolute_uri()).hostname
                request.subdomain_text = domain
                subdomain = Subdomain.objects.get(domain = domain)
                request.subdomain = subdomain
            except Subdomain.DoesNotExist:
                request.subdomain = None
            return None
            
