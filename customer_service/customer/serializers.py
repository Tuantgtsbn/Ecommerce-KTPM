from rest_framework import serializers
from .models import Customer, Address

class CustomerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'email', 'username', 'customer_type', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        customer = Customer(**validated_data)
        customer.set_password(password)
        customer.save()
        return customer

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'