import os
import sys
import time

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__))[:-12])

from coursepagemonitor.models import CoursePageMonitor

SLEEP_INTERVAL = 300 


LOG_FILE = 'log_course_page_monitor'

def log(s):
    if LOG_FILE:
        log_file = open(LOG_FILE, 'a')
        log_file.write(s + '\n')
        log_file.close()
    else:
        print s


while True:
    try:
        log("Fetch all again...")
        course_page_monitor_list = CoursePageMonitor.objects.all()

        for course_page in course_page_monitor_list:
            course_page.fetch()
        log("Sleep for %d second(s)..." % SLEEP_INTERVAL)
        time.sleep(SLEEP_INTERVAL)
    except Exception as e:
        errorlog(e)
