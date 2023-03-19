from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Task

import json 

class TaskTests(APITestCase):

    def setUp(self):
        Task.objects.create(name='Sample')

    def test_create_task(self):
        url = reverse('task-list') + '?format=json'
        data = {
            'name': 'Write tests first',
            'is_done': False
        }
        response = self.client.post(url, 
                                   data, 
                                   format='json',
                                   follow=True
                                )
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(Task.objects.count(), 2)
        self.assertTrue(Task.objects.filter(name=data['name']).exists())

    def test_list_task(self):
        url = reverse('task-list') + '?format=json'
        response = self.client.get(url,
                                   format='json'
                                )
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(Task.objects.count(), response.data['count'])
        self.assertEqual(response.data['results'][0]['name'], 'Sample')

    def test_retrieve_task(self):
        my_task = Task.objects.get(name='Sample')
        url = reverse('task-list') + str(my_task.id) + '?format=json'
        response = self.client.get(url,
                                   format='json',
                                   follow=True
                                   )
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data['name'], my_task.name)
        self.assertFalse(response.data['is_done'])

    def test_update_task(self):
        my_task = Task.objects.get(name='Sample')
        url = reverse('task-list') + str(my_task.id) + '/' + '?format=json'
        data = {
            'name': 'Sample_Replaced',
            'is_done': True
            }
        response = self.client.put(url,
                                   data,
                                   format='json',
                                   follow=True
                                   )
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data['name'], 'Sample_Replaced')
        self.assertTrue(response.data['is_done'])

    def test_partial_update_task(self):
        my_task = Task.objects.get(name='Sample')
        url = reverse('task-list') + str(my_task.id) + '/' + '?format=json'
        data = {
            'is_done': True
            }
        response = self.client.patch(url,
                                   data,
                                   format='json',
                                   follow=True
                                   )
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data['name'], my_task.name)
        self.assertTrue(response.data['is_done'])

    def test_delete_task(self):
        my_task = Task.objects.get(name='Sample')
        url = reverse('task-list') + str(my_task.id) + '/' + '?format=json'
        response = self.client.delete(url,
                                   format='json',
                                   follow=True
                                   )
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data, None)

    