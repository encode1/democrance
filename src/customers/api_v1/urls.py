from django.urls import path

from .apiviews import CreateCustomerAPIView, CustomerListAPIView

urlpatterns = [
    path('create_customer/', CreateCustomerAPIView.as_view(), name='create_customer'),
    path('customers/', CustomerListAPIView.as_view(), name='list_customer'),
]