import bleach
from rest_framework import serializers
from core.models import User
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import Util
import uuid

from core.models import (Product, Address, BigBanner, SideBanner, MainCategory, SubCategory, Category, CartOrder, CartOrderProducts, ProductImages,
                         SpecialTimeOffer, Coupon, Shipping, Order, OrderProducts, ProductReview, wishlist_model, Prescribtion, Advices, Locations, BankInfo)

from userauths.models import Profile, ContactUs


class UserRegistrationSerializer(serializers.ModelSerializer):
    # We are writing this becoz we need confirm password field in our Registratin Request
    class Meta:
        model = User
        fields = ['email', 'username', 'phone', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # Validating Password and Confirm Password while Registration
    def validate(self, attrs):
        password = attrs.get('password')

        if not password:
            raise serializers.ValidationError("Password is necessary")
        return attrs

    def create(self, validate_data):
        user = User.objects.create_user(**validate_data)
        return user


class ProfileForUserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class UserDetailsSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'phone', 'email', ]


class UserWithIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    userdata = UserDetailsSerializers(read_only=True)

    class Meta:
        model = User
        fields = ['phone', 'password',  'userdata']


class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError(
                "Password and Confirm Password doesn't match")
        user.set_password(password)
        user.save()
        return attrs


class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('Encoded UID', uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('Password Reset Token', token)
            link = 'http://localhost:8000/api-v1/reset-password/'+uid+'/'+token
            print('Password Reset Link', link)
            # Send EMail
            body = 'Click Following Link to Reset Your Password '+link
            data = {
                'subject': 'Reset Your Password',
                'body': body,
                'to_email': user.email
            }
            Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError('You are not a Registered User')


class SendResetEmail(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)

            token = Profile.objects.get(user=user).token
            link = 'http://localhost:8000/reset-password/'+token

            # Send EMail
            body = 'Click Following Link to Reset Your Password '+link
            data = {
                'subject': 'Reset Your Password',
                'body': body,
                'to_email': user.email
            }
            Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError('You are not a Registered User')


class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError(
                    "Password and Confirm Password doesn't match")
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError(
                    'Token is not Valid or Expired')
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError('Token is not Valid or Expired')


class MainCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MainCategory
        fields = '__all__'


class SubCategorySerializer(serializers.ModelSerializer):
    main_cat = MainCategorySerializer()

    class Meta:
        model = SubCategory
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    sub_cat = SubCategorySerializer()

    class Meta:
        model = Category
        fields = '__all__'


class ProductByIdSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id']


class ProductImagesSerializer(serializers.ModelSerializer):
    # product = ProductByIdSerializer()
    class Meta:
        model = ProductImages
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    english_description = serializers.SerializerMethodField()
    arabic_description = serializers.SerializerMethodField()
    english_specifications = serializers.SerializerMethodField()
    arabic_specifications = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'category', 'title', 'image',  'english_description', 'arabic_description', 'price', 'old_price',
                  'english_specifications', 'arabic_specifications', 'stock_count', 'in_stock', 'featured', 'is_prescription',
                  'images']

    def get_english_description(self, obj):

        try:
            return bleach.clean(obj.description_en, tags=[], strip=True)
        except:
            return ""

    def get_arabic_description(self, obj):

        try:
            return bleach.clean(obj.description_ar, tags=[], strip=True)
        except:
            return ""

    def get_english_specifications(self, obj):
        try:
            return bleach.clean(obj.specifications_en, tags=[], strip=True)
        except:
            return ""

    def get_arabic_specifications(self, obj):
        try:
            return bleach.clean(obj.specifications_ar, tags=[], strip=True)
        except:
            return ""

    def get_images(self, obj):
        images = obj.p_images.all()
        return ProductImagesSerializer(images, many=True).data


class SpecialTimeOfferSerializer(serializers.ModelSerializer):
    product = ProductByIdSerializer()

    class Meta:
        model = SpecialTimeOffer
        fields = '__all__'


