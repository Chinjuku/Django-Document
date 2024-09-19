from django.urls import path
from .views import *

urlpatterns = [
    path('', ViewEmployee.as_view(), name="employee"),
    path('position/', ViewPosition.as_view(), name="position"),
    path('project/', ViewProject.as_view(), name="project"),
    path('project/create/', ViewCreateProject.as_view(), name="new-project"),
    path('project/edit/<int:project_id>', ViewProjectById.as_view(), name="edit-project"),
    path('api/example/<int:pro_id>/', ViewDeleteId.as_view()),
    path('api/example/<int:pro_id>/<int:emp_id>/', ViewManageStaff.as_view()),
    path('forms/', ViewEmployeeForm.as_view(), name="employee_form"),
    
]
