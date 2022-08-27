from django.contrib import admin
from .models import *

admin.site.register(Department)
admin.site.register(Role)
admin.site.register(Employee)
admin.site.register(Address)

admin.site.register(Attendance)

