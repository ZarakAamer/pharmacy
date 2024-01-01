from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action


from .serializers import *
from core.models import (Product, Address, BigBanner, SideBanner, MainCategory, SubCategory, Category, CartOrder, CartOrderProducts, ProductImages, 
                         SpecialTimeOffer, Coupon, Shipping, Order, OrderProducts, ProductReview, wishlist_model, Prescribtion, Advices, Locations, BankInfo)

# Generate Token Manually


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token = get_tokens_for_user(user)
        return Response({'token': token, 'msg': 'Registration Successful'}, status=status.HTTP_201_CREATED)



class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        user = authenticate(request, **request.data)
        if user is None:
            return Response({'error': 'Invalid login credentials'}, status=400)
        # Create access and refresh tokens for the user
        if Profile.objects.filter(user=user).first():
            token = get_tokens_for_user(user)
            # Get the user's orders
            user_id = user.id
            user_for_data = User.objects.get(id=user_id)
            user_profile = Profile.objects.filter(user=user_for_data).first()
            user_cart = CartOrder.objects.filter(
                user=user_for_data)
            user_orders = Order.objects.filter(
                user=user_for_data)
            user_data = UserDetailsSerializers(user_for_data, many=False)
            user_carts = CartOrderSerializers(user_cart, many=True)
            user_orders = OrderSerializers(user_orders, many=True)

            user_profile = ProfileForUserDataSerializer(
                user_profile, many=False)
            return Response({'msg': 'Login Success', 'user': user_data.data, 'user_profile': user_profile.data, 'Carts': user_carts.data, 'Orders':user_orders.data,  'token': token}, status=status.HTTP_200_OK)
            # return Response({'msg': 'Login Success', 'user_profile': user_profile.data,  'token': token}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Email is not verified'}, status=400)


class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(
            data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Changed Successfully'}, status=status.HTTP_200_OK)


class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)


class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(
            data=request.data, context={'uid': uid, 'token': token})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Reset Successfully'}, status=status.HTTP_200_OK)





class ProductsViewSet(ModelViewSet):
    renderer_classes = [UserRenderer]
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all()


    @action(detail=True, methods=['get'])
    def retrieve_product(self, request, pk=None):
        product = self.get_object()
        serializer = self.get_serializer(product)
        return Response(serializer.data)



    
    
class ProductReviewViewSet(ModelViewSet):
    serializer_class = ProductReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    renderer_classes = [UserRenderer]
    

    def get_queryset(self):
        queryset = ProductReview.objects.all()
        product_id = self.kwargs.get('product_id')
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        return queryset

    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_id')
        product = Product.objects.get(pk=product_id)
        serializer.save(user=self.request.user, product=product)
    
    







class MainCategoriesViewSet(ModelViewSet):
    serializer_class = MainCategorySerializer
    renderer_classes = [UserRenderer]
    
    def get_queryset(self):
        queryset = MainCategory.objects.all()
       
        return queryset



class CategoryViewSet(ModelViewSet):
    renderer_classes = [UserRenderer]
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.all()


    @action(detail=True, methods=['get'])
    def retrieve_category(self, request, pk=None):
        category = self.get_object()
        serializer = self.get_serializer(category)
        return Response(serializer.data)




class SpecialOfferViewSet(ModelViewSet):
    renderer_classes = [UserRenderer]
    serializer_class = SpecialTimeOfferSerializer

    def get_queryset(self):
        return SpecialTimeOffer.objects.all()






class CartOrderViewSet(ModelViewSet):
    serializer_class = CartOrderSerializers

    def get_queryset(self):
        return CartOrder.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)




class CartOrderProductsViewSet(ModelViewSet):
    serializer_class = CartOrderProductsEditibleSerializers
    def get_queryset(self):
        return CartOrderProducts.objects.filter(cart__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save()
        
        
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
        
        
        




class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializers

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)




class OrderProductsViewSet(ModelViewSet):
    serializer_class = OrderProductsSerializers
    def get_queryset(self):
        return OrderProducts.objects.filter(order__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save()
        
        
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
        
        
    



class WishlistViewSet(ModelViewSet):
    serializer_class = WishlistSerializers
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]
    
    def get_queryset(self):
        user = self.request.user
        queryset = wishlist_model.objects.filter(user=user)
       
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    

    @action(detail=True, methods=['get'])
    def retrieve_wishlist(self, request, pk=None):
        address = self.get_object()
        serializer = self.get_serializer(address)
        return Response(serializer.data)
    
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    

    
    


class AddressViewSet(ModelViewSet):
    serializer_class = AddressSerializers
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]
    
    def get_queryset(self):
        user = self.request.user
        queryset = Address.objects.filter(user=user)
       
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    

    @action(detail=True, methods=['get'])
    def retrieve_address(self, request, pk=None):
        address = self.get_object()
        serializer = self.get_serializer(address)
        return Response(serializer.data)
    
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)






class BigBannersViewSet(ModelViewSet):
    serializer_class = BigBannerSerializer
    renderer_classes = [UserRenderer]
    
    def get_queryset(self):
        queryset = BigBanner.objects.all()
       
        return queryset
    
    
class SideBannersViewSet(ModelViewSet):
    serializer_class = SideBannerSerializer
    renderer_classes = [UserRenderer]
    
    def get_queryset(self):
        queryset = SideBanner.objects.all()
       
        return queryset
    
    
class ShippingViewSet(ModelViewSet):
    serializer_class = ShippingSerializer
    renderer_classes = [UserRenderer]
    
    def get_queryset(self):
        queryset = Shipping.objects.all()
       
        return queryset
    

    
    

class BankinfoViewSet(ModelViewSet):
    serializer_class = BankInfoSerializer
    renderer_classes = [UserRenderer]
    
    def get_queryset(self):
        queryset = BankInfo.objects.all()
       
        return queryset
    
    


class PrescriptionViewSet(ModelViewSet):
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]
    
    def get_queryset(self):
        user = self.request.user
        queryset = Prescribtion.objects.filter(user=user)
       
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    

    @action(detail=True, methods=['get'])
    def retrieve_prescription(self, request, pk=None):
        address = self.get_object()
        serializer = self.get_serializer(address)
        return Response(serializer.data)
    
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)





class AdvicesViewSet(ModelViewSet):
    serializer_class = AdvicesSerializer
    renderer_classes = [UserRenderer]
    
    def get_queryset(self):
        user = self.request.user
        queryset = Advices.objects.all()
       
        return queryset

    @action(detail=True, methods=['get'])
    def retrieve_advice(self, request, pk=None):
        address = self.get_object()
        serializer = self.get_serializer(address)
        return Response(serializer.data)
    
    
    


class LocationsViewSet(ModelViewSet):
    serializer_class = LocationsSerializer
    renderer_classes = [UserRenderer]
    
    def get_queryset(self):
        user = self.request.user
        queryset = Locations.objects.all()
       
        return queryset

    @action(detail=True, methods=['get'])
    def retrieve_locations(self, request, pk=None):
        address = self.get_object()
        serializer = self.get_serializer(address)
        return Response(serializer.data)