from django.db import models
from django.contrib.auth.models import User
import smtplib
import urllib
from common.utils import generate_password
# Create your models here.

class MainScheduleCourse(models.Model):
    friendly_name = models.CharField(max_length=100)
    course_id = models.IntegerField()
    course_ccn = models.IntegerField()

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

    cellphone = models.CharField(max_length=30, blank=True, default='0')
    cell_mail = models.CharField(max_length=100, blank=True, default='txt.att.net')

    def __unicode__(self):
        if self.realname:
            return self.realname
        return self.user.username

    def is_all_imported(self):
        return self.is_main_schedule_imported and self.is_friend_list_imported

    @classmethod
    def get_or_create_user(cls, username, password):
        username = username.lower()
        if User.objects.filter(username=username).count():
            print username, password
            user = User.objects.get(username=username)
            if password:
                print "Setting password"
                user.profile.set_password(password)
            user_profile = user.profile
            print user.username, user.password, user.profile.ninjacourses_password
        else:
            user = User.objects.create_user(username=username, email='', password=password)
            user_profile = UserProfile.objects.create(user=user, ninjacourses_password=password)
        return user, user_profile

    def add_course(self, friendly_name, course_id, course_ccn):
        print friendly_name, course_id
        if MainScheduleCourse.objects.filter(friendly_name=friendly_name).count():
            course = MainScheduleCourse.objects.get(friendly_name=friendly_name)
        else:
            course = MainScheduleCourse.objects.create(friendly_name=friendly_name, course_id=course_id, course_ccn=course_ccn)
        ScheduleManager.objects.create(user_profile=self, course=course)

    def update(self, realname, url_as_friend):
        if realname:
            self.realname = realname
        if url_as_friend:
            self.url_as_friend = url_as_friend
        self.save()

    def set_phone(self, cellphone):
        self.cellphone = cellphone
        self.save()

    def add_friend(self, username, realname, url_as_friend):
        user, user_profile = UserProfile.get_or_create_user(username=username, password=generate_password())
        user_profile.update(realname=realname, url_as_friend=url_as_friend)
        self.friend.add(user_profile)

    @property
    def course_list(self):
        print "searching"
        print self.is_main_schedule_imported
        assert self.is_main_schedule_imported, 'Need to import main schedule first'
        print self.course.all()
        return [[x.friendly_name, x.course_id] for x in self.course.all()]


    @property
    def friend_list(self):
        assert self.is_friend_list_imported, 'Need to import friend list first'
        return [[x.user.username, x.realname, x.url_as_friend] for x in self.friend.all()]

    def set_main_schedule_imported(self):
        self.is_main_schedule_imported = True
        self.save()

    def set_main_schedule(self, course_list):
        print "Setting main schedule"
        self.set_main_schedule_imported()
        ScheduleManager.objects.filter(user_profile=self).delete() 
        if type(course_list) is list:
            for friendly_name, course_id, course_ccn in course_list:
                self.add_course(friendly_name=friendly_name, course_id=course_id, course_ccn=course_ccn)
        self.save()
        print "finished"

    def set_friend_list(self, friend_list):
        self.is_friend_list_imported = True
        self.friend.clear()
        if type(friend_list) is list:
            for username, realname, url_as_friend in friend_list:
                self.add_friend(username=username, realname=realname, url_as_friend=url_as_friend)
        self.save()

    def set_friend_list_imported(self):
        self.is_friend_list_imported = True
        self.save()

    def set_password(self, password):
        print "Setting..."
        self.user.set_password(password)
        self.user.save()
        self.ninjacourses_password = password
        self.save()

    @property
    def shortlink(self):
        return ShortLink.objects.filter(user_profile=self)

class ScheduleManager(models.Model):
    user_profile = models.ForeignKey(UserProfile)
    course = models.ForeignKey(MainScheduleCourse)

    def __unicode__(self):
        return '%s is taking %s' % (str(self.user_profile), str(self.course))

