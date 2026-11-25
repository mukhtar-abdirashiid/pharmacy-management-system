from decimal import Decimal
from datetime import timedelta
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import CategoryForm, MedicineForm, CustomerForm, SaleForm
from .models import Category, Medicine, Customer, Sale, SaleItem

def dashboard(request):
    context = {
        "medicine_count": Medicine.objects.count(),
        "customer_count": Customer.objects.count(),
        "category_count": Category.objects.count(),
        "sales_total": Sale.objects.aggregate(total=Sum("total_amount"))["total"] or Decimal("0.00"),
        "low_stock": Medicine.objects.filter(quantity__lte=5),
        "expiring": Medicine.objects.filter(expiry_date__gte=timezone.localdate(),
                                            expiry_date__lte=timezone.localdate() + timedelta(days=30)),
    }
    return render(request, "pharmacy/dashboard.html", context)

def category_list(request):
    return render(request, "pharmacy/category_list.html", {"categories": Category.objects.all()})

def category_create(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Category added.")
        return redirect("category_list")
    return render(request, "pharmacy/form.html", {"form": form, "title": "Add category"})

def category_update(request, pk):
    obj = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, "Category updated.")
        return redirect("category_list")
    return render(request, "pharmacy/form.html", {"form": form, "title": "Edit category"})

def category_delete(request, pk):
    obj = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        try:
            obj.delete()
            messages.success(request, "Category deleted.")
        except Exception:
            messages.error(request, "This category is in use. Reassign its medicines before deleting it.")
        return redirect("category_list")
    return render(request, "pharmacy/confirm_delete.html", {"object": obj, "back": "category_list"})

def medicine_list(request):
    query = request.GET.get("q", "").strip()
    category_id = request.GET.get("category", "")
    medicines = Medicine.objects.select_related("category")
    if query:
        medicines = medicines.filter(Q(name__icontains=query) | Q(category__name__icontains=query))
    if category_id:
        medicines = medicines.filter(category_id=category_id)
    return render(request, "pharmacy/medicine_list.html", {
        "medicines": medicines, "categories": Category.objects.all(),
        "query": query, "selected_category": category_id,
    })

def medicine_create(request):
    form = MedicineForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Medicine registered.")
        return redirect("medicine_list")
    return render(request, "pharmacy/form.html", {"form": form, "title": "Register medicine"})

def medicine_update(request, pk):
    obj = get_object_or_404(Medicine, pk=pk)
    form = MedicineForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, "Medicine updated.")
        return redirect("medicine_list")
    return render(request, "pharmacy/form.html", {"form": form, "title": "Edit medicine"})

def medicine_delete(request, pk):
    obj = get_object_or_404(Medicine, pk=pk)
    if request.method == "POST":
        try:
            obj.delete()
            messages.success(request, "Medicine deleted.")
        except Exception:
            messages.error(request, "This medicine is part of a sale and cannot be deleted.")
        return redirect("medicine_list")
    return render(request, "pharmacy/confirm_delete.html", {"object": obj, "back": "medicine_list"})

def customer_list(request):
    return render(request, "pharmacy/customer_list.html", {"customers": Customer.objects.all()})

def customer_create(request):
    form = CustomerForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Customer registered.")
        return redirect("customer_list")
    return render(request, "pharmacy/form.html", {"form": form, "title": "Register customer"})

def customer_update(request, pk):
    obj = get_object_or_404(Customer, pk=pk)
    form = CustomerForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, "Customer updated.")
        return redirect("customer_list")
    return render(request, "pharmacy/form.html", {"form": form, "title": "Edit customer"})

def customer_delete(request, pk):
    obj = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        try:
            obj.delete()
            messages.success(request, "Customer deleted.")
        except Exception:
            messages.error(request, "This customer has sales and cannot be deleted.")
        return redirect("customer_list")
    return render(request, "pharmacy/confirm_delete.html", {"object": obj, "back": "customer_list"})

def sale_list(request):
    return render(request, "pharmacy/sale_list.html", {"sales": Sale.objects.select_related("customer").prefetch_related("items__medicine")})

def sale_create(request):
    form = SaleForm(request.POST or None)
    if form.is_valid():
        customer = form.cleaned_data["customer"]
        medicine = form.cleaned_data["medicine"]
        quantity = form.cleaned_data["quantity"]
        with transaction.atomic():
            locked_medicine = Medicine.objects.select_for_update().get(pk=medicine.pk)
            if locked_medicine.expiry_date < timezone.localdate():
                form.add_error("medicine", "Expired medicines cannot be sold.")
            elif locked_medicine.quantity < quantity:
                form.add_error("quantity", "Not enough stock available.")
            else:
                price = locked_medicine.price
                sale = Sale.objects.create(customer=customer, total_amount=price * quantity)
                SaleItem.objects.create(sale=sale, medicine=locked_medicine,
                                         quantity=quantity, unit_price=price)
                locked_medicine.quantity -= quantity
                locked_medicine.save(update_fields=["quantity"])
                messages.success(request, "Sale recorded and stock updated.")
                return redirect("sale_list")
    return render(request, "pharmacy/form.html", {"form": form, "title": "Record sale"})
