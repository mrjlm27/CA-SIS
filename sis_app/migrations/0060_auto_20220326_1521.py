# Generated by Django 3.0.2 on 2022-03-26 07:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sis_app', '0059_auto_20220326_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='school_year_end',
            field=models.IntegerField(error_messages={'invalid': 'Invalid'}, validators=[django.core.validators.MinValueValidator(2000)], verbose_name='year'),
        ),
    ]
