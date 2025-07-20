from django.shortcuts import render
from .models import Services
# Create your views here.

def home(request):
    services = Services.objects.filter(status = True)
    return render(request,'root/index.html',
        context= {
            'services' : services,
        })

def about(request):
    return render(request,'root/about.html')

def contact_us(request):
    return render(request,'root/contact.html')
