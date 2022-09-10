from django.urls import path
from .views import *
app_name='home'
urlpatterns=[
    path('',home,name='home'),
    path('login/',signin,name='login'),
    path('register/',register,name='register'),
    path('logout/',signout,name='logout'),
]