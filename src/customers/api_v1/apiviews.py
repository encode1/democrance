from rest_framework.generics import CreateAPIView
from .serializers import CustomerSerializer


class CreateCustomerAPIView(CreateAPIView):
    """
    Generic View for Customer
    """
    serializer_class = CustomerSerializer