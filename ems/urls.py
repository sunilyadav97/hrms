from django.urls import path
from .views import *
app_name='ems'
urlpatterns=[
    path('',home,name='home'),
    path('dashboard/',home,name='dashboard'),
    path('create-department/',createDepartment,name='create-department'),
    path('view-department/',viewDepartment,name='view-department'),
]