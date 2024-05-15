from django.urls import path
from . import views as v

# blogs/ urls.
urlpatterns = [
    path("", v.blog_home, name="blog_home"),
    path("create-blog", v.blog_create, name="blog_create"),
    path("create-save", v.blog_saving, name="save_blog"),
]
