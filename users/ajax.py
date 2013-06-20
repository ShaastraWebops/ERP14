# For simple dajax(ice) functionalities
from django.utils import simplejson
from misc.dajaxice.decorators import dajaxice_register
from misc.dajax.core import Dajax
from misc.dajaxice.utils import deserialize_form
# For rendering templates
from django.template import RequestContext
from django.template.loader import render_to_string
# From views
from users.views import edit_profile as view_edit_profile
# From forms
from users.forms import *
# From models
from users.models import *
import users.models
# From Misc to show bootstrap alert
from misc.utilities import show_alert, get_position


def model_validate(request, model, fields):
    return generate_model_validation(users.model, request, model, fields)

@dajaxice_register
def hello_world(request):
    """
        Used for testing Dajax + Dajaxice
    """
    dajax = Dajax()
    dajax.assign('id_content','innerHTML', "Hello world !")
    return dajax.json()
    
@dajaxice_register
def hello(request):
    """
        Used for testing Dajaxice
    """
    return simplejson.dumps({'message': 'hello'})

@dajaxice_register
def display_profile(request, userid=None):
    """
        Used to show profile using Dajax(ice)
        Renders in : modal
        Refreshes : none
    """
    dajax = Dajax()
    profile_dict = dict ()
    profile_dict['userexists'] = True
    html_content = ""
    
    try:
        if userid == None:
            profile = request.user.get_profile()
        else:
            profile = ERPUser.objects.get ( pk = userid )
        
        # Profile seems to exist, get data
        userprofile = request.user.get_profile()
        
        profile_dict['nickname'] = profile.nickname
        profile_dict['position'] = get_position ( profile )
        profile_dict['fullname'] = profile.user.get_full_name()
        profile_dict['chennaino'] = profile.chennai_number
        profile_dict['summerno'] = profile.summer_number
        profile_dict['summerstay'] = profile.summer_stay
        profile_dict['hostel'] = profile.hostel
        profile_dict['roomno'] = str(profile.room_no)
        
        #This is a flag which indicates that the profile being viewed is the user's own. Hence there will be 
        #a button to edit.
        profile_dict['ownprofile'] = ( profile == userprofile )
        
        # Render the template with given info
        html_content = render_to_string('users/view_profile.html', profile_dict, RequestContext(request))
    
    except:
        # Profile given was invalid.
        profile_dict['userexists'] = False
        html_content = render_to_string('users/view_profile.html', locals(), RequestContext(request))
    
    dajax.remove_css_class('#id_modal', 'hide') # Show modal
    dajax.assign('#id_modal','innerHTML', html_content) # Populate modal
    return dajax.json()

@dajaxice_register(method="GET", name="users.edit_profile_get")
@dajaxice_register(method="POST", name="users.edit_profile_post")
def edit_profile(request, edit_form=None):
    """
        Used to give Dajax(ice) the edit profile page
        Renders in : modal
        Refreshes : right_content
    """
    dajax = Dajax()
    errors = False
    userprofile = request.user.get_profile()
    fullname = userprofile.user.get_full_name()
    nickname = userprofile.nickname
    if request.method == 'POST' and edit_form != None:
        edit_form = EditProfileForm(deserialize_form(edit_form), instance=userprofile)
        
        if edit_form.is_valid():
            print "form is valid"
            edit_form.save()
            dajax.assign("#edit_profile_nickname", "innerHTML", edit_form.cleaned_data['nickname'])
            dajax.remove_css_class('#profile_edit_form input', 'error')
            dajax.script('modal_hide()') # Hide modal
            show_alert(dajax, 'success', 'Profile was edited and saved')
        else:
            print "form is not valid"
            errors = True
            dajax.remove_css_class('#profile_edit_form input', 'error')
            for error in edit_form.errors:
                dajax.add_css_class('#id_%s' % error, 'error')
            #show_alert(dajax, 'error', "There were errors in the form") # as it is in modal, not req
    else:
        edit_form = EditProfileForm ( instance = userprofile )
        html_content = render_to_string("users/edit_profile.html", locals(), RequestContext(request))
        dajax.remove_css_class('#id_modal', 'hide') # Show modal
        dajax.assign("#id_modal", "innerHTML", html_content) # Populate modal
    
    return dajax.json()

@dajaxice_register
def contact_us(request):
    """
        Used to populate the Modal with Contact Us page
    """
    dajax = Dajax()
    
    html_content = render_to_string("common/contact_us.html", locals(), RequestContext(request))
    dajax.remove_css_class('#id_modal', 'hide') # Show modal
    dajax.assign("#id_modal", "innerHTML", html_content) # Populate modal
    #print "added"
    
    return dajax.json()
   
    
    
