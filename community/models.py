from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class MainScheduleCourse(models.Model):
    friendly_name = models.CharField(max_length=100)
    course_id = models.IntegerField()

    def __unicode__(self):
        return self.friendly_name

class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True, related_name='profile')
    ninjacourses_password = models.CharField(max_length=100)
    course = models.ManyToManyField(MainScheduleCourse, through='ScheduleManager', related_name='user_profile')
    is_main_schedule_imported = models.BooleanField(default=False)
    is_friend_list_imported = models.BooleanField(default=False)
    friend = models.ManyToManyField('self')

    url_as_friend = models.CharField(max_length=100, blank=True)
    realname = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        if self.realname:
            return self.realname
        return self.user.username

    @classmethod
    def get_or_create_user(cls, username, password):
        if User.objects.filter(username=username).count():
            user = User.objects.get(username=username)
            if password:
                user.set_password(password)
            user_profile = user.profile
        else:
            user = User.objects.create_user(username=username, email='', password=password)
            user_profile = UserProfile.objects.create(user=user, ninjacourses_password=password)
        return user, user_profile

    def add_course(self, friendly_name, course_id):
        if MainScheduleCourse.objects.filter(friendly_name=friendly_name).count():
            course = MainScheduleCourse.objects.get(friendly_name=friendly_name)
        else:
            course = MainScheduleCourse.objects.create(friendly_name=friendly_name, course_id=course_id)
        ScheduleManager.objects.create(user_profile=self, course=course)

    def update(self, realname, url_as_friend):
        if realname:
            self.realname = realname
        if url_as_friend:
            self.url_as_friend = url_as_friend
        self.save()

    def add_friend(self, username, realname, url_as_friend):
        user, user_profile = UserProfile.get_or_create_user(username=username, password='')
        user_profile.update(realname=realname, url_as_friend=url_as_friend)
        self.friend.add(user_profile)

    @property
    def course_list(self):
        assert self.is_main_schedule_imported, 'Need to import main schedule first'
        return [[x.friendly_name, x.course_id] for x in self.course.all()]


    @property
    def friend_list(self):
        assert self.is_friend_list_imported, 'Need to import friend list first'
        return [[x.user.username, x.realname, x.url_as_friend] for x in self.friend.all()]

    def set_main_schedule_imported(self):
        self.is_main_schedule_imported = True
        self.save()

    def set_main_schedule(self, course_list):
        self.is_main_schedule_imported = True
        ScheduleManager.objects.filter(user_profile=self).delete() 
        if type(course_list) is list:
            for friendly_name, course_id in course_list:
                self.add_course(friendly_name=friendly_name, course_id=course_id)
        self.save()

    def set_friend_list(self, friend_list):
        self.is_friend_list_imported = True
        self.friend.all().delete()
        if type(friend_list) is list:
            for username, realname, url_as_friend in friend_list:
                self.add_friend(username=username, realname=realname, url_as_friend=url_as_friend)
        self.save()

    def set_friend_list_imported(self):
        self.is_friend_list_imported = True
        self.save()

class ScheduleManager(models.Model):
    user_profile = models.ForeignKey(UserProfile)
    course = models.ForeignKey(MainScheduleCourse)

    def __unicode__(self):
        return '%s is taking %s' % (str(self.user_profile), str(self.course))
