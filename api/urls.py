from django.urls import include, path

from rest_framework import routers

from rest_framework.authtoken import views

from .views import TaskView, TaskViewXML, TaskViewSet, CustomAuthToken

router = routers.DefaultRouter()
router.register(r'tareas', TaskViewSet)

urlpatterns = [
    path('tasks/', TaskView.as_view(), name='task_list'),
    path('tasks/<int:pk>', TaskView.as_view(), name='task_detail'),
    path('tasks_xml/', TaskViewXML.as_view(), name='task_list_xml'),
    path('', include(router.urls)),
    path('api-token-auth/', CustomAuthToken.as_view()),
] 
