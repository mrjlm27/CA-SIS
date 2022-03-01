# Generated by Django 2.2 on 2022-02-12 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sis_app', '0021_gradereport_sem_average'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gradereport',
            name='filipino_grade',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='gradereport',
            name='language_grade',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='gradereport',
            name='mathematics_grade',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='gradereport',
            name='penmanship_grade',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='gradereport',
            name='reading_grade',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='gradereport',
            name='science_grade',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='gradereport',
            name='sem_average',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
    ]