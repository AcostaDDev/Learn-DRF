import json

from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import Task

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

