from django.urls import path
from .views import ( check_user_existence,
    generate_otp_sign_up, generate_otp_sign_in, generate_otp_forgot,
      sign_up_verify_otp, verify_and_create_tokens,
    BuyerPersonalInfoAPIView, SellerPersonalInfoAPIView,
    AgentInfoAPIView, TicketListCreateView, UserMeView,
    ChangePasswordView, DeviceListView, RevokeTokenView, sign_in_verify_otp,
    verify_otp_forgot, reset_password_with_otp
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    #Auth
    path('generate-otp-sign-up/', generate_otp_sign_up, name='generate_otp_sign_up'),
    path('generate-otp-sign-in/', generate_otp_sign_in, name='generate_otp_sign_in'),
    path('generate-otp-forgot/', generate_otp_forgot, name='generate_otp_forgot'),
    path('sign-up-verify-otp/', sign_up_verify_otp, name='sign_up_verify_otp'),
    path('sign-in-verify-otp/', sign_in_verify_otp, name='sign_in_verify_otp'),
    path('verify-otp-forgot/', verify_otp_forgot, name='verify_otp_forgot'),
    path('reset-pass-with-otp/', reset_password_with_otp, name='reset_password_with_otp'),
    path('google-login/', verify_and_create_tokens, name='google_login'),
    path('verify-jwt/', TokenVerifyView.as_view(), name='verify_jwt'),
    path('refresh-jwt/', TokenRefreshView.as_view(), name='refresh_jwt'),
    path('check-user-existence/<str:phone_number>/', check_user_existence, name = 'check_user_existence'),

    #Profile and info
    path('user/me/', UserMeView.as_view(), name='user-me'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('buyer-personal-info/', BuyerPersonalInfoAPIView.as_view(), name='buyer_personal_info'),
    path('seller-personal-info/', SellerPersonalInfoAPIView.as_view(), name='seller_personal_info'),
    path('agent-info/', AgentInfoAPIView.as_view(), name='agent_personal_info'),

    #Device managements
    path('devices/', DeviceListView.as_view(), name="devices_list"),
    path('revoke-token/<int:pk>/', RevokeTokenView.as_view(), name='revoke_token'),
    
    path('tickets/', TicketListCreateView.as_view(), name='ticket-list-create'),
]