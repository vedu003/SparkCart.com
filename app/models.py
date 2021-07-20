from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import date


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    contact = models.PositiveIntegerField(default=0)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    zipcode = models.PositiveIntegerField()
    state = models.CharField(max_length=50)

    def str(self):
        return str(self.id)


CATEGORY_CHOICES = (
('E','Electronics'),
('Mobile','Mobile'),
('L','Laptop'),
('C','Camera'),
('MTS','Mens Tshirt'),
('MS','Mens Shirt'),
('MJ','Mens Jeans'),
('MSU','Mens Suit'),
('MW','Mens Watch'),
('MSH','Mens Shoes'),
('WTS','Womens Tshirt'),
('WJ','Womens Jeans'),
('WT','Womens Tops'),
('WK','Womens Kurti'),
('WSA','Womens Saree'),
('WW','Womens Watch'),
('WSH','Womens Shoes'),
)

class Product(models.Model): 
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField( choices= CATEGORY_CHOICES , max_length=7)
    product_image = models.ImageField(upload_to='productimg')

    def str(self):
        return str(self.id)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def str(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price


STATUS_CHOICES = (
('Accepted','Accepted'),
('Packed','Packed'),
('On The Way','On The Way'),
('Delivered','Delivered'),
('Cancel','Cancel'),
)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add =True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES,default= 'Pending')

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price



class Contact(models.Model):
    
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=50)
    contact = models.PositiveIntegerField()
    feedback = models.TextField()

    def str(self):
        return str(self.id)


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    name = models.CharField(max_length=200)
    dob = models.DateField(blank= True, null= True)
    contact = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)

    def str(self):
        return str(self.id)

