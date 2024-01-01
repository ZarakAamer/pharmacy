from core.models import *
from django.db.models import Min, Max
from django.contrib import messages
from django.utils import timezone


def default(request):
    bank_details = ''
    if len(BankInfo.objects.all()) <= 0:
        pass
    else:
        bank_details = BankInfo.objects.all().order_by('-id')[0]
    offers = SpecialTimeOffer.objects.all()
    for i in offers:
        # Get the current datetime in the timezone defined in your project settings
        current_datetime = timezone.now()

        # Compare the end_at value with the current datetime
        if i.end_at > current_datetime:
            # end_at is in the future
            pass
        else:
            # end_at has already passed
            i.delete()
    locations = Locations.objects.all()
    main_cats = MainCategory.objects.all()
    main_cats_8 = MainCategory.objects.all()[:8]
    sub_cats = SubCategory.objects.all()
    cats = Category.objects.all()
    shipping = Shipping.objects.all()[0]
    min_max_price = Product.objects.aggregate(Min("price"), Max("price"))

    if request.user.is_authenticated:
        try:
            wishlist = wishlist_model.objects.filter(user=request.user)
        except:
            messages.warning(
                request, "You need to login before accessing your wishlist.")
            wishlist = 0
    else:
        wishlist = 0

    try:
        address = Address.objects.get(user=request.user)
    except:
        address = None
    if request.user.is_authenticated:
        cart = CartOrder.objects.filter(user=request.user).first()

        return {
            'bank_details': bank_details,
            'shipping': shipping,
            'offers': offers,
            'main_cats_8': main_cats_8,
            'locations': locations,
            'cart': cart,
            'cats': cats,
            'sub_cats': sub_cats,
            'main_cats': main_cats,
            'wishlist': wishlist,
            'address': address,
            'min_max_price': min_max_price,
        }

    else:

        return {
            'shipping': shipping,
            'bank_details': bank_details,
            'offers': offers,
            'main_cats_8': main_cats_8,
            'locations': locations,
            'cats': cats,
            'sub_cats': sub_cats,
            'main_cats': main_cats,
            'wishlist': wishlist,
            'address': address,
            'min_max_price': min_max_price,
        }


def banners(request):
    big_banners = BigBanner.objects.all().order_by('-id')
    side_banners = SideBanner.objects.all().order_by('-id')

    return {
        "big_banners": big_banners, "side_banners": side_banners
    }
