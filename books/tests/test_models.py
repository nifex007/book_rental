from django.test import TestCase
from books.models import Book, Rent
from customers.models import Customer
import datetime



class TestBookAndRentModels(TestCase):

    def setUp(self):
        self.today = datetime.date.today()

        self.book1 = Book.objects.create(
            title='Black Boy',
            stock=5,
            authors='Richard Wright'
        )

        self.book2 = Book.objects.create(
            title='As the Crow Flies',
            stock=0,
            authors='Jeffrey Archer'
        )

        self.customer1 = Customer.objects.create(
            full_name='Nifemi Sola-Ojo',
            username='nifemi',
            is_staff=True,
            email='nifemisolaojo@ymail.com',
            password='pass123'
        )

        self.customer2 = Customer.objects.create(
            full_name='Nifemi Sola-Ojo II',
            username='nifemi2',
            email='nifemisolaojo2@ymail.com',
            password='pass1232'
        )

        self.rent1 = Rent.objects.create(
            customer=self.customer1,
             book=self.book1,
              start_date=self.today
        )

        
    def test_book_model(self):
        self.assertEquals(self.book1.title, 'Black Boy')
        self.assertEquals(self.book1.is_available(), True)
        self.assertEquals(self.book2.is_available(), False)

    def test_rent_model(self):
        self.assertEquals(self.rent1.customer.id, self.customer1.id)
        self.assertEquals(self.rent1.book.id, self.book1.id)
        
    
