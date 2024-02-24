from django.urls import path
from . import views

urlpatterns = [
    path('invoices',views.InvoiceList.as_view()),
]