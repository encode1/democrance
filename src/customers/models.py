from django.db import models
from core.models import TimeStampedModel


class Customer(TimeStampedModel):
    """
    This represents a customer
    """
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)
    dob = models.DateField(blank=False, null=False)

    def __str__(self):
        return f'{self.first_name.capitalize()} {self.last_name.capitalize()}'