def _analyze_num(s):
    l = len(s)
    num_list = []
    i = 0
    while i < l: 
        try:
            n = int(s[i])
            flag = True
            t = 2
            while flag:
                try:
                    n = int(s[i:i + t])
                    t += 1
                except ValueError:
                    num_list.append(n)
                    i += t
                    flag = False
        except ValueError:
            i += 1
    return num_list

def _find_info(number):
    f = urllib.urlopen("http://infobears.berkeley.edu:3400/osc/?_InField1=RESTRIC&_InField2=%d&_InField3=12B4" % number)
    temp = f.read()
    a , b  = temp.find('<blockquote>'), temp.find('</blockquote>')
    temp_string = temp[a : b]
    has_wait_list = (temp_string.find('does not use a Waiting List') == -1)
    return _analyze_num(temp_string), has_wait_list  

def _send_message(toaddrs='peterqian1993@hotmail.com', msg='nothing'):
    print toaddrs, msg

    fromaddr = 'ninjahelperberkeley@gmail.com'     
    # Credentials (if needed)  
    username = 'ninjahelperberkeley@gmail.com'  
    password = 'hack123456'  

    # The actual mail send  
    server = smtplib.SMTP('smtp.gmail.com:587')  
    server.starttls()  
    server.login(username,password)  
    print "Sending..."
    server.sendmail(fromaddr, toaddrs, msg)  
    print "Message sent"
    server.quit() 

class CourseMonitor(models.Model):

    user_profile = models.ForeignKey(UserProfile)

    ccn = models.IntegerField(max_length=100)

    current_enroll = models.IntegerField(default=-1)
    enroll_limit = models.IntegerField(default=-1)
    current_waitlist = models.IntegerField(default=-1)
    waitlist_limit = models.IntegerField(default=-1)
    has_waitlist = models.BooleanField(default=True)
    all_full = models.BooleanField(default=False)

    is_first_time = models.BooleanField(default=True)

    def fetch(self):
        # given a ccn, a cellphone number and a studentname
        print "running?"
        info_list, has_waitlist = _find_info(self.ccn)
        current_enroll, enroll_limit, current_waitlist, waitlist_limit = -1, -1, -1, -1
        all_full = False
        if has_waitlist:  # if this class has waitlist
            if len(info_list) == 4:
                current_enroll, enroll_limit, current_waitlist, waitlist_limit = info_list
            elif len(info_list) == 2:
                current_waitlist, waitlist_limit = info_list
            elif len(info_list) == 0:
                all_full = True
        else:
            if len(info_list) == 4:
                current_enroll, enroll_limit, current_waitlist, waitlist_limit = info_list
            elif len(info_list) == 2:
                current_enroll, enroll_limit = info_list
            elif len(info_list) == 0:
                all_full = True
        print current_enroll, enroll_limit, current_waitlist, waitlist_limit, all_full, has_waitlist
        is_different = self.update(current_enroll, enroll_limit, current_waitlist, waitlist_limit, all_full, has_waitlist)
        if is_different:
            cell_mail = '%s@%s' % (self.user_profile.cellphone, self.user_profile.cell_mail)
            msg = "There has been a change of status in your monitoring course with CCN %d." % self.ccn
            _send_message(toaddrs=cell_mail, msg=msg)


    def update(self, *args):
        assert len(args) == 6, "What??"
        name_list = ["current_enroll", "enroll_limit", "current_waitlist", "waitlist_limit", "all_full", "has_waitlist"]
        is_different = False
        for index in range(0, len(name_list)):
            arg = args[index]
            arg_name = name_list[index]
            if not self.is_first_time and hasattr(self, arg_name) and arg != getattr(self, arg_name):
                is_different = True
            setattr(self, arg_name, arg)
        self.is_first_time = False
        self.save()
        return is_different

class ShortLink(models.Model):
    user_profile = models.ForeignKey(UserProfile)
    shortname = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
