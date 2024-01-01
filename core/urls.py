from django.urls import path, include
from core.views import *

urlpatterns = [

    # Homepage
    path("", index, name="index"),
    path("products/", product_list_view, name="product-list"),
    path("product/<int:id>/", product_detail_view, name="product-detail"),

    # Category
    path("category/", category_list_view, name="category-list"),
    path("category/<int:id>/", category_product_list__view,
         name="category-product-list"),

    path("main-category/<int:id>/", main_category_products,
         name="main_category_products"),

    # Tags
    path("products/tag/<slug:tag_slug>/", tag_list, name="tags"),

    # Add Review
    path("ajax-add-review/<int:id>/", ajax_add_review, name="ajax-add-review"),

    # Search
    path("search/", search_view, name="search"),


    # Add to cart URL
    path("add-to-cart/<int:id>", add_to_cart, name="add-to-cart"),
    path("add-to-cart/", add_to_cart_form, name="add_to_cart_form"),

    # Cart Page URL
    path("cart/", cart_view, name="cart"),

    # Delete ITem from Cart
    path("delete-from-cart/", delete_item_from_cart, name="delete-from-cart"),

    # Update  Cart
    path("update-cart/", update_cart, name="update-cart"),

    # Checkout  URL
    path("checkout/", checkout_view, name="checkout"),
    path('coupon', apply_coupon, name="coupon"),
    path("cod-checkout/", cod_checkout, name="cod_checkout"),
    path("stripe-checkout", become_pro, name="stripe_checkout"),
    path("add-address",
         add_address, name="add-address"),




    # Payment Successful
    path("payment-completed/", payment_completed_view, name="payment-completed"),
    path("payment-completed-cod/", payment_completed_by_cod,
         name="payment_completed_by_cod"),


    # Payment Failed
    path("payment-failed/", payment_failed_view, name="payment-failed"),

    # Dahboard URL
    path("dashboard/", customer_dashboard, name="dashboard"),

    # Order Detail URL
    path("dashboard/order/<int:id>", order_detail, name="order-detail"),

    # Making address defauly
    path("make-default-address/", make_address_default,
         name="make-default-address"),

    # wishlist page
    path("wishlist/", wishlist_view, name="wishlist"),

    # adding to wishlist
    path("add-to-wishlist/", add_to_wishlist, name="add-to-wishlist"),


    # Remvoing from wishlist
    path("remove-from-wishlist/", remove_wishlist, name="remove-from-wishlist"),


    path("contact/", contact, name="contact"),
    path("ajax-contact-form/", ajax_contact_form, name="ajax-contact-form"),

    path("doctors/", doctors, name="doctors"),

    path("prescribtions/", prescribtions, name="prescribtions"),
    path("prescription-form/", presform, name="presform"),
    path("prescription-with-insurance-form/",
         presinsurance, name="presinsurance"),
    path("pres-create/", prescreate, name="prescreate"),
    path("pres-details/<int:id>", presdetails, name="presdetails"),

    path("advices/", advices, name="advices"),
    path("advice/<int:id>", advice, name="advice"),

    path("location/<int:id>", location, name="location"),


    path("about_us/", about_us, name="about_us"),
    path("purchase_guide/", purchase_guide, name="purchase_guide"),
    path("privacy_policy/", privacy_policy, name="privacy_policy"),
    path("terms_of_service/", terms_of_service, name="terms_of_service"),
]
