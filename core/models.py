from django.db import models
from django.utils.html import mark_safe
from userauths.models import User
from django.db.models import Count
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models import Avg
STATUS_CHOICE = (
    ("processing", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
)


RATING = (
    (1,  "★☆☆☆☆"),
    (2,  "★★☆☆☆"),
    (3,  "★★★☆☆"),
    (4,  "★★★★☆"),
    (5,  "★★★★★"),
)


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    mobile = models.CharField(max_length=300, null=True)
    address = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=False)

    class Meta:

        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')

    def __str__(self):
        return self.address


class BigBanner(models.Model):
    image = models.ImageField(upload_to="big_banners",
                              default="big_banners.jpg")
    name = models.CharField(max_length=50, default="Skin Care")
    url = models.URLField(blank=True, null=True)
    user_catcher = models.CharField(max_length=50, default="Big discount")
    short_line = models.CharField(
        max_length=100, default="Save 80 percent on all products flat")

    class Meta:

        verbose_name = _('Big Banner')
        verbose_name_plural = _('Big Banners')

    def __str__(self):
        return self.name


class SideBanner(models.Model):
    image = models.ImageField(upload_to="side_banners",
                              default="side_banners.jpg")
    type = models.CharField(max_length=50, default="organic")
    url = models.URLField(blank=True, null=True)
    user_catcher = models.CharField(
        max_length=50, default="discounts no all products")

    class Meta:

        verbose_name = _('Side Banner')
        verbose_name_plural = _('Side Banners')

    def __str__(self):
        return self.type


class MainCategory(models.Model):
    title = models.CharField(max_length=100, default="")
    image = models.ImageField(upload_to="maincategory", default="category.jpg")

    class Meta:

        verbose_name = _('Main Category')
        verbose_name_plural = _('Main Categories')

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def product_count(self):
        # count the number of products for each category
        category_counts = Category.objects.filter(
            sub_cat__main_cat=self).annotate(
            product_count=Count('products'))

        # sum up the product counts for all categories
        total_product_count = sum(
            [c.product_count for c in category_counts])

        return total_product_count

    def __str__(self):
        return self.title


class SubCategory(models.Model):
    main_cat = models.ForeignKey(
        MainCategory, on_delete=models.CASCADE, related_name="subcats")
    title = models.CharField(max_length=100, default="")
    image = models.ImageField(upload_to="subcategory", default="category.jpg")

    class Meta:

        verbose_name = _('Sub Category')
        verbose_name_plural = _('Sub Categories')

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title


class Category(models.Model):
    sub_cat = models.ForeignKey(
        SubCategory, on_delete=models.CASCADE, related_name="cats")
    title = models.CharField(max_length=100, default="")
    image = models.ImageField(upload_to="category", default="category.jpg")

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="products")
    title = models.CharField(max_length=100, default="")
    image = models.ImageField(
        upload_to="Product Images", default="product.jpg")
    # description = models.TextField(null=True, blank=True, default="This is the product")
    description = RichTextUploadingField(
        null=True, blank=True, default="This is the product")

    price = models.PositiveIntegerField()
    old_price = models.PositiveIntegerField(null=True, blank=True)

    specifications = RichTextUploadingField(null=True, blank=True)
    # specifications = models.TextField(null=True, blank=True)

    stock_count = models.CharField(
        max_length=100, default=100, null=True, blank=True)

    tags = TaggableManager(blank=True)

    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    is_prescription = models.BooleanField(default=False)

    views = models.PositiveIntegerField(default=0)

    date = models.DateTimeField(auto_now_add=True)

    class Meta:

        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title

    def get_precentage(self):
        if self.old_price is None or self.old_price == 0:
            print(f"{self.id} price is {self.old_price}")
            return 0
        else:
            new_price = (self.price / self.old_price) * 100
            return new_price

    def average_rating(self):
        return self.reviews.aggregate(Avg('rating'))['rating__avg']

    def percentage_rating(self):
        try:
            print()
            return (self.average_rating()/5)*100
        except:
            return 0


class ProductImages(models.Model):
    images = models.ImageField(
        upload_to="product-images", default="product.jpg")
    product = models.ForeignKey(
        Product, related_name="p_images", on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:

        verbose_name = _('Product Image')
        verbose_name_plural = _('Product Images')


class SpecialTimeOffer(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True)
    end_at = models.DateTimeField(null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:

        verbose_name = _('Special Time Offer')
        verbose_name_plural = _('Special Time Offers')

    def ending(self):
        date_time = self.end_at.strftime('%Y-%m-%d %H:%M:%S')
        return date_time


class Coupon(models.Model):
    coupon = models.CharField(max_length=20)
    percentage = models.PositiveIntegerField()
    avalible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.coupon}:  {self.percentage}%"


class Shipping(models.Model):
    price = models.IntegerField(default=500)

    def __str__(self):
        return f"{self.price}"


class CartOrder(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="cart")
    price = models.PositiveIntegerField(blank=True, null=True)
    order_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, null=True)

    class Meta:

        verbose_name = _('Cart Order')
        verbose_name_plural = _('Cart Orders')

    def get_total_price(self):

        total_price = 0
        for item in self.cart_products.all():
            total_price += item.qty * item.price
        self.price = total_price
        if self.coupon != None:
            discounts = self.price * (self.coupon.percentage / 100)
            self.price = total_price - discounts
            return self.price
        else:
            return self.price

    def get_all_cart_items(self):

        number = self.cart_products.all().count()
        return number


