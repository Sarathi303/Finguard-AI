from django.urls import path
from .views import TransactionListView  # unga view function/class name

urlpatterns = [
    path('transactions/', TransactionListView.as_view(), name='transaction-list'),
]