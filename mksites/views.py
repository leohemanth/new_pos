# Create your views here.
from debug import idebug
from django.http import HttpResponse

def create_subdomain(request):
    idebug()
    return HttpResponse('A')

