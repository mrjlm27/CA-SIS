from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
import json
import datetime
from django.http import JsonResponse
from .models import *
from .forms import *
from .filters import *
from django.contrib.auth.models import User
import random
import string
from django.core.mail import send_mail



# def hello_world(request):
#     return render(request, 'sis_app/hello_world.html')
    

def StudentList(request):
    students = Student.objects.all()

    myFilter = StudentFilter(request.GET, queryset=students)
    students = myFilter.qs


    context = {'studentList' : students, 'myFilter': myFilter}
    return render(request,"sis_app/Student_List.html", context)

def studentForm(request,id=0):
    model = Student
    form_class = StudentForm
    if request.method == "GET":
        if id == 0: 
            form = StudentForm()
        else:
            student = Student.objects.get(pk=id)
            form = StudentForm(instance=student)
        return render(request,"sis_app/Student_Form.html",{'form':form})
    else:
        if id == 0:
            form = StudentForm(request.POST)
        else:
            student = Student.objects.get(pk=id)
            form = StudentForm(request.POST,instance=student)
        if form.is_valid():
            form.save()
        return redirect('/studentList')

def RegistrationList(request, pk = 0):
    if request.user.is_superuser:
        registrant_ids = list(Student.objects.values_list('pk', flat=True).order_by('pk'))
        user_ids = list(User.objects.exclude(is_superuser=True).values_list('pk', flat=True).order_by('pk'))
        view_registrant_ids = list(set(registrant_ids) - set(user_ids))

        students = Student.objects.filter(pk__in=view_registrant_ids)
        myFilter = StudentFilter(request.GET, queryset=students)
        students = myFilter.qs

        #transfer to GenerateAccount later
        
        context = {'studentList' : students, 'myFilter': myFilter}

        return render(request,"sis_app/Registration_List.html", context)
    else:
        return render(request,"sis_app/no_access.html")


def username_exists(username):
    return User.objects.filter(username=username).exists()

def GenerateAccount(request, id):
    # if request.user.is_superuser:
    if request.user.is_superuser:
   
        test = Student.objects.get(pk=id)

        while True:
            user_length = 10
            pass_length = 15
            username = ''.join(random.choices(string.ascii_uppercase + string.digits, k = user_length))
            password = ''.join(random.choices(string.ascii_lowercase + string.digits, k = pass_length))

            if username_exists(username) == False:
                user = User.objects.create_user(id = test.id, username = username, email = 'lennon2@thebeatles.com', password = password, first_name = str(test.student_firstname), last_name = test.student_lastname)
            
                send_mail(
                    'CAMELEAN ACADEMY SIS username and pass',
                    "Username: {}\nPassword: {}\nPLEASE CHANGE YOUR USERNAME AND PASSWORD UPON FIRST LOG-IN".format(username, password),
                    None,
                    ['elijahjustincallantalol@gmail.com'],#this is the recipient(change this to email of student later)
                    fail_silently=False,
                )

                return redirect("/RegistrationList")
                False
            else:   
                continue

        ##MAKE A SEPARATE PAGE FOR DISPLAYING USERNAME AND PASS OF EACH USER
    else:
        return render(request,"sis_app/no_access.html")##change this to redirect to loginpage
    # Create your views here.


def paymentForm(request,id=0):
    model = Payment
    form_class = PaymentForm
    if request.method == "GET":
        if id == 0: 
            form = PaymentForm()
        else:
            payment = Payment.objects.get(pk=id)
            form = PaymentForm(instance=payment)
        return render(request,"sis_app/Payment_Form.html",{'form':form})
    else:
        if id == 0:
            form = PaymentForm(request.POST)
        else:
            payment = Payment.objects.get(pk=id)
            form = PaymentForm(request.POST,instance=payment)
        if form.is_valid():
            form.save()
        return redirect('/paymentList')

def paymentList(request):
    payments = Payment.objects.all()

    myPFilter = PaymentFilter(request.GET, queryset=payments)
    payments = myPFilter.qs

    context = {'paymentList' : payments, 'myPFilter': myPFilter}
    return render(request,"sis_app/paymentList.html", context)