from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin


class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    search_fields = ['title']
    list_filter = ['featured', 'category']
    list_editable = ['price', 'featured', ]
    list_display = ['title', 'product_image', 'price', 'stock_count',
                    'category', 'featured']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category_image']
    search_fields = ['title']


class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category_image']
    search_fields = ['title']


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category_image']
    search_fields = ['title']


class OrdersProductsAdmin(admin.TabularInline):
    model = OrderProducts


class OrderAdmin(admin.ModelAdmin):
    list_filter = ['paid_status', 'cod']
    list_editable = ['paid_status', ]
    list_display = ['user',  'price', 'paid_status', 'cod', 'order_date']
    inlines = [OrdersProductsAdmin]


class OrderProductsAdmin(admin.ModelAdmin):
    list_display = ['order',
                    'qty', 'price', 'total']


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'review', 'rating']


class wishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'date']


class AddressAdmin(admin.ModelAdmin):
    list_editable = ['address', 'status']
    list_display = ['user', 'address', 'status']


class CouponAdmin(admin.ModelAdmin):
    list_editable = ['avalible']
    list_display = ['coupon',  'percentage', 'avalible']


class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['user',  'subject']


admin.site.register(Product, ProductAdmin)
admin.site.register(MainCategory, MainCategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Category, CategoryAdmin)
# admin.site.register(CartOrder, CartOrderAdmin)
# admin.site.register(CartOrderProducts, CartOrderProductsAdmin)

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProducts, OrderProductsAdmin)

admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(wishlist_model, wishlistAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Prescribtion, PrescriptionAdmin)
admin.site.register(BigBanner)
admin.site.register(SideBanner)
admin.site.register(Insurance)
admin.site.register(Advices)
admin.site.register(Doctor)
admin.site.register(Locations)
admin.site.register(SpecialTimeOffer)
admin.site.register(CartOrder)
admin.site.register(Shipping)
admin.site.register(BankInfo)
