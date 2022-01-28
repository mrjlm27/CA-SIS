import django_filters

from .models import *

class StudentFilter(django_filters.FilterSet):
    class Meta:
        model = Student
        fields = {
            'student_lastname': ['icontains'],
        }

# class PaymentFilter(django_filters.FilterSet):
#     payment_s_account_id__student_lastname = django_filters.CharFilter(label='Student Last Name')

class PaymentFilter(django_filters.FilterSet):
    class Meta:
        model = Payment
        fields = {
            'payment_s_account_id__student_lastname': ['icontains'],
        }
    

class EnrollmentStatusAndPaymentPlanFilter(django_filters.FilterSet):
    class Meta:
        model = Student
        fields = {
            'student_lastname': ['icontains'],
            'enrollment_status': ['iexact'],
            'student_enrollment_plan': ['iexact'],
        }
