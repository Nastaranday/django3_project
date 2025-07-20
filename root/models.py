from django.db import models

# Create your models here.

class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.question
    

class Services(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default='فروشگاه ما حامی سفارشات شما')
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.name
    
class Support(models.Model):
    name = models.CharField(max_length=100)
    context = models.TextField(default='به شما کمک می کند')
    
class ShippingServices(models.Model):
    name = models.CharField(max_length=200)
    