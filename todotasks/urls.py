from django.urls import path
from . import views as v

urlpatterns = [
    path("", v.home, name="taskhome"),
    path("get-all-tasks/", v.get_tasks, name="get_all_tasks"),
    path("create-task/", v.create_tasks, name="create_task"),
    path("delete-task/<int:id>", v.delete_task, name="delete_task"),
    path("update-task/<int:id>", v.update_task, name="update_task"),
    path("get-task/<int:id>", v.get_task_id, name="get_task"),
]
