#This will store all our utility functions

from django.core.exceptions import ValidationError
from django.utils import simplejson

# _____________--- CORE CHECK FUNCTION ---______________#
def core_check (user):
    return user.get_profile().status == 2

def core_or_supercoord_check (user):
    return user.get_profile().status == 2 or user.get_profile().status == 1

#This returns the position of the ERPUser as a string.
def get_position (userprofile):
    if userprofile.status == 2:
        return 'Core'
    if userprofile.status == 1:
        return 'Supercoord'
    if userprofile.status == 0:
        return 'Coord'


# _____________--- DAJAX Alert Message ---______________#
def show_alert(dajax_, type_, msg_):
    """
        Give an alert in the bootstrap styled alert which is in base.html
    """
    dajax_.remove_css_class("#id_alert", "alert-success")
    dajax_.remove_css_class("#id_alert", "alert-warning")
    dajax_.remove_css_class("#id_alert", "alert-error")
    dajax_.remove_css_class("#id_alert", "alert-info")
    dajax_.remove_css_class("#id_alert", "hide")
    
    dajax_.add_css_class("#id_alert", "alert-" + type_.lower())
    dajax_.assign("#id_alert", "innerHTML", "<button type='button' class='close' onclick='javascript:js_alert_hide();'>&times;</button><strong>" + type_.upper() + "!</strong> " + msg_);
