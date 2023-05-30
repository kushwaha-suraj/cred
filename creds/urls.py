from creds.views import CredsAPIView,CredsDetailAPIView
from django.urls import path

urlpatterns = [
    path('', CredsAPIView.as_view(),name='creds'),
    path('<int:id>', CredsDetailAPIView.as_view(),name='creds-details'),
    path('creds/<int:id>', CredsDetailAPIView.as_view(),name='creds'),
    # path('create', CreateCredsAPIView.as_view(),name="create-creds"),
    # path('list', CredsListAPIView.as_view(),name="list-creds"),
]
