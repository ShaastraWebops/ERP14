from django.utils import simplejson 
from misc.dajaxice.decorators import dajaxice_register
from misc.dajax.core import Dajax
from misc.dajaxice.utils import deserialize_form

from django.template import RequestContext
from django.template.loader import render_to_string
from django.template import loader

from django.contrib.auth.decorators import login_required

from hospi.models import *
import json 

@dajaxice_register
def roommap(request):  
    dajax = Dajax()
    alak = AvailableRooms.objects.filter(hostel='Alakananda').order_by('room_no')
    ganga = AvailableRooms.objects.filter(hostel='Ganga').order_by('room_no')
    jam = AvailableRooms.objects.filter(hostel='Jamuna').order_by('room_no')
    mahanadhi = AvailableRooms.objects.filter(hostel='Mahanadhi').order_by('room_no')
    mandak = AvailableRooms.objects.filter(hostel='Mandakini').order_by('room_no')
    pamba = AvailableRooms.objects.filter(hostel='Pamba').order_by('room_no')
    sarayu = AvailableRooms.objects.filter(hostel='Sarayu').order_by('room_no')
    sharav = AvailableRooms.objects.filter(hostel='Sharavati').order_by('room_no')
    sindhu = AvailableRooms.objects.filter(hostel='Sindhu').order_by('room_no')
    tambi = AvailableRooms.objects.filter(hostel='Tamraparani').order_by('room_no')
    sarayu_extn = AvailableRooms.objects.filter(hostel='Sarayu Extn').order_by('room_no')
    c28 = AvailableRooms.objects.filter(hostel='C-2-8').order_by('room_no')
    html_content =  render_to_string('controlroom/RoomMap.html', locals(),RequestContext(request))
    dajax.assign('#tab1',"innerHTML",html_content)
    return dajax.json()
