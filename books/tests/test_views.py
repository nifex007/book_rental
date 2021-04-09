from django.test import TestCase, Client
from rest_framework import status
from django.urls import reverse
from books.models import Book, Rent
from customers.models import Customer
from books_rental.utils import get_days
import json
import datetime

RENT_PER_DAY = 1.00

class TestBookViews(TestCase):

    def setUp(self):
        self.client = Client()
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

        self.rent2 = Rent.objects.create(
                customer=self.customer2,
                book=self.book1,
                start_date=self.today,
                return_date=self.today + datetime.timedelta(5)
        )

        # Rent models 3 - 5 structured to meet criteria for BookRentChargeView
        self.rent3 = Rent.objects.create(
            customer=self.customer2,
                book=self.book1,
                start_date=self.today,
                return_date=self.today + datetime.timedelta(5),
                charge=5.0,
                paid=False      
        )

        self.rent4 = Rent.objects.create(
            customer=self.customer2,
                book=self.book2,
                start_date=self.today,
                return_date=self.today + datetime.timedelta(4),
                charge=4.0,
                paid=False      
        )

        self.rent5 = Rent.objects.create(
            customer=self.customer2,
                book=self.book2,
                start_date=self.today,
                return_date=self.today + datetime.timedelta(10),
                charge=10.0,
                paid=False      
        )


        self.book_payload = {
            "title": "Wonder",
            "authors": "R J Palacio",
            "stock": 5
        }

        self.rent_payload = {
            "customer" : self.customer1.id,
            "book": self.book1.id
        }

        
    def test_book_list_view_GET(self):
        response = self.client.get(reverse('book_list_add'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_book_add_view(self):
        response = self.client.post(reverse('book_list_add'),
                                data=json.dumps(self.book_payload),
                                content_type='application/json'
                                )
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(response.data['title'], self.book_payload['title'])

    def test_book_update_view_PATCH(self):
        url = 'book_rud'
        response = self.client.patch(reverse(url, args=[self.book1.id]),
                                    data=json.dumps({'authors':'R. J. Palacio'}),
                                    content_type='application/json'
                                    )
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_book_update_view_PUT(self):
        url = 'book_rud'
        response = self.client.put(reverse(url, args=[self.book1.id]),
                                    data=json.dumps({
                                            "title": "Wonder",
                                            "authors": "R. J. Palacio",
                                            "stock": 0
                                        }),
                                    content_type='application/json'
                                    )
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_book_delete_view(self):
        url = 'book_rud'
        response = self.client.delete(reverse(url, args=[self.book1.id]))
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_get_rents_view(self):
        url = 'rents'
        response = self.client.get(reverse(url))
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_rent_create_view(self):
        url = 'rent_create'
        response = self.client.post(reverse(url),
                                    data=json.dumps(self.rent_payload),
                                    content_type='application/json'
                                    )
        book1_before_rent = self.book1
        book1_after_rent = Book.objects.get(id=response.data['data']['book'])
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(book1_before_rent.stock, book1_after_rent.stock + 1)

    
    def test_book_return_view(self):
        create_rent_response = self.client.post(reverse('rent_create'),
                                    data=json.dumps(self.rent_payload),
                                    content_type='application/json'
                                    )
        rent_id = create_rent_response.data['data']['id']
        
        url = 'book_return'
        response = self.client.get(reverse(url, args=[self.book1.id, self.customer1.id]))

        return_date = response.data['data']['return_date']
        return_date = datetime.datetime.strptime(return_date, "%Y-%m-%d").date()

        expected_charge = get_days(return_date) * RENT_PER_DAY
        rent_charged = float(response.data['data']['charge'])

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(expected_charge, rent_charged)


    
    def test_rent_charge_view(self):
        url = 'rents_charge'
        response = self.client.get(reverse(url, args=[self.customer2.id]))
        
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['data']['rent_charge'], 19.0)
        



