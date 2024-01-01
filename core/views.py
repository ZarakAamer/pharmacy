
import random
from .models import Doctor, Insurance
from django.utils import timezone
from userauths.models import User
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from taggit.models import Tag
from core.models import Locations, Prescribtion, Product, Category, CartOrder, CartOrderProducts, ProductImages, SpecialTimeOffer
from .models import ProductReview, wishlist_model, Address, MainCategory, SubCategory, Advices, Order, OrderProducts, Coupon, Shipping
from userauths.models import ContactUs, Profile
from core.forms import ProductReviewForm
from django.template.loader import render_to_string
from django.contrib import messages

from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

import calendar
from django.db.models import Count, Avg
from django.db.models.functions import ExtractMonth
from django.core import serializers
import stripe
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

stripe.api_key = 'sk_test_51L3uK1BvsUtCkGsqXQRmyG0x77zJbliYFGwN8225mCjQUy6CnBZzoKHiDb0cubptFLy16DTIoAYfHMlqvoex4B7Q00YTk5w816'


def index(request):

    featured = Product.objects.filter(
        featured=True)
    products = Product.objects.all(
    ).order_by("-id")
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 30)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    trending = Product.objects.all(
    ).order_by("-views")[:10]

    recent = Product.objects.all(
    ).order_by("-id")[:10]

    rated = Product.objects.annotate(
        avg_rating=Avg('reviews__rating')).order_by('-avg_rating')[:10]

    context = {
        "products": products,
        "trending": trending,
        "rated": rated,
        "recent": recent,
        "featured": featured
    }

    return render(request, 'core/index.html', context)


def product_list_view(request):
    products = Product.objects.all().order_by("-id")
    tags = Tag.objects.all().order_by("-id")[:6]

    context = {
        "products": products,
        "tags": tags,
    }

    return render(request, 'core/product-list.html', context)


def category_list_view(request):
    main_cats = MainCategory.objects.all()
    sub_cats = SubCategory.objects.all()
    categories = Category.objects.all()

    context = {
        "main_cats": main_cats,
        "sub_cats": sub_cats,
        "categories": categories
    }
    return render(request, 'core/category-list.html', context)


def category_product_list__view(request, id):

    category = Category.objects.get(id=id)
    products = Product.objects.filter(category=category)

    context = {
        "category": category,
        "products": products,
    }
    return render(request, "core/category-product-list.html", context)


def main_category_products(request, id):
    main_category = MainCategory.objects.get(id=id)
    sub_cats = main_category.subcats.all()
    products_list = []
    for i in sub_cats:
        categs = i.cats.all()
        for j in categs:
            products_list.append(j.products.all())

    # products_counting = main_category.product_count()
    # print("This is products counted from the model function " +
    #       str(products_counting))
    # [print(i) for i in products_list]
    # products_count = len(products_list)
    products_count = main_category.product_count()
    # print(products_count)
    context = {
        "category": main_category,
        "products": products_list,
        "products_count": products_count,
    }

    return render(request, "core/main-cats-.html", context)


def product_detail_view(request, id):
    product = Product.objects.get(id=id)
    product.views += 1
    product.save()

    # product = get_object_or_404(Product, id=id)
    products = Product.objects.filter(
        category=product.category).exclude(id=id)

    # Getting all reviews related to a product
    reviews = ProductReview.objects.filter(product=product).order_by("-date")

    # Getting average review
    average_rating = ProductReview.objects.filter(
        product=product).aggregate(rating=Avg('rating'))
    # Product Review form
    review_form = ProductReviewForm()

    make_review = True

    if request.user.is_authenticated:

        user_review_count = ProductReview.objects.filter(
            user=request.user, product=product).count()

        if user_review_count > 0:
            make_review = False

    p_image = product.p_images.all()

    context = {
        "p": product,

        "make_review": make_review,
        "review_form": review_form,
        "p_image": p_image,
        "average_rating": average_rating,
        "reviews": reviews,
        "products": products,
    }

    return render(request, "core/product-detail.html", context)


