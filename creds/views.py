from creds.models import Creds
from rest_framework import permissions, filters
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from creds.serializers import CredsSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from creds.pagination import CustomPageNumberPagination
# Create your views here.

class CredsDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CredsSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = (IsAuthenticated,)
    
    lookup_field = "id"
    
    def get_queryset(self):
        return Creds.objects.filter(owner=self.request.user)


class CredsAPIView(ListCreateAPIView):
    serializer_class = CredsSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter]
    
    filterset_fields = ['id','title','desc','is_complete']
    search_fields = ['id','title','desc','is_complete']
    ordering_fields = ['id','title','desc','is_complete']
    
    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
    
    def get_queryset(self):
        return Creds.objects.filter(owner=self.request.user)
    
    

# class CreateCredsAPIView(CreateAPIView):
#     serializer_class = CredsSerializer
#     permission_classes = (IsAuthenticated,)
    
#     def perform_create(self, serializer):
#         return serializer.save(owner=self.request.user)

# class CredsListAPIView(ListAPIView):
#     serializer_class = CredsSerializer
#     permission_classes = (IsAuthenticated,)
    
#     def get_queryset(self):
#         return Creds.objects.filter(owner=self.request.user)