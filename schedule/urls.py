from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('schedule.views',
	url(r'^import_all_data/$', "import_all_data", name='import_all_data'),
	url(r'^compare_schedule/$', "compare_schedule", name='compare_schedule'),
)
