import os
from .utils import *
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
from django.contrib.sites.models import Site
import zipfile
from io import StringIO




def dashboard(request):
    context={}
    try:
        expireConnect()
        reassignAllocatedLeave()
        AllocatedLeaveOperation()
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
                if i.joining_date:
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
                emp_obj=Employee.objects.filter(user=request.user).exists()
                if not emp_obj:
                    messages.info(request,'Please check Your Email!')
                    return redirect('/')
                else:
                    profile_obj=Employee.objects.get(user=request.user)
                    context['profile']=profile_obj
                    events=Events.objects.all().order_by('-id')
                    context['events']=events
                    sub_connects=Connect.objects.filter(employee=profile_obj).order_by('-id')
                    connects=sub_connects.filter(is_completed=False)
                    context['appreciations']=Appreciation.objects.all()
                    context['newsletters']=NewsLetter.objects.all()
                    context['connects']=connects
                    return render(request,'ems/ems_home.html',context)
            else:
                departments=Department.objects.all()
                roles=Role.objects.all()
                employees=Employee.objects.all()
                leaves=Leave.objects.filter(status='Pending')
                context['filter_leaves']=filterLeave()
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
                    if profile.joining_date != '':
                        print('inside annivarsary')
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
                    else:
                        messages.warning(request,'Please Add Joining Date!')
                    
                                                                     
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
                address=request.POST['address']
                street=request.POST['street']
                locality=request.POST['locality']
                city=request.POST['city']
                state=request.POST['state']
                pincode=request.POST['pincode']
                country=request.POST['country']

                try:
                   avtar=request.FILES['profile-pic']
                   emp_obj.avtar=avtar                   
                except:
                    pass 
                
                try:
                    document=request.FILES['document']
                    emp_obj.document=document
                except:
                    pass
                
                emp_obj.name=name
                emp_obj.father_name=father_name
                emp_obj.mobile_no=phone
                if ephone != '':
                    emp_obj.emergency_mobile_no=ephone
                emp_obj.email=email
                emp_obj.dob=dob
                emp_obj.save()
                
                address_obj.address=address
                address_obj.street=street
                address_obj.locality=locality
                address_obj.pincode=pincode
                address_obj.city=city
                address_obj.state=state
                address_obj.country=country
                address_obj.save()
                messages.success(request,'Updated Successfully')
                return redirect('ems:profile')
                
        else:
            return redirect('ems:ems') 
    except Exception as e:
        print('Edit Profile Exception : ',e)

    return render(request,'ems/edit_profile.html',context)

@login_required()
def changePassword(request):
    new_password=request.POST['new-password']
    confirm_password=request.POST['confirm-password']
    user=User.objects.get(username=request.user.username)
    if new_password ==  confirm_password:
        user.set_password(new_password)
        user.save()
        messages.success(request,'Passowrd Updated Successfully!')
    else:
        messages.warning(request,'Both Passowrd should Match!')
        
    return redirect('ems:profile')
    
@login_required()
def newUsers(request):
    if request.user.is_superuser:
        context={}
        try:
            newusers=Newuser.objects.filter(completed=False)
            context['newusers']=newusers
        except Exception as e:
            print("New Users Exception : ",e)
        return render(request,'ems/new_users.html',context)
    else:
        messages.warning(request,"You don't have Permissions!")
        return redirect("ems:ems")

@login_required()
def sendVerificationMail(request,username):
    if request.user.is_superuser:
        context={}
        try:
            current_site = Site.objects.get_current()
            print("current site domain ",current_site)
            print(current_site.domain)
            domain=request.get_host()
            print('Host : ',request.get_host())
            
            res=sendMail(username,domain)
            if res == True:
                messages.success(request,'Email Sended Successfully!')
        except Exception as e:
            print("Send Verification Mail Exception : ",e)
        return redirect('ems:new-users')
    else:
        messages.warning(request,"You don't have Permissions!")
        return redirect("ems:ems")

def verifyLink(request,token):
    try:
        obj=Newuser.objects.filter(token=token).exists()
        
        if obj:
            new_obj=Newuser.objects.get(token=token)
            print(new_obj)
            messages.info(request,'Please Add your Personal Info!')
            return redirect('ems:add-employee',token)
        else:
            messages.warning(request,'This Link has been Expired!')
            return redirect('home:login')

    except Exception as e:
        print('Verify Link Exception : ',e)

