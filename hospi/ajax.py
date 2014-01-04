from django.utils import simplejson 
from misc.dajaxice.decorators import dajaxice_register
from misc.dajax.core import Dajax
from misc.dajaxice.utils import deserialize_form

from django.template import RequestContext
from django.template.loader import render_to_string
from django.template import loader
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from dashboard.models import TeamEvent
from users.models import UserProfile,College
from hospi.models import *
from hospi.forms import AddRoomForm,IndividualForm,ShaastraIDForm,RemoveRoom,RegistrationForm,TeamCheckinForm
from events.forms import ChooseEventForm
from events.models import GenericEvent, ParticipantEvent
from barcode.scripts import is_junk,create_junk_profile,get_userprofile,id_in_db
from barcode.forms import CollegeForm
import json 
from misc.utilities import show_alert
from erp.settings import DATABASES
mainsite_db = DATABASES.keys()[1]
from datetime import datetime

@dajaxice_register
def roommap(request,hostel_name):  
    
    dajax = Dajax()
    hostel_selected = AvailableRooms.objects.filter(hostel=hostel_name).order_by('room_no')
    html_content =  render_to_string('hospi/RoomMap.html', locals(),RequestContext(request))
    dajax.remove_css_class=('#id_modal','hide')
    dajax.assign('#id_modal',"innerHTML",html_content)
    return dajax.json()

@dajaxice_register
def addroom(request,addroom_form=None):

    dajax = Dajax()
    if request.method == 'POST' and addroom_form != None:
        form = AddRoomForm(deserialize_form(addroom_form))
        if form.is_valid():
            cleaned_form = form.cleaned_data
            room_num = cleaned_form['room_no']
            hostel = cleaned_form['hostel']
            already_avail = AvailableRooms.objects.filter(room_no=room_num,hostel=hostel)
            if already_avail:
                show_alert(dajax,"error","Room already exists")
                return dajax.json()
            else:
                try:
                    form.save()
                    show_alert(dajax,"success","Room Added Successfully")
                    html_content = render_to_string('hospi/AddRoom.html',locals(),RequestContext(request))
                    dajax.assign('#tab2',"innerHTML",html_content)
                    return dajax.json()
                except EditError as error:
                    show_alert(dajax,"error",error.value)
                    return dajax.json()
        else:
            show_alert(dajax,"error","Form is invalid")
            return dajax.json()
    else:
        form = AddRoomForm()
        html_content = render_to_string('hospi/AddRoom.html',locals(),RequestContext(request))
        dajax.assign('#tab2',"innerHTML",html_content)
        return dajax.json()
            
@dajaxice_register
def checkin(request,indi_form=None):
    dajax = Dajax()
    if request.method == 'POST' and indi_form != None:
        form = ShaastraIDForm(deserialize_form(indi_form))
        if form.is_valid():
            cleaned_form=form.cleaned_data
            shaastraid = 'SHA14'+cleaned_form['shaastraID']
            try:
                participant = UserProfile.objects.using(mainsite_db).get(shaastra_id = shaastraid) #So participant in the database can be pre-reg or junk
            except:
                new_form = RegistrationForm(initial={'shaastra_id':shaastraid})
                college_form = CollegeForm()
                html_content = render_to_string('hospi/Register.html',locals(),RequestContext(request))
                dajax.assign('#tab3',"innerHTML",html_content)
                return dajax.json()
            try:
                checkedin = IndividualCheckIn.objects.get(shaastra_ID=shaastraid)
                room = checkedin.room
                checkedindate = checkedin.check_in_date
                checkedoutdate = checkedin.check_out_date
                if checkoutdate:
                    show_alert(dajax,"info","Participant was checked-in into" + str(room) + ".He has already checked-out on" + str(checkoutdate))
                    return dajax.json()
                else:
                    show_alert(dajax,"info","Participant is already checked-in into" + str(room))
                    return dajax.json()
            except:
                if is_junk(shaastraid):
                    participant.user.is_staff = False
                    new_form = RegistrationForm(initial={'shaastra_id':shaastraid})
                    college_form = CollegeForm()
                    html_content = render_to_string('hospi/Register.html',locals(),RequestContext(request))
                    dajax.assign('#tab3',"innerHTML",html_content)
                    return dajax.json()
                else:
                    new_form = IndividualForm(initial={'shaastra_ID':shaastraid})
                    html_content = render_to_string('hospi/Checkin_form.html',locals(),RequestContext(request))
                    dajax.assign('#tab3',"innerHTML",html_content)
                    return dajax.json()
        else:
            show_alert(dajax,"error","Form is invalid")
            return dajax.json()
    else:
        form = ShaastraIDForm()
        html_content = render_to_string('hospi/Checkin_indi.html',locals(),RequestContext(request))
        dajax.assign('#tab3',"innerHTML",html_content)
        return dajax.json()

