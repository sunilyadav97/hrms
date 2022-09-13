import random
from .models import *


def generateId():
    id=''
    for i in range(0,6):
        id+=str(random.randint(0,9))
    id=int(id)
    obj=DepartmentQuery.objects.filter(query_id=id).exists()
    if obj:
        generateId()
    else:
        return id