from django.urls import path
from .views import *
app_name='ems'
urlpatterns=[
    path('',dashboard,name='ems'),
    path('create-department/',createDepartment,name='create-department'),
    path('view-departments/',viewDepartment,name='view-department'),
    path('delete-department/<pk>/',deleteDepartment,name='delete-department'),
    path('create-role/',createRole,name='create-role'),
    path('view-roles/',viewRole,name='view-role'),
    path('delete-role/<pk>/',deleteRole,name='delete-role'),
    path('employee-register/',addEmployee,name='employee-add'),
    path('employee-view/',viewEmployee,name='employee-view'),
    path('employee-detail/<empid>/',employeeDetail,name='employee-detail'),
    path('attendance',attendance,name='attendance'),
    
]