class CartOrderProducts(models.Model):
    cart = models.ForeignKey(
        CartOrder, on_delete=models.CASCADE, related_name="cart_products")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="in_cart_products", blank=True, null=True)
    qty = models.IntegerField(default=0)
    price = models.PositiveIntegerField(blank=True, null=True)
    total = models.PositiveIntegerField(blank=True, null=True)

    class Meta:

        verbose_name = _('Cart Order Item')
        verbose_name_plural = _('Cart Order Items')

    def __str__(self):
        return self.product.title

    def order_img(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image))

    def save(self, *args, **kwargs):
        # Get the price of the related Product instance
        product_price = self.product.price

        # Set the price and calculate the total based on the quantity
        self.price = product_price
        self.total = self.qty * product_price

        # Call the parent save method to save the model instance
        super(CartOrderProducts, self).save(*args, **kwargs)
############################################## Product Revew, wishlists, Address ##################################


class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="orders")
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, null=True, blank=True)

    price = models.PositiveIntegerField(blank=True, null=True)
    paid_status = models.BooleanField(default=False, null=True, blank=True)
    cod = models.BooleanField(default=False, null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    product_status = models.CharField(
        choices=STATUS_CHOICE, max_length=30, default="processing")
    invoice_id = models.CharField(max_length=20, default='')

    class Meta:

        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def get_total_price(self):
        return self.price


class OrderProducts(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_products")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="in_order_products", blank=True, null=True)
    qty = models.IntegerField(default=0)
    price = models.PositiveIntegerField(blank=True, null=True)
    total = models.PositiveIntegerField(blank=True, null=True)

    class Meta:

        verbose_name = _('Order Item')
        verbose_name_plural = _('Order Items')

    def __str__(self):
        return self.product.title

    def order_img(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image))

    def save(self, *args, **kwargs):
        # Get the price of the related Product instance
        product_price = self.product.price

        # Set the price and calculate the total based on the quantity
        self.price = product_price
        self.total = self.qty * product_price

        # Call the parent save method to save the model instance
        super(OrderProducts, self).save(*args, **kwargs)


class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, related_name="reviews")
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:

        verbose_name = _('Product Review')
        verbose_name_plural = _('Product Reviews')

    def __str__(self):
        return self.product.title

    def get_rating(self):
        return self.rating


class wishlist_model(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:

        verbose_name = _('Whishlist')
        verbose_name_plural = _('Whishlists')

    def __str__(self):
        return self.product.title


class Insurance(models.Model):

    company = models.CharField(max_length=200)

    class Meta:

        verbose_name = _('Insurance')
        verbose_name_plural = _('Insurances')

    def __str__(self):
        return self.company


class Prescribtion(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="prescrbtions")
    subject = models.CharField(max_length=200)
    image = models.ImageField(upload_to="prescription", null=True, blank=True)
    insurance = models.ForeignKey(
        Insurance, on_delete=models.CASCADE, related_name="prescrbtions", null=True, blank=True)

    insurance_image = models.ImageField(
        upload_to="prescription/insurance", null=True, blank=True)

    class Meta:

        verbose_name = _('Prescrbtion')
        verbose_name_plural = _('Prescrbtions')

    def __str__(self):
        return self.user.username


class Doctor(models.Model):
    name = models.CharField(max_length=70)
    details = models.TextField(null=True, blank=True)
    speciality = models.CharField(max_length=200)
    number = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to="Doctors")
    timing = models.CharField(max_length=200)

    class Meta:

        verbose_name = _('Doctor')
        verbose_name_plural = _('Doctors')

    def __str__(self):
        return self.name


class Advices(models.Model):
    image = models.ImageField(upload_to="advices")
    title = models.CharField(max_length=1000, blank=True, null=True)
    description = models.TextField()
    advice = RichTextUploadingField(
        null=True, blank=True)

    class Meta:

        verbose_name = _('Advice')
        verbose_name_plural = _('Advices')

    def __str__(self):
        return self.title


class Locations(models.Model):
    city_name = models.CharField(max_length=300, null=True, blank=True)
    map_iframe = models.CharField(max_length=2000)
    details = RichTextUploadingField(
        null=True, blank=True)

    class Meta:

        verbose_name = _('Location')
        verbose_name_plural = _('Locations')

    def __str__(self):
        return self.city_name


class BankInfo(models.Model):
    instructions = RichTextUploadingField()
    account_info = RichTextUploadingField()

    class Meta:

        verbose_name = _('Bank Information')
        verbose_name_plural = _('Bank Information')

    def __str__(self):
        return f"Account Info id={self.id}"
