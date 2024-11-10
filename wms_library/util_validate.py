from .exceptions.wms_exception import ProductException, WarrantyException, ClaimException
from datetime import date
from . import date_util as du

def validate_product(product):
    error_msg = None
    if not product:
        error_msg = "Invalid product details!"
    elif product.customer is None:
        error_msg = "Customer details required"
    elif product.product_name is None:
        error_msg = "Product Name is required"
    elif product.purchase_date is None:
        error_msg =  "Purchase Date is required"
    elif du.is_after(product.purchase_date, date.today()):
        error_msg = "Purchase Date cannot be greater than current time"
    elif product.category is None:
        error_msg = "Category is required"
    elif product.document_url is None:
        error_msg = "Document is required"
    else:
       error_msg = None 
    if error_msg:
        raise ProductException(error_msg)

def validate_product_warranty(existing_warranties):
    if existing_warranties is not None:
        for warranty in existing_warranties:
            if warranty.status!="EXPIRED":
                raise WarrantyException("Warranty for this product is already exists!")

def validate_claim_warranty(existing_warranties):
    warranties = []
    if existing_warranties is not None:
        for w in existing_warranties:
            if w.status !='ACTIVE' or du.is_before(w.expiration_date, date.today()):
                warranties.append(w)
    if len(warranties) > 0:
        raise ClaimException("No active warranties exist for this product")

def validate_extended_warranty(extended_warranty):
    if extended_warranty.warranty.product.purchase_amount < extended_warranty.warranty_amount:
        raise WarrantyException("Warranty amount is greater than purchase amount")

def validate_warranty(warranty):

    pass

def validate_claim(claim):
    pass

def validate_customer(customer):
    pass