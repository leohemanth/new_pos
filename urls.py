from django.conf.urls.defaults import *
from django.conf import settings
from os.path import join

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

prefix = '/'

urlpatterns = patterns('',
    # Example:
    # (r'^new_pos/', include('new_pos.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^grappelli/', include('grappelli.urls')),
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    (r'^$', 'simplecms.cms.views.get_path', {'template':'lazydays/page.html', 'prefix':prefix}),
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
                        #(r'^cms/', 'django.views.static.serve',
                         #{'document_root': 'cms',
                          #'show_indexes':True}),
                        )

urlpatterns += patterns('',

    (r'^(?P<path>.*)/$', 'simplecms.cms.views.get_path', {'template':'lazydays/page.html', 'prefix':prefix}),
)