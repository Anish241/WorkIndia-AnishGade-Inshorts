from typing import Any
from django.db import models
from django.contrib.auth import get_user_model
import datetime
# Create your models here.

User = get_user_model()


class Shorts(models.Model):
    category = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    publish_date = models.DateTimeField(default=datetime.datetime.now())
    content = models.CharField(max_length=500)
    actual_content_link = models.CharField(max_length=200)
    image = models.CharField(max_length=100,default=None)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)







