from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from .models import *
from datetime import datetime, date
from django.db.models import *
from django.db.models.functions import *
from .forms import EmployeeForm, ProjectForm
from django.db import transaction, IntegrityError
from company.models import *

# Create your views here.
class ViewEmployee(View):
    def get(self, request):
        query = Employee.objects.annotate(full_name=Concat(F("first_name"), Value(" "), F("last_name"))).order_by('-hire_date')
        count = Employee.objects.count()
        getaddress = EmployeeAddress.objects.all()
        for employee in query:
            employee.position = Position.objects.get(pk=employee.position_id)
        data = {
            "employees": query,
            "count": count,
            "addresses": getaddress
        }
        return render(request, "employee.html", data)

class ViewPosition(View):
    def get(self, request):
        query = Employee.objects.values("position_id", "position__name").annotate(count=Count("position_id")).order_by("position_id")
        data = {
            "position": query
        }
        return render(request, "position.html", data)

class ViewCreateProject(View):
    def get(self, request):
        form = ProjectForm()
        data = {
            "form": form
        }
        return render(request, "project_form.html", data)
    
    def post(self, request):
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/employee/project')
        return render(request, "project_form.html", {'form': form})

class ViewProject(View):
    def get(self, request):
        query = Project.objects.all()
        data = {
            "project": query
        }
        return render(request, "project.html", data)
    
class ViewProjectById(View):
    def get(self, request, project_id):
        query = Project.objects.get(pk=project_id)
        form = ProjectForm(instance=query)
        data = {
            "project": query,
            "form": form
        }
        return render(request, "project_detail.html", data)
    def post(self, request, project_id):
        query = Project.objects.get(pk=project_id)
        form = ProjectForm(request.POST, instance=query)
        if form.is_valid():                                                                      
            form.save()                                                                          
            return redirect(f"/employee/project/edit/{project_id}")
        data = {
            "project": query,
            "form": form
        }
        return render(request, "project_detail.html", data)

class ViewDeleteId(View):
    def delete(self, request, pro_id):
        try:
            Project.objects.get(pk=pro_id).delete()
            return  
        except Exception as e:
            print(f"Error: {e}")
            return HttpResponse("An error occurred while trying to delete the project.", status=500)

class ViewManageStaff(View):
    def put(self, request, emp_id, pro_id):
        try:
            emp = Employee.objects.get(pk=emp_id)
            project = Project.objects.get(pk=pro_id)
            project.staff.add(emp)
            project.save()
            return JsonResponse({"message": "Add staff successfully!!!"}, status=200)
        except Exception as e:
            return JsonResponse({"message": str(e)})
    def delete(self, request, emp_id, pro_id):
        try:
            emp = Employee.objects.get(pk=emp_id)
            project = Project.objects.get(pk=pro_id)
            project.staff.remove(emp)
            return JsonResponse({"message": "Kick staff successfully!!!"}, status=200)
        except Exception as e:
            return JsonResponse({"message": str(e)})

class ViewEmployeeForm(View):
    def post(self, request):
        form = EmployeeForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    employee = form.save()
                    EmployeeAddress.objects.create(
                        employee=employee,
                        location=form.cleaned_data['location'],
                        district=form.cleaned_data['district'],
                        province=form.cleaned_data['province'],
                        postal_code=form.cleaned_data['postal_code']
                    )
                    return redirect('/employee')
            except IntegrityError:
                return render(request, "employee_form.html", {
                "form" : form,
                "error": "There was an error saving the data. Please try again."
            })
        return render(request, "employee_form.html", {
                "form" : form
        })
        
    def get(self, request): 
        form = EmployeeForm()
        return render(request, "employee_form.html", {
            "form" : form
        })
