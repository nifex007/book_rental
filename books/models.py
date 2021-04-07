from django.db import models
from customers.models import Customer


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=255)
    stock = models.IntegerField()
    authors = models.CharField(max_length=255)

    def is_available(self):
        if self.stock > 0:
            return True
        return False


class Rent(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    start_date = models.DateField(blank=True, null=True, default=None)
    return_date = models.DateField(blank=True, null=True, default=None)
