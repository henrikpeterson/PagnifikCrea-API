# Generated by Django 5.1.6 on 2025-03-17 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TrainingCourses', '0004_remove_course_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='duration',
            field=models.CharField(default='0 min', max_length=20),
        ),
        migrations.AlterField(
            model_name='modules',
            name='duration',
            field=models.CharField(default='0 min', max_length=20),
        ),
    ]
