# Generated by Django 5.1.1 on 2024-10-15 23:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0004_remove_assignment_course_name_assignment_course"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="assignment",
            name="course_code",
        ),
        migrations.AlterField(
            model_name="assignment",
            name="link",
            field=models.URLField(null=True),
        ),
    ]