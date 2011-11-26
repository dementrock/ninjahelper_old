from django.db import models
from django.contrib.auth.models import User
from common.utils import generate_password, send_message, send_email, getsize, gethash
from settings import MAXIMUM_SIZE
import urllib
from django.core.urlresolvers import reverse

def _generate_free_btn(title, text, href, extra_style=''):
    raw_str = '<a class="helperbutton green %s" href="%s" title="%s">%s</a>'
    return raw_str % (extra_style, href, title, text)

def _generate_first_level_btn(title, text, href, is_done, extra_style=''):
    raw_str = '<a class="helperbutton %s %s" %s title="%s">%s%s</a>'
    if not is_done:
        return raw_str % ('green', extra_style, 'href="%s"' % href, title, text, '')
    else:
        return raw_str % ('gold', extra_style, '', title, text, ' (Done)')

def _generate_second_level_btn(title, text, href, is_prereq_done, extra_style=''):
    raw_str = '<a class="helperbutton secondlevel %s %s" %s title="%s">%s</a>'
    if not is_prereq_done:
        return raw_str % ('grey', extra_style, '', title, text)
    else:
        return raw_str % ('green', extra_style, 'href="%s"' % href, title, text)

class UserProfile(models.Model):

    user = models.OneToOneField(User, unique=True, related_name='profile')
    ninjacourses_password = models.CharField(max_length=100)
    course = models.ManyToManyField('schedule.MainScheduleCourse', through='schedule.ScheduleManager', related_name='user_profile')

    is_main_schedule_imported = models.BooleanField(default=False)
    is_friend_list_imported = models.BooleanField(default=False)
    is_friend_schedule_imported = models.BooleanField(default=False)
    is_phone_set = models.BooleanField(default=False)
    is_email_set = models.BooleanField(default=False)

    friend = models.ManyToManyField('self')

    url_as_friend = models.CharField(max_length=100, blank=True)
    realname = models.CharField(max_length=100, blank=True)

    cellphone = models.CharField(max_length=30, blank=True, default='0')
    cell_mail = models.CharField(max_length=100, blank=True, default='txt.att.net')

    email = models.EmailField(blank=True)
    email_to_verify = models.EmailField(blank=True)
    email_short_code = models.CharField(max_length=4, blank=True)
    email_verification_code = models.CharField(max_length=40, blank=True)

    def __unicode__(self):
        if self.realname:
            return self.realname
        return self.user.username

    @property
    def is_all_imported(self):
        return self.is_main_schedule_imported and self.is_friend_list_imported and self.is_friend_schedule_imported

    @property
    def is_contact_set(self):
        return self.is_phone_set or self.is_email_set

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

    def update(self, realname, url_as_friend):
        if realname:
            self.realname = realname
        if url_as_friend:
            self.url_as_friend = url_as_friend
        self.save()

    def set_phone(self, cellphone, cellmail):
        self.cellphone = cellphone
        self.cellmail = cellmail
        self.is_phone_set = True
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

    def set_friend_schedule_imported(self):
        self.is_friend_schedule_imported = True
        self.save()

    def set_password(self, password):
        print "Setting..."
        self.user.set_password(password)
        self.user.save()
        self.ninjacourses_password = password
        self.save()

    @property
    def str_btn_import_data(self):
        return _generate_first_level_btn (
            title="Import your data from ninjacourses.com.",
            text="Import data",
            href="javascript:import_data()",
            is_done=self.is_all_imported,
        )

    @property
    def str_btn_set_phone(self):
        return _generate_first_level_btn (
            title="Set up your cell phone number (we only support ATT & Tmobile right now).",
            text="Set phone",
            href=reverse('set_phone'),
            is_done=self.is_phone_set,
            extra_style="both",
        )

    @property
    def str_btn_set_email(self):
        return _generate_first_level_btn (
            title="Set up your email.",
            text="Set email",
            href=reverse('set_email'),
            is_done=self.is_email_set,
            extra_style="both",
        )

    @property
    def str_btn_update_data(self):
        return _generate_second_level_btn (
            title="Update your data from ninjacourses.com. Note: your friends' schedule will NOT be updated.",
            text="Update data",
            href="javascript:update_data()",
            is_prereq_done=self.is_all_imported,
        )

    @property
    def str_btn_compare_schedule(self):
        return _generate_second_level_btn (
            title="Compare your schedule with your friends.",
            text="Compare schedule",
            href=reverse('compare_schedule'),
            is_prereq_done=self.is_all_imported,
        )

    @property
    def str_btn_monitor_course(self):
        return _generate_second_level_btn (
            title="Monitor the status of a course and send you a message whenever something changes.",
            text="Monitor course",
            href=reverse('manage_monitor_course'),
            is_prereq_done=self.is_contact_set,
        )

    @property
    def str_btn_monitor_course_page(self):
        return _generate_second_level_btn (
            title="Monitor the content of a course page and send you a message whenever something changes.",
            text="Monitor course page",
            href=reverse('manage_monitor_course_page'),
            is_prereq_done=self.is_contact_set,
        )

    @property
    def str_btn_manage_shortlink(self):
        return _generate_free_btn (
            title="Manage your shortlinks.",
            text="Manage shortlink",
            href=reverse('manage_shortlink'),
        )

    def set_email(self):
        self.email = self.email_to_verify
        self.email_to_verify = ""
        self.email_short_code = ""
        self.email_verification_code = ""
        self.is_email_set = True
        self.save()
