from django.utils import simplejson 
from misc.dajaxice.decorators import dajaxice_register
from misc.dajax.core import Dajax
from misc.dajaxice.utils import deserialize_form

from django.template import RequestContext
from django.template.loader import render_to_string
from django.template import loader

from django.contrib.auth.decorators import login_required

from hospi.models import *
from hospi.forms import AddRoomForm,IndividualForm
import json 
from misc.utilities import show_alert
from erp.settings import DATABASES
mainsite_db = DATABASES.keys()[1]

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
            try:
                participant = UserProfile.objects.using(mainsite_db).filter(shaastra_id = cleaned_form['shaastra_id'])
            except:
                show_alert(dajax,"error","User with this Shaastra ID does not exist")
                return dajax.json()
            try:
                checkedin = IndividualCheckIn.objects.get(shaastra_id=cleaned_form['shaastra_id'])
                room = checkedin.room
                checkindate = checkedin.check_in_date
                checkoutdate = checkedin.check_out_date
                if checkoutdate:
                    show_alert(dajax,"info","Participant was checked-in into" + str(room) + ".He has already checked-out on "+str(checkoutdate))
                    return dajax.json()
                else:
                    show_alert(dajax,"info","Participant is checked-in into" + str(room))
            except:
                form.save()
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
