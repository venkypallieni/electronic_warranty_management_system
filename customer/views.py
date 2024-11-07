from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django import forms as DJFORM
from warranty_management import forms as WMS_FORMS
from warranty_management import models as WMS_MODALS
from . import models as customer_models
from .import forms as customer_forms
from datetime import datetime
from wms_library.helpers import s3_helper
from wms_library.helpers import data_helper
from wms_library.calculators import wms_calculator
from wms_library.util_validate import validate_product, validate_warranty, validate_product_warranty, validate_extended_warranty,validate_claim_warranty
from wms_library.exceptions.wms_exception import ProductException, WarrantyException, ClaimException
import  wms_library.date_util as date_util

S3_LAMBDA_GATEWAY = "https://rkfxfz9ix7.execute-api.ap-south-1.amazonaws.com/Staging/s3/get-token"
def login_view(request):
    form = customer_forms.UserForm()
    data = {'form':form}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/postlogin')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'common/login.html', context = data)

def register_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/postlogin')
    # Initialize empty forms for user and customer information
    user_form = customer_forms.UserForm()
    customer_form = customer_forms.CustomerForm()
    if request.method == 'POST':
        try:
            user_form= customer_forms.UserForm(request.POST)
            customer_form = customer_forms.CustomerForm(request.POST)
            if user_form.is_valid() and customer_form.is_valid():
                user = user_form.save(commit=False)
                customer =  customer_form.save(commit=False)
                profile_photo  = request.FILES["profile_photo"]
                print('user_profile: ', profile_photo)
                # token_resp = s3_helper.get_token(request, S3_LAMBDA_GATEWAY)
                # if(response['status']=='SUCCESS') :
                    # print('upload document respone: ', s3_helper.upload(response['data'], profile_photo))
                # customer.image_src = f"{response['data']['url']}{response['data']['fields']['key']}"
                user.save()
                customer.user = user
                customer.save()
                customer_group = Group.objects.get_or_create(name='WMS_CUSTOMER')
                customer_group[0].user_set.add(user)
                messages.success(request, "registration successfully!")
                return HttpResponseRedirect('/customer/login')
            else:
                messages.error(request, user_form.errors)
                messages.error(request, customer_form.errors)
        except DJFORM.ValidationError as e:
            print('exception :',str(e))
            messages.error(request, str(e))
        except Exception as e:
            print('signup exception: ',e)
            messages.error(request, 'unable to register')
    data = {'user_form': user_form, 'customer_form':customer_form}
    return render(request,'common/register.html', data)

def dashboard_view(request):
    data = {}
    try:
        customer = get_customer(request)
        tot_prods, tot_warr, tot_claims = data_helper.get_metrics(WMS_MODALS,customer)
        data['total_products'] =  tot_prods
        data['total_warranties'] = tot_warr
        data['total_claims'] = tot_claims
        data['recent_claims'] = data_helper.get_recent_claims(WMS_MODALS, customer)
        data['active_warranties'] = data_helper.get_warranties_by_status(WMS_MODALS, customer, "ACTIVE")
    except Exception as e:
        print('dashboard error: ',str(e))

    return render(request, 'customer/dashboard.html', context= data)

def add_product_view(request):
    data ={}
    customer = get_customer(request)
    try:
        products = WMS_MODALS.Product.objects.filter(customer=customer)
        paginator = Paginator(products, 2)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        data['page_obj'] = page_obj
        if request.method == 'POST':
            form = WMS_FORMS.ProductForm(request.POST)
            print('adding product: ', form)
            if form.is_valid():
                new_product = form.save(commit=False)
                new_product.customer = customer
                purchase_document  = request.FILES['purchase_document']
                token_resp = s3_helper.get_token(request, S3_LAMBDA_GATEWAY)
                if(token_resp['status']=='SUCCESS') :
                    print('upload document respone: ', s3_helper.upload(token_resp['data'], purchase_document))
                new_product.document_url = f"{token_resp['data']['url']}{token_resp['data']['fields']['key']}"
                validate_product(new_product)
                new_product.save()
                messages.success(request, "Product added successfully.")
                return HttpResponseRedirect('/customer/products')
            else:
                messages.error(request, form.errors)
    except ProductException as e:
        print('ProductException: ',e)
        messages.error(request, str(e))
    except BaseException as e:
        print("addProduct exception: ",e)
        messages.error(request, str(e))
    form= WMS_FORMS.ProductForm()
    data['form'] = form
    return render(request, 'customer/add_product.html', context=data)

