from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Hobby(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# main user class defined
class blogchatUser(AbstractUser):
    # saving name of the user image
    user_image = models.CharField(max_length=100)

    # other fields
    dob = models.DateField(null=True, blank=True)
    hobbies = models.ManyToManyField(Hobby, related_name='users')
    mobile_number = models.CharField(max_length=15, blank=True)

    # constraints to make a user unique
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['email'], name='unique_email_constraint'),
            models.UniqueConstraint(fields=['username'], name='unique_username_constraint'),
        ]

    # groups and permissions are the needed fields of a user in django
    # this creates custom blog chat user group and permission table
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='blogchat_users_groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='blogchat_users_permissions'
    )

    # what will this class return on call.
    def __str__(self):
        return self.username