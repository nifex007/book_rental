"""books_rental URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from ui.views import index_view, add_book_view, add_rent_view, customer_list_view, customer_charge_view


urlpatterns = [
    # ui routes
    path('', index_view, name='index'),
    path('add_book', add_book_view, name='add_book_view'),
    path('add_rent', add_rent_view, name='add_rent_view'),
    path('customer_list', customer_list_view, name='customer_list_view'),
    path('customer_charge', customer_charge_view, name='customer_charge_view'),
    
    path('admin/', admin.site.urls),

    # backend routes
    path('api/users/', include('customers.urls')),
    path('api/books/', include('books.urls')),

]
