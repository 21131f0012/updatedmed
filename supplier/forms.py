from django import forms
from .models import Supplier
#from accounts.validators import allow_only_images_validator

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['supplier_name']