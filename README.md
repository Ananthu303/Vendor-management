# The first thing to do is to clone the repository:
git clone https://github.com/gocardless/sample-django-app.git

# Download python.
Download pytho latest version 

# Create a virtual environment:
python -m venv venv

# Activate a virtual environment - on windows:
venv\Scripts\activate

# Activate a virtual environment - on linux based:
source venv/bin/activate

# Then install the dependencies:
pip install -r requirements.txt

# After installing the dependencies Start the development server::
python manage.py runserver


# API Endpoints
Vendors
    GET /api/vendors/: List all vendors.
    POST /api/vendors/: Create a new vendor.
    GET /api/vendors/{vendor_id}/: Retrieve a specific vendor.
    PUT /api/vendors/{vendor_id}/: Update a specific vendor.
    DELETE /api/vendors/{vendor_id}/: Delete a specific vendor.

Purchase Orders
    GET /api/purchase_orders/: List all purchase orders.
    POST /api/purchase_orders/: Create a new purchase order.
    GET /api/purchase_orders/{po_id}/: Retrieve a specific purchase order.
    PUT /api/purchase_orders/{po_id}/: Update a specific purchase order.
    DELETE /api/purchase_orders/{po_id}/: Delete a specific purchase order.

Acknowledgment
    POST /api/purchase_orders/{po_id}/acknowledge : For vendors to acknowledge POs.

Vendor Performance
    GET /api/vendors/{vendor_id}/performance/: Retrieve performance metrics for a specific vendor.