def tag_list(request, tag_slug=None):

    products = Product.objects.all(
    ).order_by("-id")

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])

    context = {
        "products": products,
        "tag": tag
    }

    return render(request, "core/tag.html", context)


def ajax_add_review(request, id):
    product = Product.objects.get(pk=id)
    user = request.user

    review = ProductReview.objects.create(
        user=user,
        product=product,
        review=request.POST['review'],
        rating=request.POST['rating'],
    )

    context = {
        'user': user.username,
        'review': request.POST['review'],
        'rating': request.POST['rating'],
    }

    average_reviews = ProductReview.objects.filter(
        product=product).aggregate(rating=Avg("rating"))

    return JsonResponse(
        {
            'bool': True,
            'context': context,
            'average_reviews': average_reviews
        }
    )


def search_view(request):
    query = request.GET.get("q")

    products = Product.objects.filter(title__icontains=query).order_by("-date")

    context = {
        "products": products,
        "query": query,
    }
    return render(request, "core/search.html", context)


def add_to_cart_form(request):
    if request.user.is_authenticated:
        quantity = request.GET.get('qty')
        id = request.GET.get('id')
        user = request.user
        product = Product.objects.get(id=id)
        if CartOrder.objects.filter(user=user).exists():
            if CartOrderProducts.objects.filter(product=product).exists():
                context = {
                    "msg": "exist"
                }
                return JsonResponse(context)
                # return redirect('/')
            else:
                cart = CartOrder.objects.filter(user=user).first()
                if int(quantity) > int(product.stock_count):
                    context = {
                        "msg": "low quantity"
                    }
                    return JsonResponse(context)
                    # return redirect('/')

                elif int(product.stock_count) == 0:
                    messages.warning(
                        request, f'{product.title} is in out of stock! ')
                    # return redirect('/')
                    context = {
                        "msg": "no stock"
                    }
                    return JsonResponse(context)

                CartOrderProducts.objects.create(
                    cart=cart,  product=product, qty=int(quantity))
                context = {
                    "msg": "added"
                }
                return JsonResponse(context)
        else:
            cart = CartOrder.objects.create(user=user)
            CartOrderProducts.objects.create(
                cart=cart, product=product, qty=int(quantity))
            context = {
                "msg": "added"
            }
            return JsonResponse(context)
    else:
        return JsonResponse({"msg": "login"})


@login_required
def add_to_cart(request, id):
    user = request.user
    product = Product.objects.get(id=id)
    if CartOrder.objects.filter(user=user).exists():
        if CartOrderProducts.objects.filter(product=product).exists():
            messages.warning(
                request, f'{product.title} already exists in your cart! ')
            return redirect('/')
        else:
            cart = CartOrder.objects.filter(user=user).first()
            CartOrderProducts.objects.create(
                cart=cart, product=product, qty=1)

    else:
        cart = CartOrder.objects.create(user=user)
        CartOrderProducts.objects.create(
            cart=cart, product=product, qty=1)
        messages.success(
            request, f'{product.title} added to your cart your cart! ')
    return redirect('/')


@login_required
def cart_view(request):
    user = request.user
    if CartOrder.objects.filter(user=user).first():
        cart = CartOrder.objects.filter(
            user=user).first()

        items = cart.cart_products.all()
        if len(items) == 0:

            messages.warning(request, "Your cart is empty")
            return redirect("index")
        else:
            cart.price = cart.get_total_price()
            cart.save()
            context = {"items": items, "cart": cart, 'cart_price': cart.price}
            print(context)
            return render(request, 'core/cart.html', context)

    else:
        return redirect("index")


def delete_item_from_cart(request):
    if request.method == "POST":
        item_id = request.POST.get("item_id")
        product = CartOrderProducts.objects.get(id=item_id)
        product.delete()
        return redirect("cart")
    else:
        return redirect("cart")


