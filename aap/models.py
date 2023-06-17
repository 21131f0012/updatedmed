from django.db import models
from django.core.mail import send_mail
from django.conf import settings

# Create your models here.

class products(models.Model):
    email = models.EmailField(max_length=100,default='@gmail.com')
    id = models.AutoField(primary_key=True)
    medicine =models.CharField(max_length=200,null=True)
    price =models.FloatField(max_length=20,null=True)
    manufacture_date= models.DateField(null=True)
    expiry=models.DateField(null=True)
    quantity = models.IntegerField(default=0,null=True)
    

    

    def __str__(self):
        return self.medicine
    


class Bill(models.Model):
    customer = models.CharField(max_length=50,null=False)
    products = models.ManyToManyField(products, through='BillProduct')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return self.customer

class BillProduct(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    product = models.ForeignKey(products, on_delete=models.CASCADE)
    quantity = models.IntegerField()


    def __str__(self):
        return self.bill
    
    
    





    




