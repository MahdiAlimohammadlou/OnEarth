from django.urls import path, include
from .views import ( check_user_existence,
    generate_and_store_otp, verify_otp, get_tokens_for_user,
    BuyerPersonalInfoAPIView, SellerPersonalInfoAPIView,
    AgentInfoAPIView, TicketListCreateView, UserMeView,
    ChangePasswordView
)

urlpatterns = [
    #Authentication urls
    path('auth/', include('djoser.urls.jwt')),

    #API urls
    path('user/me/', UserMeView.as_view(), name='user-me'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('check-user-existence/<str:phone_number>/', check_user_existence, name = 'check_user_existence'),
    path('generate-otp/', generate_and_store_otp, name='generate_otp'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('google-login/', get_tokens_for_user, name='google_login'),
    path('buyer-personal-info/', BuyerPersonalInfoAPIView.as_view(), name='buyer_personal_info'),
    path('seller-personal-info/', SellerPersonalInfoAPIView.as_view(), name='seller_personal_info'),
    path('agent-info/', AgentInfoAPIView.as_view(), name='agent_personal_info'),
    path('tickets/', TicketListCreateView.as_view(), name='ticket-list-create'),
]