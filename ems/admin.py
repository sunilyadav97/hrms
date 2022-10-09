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
admin.site.register(PayRoll)
admin.site.register(Newuser)
admin.site.register(Document)
admin.site.register(NewsLetter)
admin.site.register(Appreciation)
admin.site.register(ReimbursementTransport)
admin.site.register(ReimbursementFood)
admin.site.register(ReimbursementFoodEmployee)
admin.site.register(ReducedLeaves)

