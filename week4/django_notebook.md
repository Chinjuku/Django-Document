### Create Jupiter NoteBook ( Week 4 )
#### 1. Install Django Jupiter notebook

```
    pip install django-extensions ipython jupyter notebook
    pip install ipython==8.25.0 jupyter_server==2.14.1 jupyterlab==4.2.2 jupyterlab_server==2.27.2
    pip install notebook==6.5.7 # ถ้าไม่ได้ให้ใช้ 6.5.6
```

#### 2. Create Directory notebooks

```
    mkdir notebooks
```

#### 3. เพิ่ม `django-extensions` ใน INSTALLED_APPS ในไฟล์ settings.py

```py
    INSTALLED_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",

        "django_extensions",
        "blogs",
    ]
```

#### 4. Start Jupiter Notebook Server

```
    python manage.py shell_plus --notebook
```
จะเข้าไปที่ folder notebooks
#### 5. สร้าง/เพิ่มไฟล์ .ipynb สำหรับใช้กับ project django
#### 6. จากนั้นใน Cell แรกของไฟล์ Notebook เพิ่ม code นี้ลงไป

```py
import os
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
```

#### 7. ตั้ง Kernel ให้เป็น Django Script
#### 8. สามารถทำการ import models และ query ข้อมูลโดยใช้ API ของ Django ได้เลย

```py
from blogs.models import Blog

for blog in Blog.objects.all():
    print(blog)
    
```
ลองเพิ่มข้อมูลเข้าไปในทุกตารางเลยครับ จากนั้นลอง query ข้อมูลดู

