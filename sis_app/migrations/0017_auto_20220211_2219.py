# Generated by Django 2.2 on 2022-02-11 14:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sis_app', '0016_auto_20220210_0052'),
    ]

    operations = [
        migrations.AddField(
            model_name='gradereport',
            name='filipino1',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='gradereport',
            name='filipino2',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='gradereport',
            name='filipino3',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='gradereport',
            name='filipino4',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='gradereport',
            name='language1',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='gradereport',
            name='language10',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='gradereport',
            name='language2',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='gradereport',
            name='language3',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='gradereport',
            name='language4',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='gradereport',
            name='language5',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='gradereport',
            name='language6',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='gradereport',
            name='language7',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='gradereport',
            name='language8',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='gradereport',
            name='language9',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='gradereport',
            name='math1',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='gradereport',
            name='math10',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='gradereport',
            name='math11',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='gradereport',
            name='math2',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='gradereport',
            name='math3',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='gradereport',
            name='math4',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='gradereport',
            name='math5',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='gradereport',
            name='math6',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='gradereport',
            name='math7',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='gradereport',
            name='math8',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='gradereport',
            name='math9',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='gradereport',
            name='penmanship1',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='gradereport',
            name='penmanship2',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='gradereport',
            name='penmanship3',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='gradereport',
            name='penmanship4',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='gradereport',
            name='readingreadiness1',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='gradereport',
            name='readingreadiness10',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='gradereport',
            name='readingreadiness11',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='gradereport',
            name='readingreadiness12',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='gradereport',
            name='readingreadiness13',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='gradereport',
            name='readingreadiness2',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='gradereport',
            name='readingreadiness3',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='gradereport',
            name='readingreadiness4',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='gradereport',
            name='readingreadiness5',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='gradereport',
            name='readingreadiness6',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='gradereport',
            name='readingreadiness7',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='gradereport',
            name='readingreadiness8',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='gradereport',
            name='readingreadiness9',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='gradereport',
            name='science1',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='gradereport',
            name='science2',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='gradereport',
            name='science3',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='gradereport',
            name='science4',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='gradereport',
            name='science5',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='gradereport',
            name='science6',
            field=models.IntegerField(default=None),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_birthday',
            field=models.DateField(default=datetime.date(2022, 2, 11)),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_signdate',
            field=models.DateField(default=datetime.date(2022, 2, 11)),
        ),
    ]