@login_required()
def documents(request):
    context={}
    try:
        if not request.user.is_superuser:
            document_limit_exceed=False
            profile_obj=Employee.objects.get(user=request.user)
            context['profile']=profile_obj
            number_of_documents=Document.objects.filter(employee=profile_obj)
            context['documents']=number_of_documents
            if number_of_documents.count() == 10:
                document_limit_exceed=True
                context['document_limit_exceed']=document_limit_exceed

            if request.method == "POST":
                if number_of_documents.count() == 10:
                    messages.warning(request,"You can't Add More than 10 Documents!")
                    return redirect('ems:documents')

                document_name=request.POST['document-name']
                try:
                    document=request.FILES['document']
                except:
                    document=None
                employee=Employee.objects.get(user=request.user)
                obj=Document.objects.create(employee=employee,name=document_name,document=document)
                if obj:
                    messages.success(request,'Document Added Successfully!')
                    return redirect('ems:documents')
        else:
            messages.warning(request,"You don't have access of this page!")
            return redirect('/')

    except Exception as e:
        print("Document Exception : ",e)
    return render(request,'ems/documents.html',context)

@login_required()
def deleteDocument(request,id):
    if not request.user.is_superuser:
        employee=Employee.objects.get(user=request.user)
        obj=Document.objects.get(id=id)
        if obj.employee == employee:
            res=obj.delete()
            if res:
                messages.success(request,"Document Deleted Successfully!")
            return redirect('ems:documents')
        else:
            messages.warning(request,'Something Went Wrong!')
            return redirect('/')
    else:
        messages.warning(request,"You don't have access!")
        return redirect('/')

@login_required()
def adminDocument(request,empid):
    context={}
    try:
        employee=Employee.objects.get(empid=empid)
        documents=Document.objects.filter(employee=employee)
        context['documents']=documents
        context['employee']=employee

    except Exception as e:
        print('Admin Document Exception : ',e)
    return render(request,'ems/admin_document.html',context)



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
                messages.warning(request, 'This '+role_name + ' Role Already Exits')
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


def addEmployee(request,token):
    context = {}
    try:
        newuser_check=Newuser.objects.filter(token=token).exists()
        if newuser_check:
            newuser_obj=Newuser.objects.get(token=token)
            context['user']=newuser_obj.user
        else:
            messages.warning(request,'Invaild Link!')
            return redirect('home:login')
        
        print('New user in Add Employee',newuser_obj.user)
        print(type(newuser_obj.user))
        if request.method == 'POST':
            print('Post Method add Employee')
            user = newuser_obj.user
            full_name = newuser_obj.user.get_full_name()
            father_name = request.POST['father-name']
            mother_name = request.POST['mother-name']
            dob = request.POST['employee-dob']
            phone_number = request.POST['phone-number']
            ephone_number= request.POST['ephone-number']
            email = newuser_obj.user.email
            address = request.POST['address']
            street = request.POST['street']
            locality = request.POST['locality']
            city = request.POST['city']
            state = request.POST['state']
            pincode = request.POST['pincode']
            country = request.POST['country']
            joining_date=request.POST['joining-date']
            
            if ephone_number == '':
                ephone_number=None

            if father_name and dob  and phone_number and address and street and locality and city and state and pincode and country and joining_date:

                check_employee = Employee.objects.filter(
                    user=user).exists()
                
                if check_employee:
                    messages.warning(
                        request, 'You have Already added personal Informatin!')
                    return redirect('ems:ems')

                check_address = Address.objects.filter(user=user).exists()
                
                if check_address:
                    address_obj = Address.objects.get(user=user)
                else:
                    address_obj = Address.objects.create(
                        user=user,
                        address=address,
                        street=street,
                        locality=locality,
                        city=city,
                        state=state,
                        pincode=pincode,
                        country=country
                    )

                print('Address Obj : ', address_obj)
                

                emp_obj = Employee.objects.create(
                    user=user,
                    name=full_name,
                    father_name=father_name,
                    mother_name=mother_name,
                    dob=dob,
                    email=email,
                    mobile_no=phone_number,
                    emergency_mobile_no=ephone_number,
                    address=address_obj,
                    joining_date=joining_date,
                    status='Working'
                )
                print('Employee Obj : ', emp_obj)
                if emp_obj:
                    newuser_obj.completed=True
                    newuser_obj.token=generateToken()
                    newuser_obj.save()
                    messages.success(request, 'Added Successfully!')
                    return redirect('ems:profile')
                else:
                    messages.warning(request,'Something Went Wrong!')
                    
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
        paginator=Paginator(employees,10)
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
            employeeid = request.POST['employeeid']
            
            if department == 'None':
                messages.warning(request,'*Please Select Department!')
                return redirect('ems:employee-detail',employee_obj.empid)
            elif role == 'None':
                messages.warning(request,'*Please Select Role!')
                return redirect('ems:employee-detail',employee_obj.empid)
            

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
                
                if employeeid == '':
                    messages.warning(request,'Please Enter Employee Id!')
                    return redirect('ems:employee-detail',employee_obj.empid)
                else:
                    check_employeeid=Employee.objects.filter(employeeid=employeeid).exists()
                    
                    if check_employeeid:
                        if employee_obj.employeeid != int(employeeid):
                            messages.warning(request,'This Employee Id Already Exits! Please Try Another')
                            return redirect('ems:employee-detail',employee_obj.empid)
                    else:
                        employee_obj.employeeid=employeeid
                        employee_obj.save()

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
        departments=Department.objects.all()
        attendances_objs=Attendance.objects.all().order_by('-date')
        attendances_objs.order_by('employee')

        # Getting All Attendance Dates
        for attend in attendances_objs:
            if attend.date in attendance_dates:
                pass
            else:
                attendance_dates.append(attend.date)
     
         
        # Getting Particular Date QuerySets        
        for i in attendance_dates:
            obj=Attendance.objects.filter(date=i).order_by('employee')
            nested_attendance.append(obj)

        
        # Getting working Employee for make attendance
        for item in employees:
            if item.status == 'Working':
                em_list.append(item)
                
        paginator=Paginator(nested_attendance,4)
        page_no=request.GET.get('page')

        total_pages=paginator.page_range
        nested_attendance_pages=paginator.get_page(page_no) 
        context['pages']=total_pages

        context['employees']=em_list
        context['departments']=departments
        context['filter_employees']=employees
        context['nested_attendence']=nested_attendance_pages
       
        if request.method == 'POST':
            date=request.POST['date']
            length=request.POST['number_of_length']
            print('THis is test ', length)
            print(date)
            for i in range(1,int(length)+1):
                print('attendance Iteration ',i)
                is_late=False
                empid=request.POST['empid'+str(i)]
                intime=request.POST['intime'+str(i)]
                outtime=request.POST['outtime'+str(i)]
                attendance_status=request.POST['attendance-status'+str(i)]
                if intime == '':
                    intime=None
                else:
                    split_intime=str(intime).split(":")
                    intime_hour=int(split_intime[0])
                    intime_minute=int(split_intime[1])
                    if intime_hour == 9:
                        if intime_minute >45:
                            is_late=True
                        elif intime_hour >9:
                            is_late=True

                if outtime == '':
                    outtime=None
                

              
                     
                emp_obj=Employee.objects.get(empid=empid)
                att_obj=Attendance.objects.create(
                    employee=emp_obj,
                    intime=intime,
                    outtime=outtime,
                    date=date,
                    present=attendance_status,
                    is_late=is_late
                    )
                print('Attendance Object ',att_obj)    
                

            messages.success(request,'Attendance Added successfully!')
            return redirect('ems:attendance')        
    except Exception as e:
        print('Attendance Exception ',e)
        
    return render(request,'ems/attendance.html',context)

