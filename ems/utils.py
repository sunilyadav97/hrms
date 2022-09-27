import random
import string
from .models import *
import datetime
from datetime import timedelta,timezone
from django.contrib.auth.models import User
from techinterio import settings
from django.core.mail import send_mail

def generateId():
    id=''
    for i in range(0,6):
        id+=str(random.randint(0,9))
        
    if len(id) != 6:
        generateId()
    else:
        id=int(id)
        obj=DepartmentQuery.objects.filter(query_id=id).exists()
        if obj:
            generateId()
        else:
            return id
        
def expireConnect():
    try:
        connects=Connect.objects.all()
        for item in connects:
            create_time=item.created_at
            current_time=datetime.datetime.now(timezone.utc)
            difference=current_time-create_time

            compare_time=int(2)
            
            if difference.days >= compare_time:
                item.delete()
                print('Item Deleted')
            else:
                print('Time Need to complete')

    except Exception as e:
        print('Expire Connect Exception : ',e)
    
def checkIsLate(intime):
    split_intime=str(intime).split(":")
    intime_hour=int(split_intime[0])
    intime_minute=int(split_intime[1])
    if intime_hour == 9:
        if intime_minute >45:
            return True
    elif intime_hour >9:
        return True
    else:
        return False


def generateToken():
    token=''.join(random.choices(string.ascii_uppercase + string.digits, k = 20))
    print(token)

    if len(token) !=20:
        generateToken()
    else:
        obj=Newuser.objects.filter(token=token).exists()
        
        if obj:
            generateToken()
        else:
            return token


def sendMail(username,domain):
    user=User.objects.get(username=username)
    print('send mail user :',user)
    email=user.email
    print('email ',email)
    newuser_obj=Newuser.objects.get(user=user)
    print('send mail new user :',newuser_obj)
    token=newuser_obj.token
    subject="Welcome To Techinterio"
    message="This is Verification Email by Admin \n \n \n Follow Link given below. \n You can add your personal Info by following link. \n \n Note- This link only work when you will be connected with Techinterio Internal Server. \n \n Link: "+domain+"/ems/verify/"+token
    # message="Hello Dear Clients"
    from_email=settings.EMAIL_HOST_USER
    recipient_list=[email]
    send_mail(subject,message,from_email,recipient_list, fail_silently=True)
    print(message)
    return True
