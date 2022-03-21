from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager

# class userType(models.Model):
#     Customer = 1
#     Seller = 2 
#     Types = ((Customer,'Customer'),(Seller,'Seller'))

class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=32,unique=True)
    mobile = models.CharField(max_length=14)
    is_verified = models.BooleanField(default=False)
    # email_token = models.CharField(max_length=100,null=True,blank=True)
    # forget_password = models.CharField(max_length=100,null=True,blank=True)
    # last_login_time = models.DateField(null=True,blank=True)
    # last_logout_time = models.DateField(null=True,blank=True)
    
    type = ((1,'seller'),(2,'buyer'))
    user_type = models.IntegerField(choices=type,default=1)
    
    objects= UserManager()
    USERNAME_FIELD = "email"
    
    REQUIRED_FIELDS = []
    # This is for django Adming Column 
    # class Meta:
    #     ordering = ("first_name","email","is_verified")
    def __str__(self):
        return self.first_name + " " + self.last_name


import time
import os

def user_directory_path(instance, filename):
    e = int(round(time.time() * 1000))
    file_extension = os.path.splitext(filename)[-1]
    nameImg = os.path.splitext(filename)[0]
    name = nameImg + str(e) + file_extension
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    
    return 'user/' + format(name) 

# class Image(models.Model):
    
#     User = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
#     image_path = models.ImageField(upload_to = user_directory_path,default=0)
#     image_name = models.CharField(max_length=100,default="Sorry")
    
#     # def __str__(self):
#     #     return self.image_name


from datetime import datetime
class BiddingTime(models.Model):
    bid_day = models.DateField(auto_now=False, auto_now_add=False)
    bid_start_time = models.TimeField(auto_now=False, auto_now_add=False)
    bid_end_time = models.TimeField(auto_now=False, auto_now_add=False)
    added_date = models.DateTimeField(auto_now=True, auto_now_add=False)
    
    def __str__(self):
        mydate = self.bid_day
        day = mydate.strftime("%d-%m-%Y")
        return day

class Category(models.Model):
    category_name = models.CharField(max_length=18)
    category_details = models.CharField(max_length=150)
    added_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    
    def __str__(self):
        return self.category_name

class Product(models.Model):
    creator = models.IntegerField()
    category = models.IntegerField()
    product_bid_time = models.IntegerField()
    min_bid_amount = models.FloatField()
    product_name = models.CharField(max_length=20)
    product_description = models.CharField(max_length=200)
    product_image_name = models.CharField(max_length=100)
    product_image_path =models.ImageField(upload_to=user_directory_path)
    added_date = models.DateTimeField(auto_now=True, auto_now_add=False)
    
    def __str__(self):
        return self.product_name

class BiddingAmount(models.Model):
    bidder_name = models.IntegerField()
    product_name = models.IntegerField()
    bid_amount = models.FloatField()
    

# class Relationship(models.Model):
#     creatorname = 