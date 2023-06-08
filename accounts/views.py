from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User

from .models import User

from .forms import UserForm
from django.contrib import messages, auth

from supplier.models import Supplier
from supplier.forms import SupplierForm
from django.template.defaultfilters import slugify

# Create your views here.
def MerchantRegister(request):
    if request.user.is_authenticated:
        # messages.warning(request,"You are already Logged in !")
        return redirect('accounts:dashboard')
    
    
    elif request.method == 'POST':
        form = UserForm(request.POST)
        
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username'] 
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.Merchant
            #via verication
            user.is_active = True
            #verification
            user.save()
            print(user.id)
            #send verification mail
            mail_subject = 'Please activate your account'
            mail_template = 'accounts/emails/account_verification_email.html'
            # send_verification_email(request, user,mail_subject,mail_template)
            # messages.success(request,"Great! You just created your account! check your mail to activate.")
            return redirect('accounts:signin')
        else:
            print(form.errors)   
    else:    
        form = UserForm()
    return render(request,'accounts/MerchantRegister.html',{'form':form})


def registerSupplier(request):
    if request.user.is_authenticated:
        messages.warning(request,"You are already Logged in !")
        return redirect('accounts:dashboard')
    
    elif request.method == 'POST':
        form = UserForm(request.POST)
        v_form = SupplierForm(request.POST)
        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.Supplier
            vendor = v_form.save(commit=False)
            vendor.user = user
            vendor_name = v_form.cleaned_data['supplier_name']
            vendor.vendor_slug = slugify(vendor_name)+'-'+str(user.id)
            user.save()
            vendor.save()
            
            # #send verification mail
            # mail_subject = 'Please activate your account'
            # mail_template = 'accounts/emails/account_verification_email.html'
            # send_verification_email(request, user,mail_subject,mail_template)
            
            messages.success(request, 'Your account has been registered sucessfully! Please check your mail to activate and wait for the approval.')
            return redirect('accounts:signin')
        else:
            print(form.errors)
            print(v_form.errors)
    
    else:
        form = UserForm()
        v_form = SupplierForm()
    return render(request,'supplier/supplierRegister.html',{'form':form,'v_form':v_form})


def signin(request):
    if request.user.is_authenticated:
        # messages.warning(request,"You are already Logged in !")
        return redirect('accounts:dashboard')
    if request.method=='POST':
        email=request.POST['e-mail']
        print(email)
        password=request.POST['password']
        print(password)

        user = auth.authenticate(email=email, password=password)
        print(user)
        if user is not None:
            print('success')
            auth.login(request,user)
            #messages.success(request,'You are now Logged
            return redirect('accounts:dashboard')
        else:
            print('fail')
            # messages.error(request,'Invalid Login credentials')
            return redirect('accounts:signin')

    else:
        return render(request,"accounts/signin.html")

def dashboard(request):
    return render(request,'accounts/dash.html')

def signout(request):
    auth.logout(request)
    return redirect('accounts:signout')