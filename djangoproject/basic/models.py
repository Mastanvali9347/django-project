from django.db import models
from django.contrib.auth.hashers import make_password, check_password
class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name
class StudentNew(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name
class Users(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=200)
    email = models.EmailField(unique=True)

    # Password hashing
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    # Password checking
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.username
