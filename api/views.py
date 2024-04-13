import json

from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import Task

class TaskView(View):

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def get(self, request):
        tasks = list(Task.objects.values())
        if tasks:
            datos = {'message': 'Hecho!', 'tasks': tasks}
        else:
            datos = {'message': 'No hay tareas'}

        return JsonResponse(datos)
    
    def post(self, request):
        postr = json.loads(request.body)
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

    def put(self, request):
        pass
    def delete(self, request):
        pass

