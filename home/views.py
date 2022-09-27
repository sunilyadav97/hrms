from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout,authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from ems.models import *
import random
from ems.utils import *

def home(request):
    
    context={}
    try:
        if request.user.is_authenticated:
            check=Employee.objects.filter(user=request.user).exists()
            if check:
                return redirect('ems:ems')
        images=list(SliderImage.objects.all())
        random.shuffle(images)
        context['images']=images
    except Exception as e:
       print('Home Exception : ',e)

    return render(request,'home/home.html',context)

def register(request):
    context={}
    try:
        if request.method == 'POST':
            username=request.POST['username']
            fname=request.POST['fname']
            lname=request.POST['lname']
            email=request.POST['email']
            password=request.POST['password']
            print(username)
            print(fname)
            print(email)
            print(password)

            if username and password and fname and email == '':
                messages.warning(request,'All Fields Mandatry')
                return redirect('home:home')
            else:
                user_obj=User.objects.filter(username=username).exists()
                if user_obj:
                    messages.warning(request,'This Username not Available')
                else:
                    obj=User.objects.create(username=username,email=email)
                    if obj:
                        obj.set_password(password)
                        obj.first_name=fname
                        if lname != '':
                            obj.last_name=lname
                        obj.save()
                        token=generateToken()
                        newuser_obj=Newuser.objects.create(token=token,user=obj)
                        print('New User obj ',newuser_obj)
                        messages.success(request,'You have Registered successfully! Now Admin Will Send You Email in 24 Hour')
                        return redirect('home:login')
                    else:
                        messages.warning(request,'Somthing Went wrong!')
    except Exception as e:
        print('Rgister View Exception : ',e)
    return render(request,'home/register.html',context)

def signin(request):
    try:
        if request.user.is_authenticated:
            return redirect('ems:ems')
        if request.method == 'POST':
            username=request.POST['username']
            password=request.POST['password']
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                print('user : ',user)
                emp_obj=Employee.objects.filter(user=user).exists()
                
                if user.is_superuser:
                    messages.success(request,'Logged in successfully!')
                    return redirect('ems:ems')
                    
                if emp_obj:
                    messages.success(request,'Logged in successfully!')
                    return redirect('ems:ems')
                else:
                    messages.info(request,'Please check your Email And follow Link to add Your Persional info!')
                    return redirect('/')
            else:
                messages.warning(request,'Credentials Not Match!')
    except Exception as e:
        print("Signin Exception :",e)
    return render(request,'home/signup.html')

def signout(request):
    logout(request)
    messages.success(request,'Logout Succeesfully!')
    return redirect('home:login')