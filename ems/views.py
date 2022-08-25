from django.shortcuts import render
from django.http import HttpResponse
from .models import *

def home(request):
    context={}
    return render(request,'ems/home.html',context)

def dashboard(request):
    context={}
    return render(request,'ems/dashboard.html',context)

def createDepartment(request):
    context={}
    if request.method == 'POST':
        department_name=request.POST['department-name']
        department_discription=request.POST['department-discription']
        obj=Department.objects.create(name=department_name,description=department_discription)
        print(obj)
        
        return HttpResponse('Department Added Successfully')
    return render(request,'ems/create_department.html',context)