# Department filter for adding attending. 

@login_required()
def addAttendanceFilter(request):
    context={}
    try:
        if request.method == 'POST':
            try:
                department=request.POST['department']
            except:
                department=''

            try:
                employee=request.POST['employee']
            except:
                employee=''

            if department != '':
                department_obj=Department.objects.get(id=department)
                employees=Employee.objects.filter(department=department_obj)
                print("Department Employee : ",employees)
                context['employees']=employees
                context['department']=True

            else:
                employee_obj=Employee.objects.get(empid=employee)
                context['employee']=employee_obj
                context['department']=False
                print('Filter Employee')

    except Exception as e:
        print('Add Attendance Department Filter Exception : ',e)
    return render(request,'ems/add_attendance_filter.html',context)

@login_required()
def attendanceDateFilter(request):
    context={}
    try:
        filter_date=request.GET['filter-date']
        print('filter date ',filter_date)
        attendances=Attendance.objects.filter(date=filter_date).order_by('employee')
        context['attendances']=attendances
        context['date']=True
    except Exception as e:
        print('Filter Attendace Exception : ',e)
    return render(request,'ems/filter_attendate.html',context)

@login_required()
def attendanceDepartmentFilter(request):
    context={}
    try:
        filter_department=request.POST['filter-department']
        obj=Department.objects.get(id=filter_department)
        employees=Employee.objects.filter(department=obj)
        attendances=[]
        for item in employees:
            item_obj=Attendance.objects.filter(employee=item)
            for i in item_obj:
                attendances.append(i)
                
        context['attendances']=attendances
        context['department']=obj
        print(attendances)
    except Exception as e:
        print('Filter Attendace Exception : ',e)
    return render(request,'ems/filter_attendate.html',context)

@login_required()
def attendanceEmployeeFilter(request):
    context={}
    try:
        empid=request.POST['empid']
        obj=Employee.objects.get(empid=empid)
        attendances=Attendance.objects.filter(employee=obj).order_by('-date')
        context['attendances']=attendances
        context['employee']=obj
    except Exception as e:
        print('Attendace Employee Filter Exception : ',e)
    return render(request,'ems/filter_attendate.html',context)

