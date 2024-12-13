import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.core.files.storage import default_storage
from io import BytesIO
from django.core.files.base import ContentFile


class Course(models.Model):
    objects = None
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    instructor = models.CharField(max_length=200)
    description = models.TextField()
    course_image = models.ImageField(default='default.jpg', upload_to='course_pics')
    # schedules = models.ManyToManyField(Schedule)

    def __str__(self):
        # return f"{self.name} \n {self.instructor} \n {self.description}"
        return f"{self.name}"

    # Adjust image size
    def save(self,*args, **kwargs):
        if self.pk:
            old_course = Course.objects.get(pk=self.pk)
            old_image = old_course.course_image
            # Ensure it's not the default image and that the name has changed
            if old_image.name != self.course_image.name and old_image.name != 'default.jpg':
                old_image.delete(save=False)  # Delete the old image from S3

        super().save(*args, **kwargs)

        with default_storage.open(self.course_image.name, 'rb') as storage:
            img = Image.open(storage)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size, Image.Resampling.LANCZOS)

                in_memory_file = BytesIO()
                img_format = img.format if img.format is not None else 'JPEG'
                img.save(in_memory_file, format=img_format)
                in_memory_file.seek(0)

                # Ensure the image is saved back to storage
                self.course_image.save(self.course_image.name, ContentFile(in_memory_file.getvalue()), save=True)

                # It's important to clear the buffer after use
                in_memory_file.close()


class CourseFile(models.Model):
    FILE_TYPE_CHOICES = [
        ('txt', 'Text File'),
        ('pdf', 'PDF File'),
        ('jpg', 'JPG File')
    ]

    CONTENT_TYPE_CHOICES = [
        ('OTH', 'Other'),
        ('SYL', 'Syllabus'),
        ('SLD', 'Slides'),
        ('PAP', 'Past Paper'),
        ('SOL', 'Exam Solution'),
        ('HWK', 'Homework'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='files')
    keywords = models.CharField(max_length=255, help_text="Enter keywords separated by commas.", null = True)
    file_type = models.CharField(max_length=3, choices=FILE_TYPE_CHOICES)
    content_type = models.CharField(max_length=3, choices=CONTENT_TYPE_CHOICES, null = True)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='course-files/')
    filename = models.CharField(max_length=255, null=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    upload_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.get_file_type_display()} for {self.course.name}"

    def get_keywords_list(self):
        return self.keywords.split(',')


class Assignment(models.Model):
    ASSIGNMENT_TYPES = [
        ("HW", "HOMEWORK"),
        ("EX", "EXAM"),
        ("PRJ", "PROJECT"),
        ("Q", "QUIZ"),
    ]

    course_name = models.ForeignKey(Course, on_delete=models.CASCADE, null=True) #
    # course_name = models.CharField(max_length=100)
    description = models.TextField()
    assignment_type = models.CharField(max_length=20, choices=ASSIGNMENT_TYPES)
    priority = models.IntegerField(default=0)  # Set a default value for priority
    link = models.URLField(null=True, blank=True)
    due_date = models.DateField(null=True)
    keywords = models.CharField(max_length=40, blank=True, null=True) #Implmenting this
    date_submitted = models.DateTimeField(default=None)  # New field
    # schedules = models.ManyToManyField(Schedule)                  # Not sure if will need
    # course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.course_name}: \n {self.description} \n {self.assignment_type} \n {self.priority} \n {self.due_date}\n {self.keywords}"

    def set_course_name(self, course_name):
        self.course_name = course_name
        self.save()

    def set_description(self, description):
        self.description = description
        self.save()

    def set_course_code(self, course_code):
        self.course_code = course_code
        self.save()

    def set_assignment_type(self, assignment_type):
        self.assignment_type = assignment_type
        self.save()

    def set_priority(self, priority):
        self.priority = priority
        self.save()

    def set_link(self, link):
        self.link = link
        self.save()

    def set_due_date(self, due_date):
        self.due_date = due_date
        self.save()

    def is_due_soon(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.due_date <= now

    def set_keywords(self, keywords):
        self.keywords = keywords.split(',')
        self.save()


class UserSchedule(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    assignments = models.ManyToManyField(Assignment, related_name='user_schedules')
    completed_assignments = models.ManyToManyField(Assignment, related_name='user_schedules_complete')
    
    def __str__(self):
        return f"{self.user.username}'s Schedule"