from django.db import models


class Result(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField()
    thumbnail = models.URLField()
    video_id = models.CharField(max_length=256)
    publish_time = models.DateTimeField()

    def __str__(self):
        return self.title
