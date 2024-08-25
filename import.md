import os
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
from service.models import *
from django.db.models import *
from django.db.models.functions import *
from datetime import date, time, datetime