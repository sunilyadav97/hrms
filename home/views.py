from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout,authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def home(request):
    context={}
    try:
        if request.method == 'POST':
            username=request.POST['username']
            password=request.POST['password']
            print(username)
            print(password)
            if username and password == '':
                messages.warning(request,'All Fields Mandatry')
                return redirect('home:home')
            else:
                user_obj=User.objects.filter(username=username).exists()
                if user_obj:
                    messages.warning(request,'This Username not Available')
                else:
                    obj=User.objects.create(username=username)
                    if obj:
                        obj.set_password(password)
                        obj.save()
                        messages.success(request,'You have Registered successfully!')
                    else:
                        messages.warning(request,'Somthing Went wrong!')
    except Exception as e:
        print("Home Exception : ",e)
    
    return render(request,'home/home.html',context)


def signin(request):
    try:
        if request.method == 'POST':
            username=request.POST['username']
            password=request.POST['password']
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                messages.success(request,'Logged in successfully!')
                return redirect('/')
            else:
                messages.warning(request,'Credentials Not Match!')
    except Exception as e:
        print("Signin Exception :",e)
    return render(request,'home/signup.html')

def signout(request):
    logout(request)
    messages.success(request,'Logout Succeesfully!')
    return redirect('home:home')