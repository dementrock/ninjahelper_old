import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__))[:-12])


url_waitlist_status = 'http://infobears.berkeley.edu:3400/osc/?_InField1=RESTRIC&_InField2=%d&_InField3=12B4'

def main():
    print url_waitlist_status % 68988


from community.models import *

print UserProfile.objects.all()


if __name__ == '__main__':
    main()
