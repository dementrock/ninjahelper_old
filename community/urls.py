from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('community.views',
	url(r'^logout/$', "logout", name='logout'),
	url(r'^login/$', "login", name='login'),
    url(r'^set_phone/$', 'set_phone', name='set_phone'),
    url(r'^set_email/$', 'set_email', name='set_email'),
    url(r'^verify_email/(?P<code>[a-zA-Z0-9]+)/$', 'verify_email', name='verify_email'),
)
