from users.models import *

def id_is_valid(sh_id):
    if len(sh_id) == 10 and sh_id[:5] == 'SHA14' and sh_id[5:].isalpha():
        return True
    return False

def id_in_db(shid):
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
    
        
