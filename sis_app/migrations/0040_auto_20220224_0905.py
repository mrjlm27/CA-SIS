# Generated by Django 3.0.2 on 2022-02-24 01:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sis_app', '0039_merge_20220224_0857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='student_birthday',
            field=models.DateField(default=datetime.date(2022, 2, 24)),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_signdate',
            field=models.DateField(default=datetime.date(2022, 2, 24)),
        ),
    ]
