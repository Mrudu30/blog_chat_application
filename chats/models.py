from django.db import models
from accounts.models import blogchatUser

# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name

# room field defining
class Room(models.Model):
    host = models.ForeignKey(blogchatUser,on_delete=models.SET_NULL,null=True)
    topic = models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=200)
    desc = models.TextField(null=True,blank=True)
    # many rooms can have many participants i.e. users
    participants = models.ManyToManyField(blogchatUser,related_name="participants",blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    # defines the way in templating or the order will be returned
    class Meta:
        ordering = ['-updated','-created']

    def __str__(self):
        return str(self.name)

class Message(models.Model):
    # custom user model
    # user can have many mesages (one to many relationship)
    user = models.ForeignKey(blogchatUser,on_delete=models.CASCADE)

    # on delete = models.SET_NULL means stay in db
    # on_delete = models.CASCADE means we delete every message in room
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.CharField(max_length=1000)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    # defines the way in templating or the order will be returned
    class Meta:
        ordering = ['-updated','-created']

    def __str__(self) -> str:
        return self.body[0:50]