# Generated by Django 4.2.15 on 2024-10-06 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('course_code', models.CharField(max_length=20)),
                ('assignment_type', models.CharField(choices=[('HW', 'HOMEWORK'), ('EXM', 'EXAM'), ('PRJ', 'PROJECT'), ('Q', 'QUIZ')], max_length=20)),
                ('priority', models.IntegerField()),
                ('link', models.URLField()),
                ('due_date', models.DateField(auto_now_add=True, null=True)),
            ],
        ),
    ]
