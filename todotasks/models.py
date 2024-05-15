from django.db import models
# from django.contrib.auth.models import User
from accounts.models import blogchatUser
# Create your models here.

class TodoTask(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    color = models.CharField(max_length=10)
    due_date = models.DateField()
    user = models.ForeignKey(blogchatUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title