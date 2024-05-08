from django.db.models import Avg, F, Q
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import PurchaseOrder, Vendor
from .serializers import PurchaseOrderSerializer, VendorSerializer


# Vendor API views
@api_view(["GET", "POST"])
def vendor_list(request):
    if request.method == "GET":
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def vendor_detail(request, vendor_id):
    try:
        vendor = Vendor.objects.get(pk=vendor_id)
    except Vendor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = VendorSerializer(vendor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Purchase Order API views
@api_view(["GET", "POST"])
def purchase_order_list(request):
    if request.method == "GET":
        purchase_orders = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(purchase_orders, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def purchase_order_detail(request, po_id):
    try:
        purchase_order = PurchaseOrder.objects.get(pk=po_id)
    except PurchaseOrder.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = PurchaseOrderSerializer(purchase_order)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = PurchaseOrderSerializer(
            purchase_order, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        purchase_order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def calculate_on_time_delivery_rate(vendor):
    completed_pos = vendor.purchase_orders.filter(status="completed")
    on_time_deliveries = completed_pos.filter(
        delivery_date__lte=F("vendor__purchase_orders__delivery_date")
    ).count()
    total_completed_pos = completed_pos.count()

    if total_completed_pos > 0:
        on_time_delivery_rate = (on_time_deliveries / total_completed_pos) * 100
    else:
        on_time_delivery_rate = 0.0

    vendor.on_time_delivery_rate = on_time_delivery_rate
    vendor.save()


def calculate_quality_rating_avg(vendor):
    completed_pos = vendor.purchase_orders.filter(status="completed").exclude(
        quality_rating__isnull=True
    )
    if completed_pos.exists():
        quality_rating_avg = completed_pos.aggregate(avg_rating=Avg("quality_rating"))[
            "avg_rating"
        ]
        vendor.quality_rating_avg = quality_rating_avg
        vendor.save()
    else:
        quality_rating_avg = 0.0


def calculate_average_response_time(vendor):
    acknowledged_pos = vendor.purchase_orders.filter(
        status="completed", acknowledgment_date__isnull=False
    )
    if acknowledged_pos.exists():
        response_times = [
            (po.acknowledgment_date - po.issue_date).total_seconds() / 3600
            for po in acknowledged_pos
        ]
        average_response_time = sum(response_times) / len(response_times)
    else:
        average_response_time = 0.0

    vendor.average_response_time = average_response_time
    vendor.save()


def calculate_fulfilment_rate(vendor):
    completed_pos = vendor.purchase_orders.filter(status="completed")
    successful_pos = completed_pos.filter(~Q(issue_date=None))

    if completed_pos:
        print(successful_pos.count())
        print(completed_pos.count())
        fulfilment_rate = (successful_pos.count() / completed_pos.count()) * 100
        vendor.fulfillment_rate = fulfilment_rate
        vendor.save()
    else:
        fulfilment_rate = 0.0


@api_view(["GET"])
def vendor_performance(request, vendor_id):
    try:
        vendor = Vendor.objects.get(pk=vendor_id)
    except Vendor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    calculate_on_time_delivery_rate(vendor)
    calculate_quality_rating_avg(vendor)
    calculate_average_response_time(vendor)
    calculate_fulfilment_rate(vendor)
    serializer = VendorSerializer(vendor)
    return Response(serializer.data)


@api_view(["POST"])
def acknowledge_purchase_order(request, po_id):
    try:
        purchase_order = PurchaseOrder.objects.get(pk=po_id)
    except PurchaseOrder.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    purchase_order.acknowledgment_date = timezone.now()
    purchase_order.save()

    calculate_average_response_time(purchase_order.vendor)

    return Response(status=status.HTTP_200_OK)