@login_required()
def editAttendance(request):
    try:
        if request.method == 'POST':
            is_late=request.POST['is-late']
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
            obj.is_late=is_late
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
            paginator=Paginator(attendances,10)
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
            try:
                allocated_leaves=AllocatedLeave.objects.get(employee=profile_obj)
                print('Allocated Leaves',allocated_leaves)
            except Exception as e:
                print("Create Leave inside Exception : ",e)
                allocated_leaves=''
            
            context['allocated_leaves']=allocated_leaves    
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
        paginator=Paginator(leaves,10)
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
def allocatedLeave(request):
    context={}
    if request.user.is_superuser:
        try:
            employees=Employee.objects.all()
            allocated_leaves=AllocatedLeave.objects.all()
            
            paginator=Paginator(allocated_leaves,10)
            page_no=request.GET.get('page')

            total_pages=paginator.page_range
            allocatedleavespages=paginator.get_page(page_no) 
            context['allocated_leaves']=allocatedleavespages
            context['pages']=total_pages
            context['employees']=employees
            if request.method == 'POST':
                empid=request.POST['empid']
                start_date=request.POST['start-date']
                end_date=request.POST['end-date']
                earn=request.POST['earn']
                employee_obj=Employee.objects.get(empid=empid)
                check=AllocatedLeave.objects.filter(employee=employee_obj).exists()
                if check:
                    messages.warning(request,'This Employee has Already Allocated Leaves! Please try another.')
                    return redirect('allocated-leaves')
                obj=AllocatedLeave.objects.create(
                    employee=employee_obj,
                    start_date=start_date,
                    end_date=end_date,
                    earn=earn
                )
                print(obj)
                if obj:
                    messages.success(request,'Added Successfully!')
                    return redirect('ems:allocated-leaves')
                else:
                    messages.warning(request,'Something went wrong! Please try Again')
                    return redirect('ems:allocated-leaves')

        except Exception as e:
            print('Allocated Leave Exception : ',e)
        return render(request,'ems/allocated_leave.html',context)
    else:
        messages.warning(request,"You don't have access!")
        return redirect('ems:ems')

@login_required()
def editAllocatedLeave(request):
    try:
        if request.method == 'POST':
            id=request.POST['id']
            leaves=int(request.POST['leaves'])
            earn=int(request.POST['earn'])
            obj=AllocatedLeave.objects.get(id=id)
            obj.allocated=leaves
            obj.earn=earn
            obj.save()
            messages.success(request,'Updated Successfully!')
            return redirect('ems:allocated-leaves')
    except Exception as e:
        print("Edit Allocated Leave Exception : ",e)
        messages.warning(request,'Something went wrong!')
        return redirect('ems:allocated-leaves')

@login_required()
def deleteAllocatedLeave(request,id):
    obj=AllocatedLeave.objects.get(id=id).delete()
    if obj:
        messages.success(request,'Deleted Successfully!')
    else:
        messages.warning(request,'Something went wrong!')
        
    return redirect('ems:allocated-leaves')
    

@login_required()    
def createEvent(request):
    context={}
    try:
        if request.method == 'POST':
            title=request.POST['title']
            description=request.POST['description']
            date=request.POST['date']
            try:
                image=request.FILES['image']
            except:
                image=''

            obj=Events.objects.create(title=title,description=description, date=date,image=image)
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
        events=Events.objects.all().order_by("-id")
        paginator=Paginator(events,10)
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
                image=request.FILES['image']
                
            except Exception as e:
                image=None
                print('check image update of event update Exception E: ',e)
            
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
                if image is not None:
                    event_obj.image=image
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

@login_required()
def event(request,id):
    context={}
    try:
        if not request.user.is_superuser:
            profile_obj=Employee.objects.get(user=request.user)
            context['profile']=profile_obj
            
        event=Events.objects.get(id=id)
        context['event']=event
    except Exception as e:
        print('Events Exception : ',e)
        
    return render(request,'ems/event.html',context)

@login_required()
def createPayRoll(request):
    context={}
    if request.user.is_superuser:
        try:
            context['employees']=Employee.objects.all()
            if request.method == "POST":
                empid=request.POST['empid']
                month=request.POST['month']
                pay_slip=request.FILES['pay-slip']
                print(empid)
                print(month)
                print(pay_slip)
                emp_obj=Employee.objects.get(empid=empid)
                obj=PayRoll.objects.create(
                    employee=emp_obj,
                    month=month,
                    payroll_slip=pay_slip
                )
                if obj:
                    messages.success(request,'Added Successfully!')
                    return redirect('ems:view-payrolls')
        except Exception as e:
            print("Add PayRoll Exception : ",e)
        return render(request,'ems/add_payroll.html',context)
    else:
        messages.warning(request,"You don't Have Access!")
        return redirect('ems:ems')



