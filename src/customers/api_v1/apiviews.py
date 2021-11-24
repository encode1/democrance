from rest_framework.generics import CreateAPIView
from .serializers import CustomerSerializer


class CreateCustomerAPIView(CreateAPIView):
    """
    View to allow the creation of new customer
    """
    serializer_class = CustomerSerializer
    