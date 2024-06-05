from django.urls import path, include
from .views import ( check_user_existence,
    generate_and_store_otp, sign_up_verify_otp, get_tokens_for_user,
    BuyerPersonalInfoAPIView, SellerPersonalInfoAPIView,
    AgentInfoAPIView, TicketListCreateView, UserMeView,
    ChangePasswordView, sign_in_verify_otp, verify_jwt,
    refresh_jwt
)

urlpatterns = [
    #API urls
    path('user/me/', UserMeView.as_view(), name='user-me'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('check-user-existence/<str:phone_number>/', check_user_existence, name = 'check_user_existence'),
    path('generate-otp/', generate_and_store_otp, name='generate_otp'),
    path('sign-up-verify-otp/', sign_up_verify_otp, name='sign_up_verify_otp'),
    path('sign-in-verify-otp/', sign_in_verify_otp, name='sign_in_verify_otp'),
    path('verify-jwt/', verify_jwt, name='verify_jwt'),
    path('refresh-jwt/', refresh_jwt, name='refresh_jwt'),
    path('google-login/', get_tokens_for_user, name='google_login'),
    path('buyer-personal-info/', BuyerPersonalInfoAPIView.as_view(), name='buyer_personal_info'),
    path('seller-personal-info/', SellerPersonalInfoAPIView.as_view(), name='seller_personal_info'),
    path('agent-info/', AgentInfoAPIView.as_view(), name='agent_personal_info'),
    path('tickets/', TicketListCreateView.as_view(), name='ticket-list-create'),
]