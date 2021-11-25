from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView, RetrieveAPIView
from django.shortcuts import get_object_or_404
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from .serializers import CreateQuoteSerializer, UpdateQuoteSerializer, PolicyHistorySerializer, PolicySerializer
from ..models import Policy, PolicyHistory


class QuoteAPIView(CreateModelMixin, UpdateModelMixin, GenericAPIView):
    """
    View to allow the creation of new Quote
    """
    serializer_class = CreateQuoteSerializer
    queryset = Policy.objects.all()
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateQuoteSerializer
        if self.request.method == 'PATCH':
            return UpdateQuoteSerializer
    
    def get_object(self):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        if self.quote_id:
            return get_object_or_404(Policy, pk=self.quote_id)
        return super().get_object()
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        self.quote_id = request.data.get('quote_id')
        return self.partial_update(request, *args, **kwargs)


# class UpdateQuoteAPIView(UpdateModelMixin, GenericAPIView):
#     """
#     View to allow the update status of existing Quote
#     """
#     serializer_class = UpdateQuoteSerializer
#     queryset = Policy.objects.all()

#     def patch(self, request, *args, **kwargs):
#         return self.partial_update(request, *args, **kwargs)


class PolicyListAPIView(ListAPIView):
    serializer_class = PolicySerializer

    def get_queryset(self):
        """
        Optionally restricts the returned policies to a given customer,
        by filtering against a `customer_id` query parameter in the URL.
        """
        queryset = Policy.objects.all()
        customer_id = self.request.query_params.get('customer_id')
        if customer_id is not None:
            queryset = queryset.filter(customer__id=customer_id)
        return queryset


class PolicyRetrieveAPIView(RetrieveAPIView):
    serializer_class = PolicySerializer
    queryset = Policy.objects.all()


class PolicyHistoryAPIView(ListAPIView):
    """
    view for listing a policy history.
    """
    serializer_class = PolicyHistorySerializer
    queryset = PolicyHistory.objects.all()

    def get_queryset(self):
        return self.queryset.filter(
            policy__pk=self.kwargs['pk']
        )
    