class ProductReviewSerializer(serializers.ModelSerializer):
    user = UserWithIdSerializer()
    product = ProductByIdSerializer()
    review = serializers.CharField()
    rating = serializers.IntegerField()

    class Meta:
        model = ProductReview
        fields = '__all__'


class AddressSerializers(serializers.ModelSerializer):
    user = UserWithIdSerializer()
    mobile = serializers.CharField()
    address = serializers.CharField()
    status = serializers.BooleanField(default=False)

    class Meta:
        model = Address
        fields = '__all__'


class CouponSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coupon
        fields = '__all__'


class CartOrderProductsSerializers(serializers.ModelSerializer):

    # in_cart_products = ProductByIdSerializer()
    qty = serializers.IntegerField()
    price = serializers.IntegerField()
    total = serializers.IntegerField()

    class Meta:
        model = CartOrderProducts
        fields = ['cart', 'qty', 'price', 'total']


class CartOrderSerializers(serializers.ModelSerializer):
    user = UserWithIdSerializer()
    coupon = CouponSerializer()
    price = serializers.IntegerField()
    cart_products = CartOrderProductsSerializers(many=True)

    class Meta:
        model = CartOrder
        fields = ['id', 'user', 'price', 'coupon', 'cart_products']

    # def get_products(self, obj):
    #     products = obj.cart_products.all()
    #     return CartOrderProductsSerializers(products, many=True).data


class CartOrderProductsEditibleSerializers(serializers.ModelSerializer):

    # cart = CartOrderWithIDSerializers()
    # product = ProductByIdSerializer()
    qty = serializers.IntegerField()
    price = serializers.IntegerField()
    total = serializers.IntegerField()

    class Meta:
        model = CartOrderProducts
        fields = '__all__'


class OrderProductsSerializers(serializers.ModelSerializer):

    qty = serializers.IntegerField()
    price = serializers.IntegerField()
    total = serializers.IntegerField()

    class Meta:
        model = OrderProducts
        fields = '__all__'


class OrderSerializers(serializers.ModelSerializer):
    # user = UserWithIdSerializer()
    # address = AddressSerializers()
    price = serializers.IntegerField()
    paid_status = serializers.BooleanField(default=False)
    cod = serializers.BooleanField(default=False)
    products = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'

    def get_products(self, obj):
        products = obj.order_products.all()
        return OrderProductsSerializers(products, many=True).data


class WishlistSerializers(serializers.ModelSerializer):
    # user = UserWithIdSerializer()
    # product = ProductByIdSerializer()

    class Meta:
        model = wishlist_model
        fields = '__all__'


class BigBannerSerializer(serializers.ModelSerializer):

    class Meta:
        model = BigBanner()
        fields = '__all__'


class SideBannerSerializer(serializers.ModelSerializer):

    class Meta:
        model = SideBanner()
        fields = '__all__'


class ShippingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shipping
        fields = '__all__'


class BankInfoSerializer(serializers.ModelSerializer):
    english_instructions = serializers.SerializerMethodField()
    english_account_info = serializers.SerializerMethodField()
    arabic_instructions = serializers.SerializerMethodField()
    arabic_account_info = serializers.SerializerMethodField()

    class Meta:
        model = BankInfo
        fields = ['english_instructions', 'english_account_info',
                  'arabic_instructions', 'arabic_account_info']

    def get_english_instructions(self, obj):

        try:
            return bleach.clean(obj.instructions_en, tags=[], strip=True)
        except:
            return ""

    def get_english_account_info(self, obj):

        try:
            return bleach.clean(obj.account_info_en, tags=[], strip=True)
        except:
            return ""

    def get_arabic_instructions(self, obj):

        try:
            return bleach.clean(obj.instructions_ar, tags=[], strip=True)
        except:
            return ""

    def get_arabic_account_info(self, obj):

        try:
            return bleach.clean(obj.account_info_ar, tags=[], strip=True)
        except:
            return ""


class PrescriptionSerializer(serializers.ModelSerializer):
    user = UserWithIdSerializer()

    class Meta:
        model = Prescribtion
        fields = '__all__'


class AdvicesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Advices
        fields = '__all__'


class LocationsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Locations
        fields = '__all__'
