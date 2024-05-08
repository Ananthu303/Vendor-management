from django.db import models
import random

def generate_unique_vendor_code():
    base_code = 'VEND-'
    while True:
        random_number = random.randint(1000, 9999)
        vendor_code = f'{base_code}{random_number}'
        if not Vendor.objects.filter(vendor_code=vendor_code).exists():
            return vendor_code

def generate_unique_po_number():
    base_code = 'PO-'
    while True:
        random_number = random.randint(1000, 9999)
        po_number = f'{base_code}{random_number}'
        if not PurchaseOrder.objects.filter(po_number=po_number).exists():
            return po_number

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=20, unique=True,default=generate_unique_vendor_code)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    def __str__(self):
        return self.name


class PurchaseOrder(models.Model):
    vendor = models.ForeignKey(Vendor, related_name='purchase_orders',on_delete=models.CASCADE)
    po_number = models.CharField(max_length=20, unique=True,default=generate_unique_po_number)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, default='pending')
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"PO-{self.po_number} ({self.vendor.name})"

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor.name} - {self.date}"