# Displaying All the PayRolls to the Admin
@login_required()
def viewPayRoll(request):
    context={}
    if request.user.is_superuser:
        try:
            payrolls=PayRoll.objects.all()
            paginator=Paginator(payrolls,2)
            page_no=request.GET.get('page')

            total_pages=paginator.page_range
            payrollspages=paginator.get_page(page_no) 
            context['payrolls']=payrollspages
            context['pages']=total_pages
        except Exception as e:
            print('View Pay Slip Exception : ',e)
        return render(request,'ems/view_pay_slip.html',context)
    else:
        messages.warning(request,"You don't Have Access!")
        return redirect('ems:ems')


# Delete PayRoll By Admin
@login_required()
def deletePayRoll(request,id):
    if request.user.is_superuser:
        try:
            PayRoll.objects.get(id=id).delete()
            messages.success(request,"Deleted Successfully!")

        except Exception as e:
            print('View Pay Slip Exception : ',e)
            messages.warning(request,"Something went Wrong! Please Try Again.")
        return redirect('ems:view-payrolls')
    else:
        messages.warning(request,"You don't Have Access!")
        return redirect('ems:ems')
    
# Displaying Payroll For Employee 
@login_required()    
def payRoll(request):
    context={}
    try:
        if not request.user.is_superuser:
            profile_obj=Employee.objects.get(user=request.user)
            context['profile']=profile_obj
            employee=Employee.objects.get(user=request.user)
            payrolls=PayRoll.objects.filter(employee=employee)
            context['payrolls']=payrolls
            
    except Exception as e:
        print('Payroll Exception : ',e)
    return render(request,'ems/payroll.html',context)
# Create New Query

@login_required()
def createQuery(request):
    context={}
    try:
        if not request.user.is_superuser:
            profile_obj=Employee.objects.get(user=request.user)
            context['profile']=profile_obj
            if profile_obj.role.name != 'Manager':
                departments=Department.objects.all()
                context['departments']=departments
                if request.method == 'POST':
                    department=request.POST['department']
                    subject=request.POST['subject']
                    description=request.POST['description']
                    department_obj=Department.objects.get(id=department)
                    emp_obj=Employee.objects.get(user=request.user)
                    id=generateId()
                    obj=DepartmentQuery.objects.create(
                        employee=emp_obj,
                        subject=subject,
                        department=department_obj,
                        description=description,
                        status='pending',
                        query_id=id
                    )
                    if obj:
                        messages.success(request,'Created Successfully!')
                        return redirect('ems:queries')
                    else:
                        messages.warning(request,'Something Went Wrong! Please try after some time!')
            else:
                messages.warning(request,'Manager Can not create Query!')
                return redirect('ems:ems')
        else:
            messages.warning(request,'Admin Can not create Query!')
            return redirect('ems:ems')
            
    except Exception as e:
        print('Create Query Exception : ',e)
        
    return render(request,'ems/create_query.html',context)

# Displaying All queries of Employee
@login_required()
def displayQuerys(request):
    context={}
    try:
        if not request.user.is_superuser:
            profile_obj=Employee.objects.get(user=request.user)
            context['profile']=profile_obj
        emp=Employee.objects.get(user=request.user)
        queries=DepartmentQuery.objects.filter(employee=emp).order_by('-id')
        print(queries)
        context['queries']=queries
    except Exception as e:
        print('Display Query Excepton : ',e)
        
    return render(request,'ems/display_query.html',context)

# Getting Particular Query Detail
@login_required()
def queryDetail(request,id):
    context={}
    try:
        if not request.user.is_superuser:
            profile_obj=Employee.objects.get(user=request.user)
            context['profile']=profile_obj
        query=DepartmentQuery.objects.get(query_id=id)
        comments=QueryComment.objects.filter(query=query).order_by('-id')
        context['query']=query
        context['comments']=comments
    except Exception as e:
        print('Query Detail Exception : ',e)
    return render(request,'ems/query_detail.html',context)

