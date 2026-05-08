from django.db import models
import uuid
import datetime
from datetime import date
from django.utils import timezone
# Create your models here.

class URLModel(models.Model):
    long_link=models.CharField('Original Link', max_length=200)
    short_link=models.CharField('Modified Link', max_length=200)
    link_to= models.CharField('Link Destination', max_length=50)
    uuid=models.CharField('uuid', max_length=10, default=uuid.uuid4, editable=False)
    number_of_times_clicked=models.IntegerField('TImes Clicked', default=0)
    
class Click(models.Model):
    url_relation=models.ForeignKey(URLModel, on_delete=models.CASCADE, related_name="modified_link")
    time_clicked=models.DateField('Day Clicked')
    ip_address=models.GenericIPAddressField('IP Address')  
    

#Model to save seven consecutive days 
class DayData(models.Model):
    url_relation= models.ForeignKey(URLModel, on_delete=models.CASCADE, related_name='date_clicked')
    '''Stores the date of the latest click and stores the value linked to that date in this case our clicks'''
    day_date= models.DateField(default=None)
    day_value= models.CharField(max_length=20)
    


