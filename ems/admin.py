from django.contrib import admin
from .models import *

admin.site.register(Department)
admin.site.register(Role)
admin.site.register(Employee)
admin.site.register(Address)

admin.site.register(Attendance)
admin.site.register(Leave)
admin.site.register(Events)
admin.site.register(DepartmentQuery)
admin.site.register(QueryComment)
admin.site.register(Connect)
admin.site.register(AllocatedLeave)

