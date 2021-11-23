from rest_framework import serializers
from ..models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializer for customer
    """
    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'dob')