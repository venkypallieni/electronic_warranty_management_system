from django.db import models
from datetime import timedelta, timezone
# Create your models here.
from django.db import models
from customer.models import Customer
from wms_library.calculators.wms_calculator import calculate_warranty_end_date

class Product(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100, unique=True)
    purchase_date = models.DateField()
    category = models.CharField(max_length=100)
    purchase_document = models.FileField(upload_to='documents/products/', blank=True, null=True)
    document_url=models.CharField(max_length=1024, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    purchase_amount = models.DecimalField(max_digits=15, decimal_places=2)
    
    
    def __str__(self):
        return f"{self.product_name} ({self.serial_number})"

class Warranty(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACTIVE', 'Active'),
        ('REJECTED', 'Rejected'),
        ('EXPIRED','Expired')
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='warranties')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    warranty_period_months = models.PositiveIntegerField()  # warranty duration in months
    expiration_date = models.DateField(blank=True, null=True)
    terms_and_conditions = models.TextField(blank=True, null=True)
    warranty_document = models.FileField(upload_to='documents/warranties/', blank=True, null=True)  # Add document upload field
    document_url=models.CharField(max_length=1024, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    def save(self, *args, **kwargs):
        # Calculate the expiration date based on purchase date and warranty period
        if not self.expiration_date:
            self.expiration_date = calculate_warranty_end_date(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.product_name}- #{self.id}"
    

class Claim(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('RESOLVED', 'Resolved'),
    ]
    ISSUE_SEVERITY = [
        ('CRITICAL','Critical'),
        ('HIGH', 'High'),
        ('MODERATE','Moderate'),
        ('LOW','Low'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='claims')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    issue_description = models.TextField()
    date_of_claim = models.DateTimeField(auto_now_add=True)
    claim_amount = models.DecimalField(default=1000,max_digits=15, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    repair_document = models.FileField(upload_to='documents/cliams/', blank=True, null=True)  # Add document upload field
    document_url=models.CharField(max_length=1024, blank=True, null=True)
    issue_severity = models.CharField(max_length=10, choices=ISSUE_SEVERITY, default='MODERATE')
    resolution_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.product}-{self.id}"
    
class ExtendedWarranty(models.Model):
    warranty = models.ForeignKey(Warranty, on_delete=models.CASCADE)
    premium_amount = models.DecimalField(max_digits=15, decimal_places=2)
    warranty_amount = models.DecimalField(max_digits=15, decimal_places=2)
    amount_claimed = models.DecimalField(max_digits=15, decimal_places=2)
    warranty_period = models.IntegerField()
    remarks = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.warranty}-{self.id}"