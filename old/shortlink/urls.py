from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('shortlink.views',
    url(r'^$', 'manage_shortlink', name='manage_shortlink'),
    url(r'^add/$', 'add_shortlink', name='add_shortlink'),
    url(r'^edit/(?P<shortname>\w+)/$', 'edit_shortlink', name='edit_shortlink'),
    url(r'^delete/(?P<shortname>\w+)/$', 'delete_shortlink', name='delete_shortlink'),
)
