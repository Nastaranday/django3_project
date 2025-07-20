from django.contrib import admin
from .models import Products,ProductsColor,ProductAttribute,Category,Attribute,Guarantee,SpecialOffer
# Register your models here.

admin.site.register(Products)
admin.site.register(ProductsColor)
admin.site.register(ProductAttribute)
admin.site.register(Category)
admin.site.register(Attribute)
admin.site.register(Guarantee)
admin.site.register(SpecialOffer)
