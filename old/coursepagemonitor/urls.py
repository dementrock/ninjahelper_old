from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('coursepagemonitor.views',
	url(r'^$', "manage_monitor_course_page", name='manage_monitor_course_page'),
	url(r'^add/$', "add_monitor_course_page", name='add_monitor_course_page'),
	url(r'^delete/(?P<shortname>\w+)$', "delete_monitor_course_page", name='delete_monitor_course_page'),
)
