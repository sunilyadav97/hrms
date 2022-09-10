
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .models import *
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator
from datetime import datetime,timedelta




def dashboard(request):
    context={}
    try:
        if request.user.is_authenticated:
            employees=list(Employee.objects.all())
            birthdays=[]
            now=datetime.now()
            day=now.day
            month=now.month
            year=now.year
            
            for i in employees:
                dob_base=str(i.dob).split('-')
                dob_day=int(dob_base[2])
                dob_month=int(dob_base[1])
                dob_year=int(dob_base[0])
                if dob_day == day and dob_month == month:
                    birthdays.append(i)
                    print('Happy Birthday')
                else:
                    print('Not Happy Birthday')
            
            context['birthdays']=birthdays      
            
            anniversaries=[]
            for i in employees:
                joing_base=str(i.joining_date).split('-')    
                j_day=int(joing_base[2])
                j_month=int(joing_base[1])
                j_year=int(joing_base[0])
                completed_years=year-j_year
                data={}
                if j_day== day and j_month==month and completed_years>0:
                    print(i)
                    data['completed_years']=completed_years
                    data['employee']=i
                    anniversaries.append(data)
                    
                    print('Happy Anniversary',i.name,completed_years)
 
            context['anniversaries']=anniversaries

            if not request.user.is_superuser:
                profile_obj=Employee.objects.get(user=request.user)
                context['profile']=profile_obj
                events=Events.objects.all()[0:2]
                context['events']=events
                return render(request,'ems/ems_home.html',context)
            else:
                departments=Department.objects.all()
                roles=Role.objects.all()
                employees=Employee.objects.all()
                leaves=Leave.objects.filter(status='Pending')
                context['departments']=departments.count()
                context['employees']=employees.count()
                context['leaves']=leaves.count()
                context['roles']=roles.count()
                return render(request, 'ems/dashboard.html', context)               
        else:
            messages.warning(request,'Please Login!')
            return redirect('home:login')
    except Exception as e:
        print('EMS Dashboard Exception : ',e)
        messages.warning(request,'Somthing Went Wrong! Please Try after some time')
    return redirect('/')

def profile(request):
    context={}
    try:
        if request.user.is_authenticated:
            if not request.user.is_superuser:
                try:
                    events=Events.objects.exclude(is_completed=True).order_by('-id')[:10] 
                    profile=Employee.objects.get(user=request.user)
                    address=Address.objects.get(user=request.user)
                    dob=str(profile.dob).split('-')
                    now=datetime.now()
                    day=now.day
                    month=now.month
                    year=now.year
                    dob_day=int(dob[2])
                    dob_month=int(dob[1])
                    dob_year=int(dob[0])
                    name=str(profile.name).split(' ')
                    if dob_month == month and dob_day == day:
                        print('Happy Birthday to ',profile.name)
                        context['birthday']=True
                        context['name']=name[0]
                    else:
                        context['birthday']=False

                    # Getting Anniversary of Employee
                    joining_date=str(profile.joining_date).split('-')    
                    j_day=int(joining_date[2])
                    j_month=int(joining_date[1])
                    j_year=int(joining_date[0])
                    
                    completed_yers=year-j_year
                    if j_day == day and j_month == month and completed_yers >0:
                        print(completed_yers)
                        anniversary={
                            'name':name[0],
                            'completed_years':completed_yers
                        }
                        context['anniversary']=anniversary
                                                                     
                    context['profile']=profile
                    context['address']=address
                    context['events']=events
                except Exception as e:
                    print('Profile Inside Exception : ',e)
                    messages.warning(request, 'Profile Not found Please contact Admin')
                    return redirect('ems:ems')

                return render(request,'ems/profile.html',context)
            else:
                return redirect('ems:ems')
        else:
            messages.warning(request,'Please Login!')
            return redirect('home:login')
    except Exception as e:
        print('Profile Exception : ',e)
    return redirect('/')