@login_required
def update_cart(request):
    if request.method == 'POST':
        quantity = request.POST.get('item_quantity')
        item_id = request.POST.get('item_id')
        product = CartOrderProducts.objects.get(id=item_id)
        product.qty = int(quantity)
        product.save()

        return redirect("cart")
    else:
        return redirect("cart")


def apply_coupon(request):
    if request.method == 'POST':
        coupon = request.POST.get('coupon')
        cart_id = request.POST.get('cart')
        if Coupon.objects.filter(coupon=coupon, avalible=True).exists():
            coupon = Coupon.objects.filter(
                coupon=coupon, avalible=True).first()
            cart = CartOrder.objects.get(id=cart_id)
            cart.coupon = coupon

            cart.save()
            return redirect("cart")
        else:
            messages.warning(request, "Coupon Invalid or Expired!")
            return redirect("cart")
    else:
        return redirect('cart')


@login_required
def checkout_view(request):
    if request.method == "POST":
        cart_id = request.POST.get("cart_id")
        cart = CartOrder.objects.get(id=cart_id)
        totalcartitems = cart.cart_products.all()
        cart.price = cart.get_total_price()

        cart.save()

        updated_price = cart.price + Shipping.objects.all()[0].price
        try:
            active_address = Address.objects.get(
                user=request.user, status=True)

            return render(request, "core/checkout.html", {"cart": cart, "cart_data": totalcartitems, 'totalcartitems': len(totalcartitems), 'cart_total_amount': cart.price, "sub_total": updated_price, "active_address": active_address})

        except:
            messages.warning(
                request, "one should be activated.")
            active_address = None

            return render(request, "core/checkout.html", {"cart": cart, "cart_data": totalcartitems, 'totalcartitems': len(totalcartitems), 'cart_total_amount': cart.price,  "sub_total": updated_price, "active_address": active_address})

    else:
        return redirect("cart")


@login_required
def cod_checkout(request):
    if request.method == "POST":
        cart_id = request.POST.get("cart_id")
        cart = CartOrder.objects.get(id=cart_id)
        cart.cod = True
        cart.save()
        messages.success(request, "Order Placed Successfully!")
        url = reverse('payment_completed_by_cod') + f'?cart_id={cart_id}'
        return redirect(url)
    else:
        messages.warning(request, "Order was not placed Successfully!")
        return redirect("cart")


@login_required
def payment_completed_by_cod(request):
    cart_id = request.GET.get('cart_id')
    cart = CartOrder.objects.get(id=cart_id)
    address = Address.objects.filter(user=request.user, status=True).first()
    updated_price = int(cart.get_total_price()) + \
        int(Shipping.objects.all()[0].price)
    invoice = f"{cart_id}{random.randint(999, 999999)}"
    order = Order.objects.create(
        user=request.user, address=address, price=updated_price, paid_status=False, cod=True, invoice_id=invoice)
    cart_products = cart.cart_products.all()
    for i in cart_products:
        OrderProducts.objects.create(order=order,
                                     product=i.product, qty=i.qty, price=i.price, total=i.total)

    cart.delete()
    sub_total = order.price - int(Shipping.objects.all()[0].price)
    return render(request, 'core/payment-completed.html',  {'cart_data': order, 'sub_total': sub_total, "invoice": invoice})


@ login_required
def become_pro(request):
    if request.method == "POST":
        user_id = request.user
        cart_id = request.POST.get("cart_id")
        cart = CartOrder.objects.get(id=cart_id)
        price = cart.get_total_price() + Shipping.objects.all()[0].price
        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': user_id.username,
                        },
                        'unit_amount': int(price)*100,
                        },
                'quantity': 1,
            }],

            mode='payment',
            metadata={"user_id": user_id,
                      "cart_id": id},
            success_url=request.build_absolute_uri(
                reverse('payment-completed')) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri(
                reverse('payment-failed'))

        )

        context = {
            'session_id': session.id
        }
    return render(request, 'core/stripe_checkout.html', context)


