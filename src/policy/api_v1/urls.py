from django.urls import path

from .apiviews import QuoteAPIView, PolicyHistoryAPIView, PolicyRetrieveAPIView, PolicyListAPIView

urlpatterns = [
    path('quote/', QuoteAPIView.as_view(), name='create_quote'),
    # path('quote/<int:pk>/', UpdateQuoteAPIView.as_view(), name='update_quote'),
    path('policies/', PolicyListAPIView.as_view(), name='policy_list'),
    path('policies/<int:pk>/', PolicyRetrieveAPIView.as_view(), name='policy_details'),
    path('policies/<int:id>/history/', PolicyHistoryAPIView.as_view(), name='policy_history'),
]