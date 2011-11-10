from django.conf.urls.defaults import patterns, include, url
from root.views import index
from django.contrib import admin
import settings
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index, name="index"),
    url(r'^account/', include('community.urls')),
)

urlpatterns += patterns('', (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT}),)
