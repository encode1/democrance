from django.db import IntegrityError
from rest_framework.exceptions import ErrorDetail, ValidationError
from rest_framework import serializers
from ..models import Customer
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class CustomerSerializer(serializers.Serializer):
    """
    Serializer for customer
    """
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(allow_blank=False, max_length=150, required=True, source='user.first_name')
    last_name = serializers.CharField(allow_blank=False, max_length=150, required=True, source='user.last_name')
    email = serializers.EmailField(allow_blank=False, label='Email address', max_length=254, required=True, source='user.email')
    dob =  serializers.DateField(format="%d-%m-%Y" ,required=True)
    
    def create(self, validated_data):
        """
        Overriding the default create method of the Model serializer.
        :param validated_data: data containing all the details of customer
        :return: returns a successfully created customer record
        """
        validated_user = validated_data.pop('user')
        user_data = {
            'username': validated_user.get('email'),
            'first_name': validated_user.get('first_name'),
            'last_name': validated_user.get('last_name'),
            'email': validated_user.get('email')
        }
        try:
            user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        except IntegrityError:
            raise ValidationError({'email': [ErrorDetail(string='A customer with that email already exists', code='invalid')],})
            
        
        customer = Customer.objects.create(user=user,
                            dob=validated_data.pop('dob'))
        return customer