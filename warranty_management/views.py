from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect

def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('postlogin')  
    return render(request,'common/base.html')

def postlogin_view(request):
    if is_user_customer(request.user):
        return redirect('customer/dashboard')
    return redirect('/admin/')

def is_user_customer(user):
    print('checking user in customer group', user)
    return user.groups.filter(name='WMS_CUSTOMER').exists()