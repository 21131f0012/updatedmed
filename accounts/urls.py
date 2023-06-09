from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('register-Merchant/', views.MerchantRegister, name="MerchantRegister"),
    path('signin/', views.signin, name="signin"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('signout/', views.signout, name="signout"),
    path('register-Supplier/',views.registerSupplier,name="SupplierRegister"),
    path('activate/<uidb64>/<token>/', views.activate,name="activate"),
    
]
