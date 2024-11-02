

def get_common_data(WMS_MODELS, customer):
    products = WMS_MODELS.Product.objects.filter(customer = customer)
    warranties = WMS_MODELS.Warranty.objects.filter(customer = customer)
    claims = WMS_MODELS.Claim.objects.filter(customer = customer)
    return products, warranties, claims

def get_metrics(WMS_MODELS, customer):
    products, warranties, claims = get_common_data(WMS_MODELS, customer)
    return products.count(), warranties.count(), claims.count()

def get_recent_claims(WMS_MODELS, customer):
    claims = WMS_MODELS.Claim.objects.filter(customer = customer)
       
    return claims
def get_warranties_by_status(WMS_MODELS, customer, status):
    warranties = WMS_MODELS.Warranty.objects.filter(customer=customer)
    status_warranties=[]
    for w  in warranties:
        if w.status==status:
            status_warranties.append(w)
    return status_warranties

def get_warranty_products(WMS_MODELS, product):
    return WMS_MODELS.Warranty.objects.filter(product = product)
    
def get_warranty_products_by_status(WMS_MODELS, product, status):
    warranties = []
    for warranty in get_warranty_products(WMS_MODELS, product):
        if warranty.status == status:
            warranties.append(warranty)
    return warranties