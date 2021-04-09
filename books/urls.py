from django.urls import path, include
from books.views import BookListCreate, BookRetrieveUpdateDestroyView, RentCreateView, ReturnBookView, RentsListView, \
    BookRentChargeView


urlpatterns = [
    path('', BookListCreate.as_view(), name='book_list_add'),
    path('<int:id>', BookRetrieveUpdateDestroyView.as_view(), name='book_rud'),
    path('rent', RentCreateView.as_view(), name='rent_create'),
    path('return/<int:book_id>/<int:customer_id>' , ReturnBookView.as_view(), name='book_return'),
    path('rents/', RentsListView.as_view(), name='rents'),
    path('rent_charge/<int:customer_id>', BookRentChargeView.as_view(), name='rents_charge')
]