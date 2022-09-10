from django.db import models

class SliderImage(models.Model):
    image=models.ImageField(upload_to='slider_images')
    created_at=models.DateTimeField(auto_now_add=True)
