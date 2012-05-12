from django.db import models

class MainScheduleCourse(models.Model):
    friendly_name = models.CharField(max_length=100)
    course_id = models.IntegerField()
    course_ccn = models.IntegerField()

    def __unicode__(self):
        return self.friendly_name 

    @classmethod
    def add_course(cls, user_profile, friendly_name, course_id, course_ccn):
        print user_profile.is_main_schedule_imported
        print friendly_name, course_id
        if cls.objects.filter(friendly_name=friendly_name).count():
            course = cls.objects.get(friendly_name=friendly_name)
        else:
            course = cls.objects.create(friendly_name=friendly_name, course_id=course_id, course_ccn=course_ccn)
        ScheduleManager.objects.create(user_profile=user_profile, course=course)

class ScheduleManager(models.Model):
    user_profile = models.ForeignKey('community.UserProfile')
    course = models.ForeignKey(MainScheduleCourse)

    def __unicode__(self):
        return '%s is taking %s' % (str(self.user_profile), str(self.course))

    @classmethod
    def set_main_schedule(cls, user_profile, course_list):
        print "Setting main schedule"
        user_profile.set_main_schedule_imported()
        cls.objects.filter(user_profile=user_profile).delete() 
        print user_profile.is_main_schedule_imported
        if type(course_list) is list:
            for friendly_name, course_id, course_ccn in course_list:
                MainScheduleCourse.add_course(user_profile=user_profile, friendly_name=friendly_name, course_id=course_id, course_ccn=course_ccn)
        print "finished"
