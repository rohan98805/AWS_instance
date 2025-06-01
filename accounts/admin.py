from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser, Message, BuyerProfile, SellerProfile,
    LandProperty, LegalCase, OwnershipHistory
)

# Extend UserAdmin to register CustomUser
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'is_verified', 'is_buyer', 'is_seller')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('is_verified', 'is_buyer', 'is_seller', 'adhar_card', 'pan_card', 'profile_photo')
        }),
    )

from django.contrib import admin
from .models import LandRecord, LandImage

class LandImageInline(admin.TabularInline):  # or admin.StackedInline for vertical layout
    model = LandImage
    extra = 5  # Show 5 empty slots by default
    min_num = 5  # Minimum images required
    max_num = 10  # Optional: limit maximum
    verbose_name = "Land Image"
    verbose_name_plural = "Land Images"

class LandRecordAdmin(admin.ModelAdmin):
    list_display = ('place', 'area', 'land_type')
    inlines = [LandImageInline]

admin.site.register(LandRecord, LandRecordAdmin)
admin.site.register(LandImage)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Message)
admin.site.register(BuyerProfile)
admin.site.register(SellerProfile)
admin.site.register(LandProperty)
admin.site.register(LegalCase)
admin.site.register(OwnershipHistory)
