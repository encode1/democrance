from collections import OrderedDict
from rest_framework import serializers
from rest_framework.exceptions import ErrorDetail, ValidationError
from ..models import Coverage, Policy, PolicyHistory
from customers.models import Customer
from customers.api_v1.serializers import CustomerSerializer


class CreateQuoteSerializer(serializers.Serializer):
    """
    Serializer for creating a policy's quote
    """
    id = serializers.IntegerField(read_only=True)
    customer_id = serializers.IntegerField(required=True, source='customer.id')
    type = serializers.CharField(max_length=100, required=True, source='coverage.type')
    premium = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    cover = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    state = serializers.CharField(max_length=100, read_only=True)

    def create(self, validated_data):
        """
        create method of the serializer.
        :param validated_data: data containing customer_id and policy type
        :return: returns a successfully created Quote for the customer
        """
        errors = OrderedDict()
        try:
            customer = Customer.objects.get(id=validated_data['customer']['id'])
        except Customer.DoesNotExist as exc:
            errors['customer_id'] = [ErrorDetail(string=exc, code='invalid')]

        try:
            coverage = Coverage.objects.get(type=validated_data['coverage']['type'])
        except Coverage.DoesNotExist as exc:
            errors['type'] = [ErrorDetail(string=exc, code='invalid')]

        if errors:
            raise ValidationError(errors)

        quote = Policy.objects.create(coverage=coverage, customer=customer, state='quoted')
        if quote:
            PolicyHistory.objects.create(policy=quote, state=quote.state)
        return quote


class UpdateQuoteSerializer(serializers.ModelSerializer):
    """
    Serializer for updating a policy's quote
    """
    quote_id = serializers.IntegerField(required=True, source='id')
    customer_id = serializers.IntegerField(read_only=True, source='customer.id')
    type = serializers.CharField(read_only=True, max_length=100, source='coverage.title')
    premium = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    cover = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    state = serializers.CharField(max_length=100, read_only=True)
    status = serializers.ChoiceField(choices=Policy.STATE, required=True, write_only=True)
    class Meta:
        model = Policy
        fields = ('quote_id', 'customer_id', 'type', 'premium', 'cover', 'state', 'status')

    def update(self, instance, validated_data):
        """
        Update and return an existing `Quote` instance, given the validated data.
        """
        # this check will prevent it from update to the same state
        if instance.state != validated_data.get('status'):
            instance.state = validated_data.get('status')
            instance.save()
            PolicyHistory.objects.create(policy=instance, state=instance.state)
        return instance


# class QuoteSerializer(serializers.Serializer):
#     """
#     Serializer for creating a policy's quote
#     """
#     quote_id = serializers.IntegerField(source='id')
#     customer_id = serializers.IntegerField(source='customer.id')
#     type = serializers.CharField(max_length=100, source='coverage.title')
#     premium = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
#     cover = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
#     state = serializers.CharField(max_length=100, read_only=True)
#     status = serializers.CharField(max_length=100, write_only=True)


class PolicySerializer(serializers.ModelSerializer):
    """
    Serializer for Policy
    """
    customer = CustomerSerializer(read_only=True)
    type = serializers.CharField(read_only=True, source='coverage.title')
    class Meta:
        model = Policy
        fields = ('id', 'type', 'customer', 'premium', 'cover','state')


class PolicyHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for PolicyHistory
    """
    timestamp = serializers.DateTimeField(source='created')
    class Meta:
        model = PolicyHistory
        fields = ('timestamp', 'state')