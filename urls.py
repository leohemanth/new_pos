from django.conf.urls.defaults import *
from django.conf import settings
from os.path import join

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.views.generic.simple import redirect_to
prefix = '/'

urlpatterns = patterns('',
    # Example:
    # (r'^new_pos/', include('new_pos.foo.urls')),

  #  (r'^contact/thankyou/', 'contact.views.thankyou'),
   # (r'^contact/', 'contact.views.contactview'),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^grappelli/', include('grappelli.urls')),
    # Uncomment the next line to enable the admin:
    (r'^erp/', include(admin.site.urls)),

    (r'^$', 'simplecms.cms.views.get_path', {'template':'lazydays/page.html', 'prefix':prefix}),
    url(r'^new/$', 'mksites.views.create_subdomain',name='new_sub'),
    (r'^plan/$', 'simplecms.cms.views.plan', {'template':'lazydays/plan.html', 'prefix':prefix}),
)

#For static and media files
urlpatterns += patterns('',
                        (r'^admin_media/(.*)', 'django.views.static.serve',
                         {'document_root': 'admin_media',
                          'show_indexes':True}),
                        (r'^media/(.*)', 'django.views.static.serve',
                         {'document_root': 'media',
                          'show_indexes':True}),
                        )

urlpatterns += patterns('',
    (r'^admin/',redirect_to,{'url':'/erp/',}),
    (r'^(?P<path>.*)/$', 'simplecms.cms.views.get_path', {'template':'lazydays/page.html', 'prefix':prefix}),
)
