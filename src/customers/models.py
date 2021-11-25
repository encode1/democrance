from django.db import models
from django.conf import settings
from core.db import TimeStampedModel
from datetime import date


class Customer(TimeStampedModel):
    """
    This represents a customer
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dob = models.DateField(blank=False, null=False)

    def __str__(self):
        return f'{self.user.first_name.capitalize()} {self.user.last_name.capitalize()}'
    
    @property
    def age(self):
        today = date.today()
        return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
    
    @property
    def full_name(self):
        return self.user.get_full_name()

    @property
    def email(self):
        return self.user.email