from django.db import models
from chats.models import Topic
from accounts.models import blogchatUser
from datetime import datetime

# Create your models here.
class Blog(models.Model):
    # one blog can have many topics
    topic = models.ManyToManyField(Topic)
    title = models.CharField(max_length=100)
    images = models.CharField(max_length=1000)
    content = models.TextField()
    # one blog will have one user id only. but user can have many blogs.
    user = models.ForeignKey(blogchatUser,on_delete=models.SET_NULL,null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated','-created']

    def __str__(self) -> str:
        return self.title