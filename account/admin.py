from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .forms import UserCreationForm, UserChangeForm
from .models import User, BuyerPersonalInfo, SellerPersonalInfo, AgentInfo, Ticket


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

class TicketAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user', 'assigned_user', 'status', 'department', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at', 'department')
    search_fields = ('subject', 'user__email', 'assigned_user__email', 'department')

class AgentInfoAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'company_address', 'company_email', 'company_phone_number', 'approval_status']
    list_filter = ['approval_status']

class BuyerPersonalInfoAdmin(admin.ModelAdmin):
    list_display = [ 'buyer_user', 'approval_status']
    list_filter = ['approval_status']

class SellerPersonalInfoAdmin(admin.ModelAdmin):
    list_display = [ 'seller_user', 'approval_status']
    list_filter = ['approval_status']

admin.site.register(Ticket, TicketAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(BuyerPersonalInfo, BuyerPersonalInfoAdmin)
admin.site.register(SellerPersonalInfo, SellerPersonalInfoAdmin)
admin.site.register(AgentInfo, AgentInfoAdmin)