@login_required
def payment_completed_view(request):
    # cart_id = request.GET.get('cart_id')
    # cart = CartOrder.objects.get(id=cart_id)
    session_id = request.GET.get('session_id')
    session = stripe.checkout.Session.retrieve(session_id)

    # user_id, cart_id = client_reference_id.split('-')
    print('**************************888')
    print(session)
    # print(session["metadata"]["cart_id"])

    cart_id = session["metadata"]["cart_id"]
    cart = CartOrder.objects.get(id=cart_id)
    coupon = cart.coupon
    updated_price = int(cart.get_total_price()) + \
        int(Shipping.objects.all()[0].price)
    order = Order.objects.create(
        user=request.user, price=updated_price, paid_status=True, cod=False)
    cart_products = cart.cart_products.all()
    for i in cart_products:
        OrderProducts.objects.create(order=order,
                                     product=i.product, qty=i.qty, price=i.price, total=i.total)
    cart.delete()
    sub_total = order.price - int(Shipping.objects.all()[0].price)
    return render(request, 'core/payment-completed.html',  {'cart_data': order, 'sub_total': sub_total, "coupon": coupon})


@login_required
def payment_failed_view(request):
    return render(request, 'core/payment-failed.html')


@login_required
def add_address(request):
    if request.method == 'POST':
        user = request.user
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        billing_address = request.POST.get('billing_address')
        if Address.objects.filter(user=user).exists():
            for address in Address.objects.filter(user=user):
                if address.status == True:
                    address.status = False
                    address.save()
        Address.objects.create(user=user, mobile=lname,
                               address=billing_address, status=True)
        messages.success(request, 'Your address was added!')
        return redirect('checkout')
    else:
        messages.warning(request, 'Your address was not added!')
        return redirect('checkout')


@login_required
def customer_dashboard(request):
    orders_list = Order.objects.filter(user=request.user).order_by("-id")
    address = Address.objects.filter(user=request.user)

    orders = Order.objects.annotate(month=ExtractMonth("order_date")).values(
        "month").annotate(count=Count("id")).values("month", "count")
    month = []
    total_orders = []

    for i in orders:
        try:

            month.append(calendar.month_name[i["month"]])
            total_orders.append(i["count"])
        except:
            pass
    if request.method == "POST":
        address = request.POST.get("address")
        mobile = request.POST.get("mobile")

        new_address = Address.objects.create(
            user=request.user,
            address=address,
            mobile=mobile,
        )
        messages.success(request, "Address Added Successfully.")
        return redirect("dashboard")
    else:
        print("Error")

    user_profile = Profile.objects.get(user=request.user)
    print("user profile is: #########################",  user_profile)

    context = {
        "user_profile": user_profile,
        "orders": orders,
        "orders_list": orders_list,
        "address": address,
        "month": month,
        "total_orders": total_orders,
    }
    return render(request, 'core/dashboard.html', context)


@login_required
def order_detail(request, id):
    order = Order.objects.get(user=request.user, id=id)
    order_items = order.order_products.all()

    context = {
        "order_items": order_items,
    }
    return render(request, 'core/order-detail.html', context)


def make_address_default(request):
    id = request.GET['id']
    Address.objects.update(status=False)
    Address.objects.filter(id=id).update(status=True)
    return JsonResponse({"boolean": True})


@login_required
def wishlist_view(request):
    wishlist = wishlist_model.objects.all()
    context = {
        "w": wishlist
    }
    return render(request, "core/wishlist.html", context)

    # w
# @login_required


def add_to_wishlist(request):
    if request.user.is_authenticated:

        product_id = request.GET['id']
        product = Product.objects.get(id=product_id)
        print("product id isssssssssssss:" + product_id)

        context = {}

        wishlist_count = wishlist_model.objects.filter(
            product=product, user=request.user).count()
        print(wishlist_count)

        if wishlist_count > 0:
            context = {
                "bool": True

            }
        else:
            new_wishlist = wishlist_model.objects.create(
                user=request.user,
                product=product,
            )
            context = {
                "bool": True
            }

        return JsonResponse(context)
    else:
        context = {
            "bool": False
        }

        return JsonResponse(context)


