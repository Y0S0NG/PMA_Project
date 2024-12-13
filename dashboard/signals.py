
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Course, CourseFile
from django.db.models.signals import post_save
from .models import Assignment, UserSchedule
from enroll.models import Enrollment

@receiver(post_delete, sender=Course)
def delete_course_image_from_s3(sender, instance, **kwargs):
    # This ensures that the image file is deleted from S3
    if instance.course_image and instance.course_image.name != 'default.jpg':
        instance.course_image.delete(save=False)


@receiver(post_delete, sender=CourseFile)
def delete_course_file_from_s3(sender, instance, **kwargs):
    # This ensures that the course file is deleted from S3
    if instance.file:
        instance.file.delete(save=False)


@receiver(post_save, sender=Assignment)
def update_user_schedules_on_assignment_addition(sender, instance, created, **kwargs):
    if created:
        course = instance.course_name

        enrollments = Enrollment.objects.filter(course=course, status='apv')
        enrolled_users = {enrollment.user for enrollment in enrollments}
        enrolled_users.add(course.owner)

        for user in enrolled_users:
            user_schedule, _ = UserSchedule.objects.get_or_create(user=user)
            user_schedule.assignments.add(instance)
            user_schedule.save()