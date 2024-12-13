# Generated by Django 5.1.1 on 2024-10-06 20:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="assignment",
            name="assignment_type",
            field=models.CharField(
                choices=[
                    ("HW", "HOMEWORK"),
                    ("EX", "EXAM"),
                    ("PRJ", "PROJECT"),
                    ("Q", "QUIZ"),
                ],
                max_length=20,
            ),
        ),
    ]