# def remove_wishlist(request):
#     id = request.GET['id']
#     wishlist = wishlist_model.objects.filter(user=request.user).values()

#     product = wishlist_model.objects.get(id=id)
#     h = product.delete()

#     context = {
#         "bool": True,
#         "wishlist":wishlist
#     }
#     t = render_to_string("core/async/wishlist-list.html", context)
#     return JsonResponse({"data": t, "w":wishlist})

def remove_wishlist(request):
    id = request.GET['id']
    wishlist = wishlist_model.objects.filter(user=request.user)
    wishlist_d = wishlist_model.objects.get(id=id)
    delete_product = wishlist_d.delete()

    context = {
        "bool": True,
        "w": wishlist
    }
    wishlist_json = serializers.serialize('json', wishlist)
    t = render_to_string('core/wishlist-list.html', context)
    return JsonResponse({'data': t, 'w': wishlist_json})


# Other Pages
def contact(request):
    return render(request, "core/contact.html")


def ajax_contact_form(request):
    full_name = request.GET['full_name']
    email = request.GET['email']
    phone = request.GET['phone']
    subject = request.GET['subject']
    message = request.GET['message']

    contact = ContactUs.objects.create(
        full_name=full_name,
        email=email,
        phone=phone,
        subject=subject,
        message=message,
    )

    data = {
        "bool": True,
        "message": "Message Sent Successfully"
    }

    return JsonResponse({"data": data})


def doctors(request):
    doctors = Doctor.objects.all()
    context = {"doctors": doctors}
    return render(request, 'core/doctors.html', context)


@login_required
def prescribtions(request):
    preses = Prescribtion.objects.filter(user=request.user)
    return render(request, "core/prescribtions.html", {"preses": preses})


@login_required
def presform(request):

    return render(request, "core/presform.html")


@login_required
def presinsurance(request):
    insurances = Insurance.objects.all()

    return render(request, "core/presinsurance.html", {"insurances": insurances})


@login_required
def prescreate(request):
    user = request.user
    if request.method == 'POST':
        if request.FILES.get("insurance_img") and request.POST.get("insu_comp"):
            insurance_img = request.FILES.get("insurance_img")
            company = Insurance.objects.get(id=request.POST.get("insu_comp"))
            subject = request.POST.get("subject")
            image = request.FILES.get("img")
            Prescribtion.objects.create(
                user=user, subject=subject,  image=image, insurance=company, insurance_image=insurance_img)
            messages.success(
                request, 'Your request is submitted you will soon get a verification email with the invoice')
            return redirect("prescribtions")
        else:
            subject = request.POST.get("subject")
            image = request.FILES.get("img")
            Prescribtion.objects.create(
                user=user, subject=subject,  image=image)
            messages.success(
                request, 'Your request is submitted you will soon get a verification email with the invoice')
            return redirect("prescribtions")
    else:
        messages.warning(
            request, 'Something Went Wrong')

        return redirect("prescribtions")


def presdetails(request, id):
    pres = Prescribtion.objects.get(id=id)
    return render(request, "core/pres_details.html", {"pres": pres})


def advices(request):
    advices = Advices.objects.all()
    return render(request, "core/advices.html", {"advices": advices})


def advice(request, id):
    advice = Advices.objects.get(id=id)
    return render(request, "core/advice.html", {"advice": advice})


def location(request, id):
    location = Locations.objects.get(id=id)
    return render(request, "core/location.html", {"location": location})


def about_us(request):
    return render(request, "core/about_us.html")


def purchase_guide(request):
    return render(request, "core/purchase_guide.html")


def privacy_policy(request):
    return render(request, "core/privacy_policy.html")


def terms_of_service(request):
    return render(request, "core/terms_of_service.html")
