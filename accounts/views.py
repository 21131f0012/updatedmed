from django.http import HttpResponse
from django.shortcuts import redirect, render
from accounts.models import User
from django.contrib.auth.tokens import default_token_generator
from .models import User
from .utils import send_verification_email
from .forms import UserForm
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
from supplier.models import Supplier
from supplier.forms import SupplierForm
from django.template.defaultfilters import slugify
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from aap.models import products
from .utils import send_notification
from django.core.mail import send_mail
from datetime import date,timedelta,datetime
from django.utils import timezone

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
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email,password=password)
            user.role = User.Merchant
            user.set_password(password)
            user.save()
            print(user.id)
            #verification
            
            #send verification mail
            mail_subject = 'Please activate your account'
            mail_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user,mail_subject,mail_template)
            messages.success(request,"Great! You just created your account! check your mail to activate.")
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
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email,password=password)
            user.role = User.Supplier
            vendor = v_form.save(commit=False)
            vendor.user = user
            vendor_name = v_form.cleaned_data['supplier_name']
            vendor.vendor_slug = slugify(vendor_name)+'-'+str(user.id)
          
            user.set_password(password)
            user.save()
            vendor.save()
            #send verification mail
            mail_subject = 'Please activate your account'
            mail_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user,mail_subject,mail_template)
            
            messages.success(request, 'Your account has been registered sucessfully! Please check your mail to activate and wait for the approval.')
            return redirect('accounts:signin')
        else:
            print(form.errors)
            print(v_form.errors)
    
    else:
        form = UserForm()
        v_form = SupplierForm()
    return render(request,'supplier/supplierRegister.html',{'form':form,'v_form':v_form})


# def signin(request):
#     if request.user.is_authenticated:
#         return redirect('aap:prod')

#     if request.method == 'POST':
#         email = request.POST['e-mail']
#         password = request.POST['password']

#         try:
#             user = User.objects.get(email=email)
#             user_role = user.get_role()
#             print(user,user_role)

#             if user is not None and user_role == 'Merchant':
#                 login(request, user)
#                 return redirect('aap:prod')
        
#             elif user is not None and user_role == 'Supplier':
#                 login(request, user)
#                 return redirect('accounts:dashboard')
#             else:
#                 return redirect('accounts:signin')
#         except User.DoesNotExist:
#             return redirect('accounts:signin')

#     else:
#         return render(request, "accounts/signin.html")

from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.contrib.auth.hashers import check_password
from accounts.models import User

# def signin(request):
#     if request.user.is_authenticated:
#         return redirect('aap:prod')

#     if request.method == 'POST':
#         email = request.POST['e-mail']
#         password = request.POST['password']

#         try:
#             user = User.objects.get(email=email)
#             if check_password(password, user.password):  # Compare entered password with stored password
#                 user_role = user.get_role()
#                 print(user,user_role,password)

#                 if user_role == 'Merchant':
#                     login(request, user)
#                     cont={}
#                     cont = products.objects.all()
#                     expiring_products = []
#                     today = timezone.now().date()
#                     for product in products.objects.all():
#                         delta = product.expiry - product.manufacture_date
#                         if delta <= timezone.timedelta(days=30):
#                             expiring_products.append(product)

#                     mail_subject = "Medicines are low! Be Cautious"
#                     mail_template = "emails/expiry_notification.html"

#                     context = {
#                         'expiring_products': expiring_products,
#                         'today': today,
#                         'to_email':email,
#                     }
#                     send_notification(mail_subject,mail_template,context)
#                     return render(request,"products.html",{'cont':cont,'email':email}) 
#                 elif user_role == 'Supplier':
#                     login(request, user)
#                     return render(request,'dash.html',{'email':email})
#             else:
#                 print('passwords not equal.')

#         except User.DoesNotExist:
#             pass

#         return redirect('accounts:signin')

#     else:
#         return render(request, "accounts/signin.html")


def signout(request):
    logout(request)
    return redirect('/')

def activate(request, uidb64, token):
    # Activate the user by setting the is_active status to True
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is now activated.')
        return redirect('accounts:signin')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('accounts:signin')
    

def signin(request):
    if request.user.is_authenticated:
        return redirect('aap:prod')

    if request.method == 'POST':
        email = request.POST['e-mail']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)
        if user is not None:
            user_role = user.get_role()
            print(user, user_role)

            if user_role == 'Merchant':
                login(request, user)
                return redirect('aap:prod')
        
            elif user_role == 'Supplier':
                login(request, user)
                return redirect('accounts:dashboard')
        
        return redirect('accounts:signin')

    else:
        return render(request, "accounts/signin.html")
    
def dashboard(request):
    return render(request,'accounts/dash.html')