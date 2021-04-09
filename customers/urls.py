from django.urls import path, include
from .views import Register, Login, CustomerView, LogOut

urlpatterns = [
    path('register', Register.as_view(), name='register_customer'),
    path('login', Login.as_view(), name='login'),
    path('', CustomerView.as_view(), name='get_customer'),
    path('logout', LogOut.as_view(), name='logout')
]