from django.shortcuts import render,HttpResponse,redirect, get_object_or_404
from django.urls import reverse
from .models import products
from django.utils import timezone
from datetime import date,timedelta,datetime
from .forms import ProductSearchForm,MedicineForm 
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from .utils import send_notification

# Create your views here.
'''

rooms = [
        {'id':1,'name':'manoj'},
        {'id':2,'name':'suresh'},
        {'id':3,'name':'nagesh'},
]
def home(request):
    return render(request,'hello.html')

def add(request):
    name = request.POST['name']
    context = {'rooms':rooms}
    return render(request,'result.html',context)

'''
def home(request):
    return render(request,"index.html")

def prod(request):
    cont={}
    cont = products.objects.all()
    return render(request,"products.html",{'cont':cont}) 
  


def tim(request):
    today = date.today()
    expt = products.objects.filter(expiry__lte =today)
    low = products.objects.filter(quantity__lte=15)
    cent = products.objects.all()
    senti ={
        'cent':cent,
        'exp':expt,
        'low':low,
    }
    return render(request,'medicines.html',senti)


def delet(request,id):

    product = products.objects.get(pk=id)

    product.delete()
    return redirect(reverse('expi'))

def update(request, id):
    u_prod = products.objects.get(pk=id)

    if request.method == "POST":
        u_prod.medicine = request.POST['medicine']
        u_prod.manufacture_date = request.POST['manufacture_date']
        u_prod.price = request.POST['price']
        u_prod.expiry = request.POST['expiry']
        u_prod.quantity = request.POST['quantity']
        u_prod.save()
        # Convert manufacture_date to the correct format
        #return render(request, 'update.html', {'u': u_prod})
        return redirect('prod')
    else:
        return render(request, 'update.html', {'u': u_prod})
def success(request):
    return render(request, 'success.html')

def product_detail(request, id):
    # Get the product object from the database
    product = products.objects.get(pk=id)
    
    # Calculate the expiry date and the date 30 days from today
    manufacture = product.manufacture_date
    expiry_period = product.expiry
    expiry_date = manufacture + timedelta(days=expiry_period)
    thirty_days_from_today = date.today() + timedelta(days=30)
    sixty_days_from_today = date.today() + timedelta(days=60)
    
    # Check if the expiry date is within the next 30 days
    if thirty_days_from_today >= expiry_date > date.today():
        # Do something, such as display a warning message to the user
        days_until_expiry = (expiry_date - date.today()).days
        warning_message = "Warning: This product will expire in {} days.".format(days_until_expiry)
    elif sixty_days_from_today >= expiry_date > date.today():

        days_until_expiry >= (expiry_date - date.today()).days
        warning_message = "Warning: This product will expire in {} days.".format(days_until_expiry)
    else:
        # No action needed
        warning_message = ""
    
    # Render the product detail template with the product and warning message
    return render(request, 'product_detail.html', {'product': product, 'warning_message': warning_message})


def expiring_products(request):
    # Calculate the date 30 days from today
    thirty_days_from_today = date.today() + timedelta(days=30)
    
    # Query the database for products that will expire in the next 30 days
    expiring_products = products.objects.filter(manufacture_date__lte=thirty_days_from_today, expiry__gt=(thirty_days_from_today - date.today()).days)
    

    # Render the expiring products template with the list of products
    return render(request, 'expiring_products.html', {'expiring_products': expiring_products})


def expiring_soon(request):
    expiring_products = []
    today = timezone.now().date()
    for product in products.objects.all():
        delta = product.expiry - product.manufacture_date
        if delta <= timezone.timedelta(days=30):
            expiring_products.append(product)

    mail_subject = "Medicines are low! Be Cautious"
    mail_template = "emails/expiry_notification.html"

    context = {
        'expiring_products': expiring_products,
        'today': today,
        'to_email':'21131f0012@gvpce.ac.in',
    }
    send_notification(mail_subject,mail_template,context)
    return render(request, 'expiring_soon.html', context)


def exp_60(request):
    expiring_products = []
    today = timezone.now().date()
    for product in products.objects.all():
        delta = product.expiry - product.manufacture_date
        if delta <= timezone.timedelta(days=60) and delta >= timezone.timedelta(days=30):
            expiring_products.append(product)
    context = {
        'expiring_products': expiring_products,
        'today': today
    }
    return render(request, 'exp_60.html', context)

 


def product_search(request):

    query = request.GET.get('q')
    p = products.objects.all()
    
    if query:
        product = products.objects.filter(Q(medicine__icontains=query))
    else:
        product=[]

    context ={
        'products':product,
        'query':query,
        'p':p,
    }

    return render(request, 'product_search.html', context)


def ordered(request):

    cont = products.objects.all().order_by('medicine','price')

    context = {
        'cont':cont
    }

    return render(request,'orderby.html',context)


def order(request):
    prod = products.objects.all()
    if request.method == 'POST':
        selected_products = request.POST.getlist('check')   # Get the list of selected product IDs
        print(selected_products)
        request.session['selected_products'] = selected_products  # Save selected products in session
        # l=[]
        # for i in selected_products:
        #     l.append(int(i))
        # ordered_prod = []
        # for i in l:
        #     for j in prod:
        #         if i == j.id:
        #             ordered_prod.append(j.medicine)
        
        ordered_products = []
        for product_id in selected_products:
            product = products.objects.get(id=product_id)
            ordered_products.append({
                'id': product.id,
                'medicine': product.medicine,
                'price': product.price,
                'manufacture_date': product.manufacture_date,
                'expiry':product.expiry,
                'quantity':product.quantity,
            })
        print(ordered_products,selected_products)

        context = {
            'ordered_products': ordered_products
        }
        
        return render(request, "order.html", context)
            
        
        # Redirect to the 'bill' URL to display the bill
    return render(request,"order.html")
    #return HttpResponse("try agIn")



def bill(request):
    prod = products.objects.all()
    selected_products = request.session.get('selected_products', [])  # Retrieve selected products from session
    print(selected_products)
    
    # Perform any additional processing or database operations related to the bill
    
    # Pass the selected products and any other relevant data to the 'bill.html' template
    return render(request, 'bill.html')

def search_jav(request):
    prod = products.objects.all()
    return render(request, 'search_jav.html',{'ordered_products':prod})

def newpage(request):
    return render(request,"newpage.html")

def nextpage(request):
    return render(request,"next_page.html")


def submit_form(request):
    if request.method == 'POST':
        selected_products = []
        art = 0
        for key, value in request.POST.items():
            if key.startswith('quantity_'):
                product_id = key.split('_')[1]
                quantity = int(value)
                
                # Retrieve other product details using the product_id
                # Save the product details and quantity as needed
                # For example, you could store them in a database or session
                
                # Example: Append the selected product and quantity to the list
                product = products.objects.get(id=product_id)
                total = int(product.price * quantity)
                art+=total
                selected_products.append({
                    'product_id': product.id,
                    'medicine': product.medicine,
                    'price': product.price,
                    'manufacture': product.manufacture_date,
                    'expiry': product.expiry,
                    'quantity': quantity,
                    'total': total,
                    'sum':art,
                })
        
                
                    
        return render(request, 'supplier.html', {'selected_products': selected_products})




def insertbysupplier(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            print(form)
            return redirect('search')  # Redirect to a view that displays the medicine list
    else:
        form = MedicineForm()

    return render(request, 'supplier/add_medicine.html', {'form': form})







