from django.urls import reverse
from django.contrib.auth.models import User, Group
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Task

class TaskTests(APITestCase):

    def setUp(self):
        Group.objects.get_or_create(name='common_users')
        # Create a legitimate user. It has the good permission.
        good_user = User.objects.create(username='Anakin')
        good_user.set_password('not_yet_the_dark_side')
        good_user.save()
        my_group = Group.objects.get(name='common_users') 
        my_group.user_set.add(good_user.id)
        # Create a user without permission
        bad_user = User.objects.create(username='Dark_Vador')
        bad_user.set_password('the_dark_side')
        bad_user.save()

        Task.objects.create(name='Sample')

    def authenticate_me(self, wrong_user=False):
        if wrong_user:
            self.client.login(username='Dark_Vador', password='the_dark_side')
        else:
            self.client.login(username='Anakin', password='not_yet_the_dark_side')

    def test_authentication(self):
        url = reverse('task-list') + '?format=json'
        response = self.client.get(url,
                                   format='json'
                                )
        self.assertFalse(status.is_success(response.status_code))
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_permission(self):
        self.authenticate_me(wrong_user=True)
        url = reverse('task-list') + '?format=json'
        response = self.client.get(url,
                                   format='json'
                                )
        self.assertFalse(status.is_success(response.status_code))
        self.assertEqual(response.data['detail'], 'You do not have permission to perform this action.')
    

    def test_create_task(self):
        self.authenticate_me()
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
        self.authenticate_me()
        url = reverse('task-list') + '?format=json'
        response = self.client.get(url,
                                   format='json'
                                )
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(Task.objects.count(), response.data['count'])
        self.assertEqual(response.data['results'][0]['name'], 'Sample')

    def test_retrieve_task(self):
        self.authenticate_me()
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
        self.authenticate_me()
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
        self.authenticate_me()
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
        self.authenticate_me()
        my_task = Task.objects.get(name='Sample')
        url = reverse('task-list') + str(my_task.id) + '/' + '?format=json'
        response = self.client.delete(url,
                                   format='json',
                                   follow=True
                                   )
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data, None)

    