def submit_warranty_view(request):
    data = {}
    customer = get_customer(request)
    try:
        warranties = WMS_MODALS.Warranty.objects.filter(customer = customer)
        paginator = Paginator(warranties, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        data['page_obj'] = page_obj
        if request.method == 'POST':
            form = WMS_FORMS.WarrantyForm(request.POST)
            print('adding warranty: ', form)
            if form.is_valid():
                new_warranty = form.save(commit=False)
                new_warranty.customer = customer
                warranty_document  = request.FILES['warranty_document']
                # token_resp = s3_helper.get_token(request, S3_LAMBDA_GATEWAY)
                # if(token_resp['status']=='SUCCESS') :
                #     print('upload document respone: ', s3_helper.upload(token_resp['data'], warranty_document))
                # new_warranty.document_url = f"{token_resp['data']['url']}{token_resp['data']['fields']['key']}"
                existing_warranties = data_helper.get_warranty_products(WMS_MODALS, new_warranty.product)
                validate_product_warranty(existing_warranties)
                validate_warranty(new_warranty)
                new_warranty.save()
                messages.success(request, "Warranty submitted successfully.")
                return HttpResponseRedirect('/customer/warranties')
            else:
                messages.error(request, form.errors)
    except WarrantyException as e:
        print('Warranty Error: ', e)
        messages.error(request, str(e))
    except BaseException as e:
        print("submit warranty exception: ",e)
        messages.error(request, str(e))
    form= WMS_FORMS.WarrantyForm(customer=customer)
    data['form'] = form
    return render(request, 'customer/warranty.html', context=data)

def claim_product_repair_view(request):
    data = {}
    customer = get_customer(request)
    try:
        claims = WMS_MODALS.Claim.objects.filter(customer = customer)
        paginator = Paginator(claims, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        data['page_obj'] = page_obj
        if request.method == 'POST':
            form = WMS_FORMS.ClaimForm(request.POST)
            print('claim form: ', form)
            if form.is_valid():
                new_claim = form.save(commit=False)
                new_claim.customer = customer
                print('new cliam: ', new_claim)
                warranties = data_helper.get_warranty_products_by_status(WMS_MODALS, new_claim.product, "ACTIVE")
                prev_claims = data_helper.get_recent_claims(WMS_MODALS, customer)
                validate_claim_warranty(warranties)
                print('warranties: ', warranties)
                claim_document  = request.FILES['repair_document']
                if warranties is None or len(warranties) <= 0:
                    raise ClaimException("No active warranties exist for this product")
                new_claim.claim_amount =wms_calculator.calculate_claim_amount(new_claim.product,new_claim, prev_claims)
                new_claim.save()
                messages.success(request, "Claim submitted successfully.")
                return HttpResponseRedirect('/customer/claims')
            else:
                messages.error(request, form.errors)
    except ClaimException as e:
        print('Claim error: ', e)
        messages.error(request, str(e))
    except BaseException as e:
        print("submit claim exception: ",e)
        messages.error(request, str(e))
    form= WMS_FORMS.ClaimForm(customer = customer)
    data['form'] = form
    return render(request, 'customer/claims.html', context=data)

def extend_warranty(request):
    data = {}
    customer = get_customer(request)
    try:
        warranties = WMS_MODALS.ExtendedWarranty.objects.filter(customer = customer)
        paginator = Paginator(warranties, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        data['page_obj'] = page_obj
        if request.method == 'POST':
            form = WMS_FORMS.ExtendedWarrantyForm(request.POST)
            print('extended warranty form: ', form)
            if form.is_valid():
                extended_warranty = form.save(commit=False)
                extended_warranty.customer = customer
                validate_extended_warranty(extended_warranty)
                purchase_amount = extended_warranty.warranty.product.purchase_amount
                extended_months = extended_warranty.warranty_period
                expired_warranty = extended_warranty.warranty
                print('purchasedmounts: ', purchase_amount, extended_months)
                premium_amount,max_claim_amount=wms_calculator.calculate_extended_warranty_costs(extended_months, purchase_amount)
                if max_claim_amount > extended_warranty.warranty_amount:
                    raise WarrantyException('Warranty Amount is greater than product purchase amount')
                extended_warranty.premium_amount = premium_amount
                expiration_date = wms_calculator.calculate_extended_warranty_end_date(expired_warranty, extended_months)
                if date_util.is_before(expiration_date):
                    raise WarrantyException("Warranty period cannot be lessthan today")
                extended_warranty.save()
                expired_warranty.expiration_date = expiration_date
                expired_warranty.status = 'ACTIVE'
                expired_warranty.save()
                return HttpResponseRedirect('/customer/extended_warranties')
            else:
                messages.error(request, form.errors)
    except WarrantyException as e:
        messages.error(request, str(e))
    except Exception as e:
        print('Extend Warranty Exception: ',e)
        messages.error(request, str(e))
    form= WMS_FORMS.ExtendedWarrantyForm(customer=customer)
    data['form'] = form
    data['customer'] = customer
    return render(request, 'customer/extended_warranty.html', context=data)

def get_customer(request):
    return customer_models.Customer.objects.get(user=request.user)