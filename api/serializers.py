from rest_framework import serializers

from .models import Task

class TaskSerializer (serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        # fields = ('title', 'description', 'complete') --> A través de una tupla se le pasan los campos que queramos
        