@login_required()
def editProfile(request):
    context={}
    try:
        if not request.user.is_superuser:
            profile_obj=Employee.objects.get(user=request.user)
            context['profile']=profile_obj
            emp_obj=Employee.objects.get(user=request.user)
            address_obj=Address.objects.get(user=request.user)
            context['employee']=emp_obj
            context['address']=address_obj
            if request.method == 'POST':
                
                name=request.POST['name']
                father_name=request.POST['father-name']
                phone=request.POST['phone']
                ephone=request.POST['ephone']
                email=request.POST['email']
                dob=request.POST['dob']
                try:
                   avtar=request.FILES['profile-pic']
                   emp_obj.avtar=avtar
                except:
                    pass 
                emp_obj.name=name
                emp_obj.father_name=father_name
                emp_obj.mobile_no=phone
                emp_obj.emergency_mobile_no=ephone
                emp_obj.email=email
                emp_obj.dob=dob
                emp_obj.save()
                messages.success(request,'Updated Successfully')
                return redirect('ems:profile')
                
        else:
            return redirect('ems:ems') 
    except Exception as e:
        print('Edit Profile Exception : ',e)

    return render(request,'ems/edit_profile.html',context)
    
@login_required()
def createDepartment(request):
    context = {}
    if not request.user.is_superuser:
        profile_obj=Employee.objects.get(user=request.user)
        context['profile']=profile_obj
    if request.method == 'POST':
        department_name = request.POST['department-name']
        department_description = request.POST['department-description']

        text = str(department_name).upper()
        department_pool = Department.objects.all()
        for d in department_pool:
            loopstr = str(d).upper()
            if text == loopstr:
                messages.warning(request, 'This ' +
                                 department_name+' Department Already Exits')
                return redirect('ems:create-department')

        obj = Department.objects.create(
            name=department_name, description=department_description)
        messages.success(request, 'New Department created Successfully!')
        return redirect('ems:view-department')
    return render(request, 'ems/create_department.html', context)

@login_required()
def viewDepartment(request):
    context = {}
    try:
        if not request.user.is_superuser:
            profile_obj=Employee.objects.get(user=request.user)
            context['profile']=profile_obj
        departments = Department.objects.all()
        context['departments'] = departments
        if request.method=='POST':
            id=request.POST['id']
            name=request.POST['department-name']
            des=request.POST['department-description']
            obj=Department.objects.get(id=id)
            if obj.name !=name or obj.description !=des :
                obj.name=name
                obj.description=des
                obj.save()
                messages.success(request,'Updated successfully!')

    except Exception as e:
        print('View Department Exception : ', e)
    return render(request, 'ems/view_department.html', context)

@login_required()
def deleteDepartment(request, pk):
    try:
        Department.objects.get(id=pk).delete()
        messages.success(request, 'Department Deleted Successfully!')
        return redirect(reverse('ems:view-department'))
    except Exception as e:
        print('Delete Department Exception : ', e)

@login_required()
def createRole(request):
    context = {}
    if not request.user.is_superuser:
            profile_obj=Employee.objects.get(user=request.user)
            context['profile']=profile_obj
    if request.method == 'POST':
        role_name = request.POST['role-name']
        role_description = request.POST['role-description']
        text = str(role_name).upper()
        role_pool = Role.objects.all()
        for r in role_pool:
            item = str(r).upper()
            if text == item:
                messages.warning(request, 'This '+role_name +
                                 ' Role Already Exits')
                return redirect('ems:create-role')

        obj = Role.objects.create(name=role_name, description=role_description)
        print(obj)
        messages.success(request, 'Created New Role Successfully!')
        return redirect('ems:view-role')
    return render(request, 'ems/create_role.html', context)

@login_required()
def viewRole(request):
    context = {}
    try:
        if not request.user.is_superuser:
            profile_obj=Employee.objects.get(user=request.user)
            context['profile']=profile_obj
        roles = Role.objects.all()
        context['roles'] = roles
        if request.method=='POST':
            id=request.POST['id']
            name=request.POST['role-name']
            des=request.POST['role-description']
            obj=Role.objects.get(id=id)
            if obj.name !=name or obj.description !=des :
                obj.name=name
                obj.description=des
                obj.save()
                messages.success(request,'Updated successfully!')
    except Exception as e:
        print('View Role Exception : ', e)
    return render(request, 'ems/view_role.html', context)

