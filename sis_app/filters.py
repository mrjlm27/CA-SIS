import django_filters

from .models import *

class StudentFilter(django_filters.FilterSet):
    class Meta:
        model = Student
        fields = {
            'student_lastname': ['icontains'],
        }

class EnrollmentStatusAndPaymentPlanFilter(django_filters.FilterSet):
    class Meta:
        model = Student
        fields = {
            'student_lastname': ['icontains'],
            'enrollment_status': ['icontains'],
            'student_payment_plan': ['icontains'],
        }