from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .models import *
from django.contrib.auth.models import User


def home(request):
    context = {}
    return render(request, 'ems/home.html', context)


def dashboard(request):
    context = {}
    return render(request, 'ems/dashboard.html', context)


def createDepartment(request):
    context = {}
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


def viewDepartment(request):
    context = {}
    try:
        departments = Department.objects.all()
        context['departments'] = departments
    except Exception as e:
        print('View Department Exception : ', e)
    return render(request, 'ems/view_department.html', context)


def deleteDepartment(request, pk):
    try:
        Department.objects.get(id=pk).delete()
        messages.success(request, 'Department Deleted Successfully!')
        return redirect(reverse('ems:view-department'))
    except Exception as e:
        print('Delete Department Exception : ', e)


def createRole(request):
    context = {}
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


def viewRole(request):
    context = {}
    try:
        roles = Role.objects.all()
        context['roles'] = roles
    except Exception as e:
        print('View Role Exception : ', e)
    return render(request, 'ems/view_role.html', context)


def deleteRole(request, pk):
    try:
        Role.objects.get(id=pk).delete()
        messages.success(request, 'Role Deleted Successfully!')
        return redirect(reverse('ems:view-role'))
    except Exception as e:
        print('Delete Role Exception : ', e)


def addEmployee(request):
    context = {}
    try:
        users = User.objects.all()
        roles = Role.objects.all()
        departments = Department.objects.all()
        context['users'] = users
        context['roles'] = roles
        context['departments'] = departments

        if request.method == 'POST':
            user = request.POST['select-user']
            full_name = request.POST['employee-name']
            father_name = request.POST['father-name']
            dob = request.POST['employee-dob']
            phone_number = request.POST['phone-number']
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

            if user and full_name and father_name and dob and email and phone_number and address and street and locality and city and state and pincode and country and designation and department and role and joining_date and status:
                if user and role and department and status == 'default':
                    messages.warning(request, 'All fields are mandotry')
                    return redirect('ems:employee-add')

                user_obj = User.objects.get(username=user)
                check_employee = Employee.objects.filter(
                    user=user_obj).exists()

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
                    address=address_obj,
                    designation=designation,
                    role=role_obj,
                    department=d_obj,
                    joining_date=joining_date,
                    status=status
                )
                print('Employee Obj : ', emp_obj)
                messages.success(
                    request, 'New Employee Reigsterd Successfully!')
            else:
                print('fail')
                messages.warning(request, 'All fields are mandotry')

    except Exception as e:
        print('Add Employee Exception : ', e)
    return render(request, 'ems/add_employee.html', context)


def viewEmployee(request):
    context = {}
    try:
        employees = Employee.objects.all()
        context['employees'] = employees
    except Exception as e:
        print('View Employee Exception : ', e)

    return render(request, 'ems/view_employee.html', context)


def employeeDetail(request, empid):
    context = {}
    try:
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
