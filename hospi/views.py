#Django imports
from django.http import HttpResponse 
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

def home(request):
    context = {}
    context["userprofile"] = request.user.get_profile()
    return render_to_response('hospi/home.html',context,context_instance = RequestContext(request))


