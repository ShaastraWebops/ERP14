#Django imports
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from hospi.models import *
from hospi.forms import *
from hospi.generate_bill import *

def home(request):
    context = {}
    context["userprofile"] = request.user.get_profile()
    return render_to_response('hospi/home.html',context,context_instance = RequestContext(request))

def checkin(request):
    if request.method == "POST":
        form = IndividualForm(request.POST)
        if form.is_valid():
            cleaned_form = form.cleaned_data
            room = cleaned_form['room']
            shaastraid = cleaned_form['shaastra_ID']
            parti_in_room = IndividualCheckIn.objects.filter(room=room)
            if room.max_number<=len(parti_in_room):
                msg = "This room has reached its Maximum Capacity"
            else:
                form.save()
                room.already_checkedin = 1
                room.save()
                msg = "Participant checked in successfully"
                sid = shaastraid[-5:]
                return render_to_response('hospi/Bill.html',locals(),RequestContext(request))
        else:
            msg = "Form is not valid"
            return render_to_response('hospi/home.html',locals(),RequestContext(request))

def generate_bill(request,sid):
    shaastraid = 'SHA14'+sid
    pdf = generateParticipantPDF(shaastraid,0)
    return pdf
