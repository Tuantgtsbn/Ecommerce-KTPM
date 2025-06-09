from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Payment
from .serializers import PaymentSerializer, PaymentCreateSerializer, PaymentStatusUpdateSerializer
import requests
import json


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return PaymentCreateSerializer
        elif self.action == 'update_status':
            return PaymentStatusUpdateSerializer
        return PaymentSerializer

    def create(self, request, *args, **kwargs):
        """
        Tạo thanh toán mới cho đơn hàng
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Xử lý thanh toán dựa trên phương thức thanh toán
        method = serializer.validated_data.get('methodPayment')

        if method == 'paypal':
            # Giả lập gọi API PayPal
            payment = self.process_paypal_payment(serializer.validated_data)
        else:
            # Xử lý các phương thức thanh toán khác
            # Sửa từ self.perform_create(serializer) thành serializer.save()
            payment = serializer.save()

        return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)

    def process_paypal_payment(self, data):
        """
        Giả lập xử lý thanh toán qua PayPal
        Trong thực tế, bạn sẽ gọi API của PayPal ở đây
        """
        # Tạo payment record với trạng thái pending
        payment = Payment.objects.create(
            id_order=data['id_order'],
            amount=data['amount'],
            methodPayment='paypal',
            statusPayment='pending'
        )

        # Trong thực tế, bạn sẽ gọi API PayPal và cập nhật transaction_id
        # payment.transaction_id = paypal_response.transaction_id
        # payment.save()

        return payment

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """
        Cập nhật trạng thái thanh toán
        """
        payment = self.get_object()
        serializer = PaymentStatusUpdateSerializer(
            payment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Cập nhật trạng thái thanh toán
        payment = serializer.save()

        # Nếu thanh toán hoàn tất, cập nhật trạng thái đơn hàng
        if payment.statusPayment == 'paid':
            self.update_order_status(payment.id_order, 'paid')

        return Response(PaymentSerializer(payment).data)

    def update_order_status(self, order_id, status):
        """
        Gọi API của order_service để cập nhật trạng thái đơn hàng
        """
        # Trong thực tế, bạn sẽ gọi API của order_service
        # Ví dụ:
        url = f"http://localhost:8002/api/orders/{order_id}/update_status/"
        data = {"statusPayment": status}
        response = requests.patch(url, json=data)
        return response.json()

    @action(detail=False, methods=['get'])
    def order_payments(self, request):
        """
        Lấy danh sách thanh toán của một đơn hàng
        """
        order_id = request.query_params.get('order_id')
        if not order_id:
            return Response({"error": "Order ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        payments = Payment.objects.filter(id_order=order_id)
        serializer = self.get_serializer(payments, many=True)
        return Response(serializer.data)