@login_required()
def deleteRole(request, pk):
    try:
        Role.objects.get(id=pk).delete()
        messages.success(request, 'Role Deleted Successfully!')
        return redirect(reverse('ems:view-role'))
    except Exception as e:
        print('Delete Role Exception : ', e)

@login_required()
def addEmployee(request):
    context = {}
    try:
        if not request.user.is_superuser:
            profile_obj=Employee.objects.get(user=request.user)
            context['profile']=profile_obj
        users = User.objects.filter(~Q(is_superuser=True))
        new_users=list()
        
        # checking employee is created of users
        for u in users:
            obj=Employee.objects.filter(user=u).exists()
            if not obj:
                new_users.append(u)
                
        roles = Role.objects.all()
        departments = Department.objects.all()
        context['users'] = new_users
        context['roles'] = roles
        context['departments'] = departments

        if request.method == 'POST':
            user = request.POST['select-user']
            full_name = request.POST['employee-name']
            father_name = request.POST['father-name']
            dob = request.POST['employee-dob']
            phone_number = request.POST['phone-number']
            ephone_number= request.POST['ephone-number']
            email = request.POST['email']
            address = request.POST['address']
            street = request.POST['street']
            locality = request.POST['locality']
            city = request.POST['city']
            state = request.POST['state']
            pincode = request.POST['pincode']
            country = request.POST['country']
            designation = request.POST['designation']
            department = request.POST['select-department']
            role = request.POST['select-role']
            joining_date = request.POST['joining-date']
            

            if user and full_name and father_name and dob and email and phone_number and address and street and locality and city and state and pincode and country and designation and department and role and joining_date:
                if user and role and department == 'default':
                    messages.warning(request, '*All fields are Mandatory')
                    return redirect('ems:employee-add')

                user_obj = User.objects.get(username=user)
                check_employee = Employee.objects.filter(
                    user=user_obj).exists()
                print('user obj ',user_obj)
                if check_employee:
                    messages.warning(
                        request, 'This user already in use Please Create new user!')
                    return redirect('ems:employee-add')

                check_address = Address.objects.filter(user=user_obj).exists()
                if check_address:
                    address_obj = Address.objects.get(user=user_obj)
                else:
                    address_obj = Address.objects.create(
                        user=user_obj,
                        address=address,
                        street=street,
                        locality=locality,
                        city=city,
                        state=state,
                        pincode=pincode,
                        country=country
                    )

                print('Address Obj : ', address_obj)
                d_obj = Department.objects.get(name=department)
                print('Department Obj', d_obj)
                role_obj = Role.objects.get(name=role)
                print('Role Obj', role_obj)

                emp_obj = Employee.objects.create(
                    user=user_obj,
                    name=full_name,
                    father_name=father_name,
                    dob=dob,
                    email=email,
                    mobile_no=phone_number,
                   emergency_mobile_no=ephone_number,
                    address=address_obj,
                    designation=designation,
                    role=role_obj,
                    department=d_obj,
                    joining_date=joining_date,
                    status='Working'
                )
                print('Employee Obj : ', emp_obj)
                messages.success(
                    request, 'New Employee Reigsterd Successfully!')
                return redirect('ems:employee-view')
            else:
                print('fail')
                messages.warning(request, 'All fields are mandouttimery')

    except Exception as e:
        print('Add Employee Exception : ', e)
    return render(request, 'ems/add_employee.html', context)

@login_required()
def viewEmployee(request):
    context = {}
    try:
        if not request.user.is_superuser:
            profile_obj=Employee.objects.get(user=request.user)
            context['profile']=profile_obj
        employees = Employee.objects.all().order_by('-empid')
        paginator=Paginator(employees,2)
        page_no=request.GET.get('page')

        total_pages=paginator.page_range
        employeepages=paginator.get_page(page_no) 
        context['pages']=total_pages
        context['employees'] = employeepages
    except Exception as e:
        print('View Employee Exception : ', e)

    return render(request, 'ems/view_employee.html', context)

