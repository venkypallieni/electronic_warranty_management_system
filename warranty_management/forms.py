
from django.forms.widgets import DateInput
from django import forms
from .models import Product, Warranty, Claim,ExtendedWarranty
from django.forms.widgets import ClearableFileInput
from . import models as WMS_MODELS
from wms_library.helpers.data_helper import get_warranties_by_status
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'serial_number', 'purchase_date', 'category', 'purchase_amount','purchase_document','description']
        widgets = {
            'purchase_date': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'purchase_document': ClearableFileInput(attrs={'multiple': False, 'required':False}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Product Name'})
        self.fields['serial_number'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Serial Number'})
        self.fields['category'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Category'})
        self.fields['purchase_amount'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Purchase amount'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Description', 'rows': 3})

class WarrantyForm(forms.ModelForm):
    class Meta:
        model = Warranty
        fields = ['product', 'warranty_period_months', 'warranty_document','terms_and_conditions']
        widgets = {
            'warranty_period_months': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'placeholder': 'e.g., 12'}),
            'terms_and_conditions': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter warranty terms here...'}),
            'product': forms.Select(attrs={'class': 'form-control'}),
            'warranty_document': ClearableFileInput(attrs={'multiple': False, 'required':False}),
        }
        labels = {
            'product': 'Product',
            'warranty_period_months': 'Warranty Period (Months)',
            'terms_and_conditions': 'Terms and Conditions',
        }

    def __init__(self, *args, **kwargs):
        customer = kwargs.pop('customer', None)
        super().__init__(*args, **kwargs)
        print('warranty customer: ', customer)
        if customer:
            self.fields['product'].queryset = Product.objects.filter(customer = customer)
        
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = ['product', 'claim_amount','issue_severity','issue_description', 'repair_document']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'issue_severity': forms.Select(attrs={'class':'form-control'}),
            'issue_description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4, 
                'placeholder': 'Describe the issue with the product...'
            }),
            'repair_document': ClearableFileInput(attrs={'multiple': False, 'required':False}),

        }
        labels = {
            'product': 'Select Product',
            'issue_description': 'Issue Description',
        }
    def __init__(self,*args, **kwargs):
        customer = kwargs.pop('customer', None)
        super().__init__(*args, **kwargs)
        print('warranty customer: ', customer)
        if customer:
            self.fields['product'].queryset = Product.objects.filter(customer = customer)
        

class ExtendedWarrantyForm(forms.ModelForm):
    class Meta:
        model = ExtendedWarranty
        fields = ['warranty', 'warranty_amount', 'warranty_period']
    def __init__(self,*args, **kwargs):
        customer = kwargs.pop('customer', None)
        super().__init__(*args, **kwargs)
        print('extended warranty customer: ', customer)
        if customer:
            self.fields['warranty'].queryset = get_warranties_by_status(WMS_MODELS, customer,"EXPIRED")
        