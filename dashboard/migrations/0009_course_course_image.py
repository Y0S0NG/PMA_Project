# Generated by Django 5.1.1 on 2024-10-16 00:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0008_alter_assignment_due_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="course_image",
            field=models.ImageField(default="default.jpg", upload_to="course_pics"),
        ),
    ]
