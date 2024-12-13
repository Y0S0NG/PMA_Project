# Generated by Django 5.1.1 on 2024-11-03 17:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0025_alter_coursefile_content_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="coursefile",
            name="content_type",
            field=models.CharField(
                choices=[
                    ("OTH", "Other"),
                    ("SYL", "Syllabus"),
                    ("SLD", "Slides"),
                    ("PAP", "Past Paper"),
                    ("SOL", "Exam Solution"),
                    ("HWK", "Homework"),
                ],
                max_length=3,
                null=True,
            ),
        ),
    ]
