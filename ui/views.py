from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from books.models import Book, Rent
from customers.models import Customer
from books_rental.utils import days_between
from ui.utils import get_current_host, post_payload, get_request
import json

# Create your views here.

def index_view(request):
    books_list = Book.objects.all().filter(stock__gt=0).order_by('-id')

    paginator = Paginator(books_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'ui/book-list.html', {'books_list': books_list, 'page_obj': page_obj})


def customer_list_view(request):
    host = get_current_host(request)
    customer = request.GET.get('customer', None)
    book = request.GET.get('book', None)

    if customer is None:
        # show active customers.. only customers that has n't returned books
    
        customers_rents = Rent.objects.filter(return_date=None).order_by('customer__full_name').distinct('customer__full_name')
        print('customers_rent', customers_rents)
        return render(request, 'ui/customer-list.html', {'customers_rents': customers_rents})
    
    elif book is not None and customer is not None:
        # return book 
        route = 'api/books/return/{}/{}'.format(book, customer)
        url = '{}{}'.format(host,route)

        response = get_request(url)
        if response.status_code == 200:
            route = 'customer_list?customer={}'.format(customer)
            customer_rents_url = '{}{}'.format(host,route)
            print('customer_rents_route', customer_rents_url)
            
            return redirect(customer_rents_url)

    else:
        # all book rented by a customer
        customer_rents = Rent.objects.filter(customer=customer, return_date=None).order_by('start_date')
        return render(request, 'ui/customer-rents.html', {'customer_rents': customer_rents})


def add_book_view(request):
    if request.method == 'POST':
        title = request.POST.get('title', '')
        authors = request.POST.get('authors', '')
        stock = request.POST.get('stock', 1)
        book_type = request.POST.get('book_type', 'R')

        host = get_current_host(request)
        route = 'api/books/'
        url = '{}{}'.format(host,route)
        payload = {
            'title': title,
            'authors': authors,
            'stock': stock,
            'book_type': book_type
        }
        response = post_payload(url, payload)
        if response.status_code == 201:
            return HttpResponseRedirect(reverse('index'))
        return render(request, 'ui/add-book.html')
    return render(request, 'ui/add-book.html')


def add_rent_view(request):
    if request.method == 'POST':
        book = request.POST.get('book', None)
        customer = request.POST.get('customer', None)
        
        host = get_current_host(request)
        route = 'api/books/rent'
        url = '{}{}'.format(host,route)
        payload = {
            'customer': customer,
            'book': book
        }
        response = post_payload(url, payload)
        print(response.text)
        if response.status_code == 201:
            return HttpResponseRedirect(reverse('index'))
     
    else:
        book_id = request.GET.get('book', None)
        book = Book.objects.get(id=book_id)
        customers_list = Customer.objects.all().order_by('-id')
        return render(request, 'ui/add-rent.html', {'customers_list': customers_list, 'book': book})


def rent_list_view(request):
    pass


def customer_charge_view(request):
    customer = request.GET.get('customer', None)
    customer_full_name = request.GET.get('customer_name', None)
  
    if customer is not None:
        context = {}
        host = get_current_host(request)
        route = 'api/books/rent_charge/{}'.format(customer)
        url = '{}{}'.format(host, route)
        # make API call to compute reciept
        response = get_request(url)

        if response.status_code == 200:
            reciept = json.loads(response.text)
            reciept_data = reciept.get('data', {})

            customer_reciept_details = []

            if bool(reciept_data):
                customer_rents = reciept_data.get('rents', {})

                

                if bool(customer_rents):
                    for customer_rent in customer_rents:
                        temp = {}
                        r = Rent.objects.get(id=customer_rent['id'])
                        temp['book_title'] = r.book.title
                        temp['price'] = customer_rent['charge']
                        temp['days'] = days_between(customer_rent['start_date'], customer_rent['return_date'])

                        customer_reciept_details.append(temp)
                        
                else:
                    temp = {
                    "id": None,
                    "start_date": "",
                    "return_date": "",
                    "charge": "0.00",
                    "customer": None,
                    "book": None
                    }
                    customer_reciept_details = [temp]

            total_rent_charge = reciept_data.get('rent_charge', 0.00)
        
            context['total_rent_charge'] = total_rent_charge
            context['customer_full_name'] = customer_full_name
            context['customer_reciept_details'] = customer_reciept_details

            return render(request, 'ui/rent-reciept.html', context)
    else:
        # queries for customer rents that have retured books and yet to be issued reciept
        customers_uncharged = Rent.objects.filter(return_date__isnull=False,paid=False,
                                        charge__isnull=False)
        print('customers uncharged',customers_uncharged)
        return render(request, 'ui/customer-charge.html', {'customers_uncharged': customers_uncharged})
    # return HttpResponseRedirect(reverse('customer_list_view'))

    