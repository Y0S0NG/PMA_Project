from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from dashboard.models import UserSchedule

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

# @receiver(post_save, sender=User)
# def create_profile(sender, instance, **kwargs):
    

@receiver(post_delete, sender=Profile)
def delete_course_image_from_s3(sender, instance, **kwargs):
    # This ensures that the image file is deleted from S3
    if instance.image and instance.image.name != 'default.jpg':
        instance.image.delete(save=False)

#Ensures upon user creation, a user has their own schedule
@receiver(post_save, sender=User)
def create_user_schedule(sender, instance, created, **kwargs):
    if created:
        UserSchedule.objects.create(user=instance)
