from django.urls import path
from .views import *


product_list = ProductsViewSet.as_view({'get': 'list', 'post': 'create'})
product_detail = ProductsViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})
review_list = ProductReviewViewSet.as_view({'get': 'list', 'post': 'create'})
offer_list = SpecialOfferViewSet.as_view({'get': 'list'})


category_list = CategoryViewSet.as_view({'get': 'list'})
category_detail = CategoryViewSet.as_view({'get': 'retrieve'})



main_category_list = MainCategoriesViewSet.as_view({'get': 'list'})
main_category_detail = MainCategoriesViewSet.as_view({'get': 'retrieve'})



cart_list = CartOrderViewSet.as_view({'get': 'list', 'post': 'create'})
cart_product_list = CartOrderProductsViewSet.as_view({'get': 'list', 'post':'create'})
cart_product_detail = CartOrderProductsViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})




order_list = OrderViewSet.as_view({'get': 'list', 'post':'create'})
order_product_list = OrderProductsViewSet.as_view({'get': 'list', 'post':'create'})
order_product_detail = OrderProductsViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})




wishlist_list = WishlistViewSet.as_view({'get': 'list', 'post':'create'})
wishlist_product_detail = WishlistViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})




address_list = AddressViewSet.as_view({'get': 'list', 'post':'create'})
address_detail = AddressViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})





bigbanners_list = BigBannersViewSet.as_view({'get': 'list'})
sidebanners_list = SideBannersViewSet.as_view({'get': 'list'})



shipping = ShippingViewSet.as_view({'get': 'list'})


bankinfo = BankinfoViewSet.as_view({'get': 'list'})





prescription_list = PrescriptionViewSet.as_view({'get': 'list', 'post':'create'})
prescription_detail = PrescriptionViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})




advices_list = AdvicesViewSet.as_view({'get': 'list'})
advice_detail = AdvicesViewSet.as_view({'get': 'retrieve'})




locations_list = LocationsViewSet.as_view({'get': 'list'})
locations_detail = LocationsViewSet.as_view({'get': 'retrieve'})






urlpatterns = [
    # Authentication routes
    path('register', UserRegistrationView.as_view(), name='api_register'),

    path('login', UserLoginView.as_view()),
    path('changepassword', UserChangePasswordView.as_view(),
         name='api_changepassword'),
    
    path('send-reset-password-email', SendPasswordResetEmailView.as_view(),
         name='api_send-reset-password-email'),
    path('reset-password/<uid>/<token>',
         UserPasswordResetView.as_view(), name='api_reset-password'),


  

    path('products', product_list),
    path('product/<int:pk>/', product_detail),
    path('reviews/<int:product_id>/', review_list),
    
    path('offers/', offer_list),



    path('categories', category_list),
    path('category/<int:pk>/', category_detail),
    
    path('main-categories', category_list),
    path('main-category/<int:pk>/', category_detail),
    
    
    
     path('cart', cart_list),
    
     path('cart-products', cart_product_list),
     path('cart-products/<int:pk>', cart_product_detail),
     
     
     
     
     path('order', order_list),
    
     path('order-products', order_product_list),
     path('order-products/<int:pk>', order_product_detail),
     
     
     
     
     path('wishlist', wishlist_list),
     path('wishlist-product/<int:pk>', wishlist_product_detail),
     


     path('addresses', address_list),
     path('address/<int:pk>', address_detail),
     
     
     
     
     path('bigbanners', bigbanners_list),
     
     
     path('sidebanners', sidebanners_list),
     
     
     path('shipping', shipping),
     
     
     path('bankinfo', bankinfo),
     
  
  
       path('prescription', prescription_list),
     path('prescription/<int:pk>', prescription_detail),
     
     
     
          path('advice', advices_list),
     path('advice/<int:pk>', advice_detail),
     
     
     
          path('location', locations_list),
     path('location/<int:pk>', locations_detail),   
     
     
     
     
     
     
     
     
     
     

]
