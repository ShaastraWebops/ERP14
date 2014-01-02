# Create your views here.
import csv
from django.shortcuts import render_to_response
from barcode.forms import *
from django.template import RequestContext
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from events.models import GenericEvent
from models import Barcode,Event_Participant,PPM
from django.contrib import messages
from users.models import UserProfile
from barcode.scripts import *
from django.forms.models import modelform_factory


#TODO: if shaastra id not valid in portal
def get_details(request,sh_id=None):
    output_str = ""
    if sh_id:
        if not id_in_db(sh_id):
            output_str += "Entered Shaastra ID is not yet entered into database"
        elif is_junk(sh_id):
            output_str += "Entered Shaastra ID details are junk. Please request and enter the participants details"
            output_str += "<a href = '/???'>here</a>?"
            return HttpResponse(output_str)
            #TODO: link to url for edit profile!!
        else:
            profile = get_userprofile(sh_id)
            return render_to_response('barcode/profile_details.html', {'profile':profile}, context_instance=RequestContext(request))
        detailform = DetailForm()
        return render_to_response('barcode/get_details.html', {'form':detailform,'output_str':output_str}, context_instance=RequestContext(request))
    if request.method == 'POST':
        detailform = DetailForm(request.POST)
        output_str = ""
        if detailform.is_valid():
            shaastra_id  = detailform.cleaned_data['shaastra_id']
            if not id_in_db(shaastra_id):
                output_str += "Entered Shaastra ID is not yet entered into database"
            elif is_junk(shaastra_id):
                output_str += "Entered Shaastra ID details are junk. Please request and enter the participants details"
                output_str += "<a href = '/???'>here</a>?"
                return HttpResponse(output_str)
                #TODO: link to url for edit profile!!
            else:
                profile = get_userprofile(shaastra_id)
                return render_to_response('barcode/profile_details.html', {'profile':profile}, context_instance=RequestContext(request))
            return render_to_response('barcode/get_details.html', {'form':detailform,'output_str':output_str}, context_instance=RequestContext(request))
        else:
            output_str +=[str(error) for error in detailform.errors.values()]
    detailform = DetailForm(initial = {'shaastra_id':"SHA14"})
    
    return render_to_response('barcode/get_details.html', {'form':detailform,'output_str':output_str}, context_instance=RequestContext(request))

def edit_profile(request,shaastra_id=None):
    message_str = ""
    if request.method == 'POST':
        form = EditProfileForm(request.POST)
        college_form = CollegeForm(request.POST)
        if form.is_valid() and college_form.is_valid():
            profile = form.instance
            college = college_form.instance
            college.save(using = 'mainsite')
            profile.college = college
            try:
                user = User.objects.using('mainsite').get(username = shaastra_id)
            except:
                user = User(username = shaastra_id,email = shaastra_id +'@'+shaastra_id+'.com',password = 'default' + shaastra_id)
                user.save(using = 'mainsite')
            user.first_name = form.cleaned_data['first_name']
            user.email = form.cleaned_data['email']
            """
            
            try:
                user = User.objects.using('mainsite').get(username = shaastra_id)
            except:
                user = User()
                user.set_password('default')
                user.save(using = 'mainsite')
            """
            profile.user = user
            """
            try:
                db_profile = UserProfile.objects.get(shaastra_id = shaastra_id)
                db_profile = profile
                db_profile.save(using = 'mainsite')
            except:
            """
            profile.save(using = 'mainsite')
            return HttpResponse("success!!%s Added..Go  <a href='/barcode/detail_entry' >back</a>"% str(shaastra_id))
            return HttpResponseRedirect(reverse('detail_entry'))
        else:
            message_str += str(form.errors.values())
        
    if shaastra_id is None or not id_is_valid(shaastra_id):
        return HttpResponse('<strong>Invalid Shaastra ID</strong>')
    if not id_in_db(shaastra_id):
        #Here, details are not submitted-> no barcode..
        form = EditProfileForm(initial = {'shaastra_id':shaastra_id})
        college_form = CollegeForm()
    else:
        message_str = "Details already entered, may be junk, so replace with actual values."
        profile = get_userprofile(shaastra_id)
        form = EditProfileForm(instance = profile,initial = {'first_name':profile.user.first_name,'email':profile.user.email})
        college_form = CollegeForm(instance = profile.college)
    return render_to_response('barcode/edit_profile.html', {'profileform':form,'collegeform':college_form,'message_str':message_str}, context_instance=RequestContext(request))

        

