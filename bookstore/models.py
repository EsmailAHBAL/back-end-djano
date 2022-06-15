
from email.policy import default
from sre_constants import CATEGORY
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import OneToOneField
from sqlalchemy import null

# Create your models here.

class Customer(models.Model):
    user=models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    email= models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    date_creation=models.DateField(auto_now_add=True)
    image=models.ImageField(blank=True,null=True,default="user.png")
    def __str__(self) -> str:
        return self.name

class Tag(models.Model):
    name_tag = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name_tag

class Book (models.Model):
    CATEGORY=(
        ('Drama','Drama'),
        ('Fantasy','Fantasy'),
         ('Horror','Horror'),
         ('Romance','Romance')   
    )
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    ISBN = models.CharField(max_length=200)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=120,choices=CATEGORY)
    description = models.CharField(max_length=120)
    tagId=models.ManyToManyField(Tag)
    date_creation = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title



class Order(models.Model):
    STATUS=(
        ('Pending','Pending'),
        ('In Progress','In Progress'),
         ('Out In Order','Out In Order'),
         ('delivered','delivered')   
    )
    
    customerId=models.ForeignKey(Customer, null=True,on_delete=models.SET_NULL)
    date_creation=models.DateField(auto_now_add=True)
    bookId=models.ForeignKey(Book, on_delete=models.SET_NULL,null=True)
    tagId=models.ManyToManyField(Tag)
    status = models.CharField(max_length=120,choices=STATUS)


