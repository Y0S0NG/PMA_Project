from django.contrib import admin
from .models import Course, Assignment, CourseFile, UserSchedule


admin.site.register(Course)
admin.site.register(CourseFile)
admin.site.register(Assignment)
admin.site.register(UserSchedule)

