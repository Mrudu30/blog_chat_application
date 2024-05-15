from django.urls import path
from . import views as v

urlpatterns = [
    path("", v.home, name="home"),
    path('room/<str:pk>/',v.room,name='room'),
    path('create-room/',v.create_room,name='create-room'),
    path('update-room/<str:pk>/',v.update_room,name='update-room'),
    path('delete-room/<str:pk>/',v.delete,name='delete-room'),
    path('profile/<str:pk>/',v.profile,name="profile"),
    path('delete-message/<str:pk>/',v.deleteMessage,name='delete-message'),
    path('update-message/<str:pk>/',v.editMessage,name='update-message'),
]
