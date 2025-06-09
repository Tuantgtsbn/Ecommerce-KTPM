from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'id_order', 'amount', 'methodPayment', 'statusPayment',
                  'created_at', 'updated_at', 'transaction_id']
        read_only_fields = ['id', 'created_at', 'updated_at']


class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id_order', 'amount', 'methodPayment']

    def create(self, validated_data):
        return Payment.objects.create(**validated_data)


class PaymentStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['statusPayment', 'transaction_id']
