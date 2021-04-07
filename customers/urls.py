from django.urls import path, include
from .views import Register, Login, CustomerView, LogOut

urlpatterns = [
    path('register', Register.as_view()),
    path('login', Login.as_view()),
    path('customer', CustomerView.as_view()),
    path('logout', LogOut.as_view())
]