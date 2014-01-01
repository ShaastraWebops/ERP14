from users.models import *

def is_valid_id(shid):
    up = get_userprofile(shid)
    if up is None:
        return False
    return True

def is_valid_insti_roll(roll):
    #TODO::
    if len(roll)==8 and roll[:2].isalpha() and roll[2:4].isdigit() and roll[4].isalpha() and roll[5:].isdigit():
        return True
    return False

def get_userprofile(shaastra_id = None):
    if shaastra_id is None:
        return None
    try:
        up = UserProfile.objects.using('mainsite').filter(shaastra_id = shaastra_id)[0]
    except:
        return None
    return up

def is_junk(shaastra_id = None):
    #returns 0 for 
    return False
    #TODO
    
        
