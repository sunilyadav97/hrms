from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    # return HttpResponse('hello Sunil')
    return render(request,'ems/base.html')