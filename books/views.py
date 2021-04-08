from django.shortcuts import render
from django.db.models import Sum
from rest_framework.generics import GenericAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView,\
     ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from books.serializers import BookSerializer, RentSerializer
from books.models import Book, Rent
from books_rental.utils import get_days
import datetime

CHARGE_PER_DAY = 1.00

class BookListCreate(ListCreateAPIView):
    """
    Get all books and add books
    """
    serializer_class = BookSerializer
    queryset = Book.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class BookRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    lookup_field = 'id'
    serializer_class = BookSerializer

    def delete(self, request, *args, **kwargs):
        book_id = request.data.get('id')
        response = super().delete(request, *args, **kwargs)
        if response.status_code == 204:
            from django.core.cache import cache
            cache.delete('book_data_{}.format'.format(book_id))
        return response

    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code == 200:
            from django.core.cache import cache
            book = response.data
            cache.set('book_data_{}'.format(book['id']), {
                'title': book['title'],
                'authors': book['authors']
            })

        return response


class RentCreateView(CreateAPIView):

    serializer_class = RentSerializer
    # authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)  
        except ValidationError as error:
            return Response({'code': status.HTTP_400_BAD_REQUEST, 'error': error.detail})
        else:
            book = Book.objects.get(id=request.data['book'])
            if book.is_available():
                stock = book.stock
                book.stock = stock - 1
                book.save()
                serializer.save()
                return Response({'code': status.HTTP_201_CREATED, 'data': serializer.data, 'message': 'Success'})
            return Response({'code': status.HTTP_200_OK, 'message': 'Book is not available'})
        return Response({'code': status.HTTP_400_BAD_REQUEST, 'error': error.detail}, status=status.HTTP_400_BAD_REQUEST)


class ReturnBookView(GenericAPIView):

    def get(self, request, *args, **kwargs):
        try:
            rent = Rent.objects.filter(customer=self.kwargs['customer_id'], 
                                        book=self.kwargs['book_id'], return_date=None).first()
        except ValidationError as error:
            return Response({'code': status.HTTP_400_BAD_REQUEST, 'error': error.detail})
        if rent is None:
            return Response({'code': status.HTTP_400_BAD_REQUEST, 'message': 'This book is not with the customer'})
         # charge for rent
        rent_days = get_days(rent.start_date)
        rent.charge = CHARGE_PER_DAY * rent_days
        rent.return_date = datetime.date.today()
        rent.save()

        book = Book.objects.get(id=self.kwargs['book_id'])
        stock = book.stock
        # add book back to stock
        book.stock = stock + 1
        book.save()
        return Response({'code': status.HTTP_200_OK, 'message': '{} Returned'.format(rent.book.title)})


class RentsListView(APIView):
    """
    List all rents
    """
    def get(self, request):
        rents = Rent.objects.all()
        serializer = RentSerializer(rents, many=True)
        return Response({'code': status.HTTP_200_OK, 'data': serializer.data, 'message': 'Success'})

class BookRentChargeView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # books rented by a customer yet to be paid for 
            customer_rents = Rent.objects.filter(customer=self.kwargs['customer_id'], 
                                        return_date__isnull=False,paid=False,
                                        charge__isnull=False)
        except ValidationError as error:
            return Response({'code': status.HTTP_400_BAD_REQUEST, 'error': error.detail})
        if customer_rents is None or len(list(customer_rents)) == 0:
            return Response({'code': status.HTTP_400_BAD_REQUEST, 'message': 'Nothing to charge for the customer'})
        total_charge = customer_rents.aggregate(Sum('charge'))
        total_charge = float(total_charge['charge__sum'])

        customer_rents.update(paid=True)
        data = {}
        data['rent_charge'] = total_charge

        return Response({'code': status.HTTP_200_OK, 'data': data, 'message': 'Success'})


