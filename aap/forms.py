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



    

