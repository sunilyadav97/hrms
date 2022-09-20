// Rotate Arrow or side Nav
state=false
function rotate()
{

    var arrow=document.querySelectorAll('.arrow-forward')
    arrow.forEach(e=>{
        console.log('state')
    e.addEventListener("click",function(){
        console.log('state')
    
    if (!state)
    {
        arrow.classList.add('rotate-arrow')
        state = true
    }else if(state == true)
    {
        arrow.classList.remove('rotate-arrow')
        state=false

    }
})
})
    
}
// Get Department Objct 

function editDepartment(id, name, des) {
    console.log(id)
    nameDepartment = document.getElementById('department-name').value = name
    description = document.getElementById('description').value = des
    departmentID = document.getElementById('department-id').value = id
}

function editRole(id, name, des) {
    console.log(id)
    nameDepartment = document.getElementById('role-name').value = name
    description = document.getElementById('description').value = des
    departmentID = document.getElementById('department-id').value = id
}
function editevent(id, title, description, date, is_com) {
    
    document.getElementById('title').value = title
    document.getElementById('description').value = description
    document.getElementById('date').value = date
    document.getElementById('id').value = id
    var completed = document.getElementById('completed')
    if (is_com == 'True') {
        completed.setAttribute("checked", "checked");
        completed.value='True'
    }
    
}


// =========Show Leave Description=========

function showDescription(description)
{
    var descriptionContainer=document.getElementById('discription-container')

   
        descriptionContainer.innerHTML=description
        descriptionContainer.classList.remove('d-none')
    
}

// ==========Remove Notification After Some time============
 window.addEventListener("load",function(){
    setTimeout(removeNotification, 5000);

})
function removeNotification()
{
    try {
        const notification=document.getElementById('notification')
    notification.classList.add('d-none');
      }
      catch(err) {
        console.log("Notification function")
    }
    
}