@login_required()
def employeeDetail(request, empid):
    context = {}
    try:
        if not request.user.is_superuser:
            profile_obj=Employee.objects.get(user=request.user)
            context['profile']=profile_obj
        employee_obj = Employee.objects.get(empid=empid)
        user_obj = User.objects.get(username=employee_obj.user)
        department_obj = Department.objects.all()
        role_obj = Role.objects.all()
        context['departments'] = department_obj
        context['roles'] = role_obj
        context['employee_obj'] = employee_obj
        addres_obj = Address.objects.get(user=user_obj)
        context['address_obj'] = addres_obj

        if request.method == 'POST':
            full_name = request.POST['employee-name']
            father_name = request.POST['father-name']
            dob = request.POST['employee-dob']
            phone_number = request.POST['phone-number']
            ephone_number= request.POST['ephone-number']
            print('ephone ',ephone_number)
            email = request.POST['email']
            address = request.POST['address']
            street = request.POST['street']
            locality = request.POST['locality']
            city = request.POST['city']
            state = request.POST['state']
            pincode = request.POST['pincode']
            country = request.POST['country']
            designation = request.POST['designation']
            department = request.POST['select-department']
            role = request.POST['select-role']
            joining_date = request.POST['joining-date']
            status = request.POST['select-status']

            if full_name and father_name and dob and email and phone_number and address and street and locality and city and state and pincode and country and designation and department and role and joining_date and status:
                
                d_obj = Department.objects.get(name=department)
                if ephone_number == '':
                    employee_obj.emergency_mobile_no=None
                else:
                    employee_obj.emergency_mobile_no=ephone_number
                    
                r_obj = Role.objects.get(name=role)
                employee_obj.name = full_name
                employee_obj.father_name = father_name
                employee_obj.dob = dob
                employee_obj.email = email
                employee_obj.mobile_no = phone_number
                
                employee_obj.role = r_obj
                employee_obj.department = d_obj
                employee_obj.designation = designation
                employee_obj.joining_date = joining_date
                employee_obj.status = status
                employee_obj.save()

                addres_obj.address = address
                addres_obj.street = street
                addres_obj.locality = locality
                addres_obj.city = city
                addres_obj.state = state
                addres_obj.pincode = pincode
                addres_obj.country = country
                addres_obj.save()
                messages.success(request, 'Updated successfully!')
                return redirect('ems:employee-view')
            else:
                messages.warning(request, '*All Fields are complasary!')

    except Exception as e:
        print('Employee Detail Exception : ', e)
    return render(request, 'ems/employee_detail.html', context)
@login_required()
def deleteEmployee(request, empid):
    try:
        Employee.objects.get(empid=empid).delete()
        messages.success(request, 'Employee Deleted Successfully!')
        return redirect(reverse('ems:employee-view'))
    except Exception as e:
        print('Delete Employee Exception : ', e)
        messages.warning(request,'Something Went Wrong!')
    return redirect('ems:employee-view')

@login_required()
def attendance(request):
    context={}
    try:
        if not request.user.is_superuser:
            profile_obj=Employee.objects.get(user=request.user)
            context['profile']=profile_obj
        em_list=list()
        attendance_dates=list()
        nested_attendance=list()
        employees=Employee.objects.all()
        attendances_objs=Attendance.objects.all().order_by('-date')

        # Getting All Attendance Dates
        for attend in attendances_objs:
            if attend.date in attendance_dates:
                pass
            else:
                attendance_dates.append(attend.date)
     
         
        # Getting Particular Date QuerySets        
        for i in attendance_dates:
            obj=Attendance.objects.filter(date=i).order_by('date')
            nested_attendance.append(obj)
            
        
        # Getting working Employee for make attendance
        for item in employees:
            if item.status == 'Working':
                em_list.append(item)
                
        paginator=Paginator(nested_attendance,2)
        page_no=request.GET.get('page')

        total_pages=paginator.page_range
        nested_attendance_pages=paginator.get_page(page_no) 
        context['pages']=total_pages

        context['employees']=em_list
        context['nested_attendence']=nested_attendance_pages
       
        if request.method == 'POST':
            date=request.POST['date']
            print(date)
            for i in range(1,len(em_list)+1):
                empid=request.POST['empid'+str(i)]
                intime=request.POST['intime'+str(i)]
                outtime=request.POST['outtime'+str(i)]
                attendance_status=request.POST['attendance-status'+str(i)]
                if intime == '':
                    intime=None
                    
                if outtime == '':
                    outtime=None
                    
                emp_obj=Employee.objects.get(empid=empid)
                att_obj=Attendance.objects.create(
                    employee=emp_obj,
                    intime=intime,
                    outtime=outtime,
                    date=date,
                    present=attendance_status
                    )
                print(att_obj)
                print(i,'empid-',empid,'intime-',intime,'outime-',outtime,'present-',attendance_status)
            messages.success(request,'Attendance Added successfully!')
            return redirect('ems:attendance')
    except Exception as e:
        print('Attendance Exception ',e)
        
    return render(request,'ems/attendance.html',context)