@dajaxice_register
def checkout(request,shaastra_form=None):
    dajax = Dajax()
    if request.method=='POST' and shaastra_form != None:
        form = ShaastraIDForm(deserialize_form(shaastra_form))
        if form.is_valid():
            cleaned_form = form.cleaned_data
            print cleaned_form
            shaastraid = 'SHA14'+cleaned_form['shaastraID']
            print shaastraid
            try:
                participant = UserProfile.objects.using(mainsite_db).get(shaastra_id = shaastraid)
            except:
                show_alert(dajax,"error","User with this Shaastra ID does not exist")
                return dajax.json()
            try:
                checkedin = IndividualCheckIn.objects.get(shaastra_ID=shaastraid)
                if checkedin.check_out_date:
                    show_alert(dajax,"error","Participant has already checked out")
                    return dajax.json()
                else:
                    checkedin.check_out_date = datetime.now()
                    checkedin.check_out_control_room = checkedin.check_in_control_room
                    checkedin.save()
                    room = checkedin.room
                    room.max_number += 1
                    room.save()
                    show_alert(dajax,"success","Participant checked out successfully")
                    return dajax.json()
            except:
                show_alert(dajax,"error","Participant never checked in !")
                return dajax.json()
        else:
            show_alert(dajax,"error","An unexpected error has occured. Contact Webops ASAP")
            return dajax.json()
    else:
        form=ShaastraIDForm()
        html_content = render_to_string('hospi/Checkout.html',locals(),RequestContext(request))
        dajax.assign('#tab4',"innerHTML",html_content)
        return dajax.json()

@dajaxice_register
def remove(request,rem_form=None):
    dajax=Dajax()
    if request.method=='POST' and rem_form != None:
        form = RemoveRoom(deserialize_form(rem_form))
        if form.is_valid():
            cleaned_form=form.cleaned_data
            room_num = cleaned_form['room_no']
            hostel = cleaned_form['hostel']
            try:
                exist_room = AvailableRooms.objects.get(room_no=room_num,hostel=hostel)
                exist_room.delete()
                show_alert(dajax,"success","Room deleted successfully")
                return dajax.json()
            except:
                show_alert(dajax,"error","This room has not been added")
                return dajax.json()
        else:
            show_alert(dajax,"error","Form is not valid")
            return dajax.json()
    else:
        form=RemoveRoom()
        html_content = render_to_string('hospi/Remove.html',locals(),RequestContext(request))
        dajax.assign('#tab5',"innerHTML",html_content)
        return dajax.json()
@dajaxice_register
def choose(request,choose_eventform=None):
    dajax=Dajax()
    if request.method=='POST' and choose_eventform != None:
        form = ChooseEventForm(deserialize_form(choose_eventform))
        if form.is_valid():
            clean_form = form.clean()
            event_name = clean_form['event']
            generic_event_instance = GenericEvent.objects.get(title = event_name)
            event_pk = generic_event_instance.pk
            parti_event_instance = ParticipantEvent.objects.get(pk = event_pk)
            mins = parti_event_instance.team_size_min
            maxs = parti_event_instance.team_size_max
            teamformset = formset_factory(ShaastraIDForm,extra=maxs)
            data={
                    'form-TOTAL_FORMS':u'',
                    'form-INITIAL_FORMS':u'',
                    'form-MIN_NUM_FORMS':u'',
                    'form-MAX_NUM_FORMS':u'',
                    }
            html_content = render_to_string('hospi/CreateTeam.html',locals(),RequestContext(request))
            dajax.assign('#tab6',"innerHTML",html_content)
            return dajax.json()
        else:
            show_alert(dajax,"error","Form invalid")
            return dajax.json()
    else:
        form = ChooseEventForm()
        html_content = render_to_string('hospi/Choose.html',locals(),RequestContext(request))
        dajax.assign('#tab6',"innerHTML",html_content)
        return dajax.json()

