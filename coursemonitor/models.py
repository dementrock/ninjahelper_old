from django.db import models
import urllib
from common.utils import send_message, send_email, html2text
from community.models import UserProfile

# Create your models here.

class CourseMonitor(models.Model):

    user_profile = models.ForeignKey(UserProfile, related_name='monitored_course')

    ccn = models.IntegerField(max_length=100)

    current_enroll = models.IntegerField(default=-1)
    enroll_limit = models.IntegerField(default=-1)
    current_waitlist = models.IntegerField(default=-1)
    waitlist_limit = models.IntegerField(default=-1)
    has_waitlist = models.BooleanField(default=True)
    all_full = models.BooleanField(default=False)


    is_first_time = models.BooleanField(default=True)

    def __unicode__(self):
        return "%s monitoring course ccn %d" % (str(self.user_profile), self.ccn) 

    def fetch(self):
        # given a ccn, a cellphone number and a studentname
        #print "running?"
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
        #print current_enroll, enroll_limit, current_waitlist, waitlist_limit, all_full, has_waitlist
        is_different, different_list = self.update(current_enroll, enroll_limit, current_waitlist, waitlist_limit, all_full, has_waitlist)
        if is_different:
            msg = "Change in course %d:\n%s" % (self.ccn, '; '.join(different_list) + '.')
            if self.user_profile.is_phone_set:
                cell_mail = '%s@%s' % (self.user_profile.cellphone, self.user_profile.cell_mail)
                send_message(toaddrs=cell_mail, msg=msg)
            if self.user_profile.is_email_set:
                send_email(toaddrs=self.user_profile.email, title="Status change of course with CCN %s" % self.ccn, msg=msg)


    def update(self, *args):

        name_list = ["current_enroll", "enroll_limit", "current_waitlist", "waitlist_limit", "all_full", "has_waitlist"]
        friendly_name = {
            "current_enroll": "current enrollment",
            "enroll_limit": "enrollment limit",
            "current_waitlist": "current waitlist",
            "waitlist_limit": "waitlist limit",
        }
        is_different = False
        different_list = []

        def num_or_no_info(x):
            if x == -1:
                return "(no info)"
            else:
                return str(x)

        for index in range(0, len(name_list)):
            arg = args[index]
            arg_name = name_list[index]
            if not self.is_first_time and hasattr(self, arg_name) and arg != getattr(self, arg_name):
                is_different = True
                if arg_name in friendly_name:
                    different_list.append("%s changed from %s to %s" % (
                        friendly_name[arg_name],
                        num_or_no_info(getattr(self, arg_name)),
                        num_or_no_info(arg),
                    ))
                else:
                    if arg_name == "all_full":
                        if arg: # Changed from not full to full
                            diff = "course is now full"
                        else:   # Changed from full to not full
                            diff = "course now has available position or waitlist"
                    elif arg_name == "has_waitlist": # Which should not frequently happen
                        continue # This information is possibly duplicated. Won't need
                        """
                        if arg: # Changed from no waitlist to having waitlist
                            diff = "course now has a waitlist"
                        else:   # Changed from having waitlist to no waitlist
                            diff = "course now has no waitlist" """
                    else:
                        continue
                    different_list.append(diff)
            setattr(self, arg_name, arg)
        self.is_first_time = False
        self.save()
        return is_different, different_list

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

