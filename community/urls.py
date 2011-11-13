from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('community.views',
	url(r'^logout/$', "logout", name='logout'),
	url(r'^login/$', "login", name='login'),
	url(r'^import_courses/$', "import_course_data", name='import_course_data'),
	url(r'^import_friends/$', "import_friend_data", name='import_friend_data'),
	url(r'^import_all_data/$', "import_all_data", name='import_all_data'),
	url(r'^compare_schedule/$', "compare_schedule", name='compare_schedule'),
	url(r'^monitor_course/$', "monitor_course", name='monitor_course'),
)
