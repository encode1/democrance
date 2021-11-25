from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework import filters
from .serializers import CustomerSerializer
from ..models import Customer


class CreateCustomerAPIView(CreateAPIView):
    """
    View to allow the creation of new customer
    """
    serializer_class = CustomerSerializer
    

class CustomerListAPIView(ListAPIView):
    serializer_class = CustomerSerializer
    search_fields = ['dob', 'user__first_name', 'user__last_name', 'policy__coverage__type']
    queryset = Customer.objects.all()
    filter_backends = (filters.SearchFilter,)

    def get_queryset(self):
        """
        Optionally restricts the returned policies to a given customer,
        by filtering against a `customer_id` query parameter in the URL.
        """
        queryset = Customer.objects.all()
        customer_id = self.request.query_params.get('customer_id')
        if customer_id is not None:
            queryset = queryset.filter(customer__id=customer_id)
        return queryset