# Getting All the Queries For the Manager 
@login_required()
def quriesManger(request):
    context={}
    try:
        if not request.user.is_superuser:
            profile_obj=Employee.objects.get(user=request.user)
            context['profile']=profile_obj
            if profile_obj.role.name == 'Manager':
                queries=DepartmentQuery.objects.filter(department=profile_obj.department).order_by('-id')
                context['queries']=queries
                if request.method == 'POST':
                    query_id=request.POST['query-id']
                    status=request.POST['status']
                    query=DepartmentQuery.objects.get(query_id=query_id)
                    query.status=status
                    query.save()
                    messages.success(request,'Status Updated Successfully!')
                    return redirect('ems:all-queries')
            else:
                messages.warning(request,"You don't have Permission to access!")
                return redirect('ems:ems')
        else:
            queries=DepartmentQuery.objects.all().order_by('-id')
            context['queries']=queries
            
            if request.method == 'POST':
                query_id=request.POST['query-id']
                status=request.POST['status']
                query=DepartmentQuery.objects.get(query_id=query_id)
                query.status=status
                query.save()
                messages.success(request,'Status Updated Successfully!')
                return redirect('ems:all-queries')
    except Exception as e:
        print('Manager Queryes Exception : ',e)
    return render(request,'ems/all_queries.html',context)


@login_required()
def addComment(request):
    context={}
    try:
        if request.method == 'POST':
            comment=request.POST['comment']
            query_id=request.POST['query-id']
            query_obj=DepartmentQuery.objects.get(query_id=query_id)

            obj=QueryComment.objects.create(
                user=request.user,
                comment=comment,
                query=query_obj
            )
            if obj:
                messages.success(request,'Comment Added Successfully!')     
                return redirect('/ems/query/'+query_id)

    except Exception as e:
        print('Add Comment Exception : ',e)
        
    return HttpResponse('Go back to home')

@login_required()
def connect(request):
    context={}
    try:
        connects=Connect.objects.all().order_by('-id')
        expireConnect()
        employees=Employee.objects.all()
        context['employees']=employees
        context['connects']=connects
        
        if request.method == 'POST':
            id=request.POST['id']
            message=request.POST['message']
            employee_obj=Employee.objects.get(empid=id)
            obj=Connect.objects.create(
                employee=employee_obj,
                message=message
            )
            if obj:
                messages.success(request,'Connected Successfully!')
                return redirect('ems:connect')
            
    except Exception as e:
        print('Connect Exception : ',e)
    return render(request,'ems/connect.html',context)

@login_required()
def connectStatus(request):
    context={}
    try:
        if request.method == 'POST':
            id=request.POST['id']
            status=request.POST['status']
            connect=Connect.objects.get(id=id)
            if status == 'True':
                connect.is_completed=True
            else:
                connect.is_completed=False
            connect.save()
            messages.success(request,'Updated Successfully!')
            return redirect('ems:connect')
        
    except Exception as e:
        print('Connect Status Exception : ',e)
        
    return HttpResponse('Something Went wrong, Please Try After Sometime!')

@login_required()
def appreciation(request):
    context={}
    try:
        employees=Employee.objects.all()
        appreciations=Appreciation.objects.all()
        context['employees']=employees
        context['appreciations']=appreciations
        if request.method == 'POST':
            id=request.POST['id']
            message=request.POST['message']
            employee_obj=Employee.objects.get(empid=id)
            obj=Appreciation.objects.create(
                employee=employee_obj,
                message=message
            )
            if obj:
                messages.success(request,'Appreciated Successfully!')
                return redirect('ems:appreciation')
    except Exception as e:
        print('Appreciation Exception : ',e)
    return render(request,'ems/appreciation.html',context)

@login_required()
def editAppreciation(request):
    context={}
    try:
        if request.method == 'POST':
            id=request.POST['id']
            message=request.POST['editmessage']
            appricate=Appreciation.objects.get(id=id)
            appricate.message=message
            appricate.save()
            messages.success(request,'Updated Successfully!')
            return redirect('ems:appreciation')
        
    except Exception as e:
        print('Appreciation Edit Exception : ',e)
        
    return HttpResponse('Something Went wrong, Please Try After Sometime!')

@login_required()
def deleteAppreciation(request,id):
    try:
        obj=Appreciation.objects.get(id=id)

        if obj.delete():
            messages.success(request,'Deleted Successfully!')
        else:
            messages.warning(request,'Something Went Wrong!')
    except Exception as e:
        print("Delete Appreciation Exception : ",e)

    return redirect('ems:appreciation')

@login_required()
def newsletter(request):
    context={}
    try:
        newsletters=NewsLetter.objects.all()
        context['newsletters']=newsletters
        if request.method == 'POST':
            message=request.POST['message']
            obj=NewsLetter.objects.create(
                message=message
            )
            if obj:
                messages.success(request,'Added Successfully!')
                return redirect('ems:news-letter')
    except Exception as e:
        print('NewsLetter Exception : ',e)

    return render(request,'ems/news_letter.html',context)

