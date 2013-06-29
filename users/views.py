# Create your views here.

from users.forms import  ChooseIdentityForm, EditProfileForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, REDIRECT_FIELD_NAME
from django.template.context import Context, RequestContext
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from misc.dajaxice.core import dajaxice_functions
from users.models import ERPUser
from misc.utilities import get_position

def redirectToLogin(request):
    return HttpResponseRedirect('/login/')

def login(request):

    #Redirect logged in users
    if request.user.is_authenticated():
	return HttpResponseRedirect('/dash/')

    if request.method == 'POST':

	#Authenticate the user
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)

        #if everything is in order
        if user is not None and user.is_active and not user.is_superuser:
            auth_login(request, user)

	    #Set things about the user. I am assuming that status, subdept etc are set a priori for users without multiple identities.
	    
	    #check for multiple identities
	    if user.erpuser.multiple_ids == True:  
		return HttpResponseRedirect('/choose_identity/')
	    
	    return HttpResponseRedirect('/dash/')

	#If the username and password aren't in order
        invalid_login = True
        return render_to_response('users/login.html', locals(), context_instance=RequestContext(request))
    
    #rendering for the initial GET request
    else:
        return render_to_response('users/login.html', locals(), context_instance=RequestContext(request))
 
def logout(request):
    """
        View for logging out users from the session.
    """
    if request.user.is_authenticated():
        auth_logout(request)
    return HttpResponseRedirect('/login/')


@login_required
def choose_identity ( request ):
    
    #This is a Boolean which informs the template that the user has made no error
    noerror = True

    if request.method == 'POST':
	identity_form = ChooseIdentityForm (request.user.erpuser, request.POST)

	if identity_form.is_valid():
	    cd = identity_form.cleaned_data

	    #if they don't choose anything
	    if cd['coordships'] == None and cd['supercoordships'] == None:
		noerror = False
		return render_to_response ( 'dash/choose_identity.html', locals(), context_instance = RequestContext(request) )

	    #if they make choices in both.
	    if not cd['coordships'] == None and not cd['supercoordships'] == None:
		noerror = False
		return render_to_response ( 'dash/choose_identity.html', locals(), context_instance = RequestContext(request) )
	    
	    #if everything is in order, we can now set the identity and let him/her be on his way. :)
	    userprofile = request.user.erpuser

	    #if he's chosen a coordship
	    if not cd['coordships'] == None:
		userprofile.status = 0
		userprofile.subdept = cd['coordships'] #which coordship he's chosen. Don't know if this is necessary, but it can't hurt
		
	    #if he's chosen a supercoordship
	    else:
		userprofile.status = 1 #supercoord
	    userprofile.save()
	    return HttpResponseRedirect ('/dash/')
    identity_form = ChooseIdentityForm ( curruser = request.user.erpuser )
    return render_to_response ( 'dash/choose_identity.html', locals(), context_instance = RequestContext(request) )

def view_profile ( request, userid = None ) :
    profile_dict = dict ()
    profile_dict['userexists'] = True
    if userid == None:
        try:
            profile = request.user.get_profile()
        except:
            profile_dict['userexists'] = False
            render_to_response('users/view_profile.html', locals(), context_instance=RequestContext(request))
    else:
        try:
            profile = ERPUser.objects.get ( pk = userid )
        except:
            profile_dict['userexists'] = False	
            return render_to_response('users/view_profile.html', locals(), context_instance=RequestContext(request))
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

    return render_to_response('users/view_profile.html',profile_dict,context_instance = RequestContext(request))

def edit_profile ( request ) :
    errors = False
    userprofile = request.user.get_profile()
    fullname = userprofile.user.get_full_name()
    nickname = userprofile.nickname

    if request.method == 'POST':
        edit_form = EditProfileForm(request.POST, instance=userprofile )

        if edit_form.is_valid():
            userprofile.save()
            messages.success(request, "Profile was edited and saved")
            return redirect ( 'users.views.view_profile' )
        else:
            errors = True
            return render_to_response ( 'users/edit_profile.html', locals(), context_instance = RequestContext(request) )
    edit_form= EditProfileForm ( instance = userprofile )
    return render_to_response ( 'users/edit_profile.html', locals(), context_instance = RequestContext(request) )
 
