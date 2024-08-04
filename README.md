# Document สรุปวิชา Server-Side-Web
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

### Create/Save/Add Data into Model

```python
>>> from blogs.models import Blog
>>> b = Blog(name="Beatles Blog", tagline="All the latest Beatles news.")
>>> b.save()
```

ซึ่ง Django จะเป็นการ generate SQL command `INSERT` เมื่อเราสั่ง `save()`

### Saving changes to objects

ในการบันทึกการแก้ไข record ที่มีอยู่ใน database แล้วก็ใช้ `save()` เช่นเดียวกัน

```python
>>> b.name = "New name"
>>> b.save()
```

ซึ่ง Django จะเป็นการ generate SQL command `UPDATE` เมื่อเราสั่ง `save()`

### Saving ForeignKey and ManyToManyField fields

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

### Retrieving objects

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

### Comparing objects

การเปรียบเทียบ instance ของ model 2 ตัวว่าเป็นตัวเดียวกันไหม สามารถทำได้โดยใช้ `==`

```python
>>> some_entry == other_entry
>>> some_entry.id == other_entry.id
```

### Update objects
การแก้ไขข้อมูลจาก database สามารถทำได้โดยใช้ method `update()`
```python
    nickname = "Chinjuku"
    change = Blog.objects.filter(id=5).update(
        name=nickname
    )
```

### Deleting objects
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

## Field Lookups ( Week 4 )

