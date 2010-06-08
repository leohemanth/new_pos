from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from contacts.models import ContactForm
from django.template import RequestContext, Context
from django import  forms
from django.forms.widgets import *
from django.core.mail import send_mail, BadHeaderError

def contactview(request):
		subject = request.POST.get('topic', '')
		message = request.POST.get('message', '')
		from_email = request.POST.get('email', '')

		if subject and message and from_email:
		        try:
					send_mail(subject, message, from_email, ['change@this.com'])
        		except BadHeaderError:
            			return HttpResponse('Invalid header found.')
        		return HttpResponseRedirect('/contact/thankyou/')
		else:
			return render_to_response('lazydays/contacts.html', {'form': ContactForm()})
	
		return render_to_response('lazydays/contacts.html', {'form': ContactForm()},
			RequestContext(request))

def thankyou(request):
		return render_to_response('lazydays/thankyou.html')
