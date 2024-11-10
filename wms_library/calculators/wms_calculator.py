from datetime import timedelta
from decimal import *
from ..exceptions.wms_exception import WarrantyException, ClaimException
from .. import date_util as du
def calculate_warranty_end_date(warranty):
    if(warranty.product is None):
        raise WarrantyException("Product details is required")
    purchase_date = warranty.product.purchase_date
    warranty_period = warranty.warranty_period_months
    if warranty_period is None or warranty_period < 1:
        raise WarrantyException("A minimum of 1 month Warranty Period is required")
    return purchase_date + timedelta(days=(warranty_period * 30))


def calculate_claim_amount(product, new_claim,prev_claims):
    issue_severity = new_claim.issue_severity
    total_claim = 0
    for claim in prev_claims:
        if(claim.status !='REJECTED'):
            total_claim += Decimal(claim.claim_amount)
    if total_claim >= product.purchase_amount:
        raise ClaimException("Customer claim limit reached for this product")
    pending_amount = Decimal(product.purchase_amount) - Decimal(total_claim)
    if issue_severity == "CRITICAL":
        return Decimal(pending_amount) * Decimal(0.9)
    elif issue_severity == "HIGH":
        return Decimal(pending_amount) * Decimal(0.7)
    elif issue_severity == 'MODERATE':
        return Decimal(pending_amount) * Decimal(0.5)
    else:
        return min(1000, pending_amount * Decimal(0.3))

def calculate_extended_warranty_end_date(warranty, additional_months):
    # Add the extended warranty period to the current expiration date
    if warranty.expiration_date and du.is_before(warranty.expiration_date):
        extended_expiration_date = warranty.expiration_date + timedelta(days=30 * additional_months)
        return extended_expiration_date
    else:
        return du.today_date()+timedelta(days=(additional_months*30))
    
def calculate_premium_amount(product, extension_period_months):
    base_rate = 0.02  # Assume a 2% monthly rate
    premium = product.purchase_amount * base_rate * extension_period_months
    return premium

def calculate_extended_warranty_costs(extended_warranty_months, product_purchase_amount):
    base_premium_rate = Decimal(0.02)  # Assume monthly premium rate (2% of purchase amount)
    max_claim_factor = Decimal(0.8)     # Maximum claimable amount as 80% of the purchase amount

    # Calculate premium amount
    premium_amount = product_purchase_amount * base_premium_rate * extended_warranty_months

    # Calculate max claim amount
    max_claim_amount = product_purchase_amount * max_claim_factor
    print('max_claim_amount: ',max_claim_amount, ', premium_amount: ', premium_amount)
    return premium_amount, max_claim_amount