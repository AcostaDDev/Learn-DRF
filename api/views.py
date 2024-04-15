import json

from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from .models import Task
from .serializers import TaskSerializer

class TaskView(View):

    @csrf_exempt                                            # Ignoramos la validacion de CSRF para que nos deje realizar la peticion POST
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def get(self, request, pk=0):

        if pk > 0:
            tasks = list(Task.objects.filter(id=pk).values())
            if tasks:
                task = tasks[0]
                datos = {'message': f'Consulta con id {task['id']}', 'task': task}
            else:
                datos = {'message' : f'No hay tareas con el id {pk}'}

        else:

            tasks = list(Task.objects.values())
            if tasks:
                datos = {'message': 'Hecho!', 'tasks': tasks}
            else:
                datos = {'message': 'No hay tareas'}

        return JsonResponse(datos)
    
    def post(self, request):
        postr = json.loads(request.body)        # Cargamos el cuerpo del json posteado --> Datos a insertar
        try: 
            task = Task.objects.create(
                title = postr['title'],
                description = postr['description'],
                complete = postr['complete']
            )
            datos = {'message': 'Datos insertados'}
        except:
            datos = {'message': 'Error al insertar datos'}
        return JsonResponse(datos)

    def put(self, request, pk=0):
        putr = json.loads(request.body)        # Cargamos el cuerpo del json posteado --> datos a insertar
        tasks = list(Task.objects.filter(id=pk).values())

        if tasks:
            task = Task.objects.get(id=pk)      # Coge el objeto para poder modificarlo, no el valor del mismo a diferencia del método get
            task.title = putr['title']
            task.description = putr['description']
            task.complete = putr['complete']
            task.save()
            datos = {'message': 'Datos actualizados'}
        else:
            datos = {'message' : f"No hay tareas con el id {pk}"}
        return JsonResponse(datos)

    def delete(self, request, pk=0):
        tasks = list(Task.objects.filter(id=pk).values())
        if tasks:
            Task.objects.filter(id=pk).delete()
            datos = {'message': 'Tarea eliminada'}
        else:
            datos = {'message' : f"No hay tareas con el id {pk}"}
        return JsonResponse(datos)

class TaskViewXML(View):
    
    def get(self, request):
        data = serializers.serialize("xml", Task.objects.all())
        return HttpResponse(data)
    

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    authentication_classes = [SessionAuthentication ,TokenAuthentication]
    #permission_classes = [IsAuthenticated]

    def get(self, request, format = None):
        content = {
            'user': str(request.user), # django.contrib.auth.User 
            'auth': str(request.auth), # None
        }
        return Response(content)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class( 
            data = request.data,
            context = {'request': request}
        )
        serializer.is_valid(raise_exception = True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user = user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })