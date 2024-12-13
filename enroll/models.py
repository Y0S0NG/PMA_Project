from django.db import models
from django.contrib.auth.models import User
from dashboard.models import Course


class Enrollment(models.Model):
    ENROLL_STATUS = [
        ('ude', 'Under Examination'),
        ('rjt', 'Rejected'),
        ('apv', 'Approved')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    status = models.CharField(max_length=3, choices=ENROLL_STATUS, default='ude')

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.name} - Approved: {self.status}"
