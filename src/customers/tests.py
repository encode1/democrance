from django.test import TestCase
from .models import Customer
from django.contrib.auth.models import User
from datetime import date
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


# Models test
class CustomerTest(TestCase):
    first_name = 'test_first_name'
    last_name = 'test_last_name'
    email = 'test@localhost.dev'
    dob = date.today()
    def setUp(self):
        self.test_user = User.objects.create(
            first_name = self.first_name,
            last_name = self.last_name,
            email = self.email,
            username = self.email
        )
        self.test_user.save()
        self.customer = Customer.objects.create(user=self.test_user, dob=self.dob)
    
    def tearDown(self) :
        self.customer.delete()
        self.test_user.delete()
    
    def test_customer_creation(self):
        self.assertTrue(isinstance(self.customer, Customer))
        self.assertEqual(self.first_name, self.customer.user.first_name)
        self.assertEqual(self.last_name, self.customer.user.last_name)
        self.assertEqual(self.dob, self.customer.dob)
        
# endpoint test
class CreateCustomerAPIViewTestCase(APITestCase):

    def setUp(self):
        self.endpoint = reverse('create_customer')
        self.data = {
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'email': 'test@localhost.dev',
            'dob': date.today()
        }

    def test_create_customer(self):
        response = self.client.post(self.endpoint, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.new_customer = Customer.objects.get(user__username=self.data['email'])
        self.assertEqual(self.new_customer.dob, self.data['dob'])

    def test_if_customer_email_already_exists_dont_create(self):
        self.test_user = User.objects.create(
            first_name = self.data['first_name'],
            last_name = self.data['last_name'],
            email = self.data['email'],
            username = self.data['email']
        )
        self.test_user.save()
        self.customer = Customer.objects.create(user=self.test_user, dob=self.data['dob'])
        self.customer.save()
        # Make request
        response = self.client.post(self.endpoint, self.data)
        # Check status response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            str(response.data['email'][0]),
            'A customer with that email already exists',
        )
