from django.test import TestCase
from .models import Customer
from datetime import date


# Models test
class CustomerTest(TestCase):
    first_name = 'test_first_name'
    last_name = 'test_last_name'
    dob = date.today()
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name = self.first_name,
            last_name = self.last_name,
            dob = self.dob
        )
        self.customer.save()
    
    def tearDown(self) :
        self.customer.delete()
    
    def test_customer_creation(self):
        self.assertTrue(isinstance(self.customer, Customer))
        self.assertEqual(self.first_name, self.customer.first_name)
        self.assertEqual(self.last_name, self.customer.last_name)
        self.assertEqual(self.dob, self.customer.dob)
        
