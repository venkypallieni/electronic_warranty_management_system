def get_common_data(WMS_MODELS, customer):
    products = WMS_MODELS.Product.objects.filter(customer = customer)
    warranties = WMS_MODELS.Warranty.objects.filter(customer = customer)
    claims = WMS_MODELS.Claim.objects.filter(customer = customer)
    return products, warranties, claims

def get_metrics(WMS_MODELS, customer):
    products, warranties, claims = get_common_data(WMS_MODELS, customer)
    return products.count(), warranties.count(), claims.count()

def get_recent_claims(WMS_MODELS, customer):
    claims = WMS_MODELS.Claim.objects.filter(customer = customer).order_by('date_of_claim')[:5]
    return claims
def get_all_claims(WMS_MODELS, customer):
    return WMS_MODELS.Claim.objects.filter(customer=customer)
def get_warranties_by_status(WMS_MODELS, customer, status):
    return WMS_MODELS.Warranty.objects.filter(customer=customer,status=status)

def get_warranty_products(WMS_MODELS, product):
    return WMS_MODELS.Warranty.objects.filter(product = product)
    
def get_warranty_products_by_status(WMS_MODELS, product, status):
    warranties = []
    prod_warranties = get_warranty_products(WMS_MODELS, product)
    print('prod_warranties: ', prod_warranties)
    for warranty in prod_warranties:
        print('warranty status: ', warranty.status)
        if warranty.status == status:
            warranties.append(warranty)
    print('warranties: ', warranties)
    return warranties