@login_required()
def editNewsLetter(request):
    context={}
    try:
        if request.method == 'POST':
            id=request.POST['id']
            message=request.POST['editmessage']
            appricate=NewsLetter.objects.get(id=id)
            appricate.message=message
            appricate.save()
            messages.success(request,'Updated Successfully!')
            return redirect('ems:news-letter')
        
    except Exception as e:
        print('NewsLetter Edit Exception : ',e)
        
    return HttpResponse('Something Went wrong, Please Try After Sometime!')

@login_required()
def deleteNewsletter(request,id):
    try:
        obj=NewsLetter.objects.get(id=id)

        if obj.delete():
            messages.success(request,'Deleted Successfully!')
        else:
            messages.warning(request,'Something Went Wrong!')
    except Exception as e:
        print("Delete NewsLetter Exception : ",e)

    return redirect('ems:news-letter')

@login_required()
def reimbursement(request):
    context={}
    try:
        if not request.user.is_superuser:
            profile_obj=Employee.objects.get(user=request.user)
            context['profile']=profile_obj

            if request.method =='POST':
                
                bill=request.POST['type-of-bill']
                return redirect('ems:reimbursement-bill',bill)
        else:
            messages.warning(request,"You Don't have Access!")
    except Exception as e:
        print("Reimbursement Exception : ",e)
    return render(request,'ems/reimbursement.html',context)

@login_required()
def reimbursementBill(request,bill):
    context={}
    try:
        if not request.user.is_superuser:
            profile_obj=Employee.objects.get(user=request.user)
            context['profile']=profile_obj
            context['bill']=bill
            if bill == 'food':
                return render(request,'ems/reimbursement_food.html',context)
            if request.method =='POST':
                
                transport_company=request.POST['transport-company']
                print('bill ',transport_company)
                return redirect('ems:reimbursement-transport-company',bill,transport_company)
        else:
            messages.warning(request,"You Don't have Access!")
    except Exception as e:
        print('Reimbursement Bill Exception : ',e)
    return render(request,'ems/reimbursement_bill.html',context)

@login_required()
def reimbursementTransportCompany(request,bill,transport_company):
    context={}
    try:
        if not request.user.is_superuser:
            profile_obj=Employee.objects.get(user=request.user)
            context['profile']=profile_obj
            context['bill']=bill
            context['vehicle_company']=transport_company
            if request.method =='POST':
                
                vehicle_name=request.POST['vehicle-name']
                vehicle_number=request.POST['vehicle-number']
                date=request.POST['date']
                amount=request.POST['amount']
                obj=ReimbursementTransport.objects.create(employee=profile_obj,
                transport_company=transport_company,
                vehicle_name=vehicle_name,
                vehicle_number=vehicle_number,
                amount=amount,
                date=date,
                )
                if obj:
                    print(obj)
                    messages.success(request,'Reimbursement Requested Successfully!')
                    return redirect('ems:reimbursement-transport-all')
                else:
                    messages.warning(request,'Something went wrong please try again!')
                    return redirect('ems:reimbursement')
    except Exception as e:
        print('Reimbursement Vehicle Company Exception : ',e)
        messages.warning(request,'Please fill al the Details!')
    return render(request,'ems/reimbursement_transport_company.html',context)


# Displaying All Cab Reimubrsement of Employee
@login_required()
def reimbursementTransportAll(request):
    context={}
    try:
        if not request.user.is_superuser:
            profile_obj=Employee.objects.get(user=request.user)
            context['profile']=profile_obj
            cabreimbursements=ReimbursementTransport.objects.filter(employee=profile_obj).order_by('-id')
            context['cabreimbursements']=cabreimbursements
    except Exception as e:
        print('Display All Reimbursement Exception : ',e)
    return render(request,'ems/reimbursement_all_transport.html',context)


# Reimbursement For Admin
@login_required()
def adminTransportReimbursement(request):
    context={}
    try:
        cab_reimbursements=ReimbursementTransport.objects.all().order_by('-id')
        paginator=Paginator(cab_reimbursements,10)
        page_no=request.GET.get('page')

        total_pages=paginator.page_range
        cab_reimbursementspages=paginator.get_page(page_no) 
        context['cab_reimbursements']=cab_reimbursementspages
        context['pages']=total_pages
        if request.method == 'POST':
            id=request.POST['id']
            status=request.POST['status']
            remark=request.POST['remark']
            try:
                obj=ReimbursementTransport.objects.get(id=id)
            except Exception as e:
                print('Admin Cab Reimbursement Inside  Exception : ',e)
                messages.warning(request,'Something went wrong!')
            
            if obj:
                obj.status=status
                obj.remark=remark
                obj.save()
                messages.success(request,'Updated Successfully!')
                return redirect('ems:admin-transport-reimbursement')

    except Exception as e:
        print('Admin Cab Reimbursement  Exception : ',e)
    return render(request,'ems/admin_transport_reimbursement.html',context)


