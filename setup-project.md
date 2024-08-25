# Setup-project

#### **1. Create virtual environment**

```python
#### step 1
# Create a virtual environment (Windows)
> py -m venv myvenv

# Activate virtual environment (Windows)
> myvenv\Scripts\activate.bat

# Create a virtual environment (MacOS)
> python -m venv myvenv

# Activate virtual environment (MacOS)
> source myvenv/bin/activate
```

#### **2. Install Django & start a new project "myblogs"**

```python
#### Install pip
> pip install psycopg2

# Install Django
> pip install django

# Create project "myblogs"
> django-admin startproject myshop

# Create the "blogs" app
> python manage.py startapp shop
```

#### 3.  Create Database in pgAdmin4

#### 4. Setting file

```python
# file >> settings.py
# Database setting
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "shop", ##แก้ตรงนี้ด้วย
        "USER": "postgres", ##postgres
        "PASSWORD": "password",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

# Add app blogs to INSTALLED_APPS
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Add your apps here
    "shop",
]
```

#### 5. Import Model

#### 6.  Makemigrations & Migrate

```python
> python manage.py makemigrations

> python manage.py migrate
```

---

#### 7.  Setup **Django Notebook Extension**

```python
# ติดตั้ง django-extensions และ jupyter notebook ด้วยคำสั่ง
> pip install django-extensions ipython jupyter notebook

# จากนั้นให้แก้ไข version ของ package ภายใน jupyter และ notebook
> pip install ipython==8.25.0 jupyter_server==2.14.1 jupyterlab==4.2.2 jupyterlab_server==2.27.2

#แก้ไข version notebook (หากติดตั้ง หรือ run jupyter ไม่ได้ให้ลองเปลี่ยน version 6.5.6)
> pip install notebook==6.5.7

#จากนั้นสร้าง directory ชื่อ notebooks
> mkdir notebooks
```

#### 8. Setting file

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

		# Add your extensions here
    "django_extensions",
    "shop",
]
```

#### 9. Start Jupyter Notebook

```python
> python manage.py shell_plus --notebook
```

#### 10. Create file .ipynb in notebook

#### 11. Cell แรกของไฟล์ Notebook

```python
import os
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

# import modules
from shop.models import *
from django.db.models import *
from django.db.models.functions import *
from django.db.models.lookups import *
from datetime import *
import json
```
---
# The Views Setup

#### **1. สร้าง ```views.py``` ใน โฟลเดอร์ app**

```python
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from django.db.models import Count 
from .models import *
from django.http import Http404
import json

class EmployeeView(View):

    def get(self, request):
        employees = Employee.objects.all()
        total_employee = employees.count()
        context = {"employees": employees, "total_employee": total_employee}
        return render(request, "employee.html", context)
```

#### **2. สร้าง ```urls.py``` ในโฟลเดอร์ app แล้วกำหนด path สำหรับเข้าถึง views**

```python
from django.urls import path

from . import views

urlpatterns = [
    path("", views.EmployeeView.as_view(), name="employee"),
    
]
```

#### **3. กำหนด path สำหรับเข้าถึง ```urls.py``` ของ app ในโฟลเดอร์ project ```urls.py```**

```python
...
from django.urls import path , include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("polls.urls")),
]
```

#### **4. แก้ไขไฟล์ใน ```setting.py```**
```python
import os
SETTINGS_PATH = os.path.dirname(os.path.dirname(__file__))

TEMPLATE_DIRS = (
    os.path.join(SETTINGS_PATH, 'templates'),
)

BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

```

#### **5. รันคำสั่ง**

```python
### Start server
> python manage.py runserver
```