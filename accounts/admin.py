from django.contrib import admin
from . import models as m

# Register your models here.
admin.site.register(m.blogchatUser)
admin.site.register(m.Hobby)