@login_required()
def editAttendance(request):
    try:
        if request.method == 'POST':
            id=request.POST['attendance-id']
            intime=request.POST['intime']
            outtime=request.POST['outtime']
            date=request.POST['date']
            attendence_status=request.POST['attendance-status']

            obj=Attendance.objects.get(id=id)
            if intime and outtime != '':
                obj.intime=intime
                obj.outtime=outtime
            elif not intime == '':
                obj.intime=intime
            elif not outtime == '':
                obj.outtime=outtime
            if attendence_status == 'False':
                obj.intime=None
                obj.outtime=None     
                           
            obj.present=attendence_status
            obj.date=date
            obj.save()
            
            messages.success(request,'Updated Successfully!')
            return redirect('ems:attendance')

    except Exception as e:
        print('Edit Attendance Exception : ',e)
        messages.warning(request,"Please don't Change Date Time Format")
    return redirect('ems:attendance')
    
@login_required()
def deleteAttendance(request, pk):
    try:
        Attendance.objects.get(id=pk).delete()
        messages.success(request, 'Deleted Successfully!')
        return redirect(reverse('ems:attendance'))
    except Exception as e:
        print('Delete Attendance Exception : ', e)
        messages.warning(request,'Something Wend Wrong!')
        return redirect('ems:attendance')
    
@login_required()
def allAttendances(request):
    context={}
    try:
        if not request.user.is_superuser:
            profile_obj=Employee.objects.get(user=request.user)
            context['profile']=profile_obj
            emp_obj=Employee.objects.get(user=request.user)
            attendances=Attendance.objects.filter(employee=emp_obj).order_by('-date')
            paginator=Paginator(attendances,2)
            page_no=request.GET.get('page')

            total_pages=paginator.page_range
            finalattendances=paginator.get_page(page_no) 
            context['attendances']=finalattendances
            context['pages']=total_pages
        else:
            return redirect('ems:ems')

    except Exception as e:
        print('All Attendance of Employee Execption : ',e)
    
    return render(request,'ems/all_attendances.html',context)
    
# Leave Functions 
@login_required()
def createLeave(request):
    context={}
    try:
        if not request.user.is_superuser:
            profile_obj=Employee.objects.get(user=request.user)
            context['profile']=profile_obj
            
        em_obj=Employee.objects.get(user=request.user)
        leaves=Leave.objects.filter(employee=em_obj).order_by('-id')
        context['leaves']=leaves
        if request.method == 'POST':
            date_from=request.POST['date-from']
            date_to=request.POST['date-to']
            type=request.POST['type']
            description=request.POST['description']
           
            obj=Leave.objects.create(
                employee=em_obj,
                date_from=date_from,
                date_to=date_to,
                type=type,
                description=description,
                status='Pending',
            )
            if obj:
                messages.success(request,'Requested Successfully!')           
                return redirect('ems:all-leaves')
            else:
                messages.warning(request,'Something Went Wrong!')
                return redirect('ems:leave-create')
    except Exception as e:
        print('Create Leave Exception : ',e)
    return render(request,'ems/create_leave.html',context)

