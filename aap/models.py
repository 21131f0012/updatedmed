from django.db import models
from django.core.mail import send_mail
from django.conf import settings

# Create your models here.

class products(models.Model):
    id = models.AutoField(primary_key=True)
    medicine =models.CharField(max_length=200,null=True)
    price =models.FloatField(max_length=20,null=True)
    manufacture_date= models.DateField(null=True)
    expiry=models.DateField(null=True)
    quantity = models.IntegerField(default=0,null=True)
    

    

    def __str__(self):
        return self.medicine
    
    
    





    




