from django import forms
from .models import products

class ProductSearchForm(forms.Form):
    class Meta:
        model = products
        fields =['medicine','price','manufacture_date','expiry','quantity']


class MedicineForm(forms.ModelForm):
    class Meta:
        model = products
        fields = ['id', 'medicine', 'manufacture_date', 'expiry', 'price']
        labels = {
            'id': 'ID',
            'medicine': 'Medicine Name',
            'manufacture_date': 'Manufacture Date',
            'expiry': 'Expiry Date',
            'price': 'Price'
        }
        widgets = {
            'manufacture_date': forms.DateInput(attrs={'type': 'date'}),
            'expiry': forms.DateInput(attrs={'type': 'date'}),
            'price': forms.NumberInput(attrs={'step': '0.01'})
        }



from django import forms
from django.forms import formset_factory

class ProductForm(forms.Form):
    product = forms.ModelChoiceField(queryset=products.objects.all())
    quantity = forms.IntegerField(min_value=1)

ProductFormSet = formset_factory(ProductForm)

class BillForm(forms.Form):
    customer = forms.CharField(max_length=50)
    product_formset = ProductFormSet




    

