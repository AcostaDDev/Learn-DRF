from django.urls import path

from .views import TaskView

urlpatterns = [
    path('tasks/', TaskView.as_view(), name='task_list'),
    path('tasks/<int:pk>', TaskView.as_view(), name='task_detail'),
]
