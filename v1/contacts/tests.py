import base64

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Contact

User = get_user_model()


# Create your tests here.

class ContactsTests(APITestCase):
    def setUp(self):
        # create user
        registration_data = {'email': 'test@gmail.com',
                             'password1': 'password',
                             'password2': 'password'
                             }
        self.client.post('/rest-auth/registration/', registration_data, format='json')
        credentials = base64.b64encode(b'test@gmail.com:password').decode("ascii")
        self.client.defaults['HTTP_AUTHORIZATION'] = 'Basic ' + credentials

        created_user = User.objects.get(email='test@gmail.com')
        Contact.objects.create(name='contact1', email='contact1@gmail.com',
                               created_by=created_user)

        Contact.objects.create(name='contact2', email='contact2@gmail.com',
                               created_by=created_user)

    # list of users created is 1
    def test_list_users(self):
        url = reverse('users-list')
        response = self.client.get(url, format='json')
        self.assertEqual(len(response.data), 1)

    def test_list_contacts(self):
        url = reverse('contacts-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data['results']), 2)

    def test_update_contact(self):
        data = {'name': 'contact1_updated'}
        response = self.client.patch('/v1/contacts/1/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_contact = Contact.objects.get(pk=1)
        self.assertEqual(updated_contact.name, 'contact1_updated')

    def test_delete_contacts(self):
        response = self.client.delete('/v1/contacts/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Contact.objects.count(), 1)
