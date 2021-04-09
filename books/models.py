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

    def __str__(self):
        return '{} - {}'.format(self.title, self.authors)


class Rent(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    start_date = models.DateField(blank=True, null=True, default=None)
    return_date = models.DateField(blank=True, null=True, default=None)
    charge = models.DecimalField(blank=True, null=True, max_digits=6, decimal_places=2)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return '{} - {}'.format(self.customer, self.book)

    def is_returned(self):
        if self.return_date is None:
            return False
        return True
