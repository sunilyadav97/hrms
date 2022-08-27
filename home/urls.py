from django.urls import path
from .views import *
app_name='home'
urlpatterns=[
    path('',home,name='home'),
    path('lgoin/',signin,name='login'),
    path('logout/',signout,name='logout'),
]