from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.conf import settings
from django.core.files.storage import default_storage
from io import BytesIO
from django.core.files.base import ContentFile


# Create your models here.
'''
class User(models.Model):  
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return f"{self.name} \n {self.email}"
'''


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image.name != 'default.jpg':
            with default_storage.open(self.image.name, 'rb') as storage:
                img = Image.open(storage)
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size, Image.Resampling.LANCZOS)

                    in_memory_file = BytesIO()
                    img_format = img.format if img.format is not None else 'JPEG'
                    img.save(in_memory_file, format=img_format)
                    in_memory_file.seek(0)

                    # Ensure the image is saved back to storage
                    self.image.save(self.image.name, ContentFile(in_memory_file.getvalue()), save=True)

                # It's important to clear the buffer after use
                    in_memory_file.close()
