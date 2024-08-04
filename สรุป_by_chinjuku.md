# สรุป by Chinjuku
### CRUD in django abstraction api
- `create()` create data and add it to table
```py
    # ทำได้ 2 แบบ
    # 1.
    pd1 = Product(
        name="Philosopher's Stone (1997)",
        description="By J. K. Rowling.",
        remaining_amount=20,
        price=790
    )
    # 2.
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

### Concat() function
```py
    from django.db.models.functions import Concat
    customers = Customer.objects.annotate(full_name=Concat(F("first_name"), Value(' '), F("last_name")))
```

### Avg(), Sum(), Min(), Max() function
```py
    from django.db.models import *
    # Avg()
    pd = Product.objects.aggregate(avg=Avg("price"))
    print(pd)
    # Sum()
    cartitem = CartItem.objects.filter(cart__create_date__month=5).aggregate(sum=Sum('product__price'))
print(cartitem)
    # Min()
    cartitem = CartItem.objects.aggregate(min=Min('product__price'))
    # Max()
    cartitem = CartItem.objects.aggregate(max=Max('product__price'))
```

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
