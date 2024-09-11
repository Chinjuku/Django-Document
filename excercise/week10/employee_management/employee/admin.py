from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Employee)
admin.site.register(EmployeeAddress)
admin.site.register(Department)
admin.site.register(Position)
admin.site.register(Project)
