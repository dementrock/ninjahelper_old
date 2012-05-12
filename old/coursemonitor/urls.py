from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('coursemonitor.views',
	url(r'^$', "manage_monitor_course", name='manage_monitor_course'),
	url(r'^add/$', "add_monitor_course", name='add_monitor_course'),
	url(r'^delete/(?P<ccn>\w+)$', "delete_monitor_course", name='delete_monitor_course'),
)
