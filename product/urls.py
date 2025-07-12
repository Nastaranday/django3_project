from django.urls import path
from .views import category,product_detail

urlpatterns = [
    path('',category),
]
