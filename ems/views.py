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
        department_description=request.POST['department-description']
        obj=Department.objects.create(name=department_name,description=department_description)
        print(obj)
        
        return HttpResponse('Department Added Successfully')
    return render(request,'ems/create_department.html',context)

def viewDepartment(request):
    context={}
    try:
        departments=Department.objects.all()
        context['departments']=departments
    except Exception as e:
        print('View Department Exception : ',e)
    return render(request,'ems/view_department.html',context)