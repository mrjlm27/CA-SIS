from email.policy import default
from time import timezone
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
    student_middlename = models.CharField(max_length=128)
    student_nickname = models.CharField(max_length=128)
    student_birthday = models.DateField()

    grade_levels = [
        ('Nursery','Nursery'),
        ('Kinder 1','Kinder 1'),
        ('Kinder 2', 'Kinder 2')
    ]
    student_grade_level = models.CharField(max_length=128, choices=grade_levels, default='Nursery')#
    status =[
    ('Not Enrolled','Not Enrolled'),
    ('Enrolled', 'Enrolled'),
    ]#
    enrollment_status = models.CharField(max_length=20, choices=status,default='Not Enrolled')#
    student_schoolyear_start=models.IntegerField(('year'), validators=[MinValueValidator(2000), max_value_current_year])#
    student_address = models.CharField(max_length=300)
    student_religion = models.CharField(max_length=128)
    student_nationality = models.CharField(max_length=128)
    student_hobbies = models.TextField(max_length=500)
    student_likes = models.TextField(max_length=500)
    student_dislikes = models.TextField(max_length=500)
    student_shm = models.TextField(max_length=500)
    student_allergies = models.TextField(max_length=500)
    student_sd = models.TextField(max_length=500)
    student_oconsiderations = models.TextField(max_length=500)
    student_guardianemail = models.EmailField(max_length = 254)
    student_f_firstname = models.CharField(max_length=128)
    student_f_lastname = models.CharField(max_length=128)
    student_f_middlename = models.CharField(max_length=128)
    student_f_telno = models.CharField(max_length=128)
    student_f_address = models.CharField(max_length=300)
    student_f_occupation = models.CharField(max_length=128)
    student_f_employer = models.CharField(max_length=128)
    student_f_oaddress = models.CharField(max_length=300)
    student_f_otelno = models.CharField(max_length=128)
    student_f_natureofbusiness = models.CharField(max_length=128)
    student_m_firstname = models.CharField(max_length=128)
    student_m_lastname = models.CharField(max_length=128)
    student_m_middlename = models.CharField(max_length=128)
    student_m_telno = models.CharField(max_length=128)
    student_m_address = models.CharField(max_length=300)
    student_m_occupation = models.CharField(max_length=128)
    student_m_employer = models.CharField(max_length=128)
    student_m_oaddress = models.CharField(max_length=300)
    student_m_otelno = models.CharField(max_length=128)
    student_m_natureofbusiness = models.CharField(max_length=128)
    student_sibling_name = models.CharField(max_length=300)
    student_sibling_gender = models.CharField(max_length=128)
    student_sibling_age = models.IntegerField()
    student_sibling_school=models.CharField(max_length=300)
    student_medexp = models.BooleanField(default = False)
    student_rules = models.BooleanField(default = False)
    student_accuracy = models.BooleanField(default = False)
    student_signedname = models.CharField(max_length=300)
    student_signdate = models.DateField(default=datetime.date.today())

    


def year_choices():
    return [(r,r) for r in range(1984, datetime.date.today().year+1)]

class Teacher(Account):
    t_name = models.CharField(max_length=128)