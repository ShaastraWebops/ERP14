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
            room.max_number = room.max_number - 1
            #if room.max_number<=len(parti_in_room):
            #    msg = "This room has reached its Maximum Capacity"
            #else:
            form.save()
            room.already_checkedin = 1
            room.save()
            msg = "Participant checked in successfully"
            pdf = generateParticipantPDF(shaastraid,0)
            return pdf
        else:
            msg = "Form is not valid"
            return render_to_response('hospi/home.html',locals(),RequestContext(request))

def teamcheckin(request,pk):
    tcheckinformset = formset_factory(IndividualForm)
    event_pk = pk[:2]
    team_id_num = pk[2:]
    generic_event_instance = GenericEvent.objects.get(pk=event_pk)
    event_name = generic_event_instance.title
    team_id = 'TEAM#'+str(event_name[:5])+'#'+str(team_id_num)
    if request.method=="POST":
        formset = tcheckinformset(request.POST)
        if formset.is_valid():
            shalist = []
            roomlist = []
            for f in formset:
                cd = f.cleaned_data
                shalist.append(cd.get('shaastra_ID'))
                roomlist.append(cd.get('room'))
            formset.save()
            for room in roomlist:
                room.max_number = room.max_number - 1
                room.save()
            pdf = generateParticipantPDF(shalist[0],team_id,shalist)
            return pdf

        else:
            return render_to_response('hospi/home.html',locals(),RequestContext(request))


        

