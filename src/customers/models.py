from django.db import models
from django.conf import settings
from core.db import TimeStampedModel


class Customer(TimeStampedModel):
    """
    This represents a customer
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dob = models.DateField(blank=False, null=False)

    def __str__(self):
        return f'{self.user.first_name.capitalize()} {self.user.last_name.capitalize()}'

