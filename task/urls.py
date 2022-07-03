from django.urls import path

from . import views

urlpatterns = [
    path('create', views.CreateTaskController.as_view(), name="create-task"),
    path('change-status/<int:pk>', views.UpdateTaskStatusController.as_view(), name="change-status"),
    path('delete/<int:pk>', views.DeleteTaskController.as_view(), name="delete-task"),
    path('assign/<int:pk>', views.AssignTaskController.as_view(), name="assign-task"),
]