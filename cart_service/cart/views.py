from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer

class CartViewSet(viewsets.ViewSet):
    # 1. Lấy danh sách các cart
    def list(self, request):
        carts = Cart.objects.all().order_by('-created_at')  # Sắp xếp theo thời gian tạo, mới nhất trước
        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data)
    
    # 2. Tạo mới một Cart cho khách hàng
    def create(self, request):
        serializer = CartSerializer(data=request.data)
        customer_id = request.quey_params.get('customer_id')
        if serializer.is_valid():
            serializer.save(customer_id=customer_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 3. Lấy chi tiết một Cart theo id
    def retrieve(self, request, pk=None):
        cart = get_object_or_404(Cart, pk=pk)
        items_list = []
        for item in cart.items.all():
            items_list.append({
                'itemsId': item.id,
                'quantity': item.quantity,
                'addedAt': item.added_at
            })
        data = {
            'cartId': cart.id,
            'customerId': cart.customer_id,  # lấy id của khách hàng
            'items': items_list
        }
        return Response(data)

    
    # 4. Thêm sản phẩm vào Cart: POST /cart/{pk}/add_item/
    @action(detail=True, methods=['post'], url_path='add_item')
    def add_item(self, request, pk=None):
        customer_id = request.query_params.get('customer_id')
        cart = get_object_or_404(Cart, pk=pk, customer_id=customer_id)
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(cart_id=cart)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 5. Cập nhật số lượng sản phẩm: PUT /cart/{pk}/update_item/{item_id}/
    @action(detail=True, methods=['patch'], url_path='update_item/(?P<item_id>[^/.]+)')
    def update_item(self, request, pk=None, item_id=None):
        customer_id = request.query_params.get('customer_id')
        cart = get_object_or_404(Cart, pk=pk, customer_id=customer_id)
        cart_item = get_object_or_404(CartItem, cart_id=cart, id=item_id)
        serializer = CartItemSerializer(cart_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 6. Xóa sản phẩm khỏi Cart: DELETE /cart/{pk}/remove_item/{item_id}/
    @action(detail=True, methods=['delete'], url_path='remove_item/(?P<item_id>[^/.]+)')
    def remove_item(self, request, pk=None, item_id=None):
        cart_item = get_object_or_404(CartItem, cart_id=pk, item_id=item_id)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # 7. Xóa sạch Cart: DELETE /cart/{pk}/clear/
    @action(detail=True, methods=['delete'])
    def clear(self, request, pk=None):
        cart = get_object_or_404(Cart, pk=pk, customer_id=request.user)
        cart.items.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    # 8. Checkout Cart: POST /cart/{pk}/checkout/
    @action(detail=True, methods=['post'])
    def checkout(self, request, pk=None):
        cart = get_object_or_404(Cart, pk=pk, customer_id=request.user)
        # TODO: Thực hiện logic chuyển đổi Cart thành Order và gọi tới service Order
        return Response({
            'message': 'Thanh toán giỏ hàng thành công',
            'cart': CartSerializer(cart).data
        })
