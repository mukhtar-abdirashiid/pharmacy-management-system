from django import forms
from .models import Category, Medicine, Customer

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description"]
        widgets = {"description": forms.Textarea(attrs={"rows": 3})}

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ["name", "category", "description", "price", "quantity", "expiry_date"]
        widgets = {"expiry_date": forms.DateInput(attrs={"type": "date"})}

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["name", "phone", "email", "address"]

class SaleForm(forms.Form):
    customer = forms.ModelChoiceField(queryset=Customer.objects.all())
    medicine = forms.ModelChoiceField(queryset=Medicine.objects.all())
    quantity = forms.IntegerField(min_value=1)
