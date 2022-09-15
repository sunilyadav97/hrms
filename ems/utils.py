import random
from .models import *
import datetime
from datetime import timedelta,timezone

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
            compare_time=datetime.time(23,00,00).hour
            object_time=int(((difference.seconds)/60)/60)
            
            if object_time > compare_time:
                item.delete()
                print('Item Deleted')
            else:
                print('Time Need to complete')
    except Exception as e:
        print('Expire Connect Exception : ',e)
    
        