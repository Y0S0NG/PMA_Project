# Generated by Django 5.1.1 on 2024-11-15 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0029_assignmentfile_uploaded_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='userschedule',
            name='completed_assignments',
            field=models.ManyToManyField(related_name='user_schedules_complete', to='dashboard.assignment'),
        ),
    ]
