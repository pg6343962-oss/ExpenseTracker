from django.db import models 

# Create your models here.

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Travel', 'Travel'),
        ('Rent', 'Rent'),
        ('Other', 'Other'),
    ]

    amount= models.IntegerField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.CharField(max_length=200)
    date = models.DateField()

    def __str__(self):
        return f"{self.category} - {self.amount}"
    
    
class Income(models.Model):
    amount = models.IntegerField()
    source = models.CharField(max_length=100)
    date = models.DateField()

    def __str__(self):
        return f"{self.source} - {self.amount}"


