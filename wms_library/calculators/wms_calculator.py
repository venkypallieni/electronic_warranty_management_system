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