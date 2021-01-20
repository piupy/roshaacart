from django.db import models

from django.utils import timezone

# Create your models here.

class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=30)
    desc = models.CharField(max_length=300)
    pub_date = models.DateField()
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to='shop/images', default="")


    def __str__(self):
        return self.product_name




class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50,default="")
    email = models.CharField(max_length=70,default="")
    phone = models.CharField(max_length=70,default="")
    desc = models.CharField(max_length=500,default="")


    def __str__(self):
        return self.name




class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000,default="")
    name = models.CharField(max_length=70,default="")
    email = models.CharField(max_length=70,default="")
    address = models.CharField(max_length=200,default="")
    city = models.CharField(max_length=70,default="")
    state = models.CharField(max_length=70,default="")
    zip_code = models.IntegerField(default=0)
    phone = models.CharField(max_length=20,default="")
    amount = models.IntegerField(default=0)

    def __str__(self):
        return self.name 



class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default=0)
    update_desc = models.CharField(max_length=5000,default="")
    timestamp = models.DateField(default=timezone.now)

    def __str__(self):
        return self.update_desc[0:10] + '...'



