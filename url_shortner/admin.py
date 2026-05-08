from django.contrib import admin
from .models import URLModel
from .models import Click
from .models import DayData

# Register your models here.
admin.site.register([URLModel, Click, DayData])