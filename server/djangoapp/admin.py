from django.contrib import admin
from .models import CarMake, CarModel

class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 1

class CarModelAdmin(admin.ModelAdmin):
    list_display = ('car_make', 'name', 'year', 'car_type')

class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]

admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)


# Register your models here.
# CAR_TYPE_CHOICES = [
#     ('Sedan', 'Sedan'),
#     ('SUV', 'SUV'),
#     ('WAGON', 'WAGON'),
# ]

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

# class CarModelInline(admin.StackedInline):
#     model = CarModel
#     extra = 1  # Set the number of empty forms to display

# class CarModelAdmin(admin.ModelAdmin):
#     list_display = ('car_make', 'name', 'car_type', 'year')
#     list_filter = ('car_make', 'car_type', 'year')
#     search_fields = ('car_make__name', 'name')
#     ordering = ('car_make', 'name')

# class CarMakeAdmin(admin.ModelAdmin):
#     inlines = [CarModelInline]  # Add the CarModelInline to CarMakeAdmin

# Register models here

# from .models import related models


# Register your models here.
# CAR_TYPE_CHOICES = [
#     ('Sedan', 'Sedan'),
#     ('SUV', 'SUV'),
#     ('WAGON', 'WAGON'),
# ]

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
# CarModelInline class

# CarModelAdmin class

# CarMakeAdmin class with CarModelInline

# Register models here
