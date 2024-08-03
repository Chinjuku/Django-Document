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