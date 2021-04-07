from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from customers.serializers import CustomerSerializer, CreateCustomerSerializer
from customers.models import Customer



# Create your views here.
class Register(APIView):
    def post(self, request):
        serializer = CreateCustomerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class Login(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = Customer.objects.filter(username=username).first()

        if user is None:
            raise AuthenticationFailed('User not found')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect login details')

        return Response({"message": "success"})






