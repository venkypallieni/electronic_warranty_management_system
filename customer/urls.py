from django.urls import path, include
from . import views 
urlpatterns = [
    path('login', views.login_view,name='login'),
    path('register', views.register_view,name = 'register'),
    path('dashboard', views.dashboard_view,name='customer_dashboard'),
    path('products', views.add_product_view, name='add_product'),
    path('warranties', views.submit_warranty_view, name='submit_warranty'),
    path('claims', views.claim_product_repair_view, name='claim_warranty'),
    path('extended_warranties', views.extend_warranty, name='extend_warranty')
]