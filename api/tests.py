from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework import status

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import Task

class TaskAPITest(APITestCase):

    fixtures = ['tasks', 'user']
    
    def _authenticate(self):
        my_user = User.objects.get(username="david")      # Crea un usuario 'admin' con password 'admin' --> En la bbdd de testing
        token = Token.objects.create(user=my_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_get_tasks(self):
        #Task.objects.create(title=f'Tarea 1', description=f'Description 1', complete=False)
        #Task.objects.create(title=f'Tarea 2', description=f'Description 2', complete=True)

        self._authenticate()

        response = self.client.get('/api/tareas/')
        response_json = response.json()
        #print(response_json)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_json), 2)
        self.assertIsInstance(response_json, list)
        self.assertIsInstance(response_json[0], dict)
        self.assertIsInstance(response_json[1], dict)
 
    def test_post_tasks(self):
        self._authenticate()

        url = '/api/tareas/'
        data = {
            'title' : 'Test Task',
            'description' : 'Test Description',
            'complete' : False
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().title, 'Test Task')

    def test_put_tasks(self):
        Task.objects.create(title=f'Tarea 1', description=f'Description 1', complete=False)

        self._authenticate()

        url = '/api/tareas/1/'
        data = {
            'title' : 'Test Task',
            'description' : 'Test Description',
            'complete' : False
        }
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().title, 'Test Task')
        self.assertEqual(Task.objects.get().description, 'Test Description')
        self.assertEqual(Task.objects.get().complete, False)
