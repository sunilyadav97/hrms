from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
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
        messages.success(request,'New Department created Successfully!')
        return redirect('ems:view-department')
    return render(request,'ems/create_department.html',context)

def viewDepartment(request):
    context={}
    try:
        departments=Department.objects.all()
        context['departments']=departments
    except Exception as e:
        print('View Department Exception : ',e)
    return render(request,'ems/view_department.html',context)

def deleteDepartment(request,pk):
    try:
        Department.objects.get(id=pk).delete()
        messages.success(request,'Department Deleted Successfully!')
        return redirect(reverse('ems:view-role'))
    except Exception as e:
        print('Delete Department Exception : ',e)
        
        
def createRole(request):
    context={}
    if request.method == 'POST':
        role_name=request.POST['role-name']
        role_description=request.POST['role-description']
        obj=Role.objects.create(name=role_name,description=role_description)
        print(obj)
        messages.success(request,'Created New Role Successfully!')
        return redirect('ems:view-role')
    return render(request,'ems/create_role.html',context)

def viewRole(request):
    context={}
    try:
        roles=Role.objects.all()
        context['roles']=roles
    except Exception as e:
        print('View Role Exception : ',e)
    return render(request,'ems/view_role.html',context)

def deleteRole(request,pk):
    try:
        Role.objects.get(id=pk).delete()
        print(pk)
        messages.success(request,'Deleted Role Successfully!')
        return redirect(reverse('ems:view-role'))
    except Exception as e:
        print('Delete Role Exception : ',e)