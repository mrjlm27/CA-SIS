# Generated by Django 2.2 on 2022-01-24 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sis_app', '0006_payments'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='payment_plan',
            field=models.CharField(default='Annually', max_length=128),
        ),
    ]
