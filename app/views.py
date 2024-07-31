from django.shortcuts import render
from .models import Product

def index(request):
    products = Product.objects.order_by('-created_at')[:3]
    return render(request, 'app/index.html', {'products': products})