@dajaxice_register
def createteam(request,team_formset=None,event_pk=None):
    dajax=Dajax()
    teamformset=formset_factory(ShaastraIDForm)
    generic_event_instance = GenericEvent.objects.get(pk=event_pk)
    event_name = generic_event_instance.title
    if request.method=="POST" and team_formset != None:
        formset = teamformset(deserialize_form(team_formset))
        print '111111111111111 %s' % formset
        if formset.is_valid():
            userlist = []
            for f in formset:
                print f
                cd = f.cleaned_data
                shaastraid='SHA14'+str(cd.get('shaastraID'))
                print shaastraid
                try:
                    parti = UserProfile.objects.using(mainsite_db).get(shaastra_id=shaastraid)
                    userlist.append(parti.user)
                except:
                    if shaastraid == 'SHA14None':
                        continue
                    else:
                        prof = create_junk_profile(shaastraid)
                        userlist.append(prof.user)

            teamevent = TeamEvent(event_id=event_pk)
            teamevent.save(using='mainsite')
            teamevent.users = userlist
            teamevent.team_id = 'TEAM#'+str(event_name[:5])+'#'+str(teamevent.pk)
            teamevent.team_name = str(event_pk)
            teamevent.save(using='mainsite')
            show_alert(dajax,"success","Team Registered successfully.Team ID is %s" % str(teamevent.pk))
            return dajax.json()
        else:
            show_alert(dajax,"error","Form is invalid")
            return dajax.json()
    else:
        show_alert(dajax,"error","Unexpected Error, Contact Webops")
        return dajax.json()

@dajaxice_register
def register(request,reg_form=None,coll_form=None):
    dajax=Dajax()
    if request.method=='POST':
        form = RegistrationForm(deserialize_form(reg_form))
        collegeform = CollegeForm(deserialize_form(coll_form))
        if form.is_valid():
            if not collegeform.is_valid():
                collist = form.cleaned_data['college'].split('|')
                collquery = College.objects.using(mainsite_db).filter(name = collist[0],city=collist[1], state=collist[2])
                if collquery.count():
                    college=collquery[0]
                else:
                    college = College(name=collist[0],city=collist[1],state=collist[2])
                    college.save(using='mainsite')
            else:
                college = collegeform.instance
                college.save(using='mainsite')

            cleaned_form = form.cleaned_data
            shaastraid = cleaned_form['shaastra_id']
            if not id_in_db(shaastraid):
                new_user = User(first_name=cleaned_form['first_name'],last_name=cleaned_form['last_name'],username=cleaned_form['username'],email=cleaned_form['email']) 
                new_user.set_password('default')
                new_user.is_active = True
                new_user.save(using='mainsite')
            else:
                try:
                    userprofile = get_userprofile(shaastraid)                
                except:
                    userprofile = UserProfile(user=new_user)
                userprofile.gender = cleaned_form['gender']
                userprofile.branch = cleaned_form['branch']
                userprofile.age = cleaned_form['age']
                userprofile.mobile_number = cleaned_form['mobile_number']
                userprofile.college_roll = cleaned_form['college_roll']
                userprofile.save(using='mainsite')

            new_form = IndividualForm(initial={'shaastra_ID':shaastraid})
            html_content = render_to_string('hospi/Checkin_form.html',locals(),RequestContext(request))
            dajax.assign('#tab3',"innerHTML",html_content)
            return dajax.json()
        else:
            show_alert(dajax,"error","Form is invalid")
            return dajax.json()

