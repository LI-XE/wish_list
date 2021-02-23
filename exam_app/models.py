from __future__ import unicode_literals
from django.db import models
import re
from datetime import datetime
from django.contrib import messages
import bcrypt
# Create your models here.
class UserManager(models.Manager):
    def validate(self, data):
        errors = {}
        if len(data['name']) < 3:
            errors['name'] = "Name should be at least 3 characters!"
        if len(data['username']) < 3:
            errors['username'] = "Username should be at least 3 characters!"
        if data['date_hired'] == "":
            errors['date_hired'] = "Date Hired must be filled in."
        else:
            converted_date = datetime.strptime(data['date_hired'], '%Y-%m-%d')
            if converted_date > datetime.now():
                errors["date_hired"] = "Date Hired should be a past date!"
        username_check = self.filter(username= data['username'])
        if username_check:
            errors['username'] = "Username is already registered!"
        if len(data['password']) < 8:
            errors['password'] = "Password must be at least 8 characters."
        if data['password'] != data['confirm_pw']:
            errors['password'] = "Passwords do not match."
        return errors

    def authenticate(self, username, password):
        user = None
        try:
            user = User.objects.get(username = username)
        except:
            return False
        return bcrypt.checkpw(password.encode(), user.password.encode())

    def register(self, data):
        pw = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt()).decode()
        return self.create(
            name = data['name'],
            username = data['username'],
            date_hired = data['date_hired'],
            password = pw,
        )

class ProductManager(models.Manager):
    def validate(self, data):
        errors = {}
        if len(data['item']) < 1:
            errors['item'] = "Item should not be blank!"
        if len(data['item']) < 3:
            errors['item'] = "Item should be at least 3 characters!"
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    date_hired = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Product(models.Model):
    item = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(User, related_name="items")
    creator = models.ForeignKey(User, related_name="added_by", on_delete=models.CASCADE)
    objects = ProductManager()