@login_required()
def deleteLeave(request, pk):
    try:
        # Leave.objects.get(id=pk).delete()
        messages.success(request, 'Deleted Leave Not Allwed!')
        return redirect(reverse('ems:all-leaves'))
    except Exception as e:
        print('Delete Attendance Exception : ', e)
        messages.warning(request,'Something Wend Wrong!')
        return redirect('ems:all-leaves')
    
@login_required()    
def dashboardLeaves(request):
    context={}
    try:
        if not request.user.is_superuser:
            profile_obj=Employee.objects.get(user=request.user)
            context['profile']=profile_obj
            
        leaves=Leave.objects.all().order_by('-id')
        paginator=Paginator(leaves,2)
        page_no=request.GET.get('page')

        total_pages=paginator.page_range
        leavespages=paginator.get_page(page_no) 
        context['leaves']=leavespages
        context['pages']=total_pages
    
        if request.method == 'POST':
            status=request.POST['status']
            reply=request.POST['reply']
            id=request.POST['id']
            obj=Leave.objects.get(id=id)
            obj.status=status
            obj.reply=reply
            obj.save()
            messages.success(request,'Status Updated successfully!')
            return redirect('ems:dashboard-leaves')
    except Exception as e:
        print('Dashboard Leaves Exception : ',e)
    return render(request,'ems/dashboard_leaves.html',context)

def allLeaves(request):
    context={}
    try:
        if not request.user.is_superuser:
            profile_obj=Employee.objects.get(user=request.user)
            context['profile']=profile_obj
            emp_obj=Employee.objects.get(user=request.user)
            leaves=Leave.objects.filter(employee=emp_obj).order_by('-id')
            paginator=Paginator(leaves,2)
            page_no=request.GET.get('page')

            total_pages=paginator.page_range
            leavespages=paginator.get_page(page_no) 
            context['leaves']=leavespages
            context['pages']=total_pages
        else:
            return redirect('ems:ems')
    except Exception as e:
        print('All leaves Exception : ',e)
        
    return render(request,'ems/all_leaves.html',context)
@login_required()    
def createEvent(request):
    context={}
    try:
        if request.method == 'POST':
            title=request.POST['title']
            description=request.POST['description']
            date=request.POST['date']
            obj=Events.objects.create(title=title,description=description, date=date)
            print(obj)                          
            if obj:
                messages.success(request,'Created Successfully!')
                return redirect('ems:view-events')
            else:
                messages.warning(request,'Somthing went Wrong! Please Try Again.')
    except Exception as e:
        print('Create Event Execption : ',e)
    return render(request,'ems/create_event.html',context)

@login_required()
def viewEvents(request):
    context={}
    try:
        events=Events.objects.all().order_by("-date")
        paginator=Paginator(events,2)
        page_no=request.GET.get('page')

        total_pages=paginator.page_range
        eventespages=paginator.get_page(page_no) 
        context['events']=eventespages
        context['pages']=total_pages
        if request.method =='POST':
            id=request.POST['id']
            title=request.POST['title']
            description=request.POST['description']
            date=request.POST['date']
            try:
                is_completed=request.POST['completed']
            except Exception as e:
                is_completed=False
                print('Is_complete input Exception : ',e)

            event_obj=Events.objects.get(id=id)
            
            if event_obj.title != title or event_obj.description != description or event_obj.date != date or event_obj.is_completed != is_completed:
                event_obj.title=title
                event_obj.description=description
                event_obj.date=date
                event_obj.is_completed=is_completed 
                event_obj.save()
                messages.success(request,'Updated Successfully!')
                
            return redirect('ems:view-events')
    except Exception as e:
        print('Display Events Exception : ',e)
    
    return render(request,'ems/view_events.html',context)

def deleteEvent(request,id):
    try:
        Events.objects.get(id=id).delete()
        messages.success(request,'Deleted Successfully!')
        
    except Exception as e:
        print('Delete Event Exception : ',e)
        messages.warning(request,'Something went wrong!')
    
    return redirect('ems:view-events')

def event(request,id):
    context={}
    try:
        print('know event')
        event=Events.objects.get(id=id)
        context['event']=event
    except Exception as e:
        print('Events Exception : ',e)
        
    return render(request,'ems/event.html',context)