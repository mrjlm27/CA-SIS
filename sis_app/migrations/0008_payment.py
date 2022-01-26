# Generated by Django 2.2 on 2022-01-23 10:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sis_app', '0007_delete_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paymentdate_date', models.DateField()),
                ('payment_amount', models.IntegerField()),
                ('payment_s_account_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sis_app.Student')),
            ],
        ),
    ]
