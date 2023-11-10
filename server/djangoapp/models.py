from django.db import models
from django.utils.timezone import now
from django.contrib import admin
# from .models import CarMake, CarModel  # Import your models here

# Register your models here.
CAR_TYPE_CHOICES = [
    ('Sedan', 'Sedan'),
    ('SUV', 'SUV'),
    ('WAGON', 'WAGON'),
]

class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.IntegerField()
    name = models.CharField(max_length=100)
    car_type = models.CharField(max_length=10, choices=CAR_TYPE_CHOICES)
    year = models.DateField()

    def __str__(self):
        return f"{self.car_make.name} - {self.name} ({self.year})"


# CAR_TYPE_CHOICES = [
#     ('Sedan', 'Sedan'),
#     ('SUV', 'SUV'),
#     ('WAGON', 'WAGON'),
# ]

# Create your models here.
# class CarMake(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()

#     def __str__(self):
#         return self.name
    
# class CarModel(models.Model):
#     car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
#     dealer_id = models.IntegerField()
#     name = models.CharField(max_length=100)
#     car_type = models.CharField(max_length=10, choices=CAR_TYPE_CHOICES)
#     year = models.DateField()

#     def __str__(self):
#         return f"{self.car_make.name} - {self.name} ({self.year})"

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
