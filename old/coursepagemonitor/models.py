from django.db import models
from settings import MAXIMUM_SIZE
from common.utils import getsize, gethash, send_message, send_email
from community.models import UserProfile

# Create your models here.

class CoursePageMonitor(models.Model):

    user_profile = models.ForeignKey(UserProfile, related_name='monitored_course_page')

    url = models.URLField(max_length=100)
    shortname = models.CharField(max_length=30)
    hash_data = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return '%s monitoring %s' % (str(self.user_profile), self.shortname)

    def fetch(self):
        url = self.url
        if getsize(url) > MAXIMUM_SIZE:
            return
        new_hash = gethash(url)
        if not self.hash_data:
            self.hash_data = new_hash
            self.save()
        else:
            if new_hash != self.hash_data:
                msg = "There has been a change of status in your monitoring course page %s (%s)." % (self.shortname, self.url)
                print self.user_profile
                if self.user_profile.is_phone_set:
                    cell_mail = '%s@%s' % (self.user_profile.cellphone, self.user_profile.cell_mail)
                    send_message(toaddrs=cell_mail, msg=msg[:100]+'...')
                if self.user_profile.is_email_set:
                    send_email(toaddrs=self.user_profile.email, title="Status change of course page %s" % self.shortname, msg=msg)
                self.hash_data = new_hash
                self.save()
