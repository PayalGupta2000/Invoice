from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404  # Importing get_object_or_404


class InvoiceList(APIView):
    def get(self,request):
        id = self.request.query_params.get('id')
        if id is not None:
            invoices=get_object_or_404(Invoice,id=id)
            serializer=InvoiceSerailizer(invoices)
            return Response(serializer.data)
        
        invoices=Invoice.objects.all()
        serializer=InvoiceSerailizer(invoices,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer=AddUpdateInvoiceSerailizer(data=request.data)
        if serializer.is_valid():
            f = serializer.save()
            get_detail = eval(request.data.get('invoice_serializer_detail'))
            for x in get_detail:
                detail_serializer = AddUpdateInvoiceDetailSerailizer(data = x)
                if detail_serializer.is_valid():
                    detail_serializer.save(invoice = f)
                else:
                    pass
            return Response({'msg':'Invoice Created Successfully','id':f.id,'success':True}, status=status.HTTP_201_CREATED)
        return Response({'error':serializer.errors,'success':False}, status=status.HTTP_201_CREATED)

    def put(self,request):
        id = self.request.query_params.get('id')
        invoices=get_object_or_404(Invoice,id=id)
        serializer=InvoiceSerailizer(invoices,data=request.data)
        if serializer.is_valid():
            f = serializer.save()
            get_detail = eval(request.data.get('invoice_serializer_detail'))
            for x in get_detail:
                get_id = x.get('id')
                if get_id:
                    try:
                        ins = InvoiceDetail.objects.get(id=get_id)
                    except:
                        pass
                    detail_serializer = AddUpdateInvoiceDetailSerailizer(ins, data = x)
                    if detail_serializer.is_valid():
                        detail_serializer.save(invoice = f)
                    else:
                        pass
                else:
                    pass
            return Response({
                "msg":"Data is successfully updated",
                "status":True
            })
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self,request):
        id = self.request.query_params.get('id')
        invoices=get_object_or_404(Invoice,id=id)
        serializer=InvoiceSerailizer(invoices,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response("Data is successfully updated")
        return Response(serializer.errors)
    
    def delete(self,request):
        id = self.request.query_params.get('id')
        invoices=Invoice.objects.get(id=id)
        invoices.delete()
        return Response("data is successfully deleted")
    

