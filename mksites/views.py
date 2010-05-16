# Create your views here.
from debug import idebug
from django.http import HttpResponse
from django.shortcuts import render_to_response,redirect
from mksites.forms import SubdomainUserForm
from django.template import RequestContext
from django.contrib.auth import login,authenticate

def create_subdomain(request):
    form = SubdomainUserForm(request.POST or None)
    if form.is_valid():
        username, password, subdomain = form.save()
        user = authenticate(username=username,password=password)
        login(request,user)
        request.user.message_set.create(message='You have successfully registered %s'%subdomain.get_absolute_url())
        return redirect("%s%s/"%(subdomain.get_absolute_url(),'erp'))
    
    return render_to_response('mksites/createsite.html',
                              {'form':form},
                              RequestContext(request))

