import json
from customers.models import Customer
from django.urls import reverse
from rest_framework import status
from customers.serializers import CustomerSerializer
from django.test import TestCase, Client


class CustomerViewTest(TestCase):

    def setUp(self):
        self.valid_payload = {
            "full_name": "John Doe I",
            "username": "john_doe1",
            "email": "john@doe.com",
            "password": "john_doe_pass"
        }

        self.invalid_payload = {
            "full_name": "John Doe I",
            "email": "john@doe.com",
            "password": "john_doe_pass"
        }

        self.client = Client()

    def test_register_valid_customer(self):
        response = self.client.post(reverse('register_customer'),
                                data=json.dumps(self.valid_payload),
                                content_type='application/json'
                                )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_register_invalid_customer(self):
        response = self.client.post(reverse('register_customer'),
                                data=json.dumps(self.invalid_payload),
                                content_type='application/json'
                                )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_log_in(self):
        self.client.post(reverse('register_customer'),
                                data=json.dumps(self.valid_payload),
                                content_type='application/json'
                                )

        login_credentials = {
            "username": self.valid_payload['username'],
            "password": self.valid_payload['password']
        }
        response = self.client.post(reverse('login'),
                                data=json.dumps(login_credentials),
                                content_type='application/json'
                                )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_customer_view(self):
        self.client.post(reverse('register_customer'),
                                data=json.dumps(self.valid_payload),
                                content_type='application/json'
                                )
        login_credentials = {
            "username": self.valid_payload['username'],
            "password": self.valid_payload['password']
        }
        login = self.client.post(reverse('login'),
                                data=json.dumps(login_credentials),
                                content_type='application/json'
                                )
        url = reverse('get_customer')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['data']['username'], self.valid_payload['username'])


    