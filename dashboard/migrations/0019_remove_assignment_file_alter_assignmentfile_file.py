# Generated by Django 5.1.1 on 2024-10-30 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0018_alter_assignment_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignment',
            name='file',
        ),
        migrations.AlterField(
            model_name='assignmentfile',
            name='file',
            field=models.FileField(upload_to='assignment_files/'),
        ),
    ]