from django.utils import simplejson 
from misc.dajaxice.decorators import dajaxice_register
from misc.dajax.core import Dajax
from misc.dajaxice.utils import deserialize_form

from django.template import RequestContext
from django.template.loader import render_to_string
from django.template import loader

from django.contrib.auth.decorators import login_required
from users.models import UserProfile
from hospi.models import *
from hospi.forms import AddRoomForm,IndividualForm,ShaastraIDForm
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
    else:
        form = AddRoomForm()
        html_content = render_to_string('hospi/AddRoom.html',locals(),RequestContext(request))
        dajax.assign('#tab2',"innerHTML",html_content)
        return dajax.json()
            
@dajaxice_register
def checkin(request,indi_form=None):
    dajax = Dajax()
    if request.method == 'POST' and indi_form != None:
        form = IndividualForm(deserialize_form(indi_form))
        if form.is_valid():
            cleaned_form = form.cleaned_data
            shaastraid = cleaned_form['shaastra_ID']
            try:
                participant = UserProfile.objects.using(mainsite_db).get(shaastra_id = shaastraid)
            except:
                show_alert(dajax,"error","User with this Shaastra ID does not exist, %s" %(shaastraid,))
                return dajax.json()
            try:
                checkedin = IndividualCheckIn.objects.get(shaastra_id=cleaned_form['shaastra_ID'])
                room = checkedin.room
                checkindate = checkedin.check_in_date
                checkoutdate = checkedin.check_out_date
                if checkoutdate:
                    show_alert(dajax,"info","Participant was checked-in into" + str(room) + ".He has already checked-out on "+str(checkoutdate))
                    return dajax.json()
                else:
                    show_alert(dajax,"info","Participant is checked-in into" + str(room))
            except:
                room = cleaned_form['room']
                parti_in_room = IndividualCheckIn.objects.filter(room=room)
                if room.max_number<=len(parti_in_room):
                    show_alert(dajax,"error","This room has reached maximum capacity")
                    return dajax.json()
                else:
                    form.save()
                    room.already_checkedin = 1
                    room.save()
                    show_alert(dajax,'success',"Checked In successfully")
                    html_content = render_to_string('hospi/Checkin_indi.html',locals(),RequestContext(request))
                    dajax.assign('#tab3',"innerHTML",html_content)
                    return dajax.json()
        else:
            show_alert(dajax,"error","Form is not valis")

    else:
        form = IndividualForm()
        html_content = render_to_string('hospi/Checkin_indi.html',locals(),RequestContext(request))
        dajax.assign('#tab3',"innerHTML",html_content)
        return dajax.json()

@dajaxice_register
def checkout(request,shaastra_form=None):
    dajax = Dajax()
    if request.method=='POST' and shaastra_form != None:
        form = ShaastraIDForm(desrialize_form(shaastra_form))
        if form.is_valid():
            cleaned_form = form.cleaned_data
            try:
                participant = UserProfile.objects.using(mainsite_db).filter(shaastra_id = cleaned_form['shaastraID'])
            except:
                show_alert(dajax,"error","User with this Shaastra ID does not exist")
                dajax.json()
            try:
                checkedin = IndividualCheckin.objects.get(shaastra_ID=cleaned_form['shaastraID'])
                if checkedin.check_out_date:
                    show_alert(dajax,"error","Participant has already checked out")
                    return dajax.json()
                else:
                    checkedin.check_out_date = datetime.now()
                    checkedin.check_out_control_room = checkedin.check_in_control_room
                    checkedin.save()
                    room = checkedin.room
                    room.already_checkedin = 0
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
