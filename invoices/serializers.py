from rest_framework import serializers
from .models import *

class InvoiceDetailSerailizer(serializers.ModelSerializer):
    class Meta:
        model=InvoiceDetail
        fields="__all__"

class InvoiceSerailizer(serializers.ModelSerializer):
    details=InvoiceDetailSerailizer(many=True,required=False)
    class Meta:
        model=Invoice
        fields="__all__"

class AddUpdateInvoiceSerailizer(serializers.ModelSerializer):
    class Meta:
        model=Invoice
        fields="__all__"

class AddUpdateInvoiceDetailSerailizer(serializers.ModelSerializer):
    class Meta:
        model=InvoiceDetail
        exclude=['invoice']
