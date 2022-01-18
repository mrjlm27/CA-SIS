from email.policy import default
from django.db import models
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator



# Create your models here.

# class Student(models.Model):

def current_year():
    return datetime.date.today().year

def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)  

class Account(models.Model):
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=128)#passwords should be stored hashed 
    class Meta:
        abstract=True # Don't use this line if you want Contact to have its own table

class Student(Account):
    student_firstname = models.CharField(max_length=128)#
    student_lastname = models.CharField(max_length=128)#
    student_middlename = models.CharField(max_length=128, default="middlename")
    student_nickname = models.CharField(max_length=128, default="nickname")
    student_grade_level = models.CharField(max_length=128, blank=True)#
    status =[
    ('Not Enrolled','Not Enrolled'),
    ('Enrolled', 'Enrolled'),
    ]#
    enrollment_status = models.CharField(max_length=20, choices=status,default='Not Enrolled')#
    student_schoolyear_start=models.IntegerField(('year'), validators=[MinValueValidator(2000), max_value_current_year])#
    student_telno = models.CharField(max_length=128, default="None")
    student_address = models.CharField(max_length=300, null = False, default="cityx")
    student_religion = models.CharField(max_length=128, null = True, default="None")
    student_nationality = models.CharField(max_length=128, default="No nationality")
    student_hobbies = models.TextField(default = "None")
    student_likes = models.TextField(default = "None")
    student_dislikes = models.TextField(default = "None")
    


def year_choices():
    return [(r,r) for r in range(1984, datetime.date.today().year+1)]

class Teacher(Account):
    t_name = models.CharField(max_length=128)