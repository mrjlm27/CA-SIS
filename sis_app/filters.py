import django_filters

from .models import *

class StudentFilter(django_filters.FilterSet):
    class Meta:
        model = Student
        fields = {
            'student_lastname': ['icontains'],
        }