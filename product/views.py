from django.shortcuts import render

# Create your views here.

def category(request):
    return render(request,'product/category.html')

def product_detail(request):
    return render(request,'product/product-details.html')
