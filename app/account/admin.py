from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .forms import UserCreationForm, UserChangeForm
from .models import User, BuyerPersonalInfo, SellerPersonalInfo, AgentInfo, Ticket, Device, ReferralCode


# Register your models here.


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ("email", "is_admin")
    list_filter = ("is_admin",)

    fieldsets = (
        (None, {"fields":("email","phone_number", "password")}),
        ("permisions", {"fields" : ("is_admin", "is_superuser", "is_agent",
                                     "is_buyer", "is_seller", "last_login", "groups")})
    )

    add_fieldsets = (
        (None, {"fields" : ("phone_number", "email", "password1", "password2")}),
    )

    search_fields = ("email", "phone_number",)
    ordering = ("email",)
    filter_horizontal = ()

class AgentInfoAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'company_name', 'company_email', 'biometric_approval_status', 'approval_status')
    search_fields = ('full_name', 'company_name', 'company_email')
    list_filter = ('biometric_approval_status', 'approval_status')
    readonly_fields = ('biometric_approval_status', 'approval_status')

class BuyerPersonalInfoAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'postal_address', 'marital_status', 'basic_info_approval_status', 'id_or_driver_license_approval_status', 'passport_approval_status', 'birth_certificate_status', 'aggrement_approval_status')
    search_fields = ('full_name', 'postal_address')
    list_filter = ('marital_status', 'basic_info_approval_status', 'id_or_driver_license_approval_status', 'passport_approval_status', 'birth_certificate_status', 'aggrement_approval_status')
    readonly_fields = ('basic_info_approval_status', 'id_or_driver_license_approval_status', 'passport_approval_status', 'birth_certificate_status', 'aggrement_approval_status')

class SellerPersonalInfoAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'postal_address', 'marital_status', 'background_status', 'basic_info_approval_status', 'id_or_driver_license_approval_status', 'passport_approval_status', 'birth_certificate_status', 'aggrement_approval_status')
    search_fields = ('full_name', 'postal_address')
    list_filter = ('marital_status', 'background_status', 'basic_info_approval_status', 'id_or_driver_license_approval_status', 'passport_approval_status', 'birth_certificate_status', 'aggrement_approval_status')
    readonly_fields = ('background_status', 'basic_info_approval_status', 'id_or_driver_license_approval_status', 'passport_approval_status', 'birth_certificate_status', 'aggrement_approval_status')

class TicketAdmin(admin.ModelAdmin):
    list_display = ('user', 'assigned_user', 'subject', 'status', 'department')
    list_filter = ('status', 'department', 'subject')
    search_fields = ('user__username', 'user__email', 'assigned_user__username', 'assigned_user__email')
    raw_id_fields = ('user', 'assigned_user')

class ReferralCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'agent')
    search_fields = ('code', 'agent__username', 'agent__email')
    raw_id_fields = ('agent',)

class DeviceAdmin(admin.ModelAdmin):
    list_display = ('user', 'device_info', 'is_token_expired')
    search_fields = ('user__username', 'user__email', 'device_info')
    raw_id_fields = ('user',)

admin.site.register(AgentInfo, AgentInfoAdmin)
admin.site.register(BuyerPersonalInfo, BuyerPersonalInfoAdmin)
admin.site.register(SellerPersonalInfo, SellerPersonalInfoAdmin)
admin.site.register(Ticket, TicketAdmin)
# admin.site.register(ReferralCode, ReferralCodeAdmin)
# admin.site.register(Device, DeviceAdmin)
admin.site.register(User, UserAdmin)


