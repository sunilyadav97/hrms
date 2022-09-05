console.log('Hello Js')

// Get Department Objct 

function editDepartment(id,name,des){
    console.log(id)
    nameDepartment=document.getElementById('department-name').value=name
    description=document.getElementById('description').value=des
    departmentID=document.getElementById('department-id').value=id
    }

function editRole(id,name,des){
    console.log(id)
    nameDepartment=document.getElementById('role-name').value=name
    description=document.getElementById('description').value=des
    departmentID=document.getElementById('department-id').value=id
    }
function editevent(id,title,description,date)
{
    console.log(id)
    console.log(title)
    console.log(description)
    console.log(date)
    document.getElementById('title').value=title
    document.getElementById('description').value=description
    document.getElementById('date').value=date
    document.getElementById('id').value=id
}