def upload_ppm(request):
    PPMForm = modelform_factory(PPM)
    if request.method == 'POST':
        form = PPMForm (request.POST)
        if form.is_valid():
            form.save()
            return redirect('barcode.views.upload_ppm')

    else:
        #Display Blank Form
        form = PPMForm()
        context = {'form': form}
    
    return render_to_response ('barcode/ppm.html', {'form': form }, context_instance=RequestContext(request))    
    
def upload_csv(request, type):
    flag_str = ''
    
    eventForm = None
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        event = EventForm(request.POST)
        #TODO: get event model from this...
        if form.is_valid() and (type=="barcodeportal" or event.is_valid()):
            if not form.files:
                flag_str = 'Please upload a valid file'
                return HttpResponse(flag_str)
            elif not event and type=="participantsportal":
                flag_str = 'Choose a valid event'
                return HttpResponse(flag_str)
            else:
                display_list = []
                fail_list = []
                message_str = "Successfully uploaded "
                if type == "participantsportal":
                    (display_list,fail_list) = process_csv(request,request.FILES['file'],form.cleaned_data['title'],type,event.cleaned_data['event_title'] )
                    if display_list[1:]:
                        message_str+=str(display_list[0])
                        display_list = display_list[1:]
                        message_str += "::"
                        message_str+=str(display_list)
                else:
                    (display_list,fail_list) = process_csv(request,request.FILES['file'],form.cleaned_data['title'] ,type) 
                    if display_list:
                        message_str += str(len(display_list)) + "items;"
                        message_str += str(display_list[0:5]) + "etc.."
                        print str(display_list)
                    if fail_list:
                        message_str += "||Failed: %s" % str(fail_list)
                if display_list is None and fail_list is None:
                    return HttpResponse('File reading failed, check file format')
                
                messages.success(request,"%s..."% (message_str))
                return HttpResponseRedirect(reverse(type))
        else:
            flag_str = "Invalid Upload"
    else:
        form = UploadFileForm(initial={'title': 'SHAASTRA ID'})
        eventForm = EventForm()

    if type == "barcodeportal":
        title = "Barcode Portal"
    if type == "participantsportal":
        title = "Participant's Portal"
        eventForm = EventForm()
    return render_to_response('barcode/upload_csv.html', {'eventForm':eventForm,'flag_str':flag_str,'form': form, 'type': type, 'title': title}, context_instance=RequestContext(request))


