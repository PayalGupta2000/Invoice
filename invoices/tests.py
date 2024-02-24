from django.test import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Invoice, InvoiceDetail

class InvoiceAPITestCase(APITestCase):
    def setUp(self):
        self.invoice_data = {
            'date': '2024-02-23',
            'customer_name': 'Test Customer',
            'details': [
                {
                    'description': 'Product 1',
                    'quantity': 2,
                    'unit_price': '10.00',
                    'price': '20.00'
                },
                {
                    'description': 'Product 2',
                    'quantity': 1,
                    'unit_price': '15.50',
                    'price': '15.50'
                }
            ]
        }

    def test_create_invoice(self):
        url = reverse('invoice-list')
        response = self.client.post(url, self.invoice_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Invoice.objects.count(), 1)
        self.assertEqual(InvoiceDetail.objects.count(), 2)

    def test_update_invoice(self):
        invoice = Invoice.objects.create(date='2024-02-23', customer_name='Test Customer')
        detail1 = InvoiceDetail.objects.create(invoice=invoice, description='Product 1', quantity=2, unit_price='10.00', price='20.00')
        detail2 = InvoiceDetail.objects.create(invoice=invoice, description='Product 2', quantity=1, unit_price='15.50', price='15.50')
        updated_invoice_data = {
            'date': '2024-02-24',
            'customer_name': 'Updated Customer',
            'details': [
                {
                    'id': detail1.id,
                    'description': 'Updated Product 1',
                    'quantity': 3,
                    'unit_price': '12.00',
                    'price': '36.00'
                },
                {
                    'id': detail2.id,
                    'description': 'Updated Product 2',
                    'quantity': 2,
                    'unit_price': '18.00',
                    'price': '36.00'
                }
            ]
        }
        url = reverse('invoice-list') + f'?id={invoice.id}'
        response = self.client.put(url, updated_invoice_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['customer_name'], 'Updated Customer')
        detail1.refresh_from_db()
        detail2.refresh_from_db()
        self.assertEqual(detail1.description, 'Updated Product 1')
        self.assertEqual(detail1.quantity, 3)
        self.assertEqual(detail1.unit_price, '12.00')
        self.assertEqual(detail1.price, '36.00')
        self.assertEqual(detail2.description, 'Updated Product 2')
        self.assertEqual(detail2.quantity, 2)
        self.assertEqual(detail2.unit_price, '18.00')
        self.assertEqual(detail2.price, '36.00')

    def test_delete_invoice(self):
        invoice = Invoice.objects.create(date='2024-02-23', customer_name='Test Customer')
        detail = InvoiceDetail.objects.create(invoice=invoice, description='Product 1', quantity=2, unit_price='10.00', price='20.00')
        url = reverse('invoice-list') + f'?id={invoice.id}'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Invoice.objects.filter(id=invoice.id).exists())
        self.assertFalse(InvoiceDetail.objects.filter(id=detail.id).exists())
