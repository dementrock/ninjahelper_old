from community.models import *

def cnt_friend_imported():
    print UserProfile.objects.filter(is_friend_list_imported=True).count()
