#!/usr/bin/python
import os
import sys
import time

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__))[:-12])

from coursemonitor.models import CourseMonitor
from coursepagemonitor.models import CoursePageMonitor
from common.utils import errorlog

SLEEP_INTERVAL = 600

LOG_FILE = 'log_monitor'

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

        course_monitor_list = CourseMonitor.objects.all()
        for course in course_monitor_list:
            try:
                course.fetch()
            except Exception as e:
                errorlog(e, course.ccn)

        course_page_monitor_list = CoursePageMonitor.objects.all()
        for course_page in course_page_monitor_list:
            try:
                course_page.fetch()
            except Exception as e:
                errorlog(e, course_page.url)

    except Exception as e:
        errorlog(e)
    log("Sleep for %d second(s)..." % SLEEP_INTERVAL)
    time.sleep(SLEEP_INTERVAL)

