from django.test import SimpleTestCase
from django.urls import reverse, resolve
from books.views import BookListCreate, BookRetrieveUpdateDestroyView, BookRentChargeView, RentCreateView, ReturnBookView, \
    RentsListView, BookRentChargeView


class TestUrls(SimpleTestCase):

    def test_book_list_url_resolves(self):
        url = reverse('book_list')
        self.assertEquals(resolve(url).func.view_class, BookListCreate)

    def test_book_rud_url_resolves(self):
        url = reverse('book_rud', args=[1])
        self.assertEquals(resolve(url).func.view_class, BookRetrieveUpdateDestroyView)

    def test_rent_create_url_resolves(self):
        url = reverse('rent_create')
        self.assertEquals(resolve(url).func.view_class, RentCreateView)

    def test_book_return_url_resolves(self):
        url = reverse('book_return', args=[1,1])
        self.assertEquals(resolve(url).func.view_class, ReturnBookView)

    def test_rents_url_resolves(self):
        url = reverse('rents')
        self.assertEquals(resolve(url).func.view_class, RentsListView)

    def test_rents_url_resolves(self):
        url = reverse('rents_charge', args=[1])
        self.assertEquals(resolve(url).func.view_class, BookRentChargeView)

    

    

