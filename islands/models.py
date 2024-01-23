from django.db import models
from django.utils import timezone


# Create your models here.

class BaseModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True


class User(BaseModel):
    user_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    class Meta:
        db_table = 'user'
        app_label = 'islands'


class Island(BaseModel):
    longitude = models.FloatField()
    latitude = models.FloatField()
    island_area = models.FloatField()
    detected_time = models.DateTimeField()

    class Meta:
        db_table = 'island'
        app_label = 'islands'


class Comment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    island = models.ForeignKey(Island, on_delete=models.CASCADE)
    comment_text = models.TextField()

    class Meta:
        db_table = 'comment'
        app_label = 'islands'


class MediaAttachment(BaseModel):
    MEDIA_TYPES = (
        ('image', 'Image'),
        ('video', 'Video'),
    )

    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES)
    media_url = models.URLField()

    class Meta:
        db_table = 'media_attachment'
        app_label = 'islands'