def process_csv (request,file, title,type_str,event_title = None):
    try:
        input_file = csv.DictReader(file,delimiter=',')
        if file.content_type!='text/csv':
            return (None,None)
    except:
        return (None,None)
    return_list = []
    fail_list = []
    if type_str == "barcodeportal":
        sh_id = []
        barcode = []
        for d in input_file:
            sh_id.append(d[title])
            barcode.append(d['BARCODE'])
        i=0
        while i<len(sh_id):
            if not id_is_valid(sh_id[i]):
                fail_list.append(sh_id[i])
                i = i+1
                continue
            if id_is_valid(sh_id[i])==-1:
                sh_id[i] = 'SHA14' + sh_id[i]
            #below section is for on-spot guys
            if not id_in_db(sh_id[i]) and not barcode_in_db(barcode[i]):
                profile = create_junk_profile(sh_id[i])
                barcode_obj = Barcode(shaastra_id = sh_id[i],barcode = barcode[i])
                return_list.append(str(sh_id[i]))
                barcode_obj.save()
                i = i+1
                continue
            if barcode_in_db(barcode[i]):
                #This section is for mainsite regd. ppl who registered in events, so got a bogus profile
                if id_in_db(sh_id[i]):
                    junk_profile = get_userprofile(sh_id[i])
                    
            #This section is for on-spot ppl regd. ppl who registered in events, so got a bogus profile
                else:
                    pass
                
                #TODO: what??
            # This below check is for existing shaastra ID's(mainsite registered)
            if Barcode.objects.filter(shaastra_id = sh_id[i]).count()==0:
                barcode_obj = Barcode(shaastra_id = sh_id[i],barcode = barcode[i])
                return_list.append(str(sh_id[i]))
                barcode_obj.save()
            else:
                i=i+1
                continue
                #TODO: code to do when shaastra ID is scanned second time..
            #TODO: write to a log text file that this happened..
            i=i+1
    if type_str == "participantsportal":
        if event_title == None:
            return False
        barcode = []
        insti_list = []#List of insti roll no.s
        for d in input_file:
            if is_valid_insti_roll(d['BARCODE']):
                insti_list.append(d['BARCODE'])
            else:
                barcode.append(d['BARCODE'])
        event_list = GenericEvent.objects.filter(title = event_title)
        return_list.append(str(event_title))
        if event_list.count() == 0:
            return False
        event = event_list[0]
        sh_id = []
        error_list = []
        #TODO: implement roll no, of insti
        #NOW, get shaastra id of corresponding barcodes, and error list appended if not found
        for code in barcode:
            try:
                sh_id.append(Barcode.objects.get(barcode = code).shaastra_id)
            except:
                #if barcode object does not exist, just make a junk for given barcode
                if is_valid_barcode(code):
                #TODO!!!
                    barcode = Barcode.objects.create(barcode = code, shaastra_id = '#'+ str(code) + '#' )
                    profile = create_junk_profile('#' + str(code) + '#')
                    sh_id.append('#' + str(code) + '#')
                else:
                    error_list.append(code)
        i=0
        for roll in insti_list:
            insti_part = Insti_Participant(event = event,insti_roll = roll)
            insti_part.save()
            #TODO: what to do with roll?? store??
            
        while i<len(sh_id):
            #print barcode[i]+"||"
            ev_part = Event_Participant(event = event,shaastra_id = sh_id[i])
            return_list.append(str(sh_id[i]))
            ev_part.save()
            i=i+1
        if len(error_list):
            messages.warning(request,'%d values were invalid: some are:%s' % (len(error_list),error_list))
            #TODO: display error list??
            #return False
    return (return_list,fail_list)


#View to add an entry one at a time.
def add_single_entry(request,type):
    flag_bar = False
    flag_str = ''
    if type == "barcodeportal":
        flag_bar = True
    if request.method =='POST':
        if flag_bar:
            form = BarcodeForm(request.POST)
        else:
            form = Event_Participant_Form(request.POST)
        if form.is_valid():
            if flag_bar:
                flag_str = add_single_barcode(form.cleaned_data)
                if flag_str!='':
                    messages.success(request,'Successfully added')
                else:
                    messages.success(request,'Invalid data: Shaastra ID not valid')
                return HttpResponseRedirect(reverse('add_single_barcode'))

            else:
                flag_str = add_single_participant(form.cleaned_data)
                if flag_str !='':
                    messages.success(request,'Successfully added')
                else:
                    messages.success(request,'Invalid Shaastra ID: Not registered in Hospi Desk!!')
                return HttpResponseRedirect(reverse('add_single_participant'))
        else:
            if flag_bar:
                return HttpResponse("Enter valid event . Go <a href='/barcode/csv/add_single_barcode'>Back</a>")
            return HttpResponse("Enter valid event . Go <a href='/barcode/csv/add_single_participant'>Back</a>")
    else:
        if flag_bar:
            title = "Barcode Portal"
            form = BarcodeForm()
        else:
            title = "Participant's Portal"
            form = Event_Participant_Form()
    return render_to_response('barcode/upload_single.html', {'form':form,'flag_str':flag_str, 'type': type, 'title': title}, context_instance=RequestContext(request))


def add_single_barcode(barcodedata):
    shid = barcodedata['shaastra_id']
    code = barcodedata['barcode']
    if not id_in_db(shid):
        return ''
    
    barcode_obj = Barcode(shaastra_id = shid,barcode = code)
    barcode_obj.save()
    return 'add single success'
    
def add_single_participant(event_participant_data):
    
    try:
       shid = Barcode.objects.get(shaastra_id = event_participant_data['shaastra_id']).shaastra_id
       #NOTE: here form's shaastra id is used to get the shaastra ID, it actually barcode
    except:
        return ''
    if not id_in_db(shid):
        return ''
    
    ev_part = Event_Participant(event = event_participant_data['event'],shaastra_id = shid)
    ev_part.save()
    return 'add single success'
