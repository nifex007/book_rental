from django.test import SimpleTestCase
from django.urls import reverse, resolve

from ui.views import index_view, add_book_view, add_rent_view, customer_list_view, customer_charge_view


# Create your tests here.

class TestUIUrls(SimpleTestCase):

    def test_index_url_resolves(self):
        url = reverse('index')
        self.assertEquals(resolve(url).func, index_view)

    def test_add_book_url_resolves(self):
        url = reverse('add_book_view')
        self.assertEquals(resolve(url).func, add_book_view)

    def test_add_rent_url_resolves(self):
        url = reverse('add_rent_view')
        self.assertEquals(resolve(url).func, add_rent_view)

    def test_customer_list_url_resolves(self):
        url = reverse('customer_list_view')
        self.assertEquals(resolve(url).func, customer_list_view)

    def test_customer_charge_url_resolves(self):
        url = reverse('customer_charge_view')
        self.assertEquals(resolve(url).func, customer_charge_view)

    
