from rest_framework import serializers
from .models import Book, Rent
import datetime

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'authors', 'stock', 'is_available', 'book_type']

    def create(self, validated_data):
        return Book.objects.create(**validated_data)


class RentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rent
        fields = '__all__'
        read_only_fields = ('start_date', 'return_date', 'charge', 'paid')

    def create(self, validated_data):
        validated_data['start_date'] = datetime.date.today()
        return Rent.objects.create(**validated_data)
