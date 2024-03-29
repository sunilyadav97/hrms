from django.urls import path
from .views import *
app_name='ems'
urlpatterns=[
    path('',dashboard,name='ems'),
    path('new-users/',newUsers,name='new-users'),
    path('send-verification-mail/<username>/',sendVerificationMail,name='send-verification-mail'),
    path('verify/<token>/',verifyLink,name='verify'),
    path('create-department/',createDepartment,name='create-department'),
    path('view-departments/',viewDepartment,name='view-department'),
    path('delete-department/<pk>/',deleteDepartment,name='delete-department'),
    path('create-role/',createRole,name='create-role'),
    path('view-roles/',viewRole,name='view-role'),
    path('delete-role/<pk>/',deleteRole,name='delete-role'),
    path('add-personal-info/<token>/',addEmployee,name='add-employee'),
    path('documents/',documents,name='documents'),
    path('document-delete/<id>/',deleteDocument,name='document-delete'),
    path('document/<empid>',adminDocument,name='employee-document'),
    path('employee-view/',viewEmployee,name='employee-view'),
    path('employee-detail/<empid>/',employeeDetail,name='employee-detail'),
    path('employee-delete/<empid>/',deleteEmployee,name='employee-delete'),
    path('attendance/',attendance,name='attendance'),
    path('add-attendance-filter/',addAttendanceFilter,name='add-attendance-filter'),
    path('attendance-edit/',editAttendance,name='edit-attendance'),
    path('attendance-delete/<pk>/',deleteAttendance,name='attendance-delete'),
    path('admin-attendance-report',adminReport,name='admin-report'),
    path('leave-create/',createLeave,name='leave-create'),
    path('leave-delete/<pk>/',deleteLeave,name='leave-delete'),
    path('leaves/',dashboardLeaves,name='dashboard-leaves'),
    path('profile/',profile,name='profile'),
    path('profile-edit/',editProfile,name='profile-edit'),
    path('change-password/',changePassword,name='change-password'),
    path('all-leaves/',allLeaves,name='all-leaves'),
    path('all-attendance/',allAttendances,name='all-attendance'),
    path('create-event/',createEvent,name='create-event'),
    path('view-events/',viewEvents,name='view-events'),
    path('delete-event/<id>/',deleteEvent,name='delete-event'),
    path('event/<id>/',event,name='event'),
    path('create-payroll',createPayRoll,name='create-payroll'),
    path('view-payrolls',viewPayRoll,name='view-payrolls'),
    path('delete-payroll/<id>/',deletePayRoll,name='delete-payroll'),
    path('payroll',payRoll,name='payroll'),
    path('create-query',createQuery,name='create-query'),
    path('queries',displayQuerys,name='queries'),
    path('query/<id>/',queryDetail,name='query-detail'),
    path('all-queries',quriesManger,name='all-queries'),
    path('add-comment',addComment,name='add-comment'),  
    path('attendance-date-filter/',attendanceDateFilter,name='attendance-date-filter'),  
    path('attendance-department-filter/',attendanceDepartmentFilter,name='attendance-department-filter'),  
    path('attendance-employee-filter/',attendanceEmployeeFilter,name='attendance-employee-filter'),  
    path('connect',connect,name='connect'),  
    path('connect-status',connectStatus,name='connect-status'),  
    path('allocated-leaves',allocatedLeave,name='allocated-leaves'),  
    path('allocated-leaves-edit',editAllocatedLeave,name='edit-allocated-leaves'),  
    path('allocated-leaves-delte/<id>/',deleteAllocatedLeave,name='allocated-leaves-delete'),  
    path('appreciation',appreciation,name='appreciation'),
    path('edit-appreciation',editAppreciation,name='edit-appreciation'),
    path('delete-appreciation/<id>/',deleteAppreciation,name='delete-appreciation'),
    path('news-letter',newsletter,name='news-letter'),
    path('edit-news-letter',editNewsLetter,name='edit-news-letter'),
    path('delete-news-letter/<id>/',deleteNewsletter,name='delete-news-letter'),
    path('reimbursement',reimbursement,name='reimbursement'),
    path('reimbursement/<bill>',reimbursementBill,name='reimbursement-bill'),
    path('reimbursement/<bill>/<transport_company>/',reimbursementTransportCompany,name='reimbursement-transport-company'),
    path('reimbursement-transport-all',reimbursementTransportAll,name='reimbursement-transport-all'),
    path('reimbursements-transport',adminTransportReimbursement,name='admin-transport-reimbursement'),
    path('reimbursement-food',reimbursementFood,name='reimbursement-food'),
    path('reimbursement-food-submit',reimbursmentFoodSubmit,name='reimbursement-food-submit'),
    path('reimbursement-food-all',reimbursementFoodAll,name='reimbursement-food-all'),
    path('reimbursement-see-employee/<id>/',reimbursementEmployee   ,name='reimbursement-see-employee'),
    path('reimbursement-food-admin',adminReimbursementFood,name='reimbursement-food-admin'),
    path('get-report',generateReport,name='get-report'),
    path('permission',permission,name='permission'),
    path('permission-get/<empid>',Getpermission,name='permission-get'),
    path('permission-delete/<id>/<empid>/',deletePermission,name='permission-delete'),
]