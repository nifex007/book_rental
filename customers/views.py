from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from customers.serializers import CustomerSerializer
from customers.models import Customer
from books_rental.utils import get_jwt, decode_jwt
import jwt, datetime




# Create your views here.
class Register(CreateAPIView):

    serializer_class = CustomerSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'data': serializer.data, 'message': 'Customer Registered'}, status=status.HTTP_201_CREATED)


class Login(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        user = Customer.objects.filter(username=username).first()
        if user is None:
            raise AuthenticationFailed('User not found')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect login details')
        token = get_jwt(user.id)
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {'jwt': token}

        return response


class CustomerView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated User!')
        try:
            payload = decode_jwt(token)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Login Again')
        user = Customer.objects.filter(id=payload['id']).first()
        serializer = CustomerSerializer(user)

        return Response({'data': serializer.data}, status=status.HTTP_200_OK)



class LogOut(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            "message": "User logged out"
        }

        return response