@dajaxice_register
def team(request,team_form=None):
    dajax=Dajax()
    if request.method=="POST" and team_form != None:
        form = TeamCheckinForm(deserialize_form(team_form))
        if form.is_valid():
            cleaned_form=form.cleaned_data
            check_in_control_room = cleaned_form['check_in_control_room']
            event_name = cleaned_form['event']
            generic_event_instance = GenericEvent.objects.get(title=event_name)
            event_pk = generic_event_instance.pk
            actual_name = event_name[:5]
            team_id_num = cleaned_form['team_id_num']
            team_id = 'TEAM#'+str(actual_name)+'#'+str(cleaned_form['team_id_num'])
            print team_id
            team_instance = TeamEvent.objects.using(mainsite_db).get(team_id=team_id)
            if check_in_control_room=='Godav':
                userlist = []
                checkedlist = []
                shalist=[]
                checkedin_shalist = []
                users_in_team = team_instance.users.all()
                for user_ex in users_in_team:
                    shaastraid = user_ex.userprofile_set.all()[0].shaastra_id
                    try:
                        checkedin_already = IndividualCheckIn.objects.get(shaastra_ID=shaastraid)
                        if user_ex.userprofile_set.all()[0].gender == 'M':
                            checkedlist.append(user_ex.userprofile_set.all()[0])
                            checkedin_shalist.append(user_ex.userprofile_set.all()[0].shaastra_id)
                        else:
                            pass
                    except:
                        if user_ex.userprofile_set.all()[0].gender == 'M':
                            userlist.append(user_ex.userprofile_set.all()[0])
                            shalist.append(user_ex.userprofile_set.all()[0].shaastra_id)
                tcheckinformset = modelformset_factory(IndividualCheckIn,form=IndividualForm,extra=len(userlist))
                formset = tcheckinformset(queryset=IndividualCheckIn.objects.filter(shaastra_ID__in = checkedin_shalist),initial=[{'shaastra_ID':sid,'check_in_control_room':'Godav','check_out_control_room':'Godav'} for sid in shalist])
                data={
                        'form-TOTAL_FORMS':u'',
                        'form-INITIAL_FORMS':u'',
                        'form-MIN_NUM_FORMS':u'',
                        'form-MAX_NUM_FORMS':u'',
                        }
                html_content = render_to_string('hospi/TeamDisplay.html',locals(),RequestContext(request))
                dajax.assign('#tab7',"innerHTML",html_content)
                return dajax.json()
            else:
                userlist = []
                shalist=[]
                checkedlist =[]
                checkedin_shalist =[]
                users_in_team = team_instance.users.all()
                for user_ex in users_in_team:
                    shaastraid = user_ex.userprofile_set.all()[0].shaastra_id
                    try:
                        checkedin_already = IndividualCheckIn.objects.get(shaastra_ID=shaastraid)
                        if user_ex.usreprofile_set.all()[0].gender == 'F':
                            checkedlist.append(user_ex.userprofile_set.all()[0])
                            checkedin_shalist.append(user_ex.userprofile_set.all()[0].shaastra_id)
                        else:
                            pass
                    except:
                        if user_ex.userprofile_set.all()[0].gender == 'F':
                            userlist.append(user_ex.userprofile_set.all()[0])
                            shalist.append(user_ex.userprofile_set.all()[0].shaastra_id)
                
                tcheckinformset = modelformset_factory(IndividualCheckIn,form=IndividualForm,extra=len(userlist))
                formset = tcheckinformset(queryset=IndividualCheckIn.objects.filter(shaastra_ID__in=checkedin_shalist),initial=[{'shaastra_ID':sid,'check_in_control_room':'Sharavati','check_out_control_room':'Sharavati'} for sid in shalist])
                data={
                        'form-TOTAL_FORMS':u'',
                        'form-INITIAL_FORMS':u'',
                        'form-MIN_NUM_FORMS':u'',
                        'form-MAX_NUM_FORMS':u'',
                        }
                html_content = render_to_string('hospi/TeamDisplay.html',locals(),RequestContext(request))
                dajax.assign('#tab7',"innerHTML",html_content)
                return dajax.json()
        else:
            print form.errors
            show_alert(dajax,"error","Form is invalid")
            return dajax.json()
    else:
        form = TeamCheckinForm()
        html_content = render_to_string('hospi/TeamCheckin.html',locals(),RequestContext(request))
        dajax.assign("#tab7","innerHTML",html_content)
        return dajax.json()

