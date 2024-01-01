from modeltranslation.translator import TranslationOptions, register
from.models import *


@register(BigBanner)
class BigBannerRanslationOptions(TranslationOptions):
    fields = ("name", "user_catcher", "short_line")


@register(SideBanner)
class SideBannerRanslationOptions(TranslationOptions):
    fields = ("type", "user_catcher")


@register(MainCategory)
class MainCategoryRanslationOptions(TranslationOptions):
    fields = ("title", )


@register(SubCategory)
class SubCategoryRanslationOptions(TranslationOptions):
    fields = ("title", )


@register(Category)
class CategoryRanslationOptions(TranslationOptions):
    fields = ("title", )


@register(Product)
class ProductRanslationOptions(TranslationOptions):
    fields = ("title", "description", "specifications")


@register(Prescribtion)
class PrescribtionRanslationOptions(TranslationOptions):
    fields = ("subject", )


@register(Advices)
class AdvicesRanslationOptions(TranslationOptions):
    fields = ("title", "description", "advice")


@register(Doctor)
class DoctorRanslationOptions(TranslationOptions):
    fields = ("name", "details", "speciality")


@register(Locations)
class LocationsRanslationOptions(TranslationOptions):
    fields = ("city_name", "details")


@register(BankInfo)
class BankInfoRanslationOptions(TranslationOptions):
    fields = ("instructions", "account_info")
