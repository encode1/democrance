from django.urls import path

from .apiviews import CreateCustomerAPIView

urlpatterns = [
    path('create_customer/', CreateCustomerAPIView.as_view(), name='create_customer'),
]