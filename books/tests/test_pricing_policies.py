from django.test import SimpleTestCase
from books_rental.pricing_policies import compute_charge

class TestPricingPolicies(SimpleTestCase):
    def setUp(self):
        self.compute_charge = compute_charge

    
    def test_book_type_pricings(self):
        # regular
        self.assertEquals(self.compute_charge('R', 2), 2.0)
        self.assertEquals(self.compute_charge('R', 4), 5.0)
        self.assertEquals(self.compute_charge('R', 1), 2.0)

        # fiction 
        self.assertEquals(self.compute_charge('F', 1), 3.0)

        # novel
        self.assertEquals(self.compute_charge('N', 1), 2.0)
        self.assertEquals(self.compute_charge('N', 2), 4.5)





