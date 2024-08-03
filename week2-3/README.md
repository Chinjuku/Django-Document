## Install Django ( Week 2 - Week 3 )
### How to install django framework
#### 1. Install & Create Virtual Environment
```
    pip install virtualenv
    python -m venv myvenv
```
จะได้ folder myvenv ที่เราเราสร้าง venv ขึ้นมา
#### 2.Open Virtual Environment 
```
    myvenv\Script\activate.bat
```
เพื่อเปิดให้ virtual environment ทำงานและเก็บ version ที่ install มาลงใน venv
#### 3. Install Django and PosgresSQL
```
    pip install django psycopg2-binary
```
#### 4. Create Project Django
```
    django-admin startproject ชื่อโปรเจค
    ## ex. django-admin startproject myshop
```
#### 5. Create Django App
```
    cd ชื่อโปรเจค
    py manage.py startapp ชื่อแอป 
    ## ex. py manage.py startapp profile
```
#### 6. Add created App (เพิ่มแอปลงใน INSTALLED APP บนไฟล์ ex. myshop/setting.py)
```python
    INSTALLED_APPS = [
    "django.contrib.admin",
    ... ,
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Add your apps here
    "blogs",
]
```
#### 7. Setting Database to connect PostgresSQL Server
```python
    เปลี่ยน Database ที่ default เป็น Sqlite เป็น PostgresSQL
    DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "blogs",
        "USER": "db_username", # Default "postgres"
        "PASSWORD": "password", # Password ที่ถูกบังคับใส่ตอนโหลด PGAdmin4
        "HOST": "localhost",
        "PORT": "5432",
    }
}
```
#### 8. Verify that the PostgresSQL database is connected.
```
    py manage.py migrate # เพื่อ migrate เช็คว่าเชื่อมได้ไหม
```
#### 9. Migrate Models to Database
- Choose app that you created
```
    # blogs/models.py
    from django.db import models
    class Author(models.Model):
        first_name = models.CharField(max_length=150)
        last_name = models.CharField(max_length=200)
        def __str__(self):
            return f"{self.first_name} {self.last_name}"
```
- Use command makemigrations django to create migration file.
```
    python manage.py makemigrations
```
- In `blogs/migrations/001_initial.py` will created.
- Then create migrate app to migrate (Add/Edit Model) to Database
```
    python manage.py migrate        # Migrate all apps.
    python manage.py migrate blogs  # Migrate only blogs app.
```
#### Using Shell Scripts in Django
```
    python manage.py shell
```