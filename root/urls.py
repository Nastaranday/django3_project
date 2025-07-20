from django.urls import path
from .views import home,contact_us,about

urlpatterns = [
    path('',home),
    path('contact/',contact_us),
    path('about/',about),
]
