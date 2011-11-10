from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('community.views',
	url(r'^import_courses/$', "import_course_data", name='import_course_data'),
	url(r'^import_friends/$', "import_friend_data", name='import_friend_data'),
	url(r'^compare_schedule/$', "compare_schedule", name='compare_schedule'),
)
