from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from .models import *
from datetime import datetime, date
from django.db.models import *
from django.db.models.functions import *

# Create your views here.
class ViewEmployee(View):
    def get(self, request):
        query = Employee.objects.annotate(full_name=Concat(F("first_name"), Value(" "), F("last_name"))).order_by('hire_date')
        count = Employee.objects.count()
        data = {
            "employees": query,
            "count": count,
        }
        return render(request, "employee.html", data)

class ViewPosition(View):
    def get(self, request):
        query = Employee.objects.values("position", "position__name").annotate(count=Count("position")).order_by("position")
        data = {
            "position": query
        }
        return render(request, "position.html", data)

class ViewProject(View):
    def get(self, request):
        query = Project.objects.all()
        data = {
            "project": query
        }
        # print(data)
        return render(request, "project.html", data)
    
class ViewProjectById(View):
    def get(self, request, project_id):
        query = Project.objects.get(pk=project_id)
        query_em = Employee.objects.all()
        data = {
            "project": query,
            "start_date": query.start_date.strftime("%Y-%m-%d"),
            "due_date": query.due_date.strftime("%Y-%m-%d"),
            "employees": query_em
        }
        # print(data)
        return render(request, "project_detail.html", data)


class ViewDeleteId(View):
    def delete(self, request, pro_id):
        try:
            Project.objects.get(pk=pro_id).delete()
            return JsonResponse({ "message": 'complete'}, status=200)
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

