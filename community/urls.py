from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('community.views',
	url(r'^logout/$', "logout", name='logout'),
	url(r'^login/$', "login", name='login'),
	url(r'^import_all_data/$', "import_all_data", name='import_all_data'),
	url(r'^compare_schedule/$', "compare_schedule", name='compare_schedule'),
	url(r'^monitor_course/$', "manage_monitor_course", name='manage_monitor_course'),
	url(r'^monitor_course/add/$', "add_monitor_course", name='add_monitor_course'),
	url(r'^monitor_course/delete/(?P<ccn>\w+)$', "delete_monitor_course", name='delete_monitor_course'),
    url(r'^shortlink/$', 'manage_shortlink', name='manage_shortlink'),
    url(r'^shortlink/add/$', 'add_shortlink', name='add_shortlink'),
    url(r'^shortlink/edit/(?P<shortname>\w+)/$', 'edit_shortlink', name='edit_shortlink'),
    url(r'^shortlink/delete/(?P<shortname>\w+)/$', 'delete_shortlink', name='delete_shortlink'),
    url(r'^set_phone/$', 'set_phone', name='set_phone'),
)