[Django Doc](https://docs.djangoproject.com/en/5.0/topics/db/queries/#field-lookups)

ความสุดยอดของ Django คือการที่เราสามารถเขียน WHERE condition ในการ query ข้อมูลจาก database ได้อย่างง่ายดายโดยการกำหนด lookup type ใน methods `filter()`, `exclude()` และ `get()`

โดย format การกำหนด lookup type เป็นดังนี้ `field__lookuptype=value` (underscore 2 ตัว ระหว่าง ชื่อ field และ lookup type)

ในกรณีที่ต้องการ filter ด้วย foreign key จะต้องเติม `_id` ต่อท้ายชื่อ field ด้วย เช่น

```python
>>> Entry.objects.filter(blog_id=4)
```

[Field lookup reference](https://docs.djangoproject.com/en/5.0/ref/models/querysets/#field-lookups)

- exact
- iexact
- contains
```sql
-- Entry.objects.filter(headline__contains='Lennon')
SELECT ... WHERE headline LIKE '%Lennon%';
```
- icontains
```sql
-- Entry.objects.filter(headline__icontains='Lennon')
SELECT ... WHERE headline ILIKE '%Lennon%';
```
- startswith
- endswith
- in
```sql
-- Entry.objects.filter(headline__in=('a', 'b', 'c'))
SELECT ... WHERE headline IN ('a', 'b', 'c');
```
- gt, gte, lt, lte
```sql
SELECT ... WHERE id > 4;
```
- range
```sql
-- Entry.objects.filter(pub_date__range=(start_date, end_date))
SELECT ... WHERE pub_date BETWEEN '2005-01-01' AND '2005-03-31';
```
- date, year, month, day, week, week_day
```sql
-- Entry.objects.filter(pub_date__year=2005)
-- Entry.objects.filter(pub_date__year__gte=2005)
SELECT ... WHERE pub_date BETWEEN '2005-01-01' AND '2005-12-31';
SELECT ... WHERE pub_date >= '2005-01-01';
```
- isnull
```sql
-- Entry.objects.filter(pub_date__isnull=True)
SELECT ... WHERE pub_date IS NULL;
```
- regex
```sql
-- Entry.objects.get(title__regex=r"^(An?|The) +")
SELECT ... WHERE title ~ '^(An?|The) +'; -- PostgreSQL
```

**HINT:** ถ้าอยากลองพิมพ์ SQL query ออกมาดูสามารถทำได้โดยใช้ `.query`

```python
q = Entry.objects.filter(headline__in=('a', 'b', 'c'))

print(q.query)
```

## Lookups that span relationships

QuerySet API ของ Django ช่วยให้เราสามารถ query ข้อมูลที่เกี่ยวข้องกับตารางอื่นที่มี relationship กันได้อย่างสะดวก โดย Django จะไปจัดการเรื่องการ generate SQL JOINs ให้หลังบ้าน

ยกตัวอย่างเช่น ถ้าเราต้องการดึงข้อมูล Entry ทั้งหมดของ Blog ที่มี name = "Beatles Blog"

```python
>>> Entry.objects.filter(blog__name="Beatles Blog")
>>> Entry.objects.filter(blog__name__contains="Beatles Blog")
```

สังเกตว่าเราเพียงเอาชื่อ field foreign key มาต่อด้วยชื่อ field ของตารางที่อ้างอิงไปถึง โดยคั่นด้วย underscore 2 ตัว - `blog__name` - และยังสามารถต่อด้วย lookup type ได้อีก

นอกจากนั้นเรายังสามารถ query ข้อมูลไปกี่ต่อก็ได้ ดังตัวอย่าง

```python
Blog.objects.filter(entry__authors__name="Lennon")
Blog.objects.filter(entry__authors__name__isnull=True)
```

## Filters can reference fields on the model

ในกรณีที่เราต้องการเปรียบเทียบค่าของ field ใน model กับ field อื่นใน model เดียวกัน เราสามารถใช้ **F expressions** ได้ `F()`

```python
>>> from django.db.models import F
>>> Entry.objects.filter(number_of_comments__gt=F("number_of_pingbacks"))
>>> Entry.objects.filter(authors__name=F("blog__name")) # span relationships
```

โดย Django นั้น support การใช้ +, -, *, / ร่วมกับ `F()` ด้วย เช่น

```python
>>> Entry.objects.filter(number_of_comments__gt=F("number_of_pingbacks") * 2)
>>> Entry.objects.filter(rating__lt=F("number_of_comments") + F("number_of_pingbacks"))
```

## Complex lookups with Q objects

Keyword argument ที่ส่งเข้าไปใน method `filter()` ทุกตัวจะถูกเอามา generate เป็น `SELECT ... WHERE ... AND ...` เสมอ เช่น 

โดยปกติถ้าเราใช้ `,` ขั้นระหว่าง filter condition จะเป็นการ AND กัน

```sql
-- Entry.objects.filter(headline__contains='Lennon', pub_date__year=2005)
SELECT * FROM entry WHERE headline LIKE '%Lennon%' AND pub_date BETWEEN '2005-01-01' AND '2005-12-31';
```

ในกรณีที่เราต้องการทำการ query ที่ซับซ้อน อาจจะต้องการใช้ `OR` หรือ `NOT` ร่วมด้วย เราจะต้องใช้ `Q objects`

กรณี OR

```python
Entry.objects.filter(Q(headline__startswith="Who") | Q(headline__startswith="What"))
# SELECT ... WHERE headline LIKE 'Who%' OR headline LIKE 'What%'
```

กรณี NOT

```python
Entry.objects.filter(Q(headline__startswith="Who") | ~Q(pub_date__year=2005))
# SELECT ... WHERE headline LIKE 'Who%' OR pub_date NOT BETWEEN '2005-01-01' AND '2005-12-31'; 
```

กรณี nested conditions

```python
Poll.objects.get(
    Q(question__startswith="Who"),
    (Q(pub_date=date(2005, 5, 2)) | Q(pub_date=date(2005, 5, 6))),
)
```

แปลงเป็น SQL

```sql
SELECT * from polls WHERE question LIKE 'Who%' 
    AND (pub_date = '2005-05-02' OR pub_date = '2005-05-06')
```

## Week 5
## Query Expression ( Week 5 )
ORM ของ Django นั้น support การใช้งาน function ในการคำนวณ (+, -, *, /) การ aggregate ต่างๆ เช่น SUM(), MIN(), MAX(), COUNT(), AVG() และการทำ Subquery
#### Order by function (Sorting)
```py
    from django.db.models.functions import Length
    # Expressions can also be used in order_by(), either directly
    >>> Company.objects.order_by(Length("name").asc()) # ASC
    >>> Company.objects.order_by("-name") # DESC
```
เปิด Django shell จากนั้นสร้างแถวข้อมูลด้วยคำสั่ง

```python
>>> from company.models
>>> Company.objects.create(name="Company AAA", num_employees=120, num_chairs=150, num_tables=60)
>>> Company.objects.create(name="Company BBB", num_employees=50, num_chairs=30, num_tables=20)
>>> Company.objects.create(name="Company CCC", num_employees=100, num_chairs=40, num_tables=40)
```

**ลองทดสอบคำสั่งด้านล่างนี้ดู แล้วดูสิว่าได้ผลลัพธ์เป็นอย่างไร**

```python
>>> from company.models import Company
>>> from django.db.models import Count, F, Value
>>> from django.db.models.functions import Length, Upper
>>> from django.db.models.lookups import GreaterThan

# Find companies that have more employees than chairs.
>>> Company.objects.filter(num_employees__gt=F("num_chairs"))

# Find companies that have at least twice as many employees as chairs.
>>> Company.objects.filter(num_employees__gt=F("num_chairs") * 2)

# Find companies that have more employees than the number of chairs and tables combined.
>>> Company.objects.filter(num_employees__gt=F("num_chairs") + F("num_tables"))

# How many chairs are needed for each company to seat all employees?
>>> company = (
...     Company.objects.filter(num_employees__gt=F("num_chairs"))
...     .annotate(chairs_needed=F("num_employees") - F("num_chairs"))
...     .first()
... )
>>> company.num_employees
50
>>> company.num_chairs
30
>>> company.chairs_needed
20

# Create a new company using expressions.
>>> company = Company.objects.create(name="Google", ticker=Upper(Value("goog")))
# Be sure to refresh it if you need to access the field.
>>> company.refresh_from_db()
>>> company.ticker
'GOOG'

# Expressions can also be used in order_by(), either directly
>>> Company.objects.order_by(Length("name").asc())
>>> Company.objects.order_by(Length("name").desc())

# Lookup expressions can also be used directly in filters
>>> Company.objects.filter(GreaterThan(F("num_employees"), F("num_chairs")))
# or annotations.
>>> Company.objects.annotate(
...     need_chairs=GreaterThan(F("num_employees"), F("num_chairs")),
... )
```

## Aggregate expression

สำหรับ tutorial นี้ให้ทำตามขั้นตอนนี้ 

1. สร้าง app ใหม่ชื่อ `books` ใน project `week5_tutorial` อันเดิม
2. เพิ่ม app books ใน `settings.py`
3. แก้ไขไฟล์ `/books/models.py` และเพิ่ม code ด้่านล่างลงไป โดย models เหล่านี้เราจะใช้ในการทำ tutorial นี้กัน
4. `makemigrations` และ `migrate`

```python
from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()


class Publisher(models.Model):
    name = models.CharField(max_length=300)


class Book(models.Model):
    name = models.CharField(max_length=300)
    pages = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField()
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    pubdate = models.DateField()


class Store(models.Model):
    name = models.CharField(max_length=300)
    books = models.ManyToManyField(Book)
```

ทำการ import ข้อมูลเข้าตารางทั้งหมดด้วย SQL ในไฟล์ `books.sql`


**ลองทดสอบคำสั่งด้านล่างนี้ดู แล้วดูสิว่าได้ผลลัพธ์เป็นอย่างไร**

```python
>>> from books.models import Book
# Total number of books.
>>> Book.objects.count()
59

# Total number of books with publisher=Penguin Books
>>> Book.objects.filter(publisher__name="Penguin Books").count()
20

# Average price across all books, provide default to be returned instead
# of None if no books exist.
>>> from django.db.models import Avg
>>> Book.objects.aggregate(Avg("price", default=0))
{'price__avg': Decimal('9.7018644067796610')}

# Max price across all books, provide default to be returned instead of
# None if no books exist.
>>> from django.db.models import Max
>>> Book.objects.aggregate(Max("price", default=0))
{'price__max': Decimal('14.99')}

# All the following queries involve traversing the Book<->Publisher
# foreign key relationship backwards.

# Each publisher, each with a count of books as a "num_books" attribute.
>>> from books.models import Publisher
>>> from django.db.models import Count
>>> pubs = Publisher.objects.annotate(num_books=Count("book"))
>>> pubs
<QuerySet [<Publisher: BaloneyPress>, <Publisher: SalamiPress>, ...]>
>>> pubs[0].num_books
20

# Each publisher, with a separate count of books with a rating above and below 4
>>> from django.db.models import Q
>>> above = Publisher.objects.annotate(above_4=Count("book", filter=Q(book__rating__gt=4)))
>>> below = Publisher.objects.annotate(below_4=Count("book", filter=Q(book__rating__lte=4)))
>>> above[0].above_4
16
>>> below[0].below_4
4

# The top 5 publishers, in order by number of books.
>>> pubs = Publisher.objects.annotate(num_books=Count("book")).order_by("-num_books")[:5]
>>> pubs[0].num_books
39
```
# Model Relationships

## Many-to-one relationships

สำหรับการนิยาม Many-to-one Relationships จะใช้การประกาศ ForeignKey เป็น field ใน models

ต่อเนื่องจากตัวอย่าง `books/models.py` ใน model `Book` จะเห็นว่ามีการประกาศ ForeignKey เก็บ `publisher_id` ซึ่งชี้ไปยัง instance ใน model `Publisher`

```python
# /books/models.py
...
class Publisher(models.Model):
    name = models.CharField(max_length=300)

class Book(models.Model):
    name = models.CharField(max_length=300)
    pages = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField()
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    pubdate = models.DateField()
...
```

สมมติเราจะสร้าง book เล่มใหม่ที่มีการ FK ไปหา publisher "Penguin Books"

```python
>>> from books.models import Publisher, Book
>>> from datetime import datetime
# Get the publisher instance
>>> penguin_pub = Publisher.objects.get(name="Penguin Books")

# Create a new book
>>> book = Book.objects.create(
    name="Web Programming is HARD",
    pages=200,
    price=10.00,
    rating=4.5,
    publisher=penguin_pub,
    pubdate=datetime.now().date()
)
>>> book
<Book: Book object (61)>
>>> book.publisher.name
'Penguin Books'
>>> book.publisher.id
1
```

ในกรณีที่เราต้องการรายการ book ทั้งหมดที่เกี่ยวข้องกับ publisher "Penguin Books" สามารถทำได้ดังนี้

```python
>>> from books.models import Publisher, Book
# Get the publisher instance
>>> penguin_pub = Publisher.objects.get(name="Penguin Books")

# Get all books published by "Penguin Books"
>>> books = penguin_pub.book_set.all()
<QuerySet [<Book: Book object (2)>, <Book: Book object (3)>, <Book: Book object (4)>, <Book: Book object (5)>, <Book: Book object (6)>, <Book: Book object (7)>, <Book: Book object (8)>, <Book: Book object (9)>, <Book: Book object (10)>, <Book: Book object (11)>, <Book: Book object (12)>, <Book: Book object (13)>, <Book: Book object (14)>, <Book: Book object (15)>, <Book: Book object (16)>, <Book: Book object (17)>, <Book: Book object (18)>, <Book: Book object (19)>, <Book: Book object (20)>, <Book: Book object (21)>, '...(remaining elements truncated)...']>

# How may books?
>>> penguin_pub.book_set.count()
21

# Get top 10 best rating books
>>> penguin_pub.book_set.order_by("-rating")[:10]
<QuerySet [<Book: Book object (14)>, <Book: Book object (4)>, <Book: Book object (15)>, <Book: Book object (9)>, <Book: Book object (12)>, <Book: Book object (3)>, <Book: Book object (8)>, <Book: Book object (18)>, <Book: Book object (61)>, <Book: Book object (10)>]>

# Get books with name starting with "The"
>>> penguin_pub.book_set.filter(name__startswith="The")
<QuerySet [<Book: Book object (2)>, <Book: Book object (6)>, <Book: Book object (9)>, <Book: Book object (15)>, <Book: Book object (18)>]>

# Get only ids
>>> penguin_pub.book_set.filter(name__startswith="The").values_list("id", flat=True)
<QuerySet [2, 6, 9, 15, 18]>

# Get id and name
>>> penguin_pub.book_set.filter(name__startswith="The").values("id", "name")
<QuerySet [{'id': 2, 'name': 'The Great Gatsby'}, {'id': 6, 'name': 'The Catcher in the Rye'}, {'id': 9, 'name': 'The Odyssey'}, {'id': 15, 'name': 'The Hobbit'}, {'id': 18, 'name': 'The Hitchhiker Guide to the Galaxy'}]>
```

สมมติว่าเราต้องการต้นหาจากทางฝั่ง book บ้าง ถ้าเราต้องหนังสือที่ rating >= 4.5 และ published โดยสำนักพิมพ์ "Oxford University Press"

```python
>>> from books.models import Book

>>> results = Book.objects.filter(publisher__name="Oxford University Press", rating__gte=4.5)
>>> results
<QuerySet [<Book: Book object (24)>, <Book: Book object (27)>, <Book: Book object (30)>, <Book: Book object (33)>, <Book: Book object (44)>, <Book: Book object (56)>]>
```

หรือจะ filter จากทางฝั่ง publisher ก็ได้

```python
>>> from books.models import Publisher
>>> Publisher.objects.filter(book__id=20)
<QuerySet [<Publisher: Publisher object (1)>]>

>>> Publisher.objects.filter(book__pubdate='1967-05-30')
<QuerySet [<Publisher: Publisher object (1)>]>
# SELECT "books_publisher"."id", "books_publisher"."name" FROM "books_publisher" INNER JOIN "books_book" ON ("books_publisher"."id" = "books_book"."publisher_id") WHERE "books_book"."pubdate" = 1967-05-30
```

## One-to-one Relationships

เรามาเพิ่มความสัมพันธ์แบบ one-to-one ให้กับตารางใน database ของเรากัน

แก้ไขเพิ่ม code ด้านล่างนี้ในไฟล์ `/books/models.py`

```python
...
# เพิ่มไว้ล่างสุดเลยนะครับ
class StoreContact(models.Model):
    mobile = models.CharField(max_length=20)
    email = models.EmailField(max_length=50, blank=True, null=True)
    address = models.TextField()
    store = models.OneToOneField(Store, on_delete=models.CASCADE)
```

เรามาสร้างเพิ่ม store contact กันสำหรับ "KMITL Book Store"

```python
>>> from books.models import Store, StoreContact
# Get KMITL Book Store
>>> store = Store.objects.get(name="KMITL Book Store")
# Create contact information
>>> contact = StoreContact(
    mobile="021113333",
    email="book_shop@it.kmitl.ac.th",
    address="KMITL",
    store=store
)
>>> contact.save()
```

การเข้าถึงข้อมูล สามารถทำได้จากทั้ง 2 ฝั่ง

```python
>>> contact.store
<Store: Store object (2)>

>>> store.storecontact
<StoreContact: StoreContact object (1)>

# สามารถ filter ได้คล้ายกับ one-to-many
>>> Store.objects.filter(storecontact__mobile="021113333")
<QuerySet [<Store: Store object (2)>]>
```

## Many-to-many Relationships

จะเห็นได้ว่า model Book และ Author มีความสัมพันธ์กันแบบ many-to-many

```python
class Author(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

...

class Book(models.Model):
    name = models.CharField(max_length=300)
    pages = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField()
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    pubdate = models.DateField()
```

เมื่อเราสั่ง `python manage.py migrate` Django จะทำการสร้างตารางกลางให้อัตโนมัตื อย่างในกรณีนี้จะมีตาราง `books_book_author` ถูกสร้างขึ้นมา

สำหรับการเพิ่ม author ให้กับ book

```python
>>> from books.models import Book, Author
>>> a1 = Author.objects.get(pk=1)
>>> a2 = Author.objects.get(pk=2)

>>> book = Book.objects.get(pk=10)
>>> book.authors.add(a1, a2)

>>> book.authors.all()
<QuerySet [<Author: Author object (5)>, <Author: Author object (1)>, <Author: Author object (2)>]>
```

สำหรับการเพิ่ม book ใหม่ให้กับ author

```python
>>> from books.models import Book, Author
>>> b1 = Book.objects.get(pk=11)
>>> b2 = Book.objects.get(pk=12)

>>> author = Author.objects.get(pk=10)
>>> author.book_set.add(b1, b2)

>>> author.book_set.all()
<QuerySet [<Book: Book object (11)>, <Book: Book object (12)>, <Book: Book object (19)>, <Book: Book object (20)>, <Book: Book object (30)>, <Book: Book object (50)>]>
```

สามารถทำการ filter ได้จากทั้ง 2 ฝั่งเช่นเดียวกับ one-to-one และ one-to-many

```python
>>> Book.objects.filter(authors__name="F. Scott Fitzgerald")
<QuerySet [<Book: Book object (51)>, <Book: Book object (2)>, <Book: Book object (21)>, <Book: Book object (31)>, <Book: Book object (10)>]>

>>> Author.objects.filter(book__name="Crime and Punishment")
<QuerySet [<Author: Author object (5)>, <Author: Author object (1)>, <Author: Author object (2)>]>
```

สามารถทำการ ยกเลิก ความสัมพันธ์ ได้โดยใช้ `remove()` หรือ `clear()` ถ้าต้องการลบความสัมพันธ์ทั้งหมด

```python
>>> book = Book.objects.get(pk=10)

>>> book.authors.remove(a1)
>>> book.authors.all()
<QuerySet [<Author: Author object (2)>, <Author: Author object (5)>]>

>>> book.authors.clear()
>>> book.authors.all()
<QuerySet []>
```

# สรุป by Chinjuku
### CRUD in django abstraction api
- `create()` create data and add it to table
```py
    company = Company.objects.create(
        name="sss", email="sss@gmail.com"
    )
    company.save()
```
- `all(), get(), filter() etc..` query data to Queryset
    - filter() คัดกรองหลายตัว
    - all() เอามาทั้งหมด
    - get() เอามาตัวเดียว / ตัวที่เป็นเอกลักษณ์ ex. primarykey
```py
    pd1 = Product.objects.filter(price__gte=5000, categories__name="Information Technology").first()
    pd2 = Product.objects.get(pk=2)
    pd3 = Product.objects.all()
```
- `update()` to update data / can update many data
```py
    pd1 = Product.objects.filter(price__gte=5000).update(
        product_name="rexx",
        pub_date="brabra"
    )
    pd1.save()
```
- `delete()` to delete data / can delete many data
```py
    pd1 = Product.objects.filter(price__gte=5000).delete()
```

### การสร้าง Models Foreignkey field **(on_delete)
```py
    author = models.ForeignKey(Author, on_delete = models.CASCADE)
```
มี 4 แบบ 
- SET_NULL -> ถ้า foreignkey ถูกลบตัว ตัวที่ถูก SET_NULL จะถูก set เป็น null ทันที
- CASCADE -> ถูกลบตาม foreignkey ที่ถูกลบ
- PROTECT -> ถ้า foreignkey ถูกลบตัวที่ถูก set PROTECT จะไม่ถูกลบตาม
- DO_NOTHING -> ถ้า foreignkey ถูกลบตัวที่ถูก set DO_NOTHING จะไม่เกิดไรขึ้นเลย

### Field look up range (__range)
```py
    # Entry.objects.filter(pub_date__range=(start_date, end_date))
    from datetime import datetime
    entries = Entry.objects.filter(pub_date__range=(datetime(2023, 4, 4), datetime(2024, 5, 6)))
```

### Field look up (date, year, month, day, week, week_day)
```py
    Entry.objects.filter(pub_date__year=2005)
    Entry.objects.filter(pub_date__month=5)
```

### first() Function
เป็น functoion การดึงข้อมูลออกมาเฉพาะตัวแรกที่เจอ
```py
    company = Company.object.filter(price__gt=5).first()
    print(company.price) # 6
```

### How to print QuerySet
1. Change Queryset to list
```py
    from django.db.models import Count, F, Value
    payments = Payment.objects.annotate(news=F("id"))
    for pm in payments:
        print(pm.news)
```
2. Change Queryset to dict
```py
    ## .values() function change queryset to dict
    payments = Payment.objects.all().values("name", "id", "price")
    for pm in payments:
        print(pm["id"] + " " + pm["price"])
```

### การเข้าถึง foreignkey บน django function
1. ตอน Query จาก Models ``(Lookups that span relationships)``
```py
    ## ใช้ __ แทนการ . เข้าไปใน foreign key
    movies = Movie.objects.all(author__name__in = ("s", "l")).values("name", "id", "price")
    entry = Entry.objects.filter(blog__name__contains="Beatles Blog")
    # isnull หาว่าสิ่งที่เรา filter นั้นเป็น null
    blogs = Blog.objects.filter(entry__authors__name__isnull=True)
```
2. ตอน loop print เป็นรายตัว
```py
    # Print list (Queryset)
    for pm in payments:
        print(pm.author.name)
    # Print dict (Queryset)
    for pm in payments:
        print(pm["author"]["name"])
```

### Function .annotate()
`annotate()` is function to create new field to use
```py
    from django.db.models.lookups import GreaterThan
    company = (
        Company.objects.filter(num_employees__gt=F("num_chairs"))
        .annotate(chairs_needed=F("num_employees") - F("num_chairs"))
        .first()
    )
    print(company.chairs_needed)
```
