# Document สรุป ( Week2 - Week5 ) วิชา Server-Side-Web
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
## Models Fields ที่ใช้บ่อย ( Week 3 )
[Doc Model fields](https://docs.djangoproject.com/en/5.0/ref/models/fields/)
### Fields types
- BooleanField(**options)
- CharField(max_length=None, **options)
- EmailField(max_length=254, **options)
- URLField(max_length=200, **options)
- UUIDField(**options)
- TextField(**options)
- DateField(auto_now=False, auto_now_add=False, **options)
    - auto_now = True คือจะบันทึกค่า datetime.now() ทุกครั้งที่มีการแก้ไขค่า (INSERT + UPDATE)
    - auto_now_add = True คือจะบันทึกค่า datetime.now() ตอนที่สร้างใหม่ (INSERT)
- DateTimeField(auto_now=False, auto_now_add=False, **options)
- TimeField(auto_now=False, auto_now_add=False, **options)
- FileField(upload_to='', storage=None, max_length=100, **options)
    - upload_to คือกำหนด path ที่จะ save file
```python
class MyModel(models.Model):
    # file will be uploaded to MEDIA_ROOT/uploads
    upload = models.FileField(upload_to="uploads/")
    # or...
    # file will be saved to MEDIA_ROOT/uploads/2015/01/30
    upload = models.FileField(upload_to="uploads/%Y/%m/%d/")
```

- ImageField(upload_to=None, height_field=None, width_field=None, max_length=100, **options)

    - สืบทอด attributes และ methods ทั้งหมดจาก `FileField`
    - ทำการ validate ให้ว่าเป็น object ของ image ที่เหมาะสม และ สามารถกำหนด `height_field` และ `width_field`

- DecimalField(max_digits=None, decimal_places=None, **options)

```python
models.DecimalField(max_digits=5, decimal_places=2)
```

- IntegerField(**options)

    - ค่าตั้งแต่ -2147483648 ถึง 2147483647 รองรับใน database ทุกตัวที่ supported โดย Django.

- PositiveIntegerField(**options)
- JSONField(encoder=None, decoder=None, **options)

### Field options

- primary_key: ถ้ามีค่าเป็น True คือ column นี้เป็น primary key ของ table (ถ้าไม่กำหนด Django จะสร้าง column ชื่อ `id` ให้อัตโนมัติเป็น primary key)
- unique: ถ้ามีค่าเป็น True คือ ค่าใน column นี้ห้ามซ้ำ
- null: ถ้ามีค่าเป็น True คือ column นี้มีค่าเป็น null ได้
- blank: ถ้ามีค่าเป็น True คือ column นี้มีค่าเป็น "" หรือ empty string ได้
- default: กำหนดค่า default
- choices: กำหนด ENUM ให้เลือกเฉพาะค่าที่กำหนด

```python
from django.db import models


class Student(models.Model):
    FRESHMAN = "FR"
    SOPHOMORE = "SO"
    JUNIOR = "JR"
    SENIOR = "SR"
    GRADUATE = "GR"
    YEAR_IN_SCHOOL_CHOICES = {
        FRESHMAN: "Freshman",
        SOPHOMORE: "Sophomore",
        JUNIOR: "Junior",
        SENIOR: "Senior",
        GRADUATE: "Graduate",
    }
    year_in_school = models.CharField(
        max_length=2,
        choices=YEAR_IN_SCHOOL_CHOICES,
        default=FRESHMAN,
    )

    def is_upperclass(self):
        return self.year_in_school in {self.JUNIOR, self.SENIOR}
```
- db_index: ถ้ามีค่าเป็น True คือจะสร้าง index ใน database สำหรับ column นี้
## Python Datetime Module ( Week 3 )
### DateTime module มีทั้งหมด 5 class หลัก

1. `date` – มี attributes ได้แก่ year, month, และ day
2. `time` – มี attributes ได้แก่ hour, minute, second, microsecond, และ tzinfo
3. `datetime` – คือการรวม date และ time และมี attributes ได้แก่ year, month, day, hour, minute, second, microsecond, and tzinfo
4. `timedelta` – เป็นระยะเวลา (microsecond) ซึ่งเป็นส่วนต่างของ 2 date, time หรือ datetime
5. `tzinfo` – เป็น object สำหรับเก็บข้อมูล time zone

```python
    from datetime import datetime, timedelta
    # datetime(year, month <= 12, day, hour, minute, second, microsecond)
    a = datetime(1999, 12, 31, 24, 60, 60, 342380)
```

### Python timedelta   
```python
    # time now
    now = datetime.now()
    # timedelta (after 730 days)
    datetime_after_2years = now + timedelta(days=730)
```

### Python datetime.tzinfo()
The datetime.now() function จะไม่มีการเก็บข้อมูล time zones การเก็บข้อมูล time zines จะใช้ tzinfo ซึ่งเป็น abstract base case ใน Python

- โดยเราสามารถส่ง instance ของ class tzinfo ใน constructors ของ object datetime and time เพื่อใช้ในการกำหนด time zones

#### Naive and Aware datetime objects
- ``Naive datetime objects`` หมายถึง datetime object ที่ไม่มีการกำหนดข้อมูล time zone (tzinfo เป็น None)
- ``Aware datetime objects`` คือ datetime object ทีมีข้อมูล time zone
```python
>>> from zoneinfo import ZoneInfo
>>> from datetime import datetime

>>> dt1 = datetime(2015, 5, 21, 12, 0) 
>>> print(dt1)
2015-05-21 12:00:00
>>> dt2 = datetime(2015, 12, 21, 12, 0, tzinfo = ZoneInfo(key='Asia/Bangkok')) 
>>> print(dt2)
2015-12-21 12:00:00+07:00

>>> print("Naive Object :", dt1.tzname())
Naive Object : None
>>> print("Aware Object :", dt2.tzname())
Aware Object : +07

>>> now_aware = dt1.replace(tzinfo=ZoneInfo(key='UTC'))
>>> print(now_aware)
2015-05-21 12:00:00+00:00
```
### Django - Time zones

ถ้ามีการ enable time zone support (USE_TZ=True) โดย default Django จะบันทึก datetime information ในฐานข้อมูลเป็น UTC เมื่อ query ข้อมูลออกมาก็จะได้เป็น object datetime ที่ time-zone-aware

#### Naive and aware datetime objects
อย่างที่รู้กันว่า datetime.datetime objects ของ Python นั้นมี attribute tzinfo ที่ใช้ในการเก็บข้อมูล time zone โดยถ้ามีการ set ค่า tzinfo ก็จะส่งผลให้ datetime object นั้นเป็น time-zone-aware และถ้าไม่มีการ set ค่า tzinfo ก็จะเป็น time-zone-naive
Django จะมีfunction
- `is_aware()` เช็คว่า timezone ถูกตั้งค่าไว้ไหม ( return เป็น Boolean )
- `is_naive()` เช็คการว่าไม่มีการกำหนด timezone ( return เป็น Boolean )
```py
>>> from zoneinfo import ZoneInfo
>>> from datetime import datetime
>>> from django.utils import timezone

>>> dt1 = datetime(2015, 12, 21, 12, 0, tzinfo=ZoneInfo(key='UTC')) 
>>> print(dt1)
2015-12-21 12:00:00+00:00
>>> timezone.is_aware(dt1)
True

>>> dt1_local = timezone.localtime(dt1)
>>> print(dt1_local)
2015-12-21 19:00:00+07:00

>>> dt2 = datetime(2015, 5, 21, 12, 0) 
>>> print(dt2)
2015-12-21 12:00:00
>>> timezone.is_aware(dt2)
False
>>> timezone.is_naive(dt2)
True

>>> dt2_aware = timezone.make_aware(dt2)
>>> print(dt2_aware)
2015-05-21 12:00:00+07:00
>>> timezone.is_aware(dt2_aware)
True
```

## Making Queries ( Week 4 )
เมื่อเราทำการประกาศ `class models.Model` ใน `models.py` แล้ว เราจะสามารถใช้งาน database-abstraction API ที่จะช่วยให้่เรา create, retrieve, update และ delete ข้อมูลในฐานข้อมูลได้่อย่างง่ายและรวดเร็วมากๆ โดยไม่จำเป็นจะต้องเป็น SQL แม้แต่นิดเดียว
NOTE: ให้เปิด Django shell ขึ้นมา (`python manage.py shell`) และพิมพ์คำสั่งดังนี้

```python
>>> from blogs.models import Blog
>>> b = Blog(name="Beatles Blog", tagline="All the latest Beatles news.")
>>> b.save()
```

ซึ่ง Django จะเป็นการ generate SQL command `INSERT` เมื่อเราสั่ง `save()`

## Saving changes to objects

ในการบันทึกการแก้ไข record ที่มีอยู่ใน database แล้วก็ใช้ `save()` เช่นเดียวกัน

```python
>>> b.name = "New name"
>>> b.save()
```

ซึ่ง Django จะเป็นการ generate SQL command `UPDATE` เมื่อเราสั่ง `save()`

## Saving ForeignKey and ManyToManyField fields

การ update foreign key ก็สามารถทำได้เหมือนกับการ update field ปกติ โดยใช้ `save()`

```python
>>> from blogs.models import Blog, Entry
>>> entry = Entry.objects.get(pk=1)
>>> cheese_blog = Blog.objects.get(name="Cheddar Talk")
>>> entry.blog = cheese_blog # Update FK blog ของ entry (ID = 1) ไปที่ cheese_blog (name = "Cheddar Talk")
>>> entry.save()
```

แต่การ update ManyToManyField จะทำงานแตกต่างไปนิดหน่อย เราจะต้องใช้ `add()` ดังตัวอย่าง

สมมติเราต้องการ add instance `joe` เป็นหนึ่งใน `authors` ของ instance `entry` (ID = 1)

```python
>>> from blogs.models import Author
>>> joe = Author.objects.create(name="Joe")
>>> entry.authors.add(joe)
```

เราสามารถ `add()` ที่ละหลายๆ instances เข้าไปก็ได้

```python
>>> john = Author.objects.create(name="John")
>>> paul = Author.objects.create(name="Paul")
>>> george = Author.objects.create(name="George")
>>> ringo = Author.objects.create(name="Ringo")
>>> entry.authors.add(john, paul, george, ringo)
```

## Retrieving objects

การ `SELECT` ข้อมูลออกมาจาก database นั้นทาง Django มี API ให้เราใช้งานได้ง่ายและสามารถทำ query ที่ซับซ้อนได้ด้วย โดยเราจะได้ instance ของ class `Queryset` มาใช้งาน

> A **QuerySet** represents a collection of objects from your database. It can have zero, one or many filters. **Filters** narrow down the query results based on the given parameters. In SQL terms, a QuerySet equates to a SELECT statement, and a filter is a limiting clause such as WHERE or LIMIT.

เราจะใช้งาน API ของ Django โดยการเรียกใช้ Manager ของ class `models.Model` การเข้าใช้งาน Manager จะเข้าถึงด้วย `.objects` ยกตัวอย่างถ้าเราต้องการ SELECT ข้อมูลทั้งหมดในตาราง `Entry`

```Python
>>> Entry.objects.all() # SELECT * FROM entry;
```

### Retrieving specific objects with filters

ทีนี้เรามาลองเพิ่ม filter conditions กันบ้าง (ซึ่งก็คือการ `SELECT` โดยใส่เงื่อนไขใน `WHERE`)

ยกตัวอย่างเช่นสมมติเราต้องการ QuerySet ของ blog entries ในปี 2010

```python
>>> Entry.objects.filter(pub_date__year=2010)
```

### Chaining filters

เราสามารถ chain method `filter()` และ `exclude()` ได้

**NOTE:** `exclude()` คือการใส่เงื่อนไขที่จะกรองข้อมูลออก ดังในตัวอย่างด้านล่างคือการกรองข้อมูล blog entries หลังจากวันปัจจุบันออก

```python
>>> Entry.objects.filter(headline__startswith="What").exclude(
...     pub_date__gte=datetime.date.today()
... ).filter(pub_date__gte=datetime.date(2005, 1, 30))
```

```sql
SELECT * FROM entry WHERE entry.headline LIKE "What%" AND entry.pub_date < CURRENT_TIME AND entry.pub_date >= "2005-01-30"
```

### Retrieving a single object with get()

การใช้ method `filter()` จะ return `QuerySet` ออกมาเสมอ แม้ว่า record ของข้อมูลที่ได้จากการ filter จะมีเพียง 1 record ก็จะได้ `QuerySet` ที่มีข้อมูล 1 แถวออกจาก ดังนั้นถ้าเราต้องการที่จะได้ instance ของ class นั้นมาใช้งานเลย (ไม่ใช่ `QuerySet`) เราจะต้องใช้ `get()`

```python
>>> one_entry = Entry.objects.get(pk=1)
>>> one_entry = Entry.objects.filter(pk=1).first()
>>> one_entry = Entry.objects.filter(pk=1)[0]
>>> # ทั้ง 3 บรรทัดนี้ให้ผลเหมือนกัน
```

### Limiting QuerySets

ในกรณีที่เราต้อง SELECT และต้องการ LIMIT ผลลัพธ์เราสามารถทำได้คล้ายๆ กับการ slice list ของ Python

```python
>>> Entry.objects.all()[:5] # LIMIT 5

>>> Entry.objects.all()[5:10] # OFFSET 5 LIMIT 5
```

**NOTE:** การใช้ negative index (`Entry.objects.all()[-1]`) นั้นไม่ support

## Comparing objects

การเปรียบเทียบ instance ของ model 2 ตัวว่าเป็นตัวเดียวกันไหม สามารถทำได้โดยใช้ `==`

```python
>>> some_entry == other_entry
>>> some_entry.id == other_entry.id
```

## Deleting objects

การลบข้อมูลออกจาก database สามารถทำได้โดยใช้ method `delete()`

ลบทีละตัว

```python
>>> e.delete()
(1, {'blog.Entry': 1})
```

ลบทีละหลายตัว

```python
>>> Entry.objects.filter(pub_date__year=2005).delete()
(5, {'blog.Entry': 5})
```

## Copying model instances
Django ไม่มี method สำหรับ copy model instances แต่เราสามารถทำการ copy และสร้าง instance ใหม่ที่มีทุก field เหมือนต้นฉบับได้โดยการ set ให้ instance.pk = None และ instnace._state.adding = True

ดังในตัวอย่าง

```python
blog = Blog(name="My blog", tagline="Blogging is easy")
blog.save()  # blog.pk == 1

blog.pk = None
blog._state.adding = True
blog.save()  # blog.pk == 2
```

## Performing raw SQL query

ในกรณีที่เราต้องการที่จะเขียน SQL query เอง (ORM ของ Django อาจจะไม่รองรับ ... ซึ่งผมแทบไม่เคยเจอเลยเพราะ ORM ของ Django นั้น advanced มากๆ)

เราสามารถทำได้โดยใช้ `raw()` method

> Manager.raw(raw_query, params=(), translations=None)

```python
# สมมติเรามี model Person
class Person(models.Model):
    first_name = models.CharField(...)
    last_name = models.CharField(...)
    birth_date = models.DateField(...)
```

```sh
# สามารถเขียน SELECT query ได้ดังนี้
>>> for p in Person.objects.raw("SELECT * FROM myapp_person"):
...     print(p)
...
John Smith
Jane Jones
```

```sh
# สมมติชื่อ field ไม่ตรงกับที่ประกาศใน model
>>> name_map = {"first": "first_name", "last": "last_name", "bd": "birth_date", "pk": "id"}
>>> Person.objects.raw("SELECT * FROM some_other_table", translations=name_map)
```

ผลลัพธ์ที่ได้จาก `raw()` เป็น instance ของ class `django.db.models.query.RawQuerySet` ซึ่งใช้งานคล้ายกับ `QuerySet` ที่เราคุ้นเคย

#### Create Jupiter NoteBook
```
    pip install django-extensions ipython jupyter notebook
    pip install ipython==8.25.0 jupyter_server==2.14.1 jupyterlab==4.2.2 jupyterlab_server==2.27.2
    pip install notebook==6.5.7 # ถ้าไม่ได้ให้ใช้ 6.5.6
```