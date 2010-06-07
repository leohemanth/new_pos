from django.contrib.sites.models import Site
from django.conf import settings

import urlparse

from subdomains.models import Subdomain

class GetSubdomainMiddleware:
    
    def process_request(self, request):
        hname = urlparse.urlparse(request.build_absolute_uri()).hostname
        bits = hname.split('.')
        if len(bits) == 3:
            request.subdomain_text = bits[0]
            try:
                subdomain = Subdomain.objects.get(subdomain_text = request.subdomain_text)
                request.mainsite = False
            except Subdomain.DoesNotExist:
                subdomain = None
                request.mainsite = False
                print 'Invalid Subdomain'
        else:
            subdomain = None
            request.mainsite = True
            print 'Ah, sizeof url is bigger than expected'
        request.subdomain = subdomain
        print 'Subdomain %s'%subdomain
        