# Reimbursement Food 

@login_required()
def reimbursementFood(request):
    context={}
    try:
        if not request.user.is_superuser:
            profile_obj=Employee.objects.get(user=request.user)
            context['profile']=profile_obj
            if request.method == 'POST':
                number_of_employee=request.POST['number-of-employee']
                amount=request.POST['amount']
                x=int(amount)/int(number_of_employee)
                if x > 200:
                    print('Inside condition ',x)
                    messages.warning(request,'Your Amount is Exceeding! Per Person Allowed only ₹200/. ')
                    bill='food'
                    return redirect('ems:reimbursement-bill',bill)
                else:
                    context['amount']=amount
                    context['number_of_employee']=number_of_employee
    except Exception as e:
        print('Reimbursement Food Exception : ',e)

    return render(request,'ems/reimbursement_food_employee_detail.html',context)

@login_required()
def reimbursmentFoodSubmit(request):
    context={}
    try:
        if not request.user.is_superuser:
            profile_obj=Employee.objects.get(user=request.user)
            context['profile']=profile_obj
            if request.method == 'POST':
                amount=request.POST['amount']
                number_of_employee=request.POST['number-of-employee']
                date=request.POST['date']
                bill_number=request.POST['bill-number']

                x=int(amount)/int(number_of_employee)

                if x>200:
                    messages.warning(request,'Your Amount is Exceeding! Per Person Allowed only ₹200/. ')
                    bill='food'
                    return redirect('ems:reimbursement-bill',bill)
                else:
                    obj=ReimbursementFood.objects.create(
                        employee=profile_obj,
                        number_of_employee=number_of_employee,
                        amount=amount,
                        bill_number=bill_number,
                        date=date
                    )
                    if obj:
                        for i in range(int(number_of_employee)-1):
                            employee_name=request.POST['employee'+str(i+1)]
                            department_name=request.POST['department'+str(i+1)]
                            obj_employee=ReimbursementFoodEmployee.objects.create(
                                reimbursement_food=obj,
                                name=employee_name,
                                department=department_name,
                            )    
                            print('Reimbursment Employee Object ',obj_employee)
                        messages.success(request,'Reimbursement Requested Successfully!')



    except Exception as e:
        print("Reimbursment Food Submit Exception : ",e)
    
    return redirect('ems:reimbursement-food-all')

# Displaying All Food Reimubrsement of Employee
@login_required()
def reimbursementFoodAll(request):
    context={}
    try:
        if not request.user.is_superuser:
            profile_obj=Employee.objects.get(user=request.user)
            context['profile']=profile_obj

            reimbursement_foods=ReimbursementFood.objects.filter(employee=profile_obj).order_by('-id')
            context['reimbursement_foods']=reimbursement_foods
    except Exception as e:
        print('All Reimbursement Exception : ',e)
    return render(request,'ems/reimbursement_all_food.html',context)


# Seeing The Food Reimbursment Employee for both Employee and Admin

@login_required()
def reimbursementEmployee(request,id):
    context={}
    try:
        if not request.user.is_superuser:
            profile_obj=Employee.objects.get(user=request.user)
            context['profile']=profile_obj
        obj=ReimbursementFood.objects.get(id=id)
        print(obj)
        reimbursements_employees=ReimbursementFoodEmployee.objects.filter(reimbursement_food=obj)
        print('reimbursement EMployee ',reimbursements_employees)
        context['reimbursements_employees']=reimbursements_employees
    except Exception as e:
        print("Reimbursement Employee Exception : ",e)
    return render(request,'ems/reimbursment_employee.html',context)


# Displying All Food Reimbursement For Admin

@login_required()
def adminReimbursementFood(request):
    context={}
    try:
        reimbursement_foods=ReimbursementFood.objects.all().order_by('-id')
        paginator=Paginator(reimbursement_foods,10)
        page_no=request.GET.get('page')

        total_pages=paginator.page_range
        reimbursement_foodspages=paginator.get_page(page_no) 
        context['reimbursement_foods']=reimbursement_foodspages
        context['pages']=total_pages
        if request.method == 'POST':
            id=request.POST['id']
            status=request.POST['status']
            remark=request.POST['remark']
            try:
                obj=ReimbursementFood.objects.get(id=id)
            except Exception as e:
                print('Admin Cab Reimbursement Inside  Exception : ',e)
                messages.warning(request,'Something went wrong!')
            
            if obj:
                obj.status=status
                obj.remark=remark
                obj.save()
                messages.success(request,'Updated Successfully!')
                return redirect('ems:reimbursement-food-admin')
    except Exception as e:
        print('Admin Reimbursement Food Exception : ',e)
    return render(request,'ems/admin_reimbursement_food.html',context)