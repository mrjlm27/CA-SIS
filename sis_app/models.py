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
    enrollment_plan_choices =[
    ('Annually','Annually'),
    ('Bi-Annually', 'Bi-Annually'),
    ('Quarterly', 'Quarterly'),
    ]
    enrollment_plan = models.CharField(max_length=20, choices=enrollment_plan_choices,default='Annually')
    


def year_choices():
    return [(r,r) for r in range(1984, datetime.date.today().year+1)]

class Teacher(Account):
    t_name = models.CharField(max_length=128)


class Payment(models.Model):
    payment_s_account_id = models.ForeignKey(Student, on_delete=models.CASCADE, null = False)
    paymentdate_date = models.DateField(null = False)
    payment_amount = models.IntegerField(null = False)

    def getenrollmentplan(self):
        return self.payment_s_account_id.enrollment_plan

    def getstudentfirstname(self):
        return self.payment_s_account_id.student_firstname

    def getstudentlastname(self):
        return self.payment_s_account_id.student_lastname
    
    def outstandingbalance(self):
        annual = 37999
        biannual = 38998
        quarterly = 41663
        if self.payment_s_account_id.enrollment_plan == 'Annually':
            outstanding_balance = annual - self.payment_amount
            outstanding_balance = outstanding_balance
            return outstanding_balance 
        elif self.payment_s_account_id.enrollment_plan == 'Bi-Annually':
            return  biannual - self.payment_amount
        else:
            return  quarterly - self.payment_amount
    
    def test(self):
        return Payment.objects.values_list('payment_s_account_id','payment_amount')



     