from datetime import timedelta
from ..exceptions.wms_exception import WarrantyException
def calculate_warranty_end_date(warranty):
    if(warranty.product is None):
        raise WarrantyException("Product details is required")
    purchase_date = warranty.product.purchase_date
    warranty_period = warranty.warranty_period_months
    if warranty_period is None or warranty_period < 1:
        raise WarrantyException("A minimum of 1 month Warranty Period is required")
    return purchase_date + timedelta(days=(warranty_period * 30))


def calculate_claim_amount(product, issue_severity="standard"):
    # Example calculation: Fixed claim amount or percentage of purchase amount
    if issue_severity == "CRITICAL":
        # For severe issues, claim 80% of the purchase amount
        return product.purchase_amount * 0.8
    elif issue_severity == "HIGH":
        return product.purchase_amount * 0.65
    elif issue_severity == 'MODERATE':
        return product.purchase_amount * 0.45
    else:
        return min(1000, product.purchase_amount * 0.3)

def calculate_extended_warranty_end_date(warranty, additional_months):
    # Add the extended warranty period to the current expiration date
    if warranty.expiration_date:
        extended_expiration_date = warranty.expiration_date + timedelta(days=30 * additional_months)
        return extended_expiration_date
    return None

def calculate_premium_amount(product, extension_period_months):
    base_rate = 0.02  # Assume a 2% monthly rate
    premium = product.purchase_amount * base_rate * extension_period_months
    return premium

def calculate_extended_warranty_costs(extended_warranty_months, product_purchase_amount):
    base_premium_rate = 0.015  # Example monthly premium rate (1.5% of purchase amount)
    max_claim_factor = 0.8     # Maximum claimable amount as 80% of the purchase amount

    # Calculate premium amount
    premium_amount = product_purchase_amount * base_premium_rate * extended_warranty_months

    # Calculate max claim amount
    max_claim_amount = product_purchase_amount * max_claim_factor

    return {
        'premium_amount': premium_amount,
        'max_claim_amount': max_claim_amount,
    }