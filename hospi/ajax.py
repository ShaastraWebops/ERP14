from django.utils import simplejson 
from misc.dajaxice.decorators import dajaxice_register
from misc.dajax.core import Dajax
from misc.dajaxice.utils import deserialize_form

from django.template import RequestContext
from django.template.loader import render_to_string
from django.template import loader

from django.contrib.auth.decorators import login_required

from hospi.models import *
from hospi.forms import AddRoomForm
import json 

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
            
