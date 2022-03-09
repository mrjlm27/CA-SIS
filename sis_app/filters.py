from warnings import filters
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
        # payment_s_account_id__student_lastname = filters.CharFilter(label='Article')
        fields = {
            'payment_s_account_id__student_lastname': ['icontains'],
        }
    # def __init__(self, *args, **kwargs):
    #     super(PaymentFilter, self).__init__(*args, **kwargs)
    #     self.filters['payment_s_account_id__student_lastname'].extra.update(
    #     {'empty_label': 'All Manufacturers'})
    

class EnrollmentStatusAndPaymentPlanFilter(django_filters.FilterSet):
    class Meta:
        model = Student
        fields = {
            'student_lastname': ['icontains'],
            'enrollment_status': ['iexact'],
            'student_enrollment_plan': ['iexact'],
        }

class StudentDeleteFilter(django_filters.FilterSet):
    class Meta:
        model = Student
        fields = {
            'student_schoolyear_start': ['icontains'],
        }