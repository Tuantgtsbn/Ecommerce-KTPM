
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import authenticate, login, logout
from .models import Customer, Address
from .serializers import CustomerSerializer, LoginSerializer, AddressSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_permissions(self):
        if self.action in ['create', 'login']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return Response({'message': 'Đăng nhập thành công'})
            return Response({'error': 'Thông tin đăng nhập không hợp lệ'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        logout(request)
        return Response({'message': 'Đăng xuất thành công'})
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def upgrade(self, request, pk=None):
        """
        Endpoint: POST /api/customers/{id}/upgrade/
        Nâng cấp hạng của customer lên premium.
        """
        customer = self.get_object()
        if customer.customer_type == 'registered':
            customer.customer_type = 'premium'
            customer.save()
            return Response({'message': 'Nâng cấp lên premium thành công'}, status=status.HTTP_200_OK)
        return Response({'message': 'Customer đã ở hạng premium'}, status=status.HTTP_200_OK)

class AddressViewSet(viewsets.ViewSet):
    
    #**Lấy danh sách địa chỉ của người dùng**
    def list(self, request):
        customer_id = request.query_params.get('customer_id')
        if not customer_id:
            return Response({'message': 'customer_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        addresses = Address.objects.filter(customer_id=customer_id)
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)

    #**Xem chi tiết một địa chỉ**
    def retrieve(self, request, pk=None):
        address = get_object_or_404(Address, pk=pk)
        serializer = AddressSerializer(address)
        return Response(serializer.data)

    #**Thêm địa chỉ mới**
    def create(self, request):
        serializer = AddressSerializer(data=request.data)
        is_default = request.data.get('is_default', False)
        if is_default:
            # Đặt tất cả địa chỉ của user này thành không mặc định
            Address.objects.filter(customer_id=request.data['customer_id']).update(is_default=False)
            
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #**Cập nhật địa chỉ**
    def update(self, request, pk=None):
        address = get_object_or_404(Address, pk=pk)
        serializer = AddressSerializer(address, data=request.data, partial=True)  # Cho phép cập nhật một phần
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #**Xóa địa chỉ**
    def destroy(self, request, pk=None):
        address = get_object_or_404(Address, pk=pk)
        address.delete()
        return Response({'message': 'Address deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

    #**Đặt địa chỉ mặc định**
    @action(detail=True, methods=['post'])
    def set_default(self, request, pk=None):
        address = get_object_or_404(Address, pk=pk)
        
        # Đặt tất cả địa chỉ của user này thành không mặc định
        Address.objects.filter(customer_id=address.customer_id).update(is_default=False)
        
        # Cập nhật địa chỉ này thành mặc định
        address.is_default = True
        address.save()

        return Response({'message': 'Default address updated successfully'}, status=status.HTTP_200_OK)